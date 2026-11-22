# SENTINEL Detection Engineering

> Does your detection still work when the attacker changes tactics?

This document defines SENTINEL's detection engineering process — how detections are designed, implemented, tested, and validated against real telemetry — and tracks the current state of detections actually built in the lab, through milestone v0.9.1 (alongside v0.10 Linux FIM triage validation).

A detection is not considered working because a rule exists. It is considered working only once it has been tested against controlled activity in the lab and the result — pass, fail, or unresolved — has been documented.

---

## 1. Purpose and Scope

SENTINEL treats detection engineering as an evidence-driven discipline: every detection should be observable (grounded in real telemetry), testable (validated against a controlled scenario, not assumed), and explainable (an analyst can state exactly why it fired). This document covers the methodology used to build and validate detections, and documents the current implementation status honestly — including what is confirmed, what is partially confirmed, and what remains unresolved.

The implemented detection families are Linux File Integrity Monitoring (FIM), SSH authentication, and replayed Windows Sysmon telemetry. SENTINEL is a Linux-first lab. There is no live Windows endpoint and no Active Directory environment; Windows Sysmon events are replayed telemetry.

**Relationship to CASE-001.** [CASE-001](../investigations/CASE-001.md) was closed on 18 November 2026, and the v0.3 SOC Investigation milestone is complete. Closure applies to the reviewed case scope only. It does not mean the SENTINEL project or detection engineering is complete. Later milestones (v0.6, v0.8, v0.9, v0.9.1) are separate, post-closeout developments and are not CASE-001 evidence.

All timestamps in this document are IST (`+0530`).

---

## 2. Detection Engineering Lifecycle

```
DEFINE → IMPLEMENT → TEST → VALIDATE → TUNE → RETEST
```

| Stage | What happens |
|---|---|
| **Define** | Identify the threat/behavior, the telemetry needed to observe it, and the detection objective |
| **Implement** | Write the detection logic (e.g., a Wazuh rule) against that telemetry |
| **Test** | Execute a controlled, reversible activity in the lab and capture the resulting telemetry |
| **Validate** | Confirm the detection fired as expected, with useful alert context, against that telemetry |
| **Tune** | Adjust the rule based on false positives/negatives or missing context |
| **Retest** | Re-run the same test to confirm the tuning actually fixed the issue |

A detection only reaches **Validated** once Test and Validate have both produced the expected, documented result for the scenario under test. Validation is always scoped to the specific scenario tested — it does not automatically extend to related but untested behavior. Passing a syntax check alone is not the same as passing this lifecycle — see Section 6.

**Status vocabulary used in this document**

| Term | Meaning |
|---|---|
| **Configured** | The rule or setting exists in the configuration. Nothing is implied about behavior. |
| **Implemented** | The detection is built and operating in the lab and has produced alerts. |
| **Observed** | An alert or behavior was seen, but not as a controlled, explained test. |
| **Validated** | Passed a controlled test for a stated scenario only. |
| **Tuned** | Configuration was changed to address noise or gaps. This is not the same as the noise being resolved. |
| **Pending retest** | Tuning exists, but the retest that would confirm its effect has not been completed. |

---

## 3. Detection Specification

Each detection is specified using the template below. The specification is drafted before implementation and updated after testing: definition fields (threat, telemetry, logic, expected alert, severity, planned test procedure) are written up front, while results-dependent fields (observed test outcomes, evidence) are completed only once testing has produced them. A field that is not yet known is recorded as such, not guessed.

| Field | Description |
|---|---|
| Detection ID | Unique project identifier |
| Threat / Technique | What behavior this addresses (MITRE ATT&CK mapping where confidently applicable) |
| Telemetry Source | Required log/event source |
| Detection Logic | Condition(s) that should trigger the alert |
| Expected Alert | What the alert should look like if the logic fires correctly |
| Severity | Intended severity level |
| Test Procedure | The controlled scenario used to validate it |
| Evidence | Supporting artifacts (screenshots, logs, alert output) |

**Instance A — File Integrity Monitoring on `/home` (Rule `100002`):**

| Field | Value |
|---|---|
| Detection ID | Custom Wazuh Rule `100002` (maintained in [`detections/local_rules.xml`](../detections/local_rules.xml)) |
| Threat / Technique | Unauthorized or unexpected file modification within the configured `/home` monitoring scope. No MITRE ATT&CK mapping is asserted in this document. |
| Telemetry Source | Wazuh Syscheck (File Integrity Monitoring), real-time, with `/home` as the configured monitoring scope on SENTINEL-LINUX01 (`10.10.10.40`, Agent ID `002`) |
| Detection Logic | A read-only inspection of `/var/ossec/etc/rules/local_rules.xml` on SENTINEL-WAZUH showed Rule `100002` with Level 8, parent condition `<if_sid>550</if_sid>`, a `file` field condition containing `/home/`, and group `sentinel_fim`. Project history records the rule being standardised with the anchored pattern `^/home/` in v0.2 (see Section 5.3). This establishes the on-disk file at inspection time, **not** the version loaded by the running manager during the earlier tests. The v0.6 measurement included a `/tmp` negative control, which produced no FIM alerts. Other outside-scope paths and case behavior have **not** been systematically tested. Rules `100003` (parent Rule `554`, creation) and `100004` (parent Rule `553`, deletion) are the creation and deletion rules; Rule `100002` is the modification rule only. See Section 5.3 for the parent-rule design. |
| Expected Alert | Level 8 alert identifying the changed file |
| Severity | Level 8 (custom rule), observed for the documented controlled modification tests. Wazuh's built-in Rule 550 (Level 7, "Integrity checksum changed") was also observed during the 11 October test. |
| Test Procedure | **Controlled modifications:** (1) 11 October 2026 — `/home/sentinel-admin/sentinel-fim-validation.txt`; screenshot evidence supports custom Rule `100002` firing at `2026-10-11T20:25:14.746+0530`. (2) 26 October 2026 — `/home/sentinel-admin/sentinel-v02-mod-test.txt`; two modifications each recorded a custom Rule `100002` Level 8 alert: `2026-10-26T21:38:27.910+0530` (file size 0 → 23 bytes) and `2026-10-26T21:38:48.473+0530` (file size 23 → 61 bytes). **Controlled creation and deletion (16 October 2026):** `/home/sentinel-admin/sentinel-audit-test.txt`. The reviewed source alert record shows built-in Rule `554` for creation and built-in Rule `553` for deletion; the custom creation and deletion rules (`100003`, `100004`) are not present in the reviewed records. These are reviewed records of individual controlled actions, not validations of Rules `100003` or `100004` (see Section 5.3). **Later controlled lifecycle sessions (four, separate):** 2 November 2026 (`/home/sentinel-admin/sentinel-v03-final-test.txt`, CASE-001 evidence period); 18 November 2026 (`/home/sentinel-admin/fim-sprint-test.txt`, CASE-001 closeout evidence); 20 November 2026 (v0.6 controlled measurement, post-closeout and not CASE-001 evidence); and 21 November 2026 (v0.8 probe, `/home/sentinel-admin/.v08-check/probe.txt`, post-closeout and not CASE-001 evidence). The 2, 18 and 21 November sessions each matched Rule `100002` at the modification step (Section 5.3). The four sessions are not combined into one test. |
| Evidence | [`evidence/v0.3/`](../evidence/v0.3/readme.md); full investigation detail in [`investigations/CASE-001.md`](../investigations/CASE-001.md). **11 October:** supported by screenshot evidence; the original source alert record was not recovered during the later review, so this result is not source-log verified. **16 October:** reviewed from the source alert record at `/var/ossec/logs/alerts/2026/Oct/ossec-alerts-16.json`; this document does not claim that the raw log is committed to the repository. **26 October:** two alerts from two consecutive modifications of one file (not a regression suite); screenshot: [October 26 controlled-modification source alerts](../evidence/v0.2/screenschots/v0.2-oct26-controlled-modification-source-alerts-new.png). **18 November:** raw alert JSON at [`evidence/v0.3/raw-alerts/fim-lifecycle-evidence.json`](../evidence/v0.3/raw-alerts/fim-lifecycle-evidence.json) (Section 5.3). |

**Instance B — SSH authentication (Rules `100200` and `100201`):**

| Field | Value |
|---|---|
| Detection ID | Custom Wazuh Rules `100200` and `100201` (maintained in [`detections/sentinel_ssh_bruteforce_rules.xml`](../detections/sentinel_ssh_bruteforce_rules.xml)) |
| Threat / Technique | Repeated failed SSH authentication from one source (brute-force-style behavior). No MITRE ATT&CK mapping is asserted in this document. |
| Telemetry Source | `sshd` authentication logs on SENTINEL-LINUX01 (Agent ID `002`), collected by the Wazuh agent and evaluated by the Wazuh manager |
| Detection Logic | `100200` (Level 5) matches SSH authentication failures. `100201` (Level 10) is a frequency-based escalation after six matching failures within 60 seconds from the same source IP. |
| Expected Alert | A Level 5 alert per failure; a Level 10 escalation alert once the threshold is reached |
| Test Procedure | A controlled scenario with SENTINEL-KALI (`10.10.10.20`) generating failed SSH authentication attempts against SENTINEL-LINUX01, documented in [CASE-003](../investigations/CASE-003.md) (21 failed attempts) |
| Evidence | [`investigations/CASE-003.md`](../investigations/CASE-003.md); [v0.5 evidence index](../evidence/v0.5/readme.md); threshold behavior also examined in the [v0.6 measurement report](../metrics/v0.6-purple-team-measurement.md) |

Custom Rules `100003` and `100004` and the Sysmon replay ruleset have not been specified using this template; their observations and status are recorded in Section 5.

---

## 4. Testing and Validation Methodology

Every test compares an **expected result** against an **actual result**, and the outcome is recorded regardless of whether it passed:

```
Expected: File modification → Syscheck telemetry → Rule fires → Alert generated
Actual:   [recorded as observed, not assumed]
```

- **Pass** — the expected telemetry and alert were both observed.
- **Fail** — the expected behavior did not occur; the failure is investigated and documented, not hidden.
- **Unresolved / Inconclusive** — part of the chain was confirmed (e.g., telemetry reached the manager) but the specific detection logic under test was not confirmed to fire. This status exists specifically so a partial result isn't overstated as a pass.

This is the standard every detection in this document is held to, including those currently implemented.

---

## 5. Current Implementation and Status

### 5.1 Environment

- SENTINEL-WAZUH — Ubuntu 24.04, Wazuh 4.14.8, `10.10.10.10`
- SENTINEL-KALI — Kali Linux 2026.2, controlled adversary-emulation VM, `10.10.10.20`
- SENTINEL-LINUX01 — Ubuntu 24.04.5 LTS, Wazuh Agent 4.14.8, `10.10.10.40`, Agent ID `002`
- Isolated VirtualBox internal network `10.10.10.0/24`. Python tooling is used for telemetry conversion and triage.
- No live Windows endpoint and no Active Directory environment. Windows Sysmon events are replayed telemetry.

### 5.2 Detection inventory

| Family | Rules | Level | Rule file | Status |
|---|---|---|---|---|
| FIM | `100002` (modification, parent `550`), `100003` (creation, parent `554`), `100004` (deletion, parent `553`) | 8 | [`detections/local_rules.xml`](../detections/local_rules.xml) | Implemented. Validated only for the controlled scenarios in Section 5.3, which include four separate controlled lifecycle sessions (2, 18, 20 and 21 November) that are not a regression suite. v0.8 tuning applied; broader retest pending. |
| SSH authentication | `100200` (failure), `100201` (escalation) | 5, 10 | [`detections/sentinel_ssh_bruteforce_rules.xml`](../detections/sentinel_ssh_bruteforce_rules.xml) | Implemented. Exercised in a controlled scenario (CASE-003). See Section 5.4. |
| Sysmon replay: base rules | `100100–100104` | 0 | [`detections/sentinel_sysmon_replay_rules.xml`](../detections/sentinel_sysmon_replay_rules.xml) | Implemented. Structural (Level 0) classification rules that do not alert. |
| Sysmon replay: behavioral rules | `100110`, `100111`, `100112`, `100120`, `100130`, `100131`, `100140` | 8–14 across the seven rules | same file | Implemented. Fired on replayed telemetry only. See Section 5.5. |

**v0.6 measurement caveat.** The v0.6 controlled measurement ([report](../metrics/v0.6-purple-team-measurement.md)) results for FIM, Sysmon and SSH are summarised in Sections 5.3–5.5. They are small controlled samples and are not statistically meaningful detection or false-positive rates. Endpoint and manager clocks were skewed, so raw cross-VM timing deltas are unreliable. A negative raw delta is a clock artefact and must not be presented as negative (or valid) detection latency.

### 5.3 FIM family

**What's implemented:**

| Component | Status |
|---|---|
| Real-time FIM with `/home` as the configured monitoring scope (Wazuh Syscheck) | Implemented; generated events in the documented controlled tests |
| Built-in Wazuh **Rule 550** (Level 7, "Integrity checksum changed") | **Observed** during the 11 October controlled modification test (screenshot-supported) |
| Custom **Rule 100002** (Level 8, parent Rule 550) — modification | **Confirmed for the documented controlled modification tests.** 11 October 2026: `/home/sentinel-admin/sentinel-fim-validation.txt`, `2026-10-11T20:25:14.746+0530` — screenshot-supported; original source alert record not recovered. 26 October 2026: `/home/sentinel-admin/sentinel-v02-mod-test.txt`, two Level 8 alerts at `2026-10-26T21:38:27.910+0530` (0 → 23 bytes) and `2026-10-26T21:38:48.473+0530` (23 → 61 bytes). It also matched the modification step of the 2 November, 18 November and 21 November single-file lifecycle sessions (below). |
| Built-in **Rule 554** ("File added to the system") — creation | **Reviewed source record** (16 October 2026): `/home/sentinel-admin/sentinel-audit-test.txt` shows Rule 554 at `2026-10-16T11:40:06.007+0530`. Custom Rule 100003 (child of Rule 554) is **not present** in the reviewed record. |
| Built-in **Rule 553** ("File deleted") — deletion | **Reviewed source record** (16 October 2026): the same file shows Rule 553 at `2026-10-16T12:31:32.819+0530`. Custom Rule 100004 (child of Rule 553) is **not present** in the reviewed record. |
| Custom **Rule 100003** (Level 8, parent Rule 554) — creation | **Observed on 31 October 2026** in two separate evidence sets (see below); not established as a controlled test. **Matched in three controlled single-file lifecycle sessions** (2 November, 18 November and 21 November); the separate 20 November v0.6 controlled session detected 3/3 selected lifecycle events (see below). Four separate sessions in total, of which 2 and 18 November belong to the CASE-001 evidence period and 20 and 21 November are post-closeout. Validated only for those sessions. |
| Custom **Rule 100004** (Level 8, parent Rule 553) — deletion | **Observed on 31 October 2026** in two separate evidence sets (see below); not established as a controlled test. **Matched in three controlled single-file lifecycle sessions** (2 November, 18 November and 21 November); the separate 20 November v0.6 controlled session detected 3/3 selected lifecycle events (see below). Four separate sessions in total, of which 2 and 18 November belong to the CASE-001 evidence period and 20 and 21 November are post-closeout. Validated only for those sessions. |

**Scope of the confirmed results:** the controlled tests show that Rule 100002 fires a Level 8 alert for modification of the test files within the configured `/home` monitoring scope in the scenarios tested, and that Rules 100003 and 100004 matched creation and deletion of single dedicated files in three separate lifecycle sessions (2 November, 18 November and 21 November), each on its own dedicated file. A fourth, separate controlled lifecycle session (20 November, v0.6 measurement) detected 3/3 selected lifecycle events. The 2 and 18 November sessions belong to the CASE-001 evidence period and closeout; the 20 and 21 November sessions are post-closeout developments. This validates **only those tested scenarios**; the four sessions are not combined into one test or result, and they are not an automated regression suite. `/home` is the configured monitoring scope; that configuration does not guarantee that every change under the path is detected. A handful of tests on a handful of files is not a regression suite and does not establish a detection rate. The 31 October observations are separate and do not extend any controlled result.

**Reviewed 16 October 2026 records:** creation and deletion were each performed once as an individual controlled action. The source alert record at `/var/ossec/logs/alerts/2026/Oct/ossec-alerts-16.json` was reviewed; it shows built-in Rule 554 for creation and built-in Rule 553 for deletion. Custom Rules 100003 (child of Rule 554) and 100004 (child of Rule 553) are not present in the reviewed records. Custom Rule 100002 is the modification rule (parent Rule 550) and is not the rule designed to cover those events, so its absence from the creation and deletion records is not itself a finding. These records do **not** validate Rules 100003 or 100004. The unresolved historical question is whether custom Rules 100003 and 100004 were deployed and loaded on 16 October and, if they were, why they are not present in the reviewed records. CASE-001 leaves the historical loaded configuration unknown, and no explanation is asserted. This question was not a prerequisite for closing the case. Later sessions in which Rules 100003 and 100004 matched do **not** answer it. Any ATT&CK mappings carried by built-in events are telemetry metadata, not evidence of malicious intent.

**Superseded earlier creation claim:** an earlier report stated that Rules 554 and 100002 fired together during creation. The reviewed source alert record does not support that claim, and Rule 100002 is not the creation rule. It is not retained as a positive creation result, and no cause for the earlier report is asserted.

**Observed 31 October 2026 — Rules 100003 and 100004 (Set A, screenshot):** custom Rule 100003 (creation, Level 8) and custom Rule 100004 (deletion, Level 8) were observed at approximately 18:51:56 IST, each identifying a file path under `/home/sentinel-admin/snap/firmware-updater/262/.config/bus/`. These are **observations, not controlled tests**.

- **Evidence:** one terminal screenshot showing both alerts ([FIM lifecycle custom detections](../evidence/v0.3/screenshots/v0.3-fim-lifecycle-custom-detections.png)). It is not a raw alert record, and no raw alert record is included in this set.
- **Trigger origin:** the paths are in an application configuration directory. Whether the events were deliberately triggered or ordinary application activity has not been established, and process attribution and root cause are unestablished.
- **Separation from other results:** these are separate from the Rule 100002 modification tests and from the 16 October records. The 2 November session does not retroactively validate them.
- **Unresolved:** whether Rules 100003 and 100004 were deployed and loaded on 16 October and, if so, why they are not present in the reviewed 16 October records, given that they were observed on 31 October. CASE-001 leaves the historical loaded configuration unknown. No explanation is asserted.
- **Scope:** in Set A, each rule is evidenced by a single event. It establishes that the rule fired in that instance only.

**Second 31 October evidence set (Set B):** CASE-001 separately records two raw alert JSON records for `/home/sentinel-admin/sentinel-v03-controlled-test.txt`: Rule 100003 (creation) at `2026-10-31T22:56:46.988+0530` and Rule 100004 (deletion) at `2026-10-31T23:27:05.164+0530`. These are two individual alert records, not a complete lifecycle session. The relationship between Set A and Set B is not established. The sets are not merged, and neither is used to explain the unresolved 16 October historical configuration question.

**Controlled lifecycle session — 2 November 2026 (CASE-001 evidence period):** in one controlled session on SENTINEL-LINUX01, a single dedicated file, `/home/sentinel-admin/sentinel-v03-final-test.txt`, was created, modified, and deleted. Creation matched custom Rule 100003, modification matched Rule 100002, and deletion matched Rule 100004, each at Level 8 ([screenshot](../evidence/v0.3/screenshots/v0.3-fim-full-lifecycle-custom-rules.png)). This is one controlled lifecycle session on one dedicated file. It is **not** a regression suite or repeatability test and does not establish comprehensive FIM coverage. Raw 2 November alert JSON records are not committed. It does not explain the 16 October observations or retroactively validate the 31 October ones.

**Controlled lifecycle session — 18 November 2026 (CASE-001 closeout evidence):** in one controlled session, a single dedicated file, `/home/sentinel-admin/fim-sprint-test.txt`, was created, modified, and deleted. Creation matched custom Rule 100003 at `2026-11-18T12:57:06.508+0530`, modification matched Rule 100002 at `2026-11-18T12:59:29.407+0530`, and deletion matched Rule 100004 at `2026-11-18T13:04:23.506+0530`, each at Level 8. Evidence is raw alert JSON at [`evidence/v0.3/raw-alerts/fim-lifecycle-evidence.json`](../evidence/v0.3/raw-alerts/fim-lifecycle-evidence.json). This is a separate session on a different file from the 2 November and 21 November sessions. It is one controlled lifecycle session on one dedicated file, **not** a regression suite or repeatability test, and it does not establish comprehensive FIM coverage. It does not explain the 16 October observations or validate either 31 October evidence set.

**Evidence reconciliation:** CASE-001 was closed on 18 November 2026. Evidence reconciliation for the reviewed scope is closed, and it records the 31 October alerts as observations. Closure applies to the reviewed case scope; it does not mean all detection engineering is complete. The 11 October result remains screenshot-supported only, because its original source alert record was not recovered.

#### Post-closeout developments (not CASE-001 evidence)

The v0.6, v0.7, v0.8, v0.9 and v0.9.1 milestones are separate project developments. Their results are recorded here as engineering status and are not part of the CASE-001 evidence.

**v0.6 controlled measurement (FIM, 20 November 2026, [report](../metrics/v0.6-purple-team-measurement.md)):** 3/3 selected lifecycle events were detected, and the `/tmp` negative-control operations (outside the monitored scope) produced 0/3 alerts. This is a small controlled sample, not a statistically meaningful detection or false-positive rate, and it is a separate session from the 2, 18 and 21 November sessions. Cross-VM timing in this measurement is subject to the clock-skew caveat in Section 5.2; no detection-latency figure is claimed, and a negative raw delta is a clock artefact, not negative latency.

**Mutation and reliability observations (v0.7, [CASE-004](../investigations/CASE-004.md)):** these are observations from controlled testing, not complete characterisations.
- Hidden files inside `/home` triggered FIM.
- Staging in `/var/tmp`, outside the monitored scope, did not trigger FIM.
- Benign cache and desktop activity produced Level 8 noise.

**v0.8 tuning and verification:** the table separates what was configured, what was verified, and what remains open.

| Aspect | Status |
|---|---|
| Configuration changes | v0.8 introduced FIM path exclusions for selected noisy application activity and FIM group isolation using `sentinel_fim`. Hidden dot-directory monitoring was preserved, and FIM alert grouping was separated from SSH detection grouping. **Implemented and manager-validated.** |
| Controlled Agent `002` probe (21 November 2026) | On SENTINEL-LINUX01, `/home/sentinel-admin/.v08-check/probe.txt` was created, modified, and deleted. Creation matched Rule 100003, modification Rule 100002, and deletion Rule 100004, each at Level 8. The alerts carried the `sentinel_fim` group without the `sshd` group, and hidden dot-directory monitoring remained active. **Verified for this probe.** |
| Residual noise | Desktop noise was still observed under `/home/sentinel-admin/.config/dconf/user`. The noise problem is not resolved. |
| Broader noise-suppression assessment | **Pending retest.** The probe is one lifecycle on one file. It is not a regression suite, not a broad coverage assessment, and does not measure overall noise reduction. |

The 21 November probe results are recorded in the current detection inventory.

**Current rule design versus the historical configuration:**
- **Current on-disk design:** Rule 100002 (parent Rule 550, modification), Rule 100003 (parent Rule 554, creation) and Rule 100004 (parent Rule 553, deletion), maintained in [`detections/local_rules.xml`](../detections/local_rules.xml). They use anchored `^/home/` matching, include negative matching conditions for selected Tracker3 and Nautilus database activity, and carry the `sentinel_fim` group. This is the current post-v0.8 file. It is **not** a historical snapshot of the configuration that was in place during the CASE-001 tests.
- **On-disk vs loaded:** the on-disk definition shows the file as it is now. The 3 November read-only inspection covered Rule 100002 only. Neither establishes which versions of Rules 100002, 100003 and 100004 the running manager had loaded during earlier tests. The rules were changed after the early tests (v0.2 standardisation, v0.8 tuning), so the tested configuration differs between sessions. The historical loaded configuration is unknown, as CASE-001 records, and it has not been reconstructed.
- **Matching behavior:** the v0.6 measurement included a `/tmp` negative control, which produced no FIM alerts. Other outside-scope paths and case behavior have not been systematically tested. The Tracker3 and Nautilus negative matching conditions have not been independently validated through targeted tests. Descriptions of the rules as covering "paths under `/home/`" remain a working assumption beyond the specific scenarios tested.

The current FIM results do **not** establish:

- Whether custom Rules 100003 and 100004 were deployed and loaded on 16 October — the reviewed records show only built-in Rules 554 and 553, and the historical loaded configuration is unknown
- Broader repeatability of Rules 100003 and 100004 — they matched in three individual controlled lifecycle sessions (2, 18 and 21 November) on dedicated files, and a separate 20 November v0.6 session detected 3/3 selected lifecycle events, which is useful evidence but not a repeatable automated regression suite or comprehensive coverage; the Set A trigger origin on 31 October is not established, and the relationship between the two 31 October evidence sets is not established
- Complete FIM coverage of the configured `/home` scope, or coverage of all lifecycle event types or file types
- Measured detection rates, or broader false-positive or false-negative behavior
- A repeatable regression suite (none exists)
- That noise suppression is complete or has passed broader retesting — v0.8 tuning is implemented and probe-verified, residual noise remains, and the broader retest is pending
- Any malicious activity — the controlled tests were lab actions, not attacks; the 31 October events are observed alerts of unestablished origin and do not by themselves establish malicious activity

These results are further reviewed in [CASE-001](../investigations/CASE-001.md), which was closed on 18 November 2026 for the reviewed case scope. Post-closeout engineering, validation, noise-tuning, and historical evidence-recovery work continues separately and is not a prerequisite for that closure (follow-up work is listed in Section 7).

### 5.4 SSH authentication family

**Pipeline:**

1. SENTINEL-KALI (`10.10.10.20`) generates controlled SSH authentication failures.
2. SENTINEL-LINUX01 (`10.10.10.40`, Agent ID `002`) receives the connection attempts.
3. Wazuh Agent `002` collects the `sshd` authentication logs.
4. SENTINEL-WAZUH evaluates the events with the custom rules.
5. Resulting alerts can be processed by the external Python triage tool (Section 5.6).

| Rule | Level | Purpose |
|---|---|---|
| `100200` | 5 | Matches SSH authentication failures |
| `100201` | 10 | Frequency-based escalation after six matching failures within 60 seconds from the same source IP |

**CASE-003** ([`investigations/CASE-003.md`](../investigations/CASE-003.md)) documented 21 failed authentication attempts, baseline Rule `100200` alerts, Rule `100201` escalation, Python-assisted severity triage, and manual investigation confirming zero successful logins. Python-assisted triage is automated prioritisation only. Containment was documented as a source-scoped manual procedure with verification checks. No automated containment or persistent IP block is claimed. SENTINEL does not implement automated containment, eradication, or recovery, and no complete containment, eradication and recovery lifecycle is claimed (see [`06-incident-response.md`](06-incident-response.md)).

**Limits:** this is one controlled scenario from one source. It does not establish detection rates or false-positive behavior against legitimate authentication activity.

**v0.6 controlled measurement (SSH, [report](../metrics/v0.6-purple-team-measurement.md)):**
- **C1:** four Rule `100200` alerts and zero Rule `100201` escalations.
- **C2:** eight Rule `100200` alerts and two Rule `100201` escalations.
- The first C2 escalation occurred early because the 60-second sliding window carried over four failures from C1 and combined them with two C2 failures. The second escalation was triggered by the C2 burst.

These are small controlled samples, not statistically meaningful detection or false-positive rates. Cross-VM timing in this measurement is subject to the clock-skew caveat in Section 5.2; a negative raw delta is a clock artefact, not negative detection latency.

### 5.5 Sysmon replay family

**Ruleset:** [`detections/sentinel_sysmon_replay_rules.xml`](../detections/sentinel_sysmon_replay_rules.xml).

- **Base structural rules `100100–100104` (Level 0):** classify events without alerting. Rule `100101` is the general Level 0 structural rule for Sysmon Event ID 1 (process creation); it has no dedicated `services.exe` → `svchost.exe` condition. Alerts come only from the behavioral rules below.
- **Behavioral rules `100110`, `100111`, `100112`, `100120`, `100130`, `100131`, `100140` (Levels 8–14 across the seven):** cover process creation, script execution, `comsvcs.dll` MiniDump-related activity, PowerShell network egress, and `lsass.exe` / `rundll32.exe` process access.

**Two replay workflows:**

| | EVTX replay (v0.4) | JSON replay (v0.9) |
|---|---|---|
| Input | Pre-recorded Windows Sysmon `.evtx` captures (not committed to the repository) | Replay JSON events |
| Conversion | NDJSON via [`scripts/evtx_to_wazuh.py`](../scripts/evtx_to_wazuh.py) | None needed; already JSON |
| Ingestion | Replayed through SENTINEL-LINUX01 and processed by Wazuh | Wazuh manager-side logcollector tailing `/var/ossec/logs/sentinel-sysmon-replay.json` |
| Result | Seven selected detections observed; three benign `services.exe` → `svchost.exe` events matched the general Level 0 EID1 base Rule `100101` and generated no alerts | Alerts for Rules `100110`, `100130` and `100140` |
| Documentation | [CASE-002](../investigations/CASE-002.md); [evidence/sysmon-replay](../evidence/sysmon-replay/) | [v0.9 evidence](../evidence/v0.9/readme.md) |

For the EVTX replay, 3 captures were converted into 12 NDJSON records (24 lines replayed). The 7 raw alert records are in [`sysmon_alerts_raw.json`](../evidence/sysmon-replay/sysmon_alerts_raw.json), SHA-256 `b53473fd6340ec17365fec9cbbc1403e445523322c4c84ae28e40882995d7a59`.

**v0.6 controlled measurement (Sysmon replay, [report](../metrics/v0.6-purple-team-measurement.md)):** 7/7 selected detections fired, and 0/3 benign `svchost.exe` events alerted; they matched the general Level 0 EID1 base rule and generated no alert. Two EID 7 ImageLoad events remained uncovered by the ruleset. These are small controlled samples on replayed telemetry, not statistically meaningful detection or false-positive rates. Cross-VM timing is subject to the clock-skew caveat in Section 5.2, and no negative raw delta is presented as detection latency.

**Limits:**
- Both workflows are replay-based. Sysmon is not installed or running on a live Windows machine in the lab, and the Sysmon kernel driver is not exercised.
- The seven detections are seven selected replay detections, not seven confirmed attacks. A rule firing on replayed telemetry shows the rule logic matched that sample. It does not by itself establish malicious activity. For example, `lsass.exe` access does not show successful credential dumping, and a PowerShell network connection does not show a file transfer.
- The JSON replay produced alerts for three of the behavioral rules. No claim is made that each Sysmon rule has been validated independently beyond the replay samples above.
- **v0.7 mutation finding (CASE-004):** a Sysmon command-line mutation bypassed the keyword-specific Rule `100112` and matched base EID1 Rule `100101` at Level 0. This is an observed gap in that rule's keyword-based logic for the tested sample. Correlation with EID10/EID11 events was identified as a potential improvement and is not implemented.

### 5.6 Python-assisted triage boundary

[`python-soc-automation`](https://github.com/andyydz/python-soc-automation) is a separate project. It processes Wazuh alert JSON and provides Python-assisted severity triage. The v0.9 workflow used `--triage --min-level 8`. The integration includes fallback extraction of Sysmon fields (`targetFilename`, `image`, `targetImage`) when `syscheck.path` is absent. The project now passes 195 pytest tests across its triage, schema 1.2, and CLI flag regression suite. That count describes the Python tool's own tests, not validation of the Wazuh detections.

Boundaries:
- It is an external tool, not a native Wazuh detection rule or feature.
- It does not automatically perform containment, eradication, or recovery.
- It is not a production SOAR platform.

---

## 6. Known Limitations and Lessons

Current status, scope, and the unresolved historical 16 October question are recorded in Section 5; the lessons below are the general takeaways.

- **A limited set of validated scenarios is not complete coverage.** Rule 100002 is confirmed for the documented controlled modification scenarios, and Rules 100003 and 100004 for three single-file lifecycle sessions, with a separate v0.6 controlled lifecycle session also recorded. Other paths, file types, and event types are not established by these results.
- **An observed alert is not a validated detection.** Rules 100003 and 100004 were observed on 31 October 2026 under an application configuration path, without an established trigger, in a single terminal screenshot (Set A). That observation shows they fired in that instance only.
- **Screenshots and source records are different levels of evidence.** The 16 October results were reviewed from the source alert record; the 11 October result is supported by screenshots only; the 31 October Set A observation and the 2 November session rest on terminal screenshots; the 18 November session and 31 October Set B are supported by raw alert JSON records. Claims should state which level of evidence supports them.
- **A built-in rule alert is not a custom rule alert.** Each custom FIM rule is a child of a built-in rule (100002 of 550, 100003 of 554, 100004 of 553). A built-in alert for an event type does not by itself show that the corresponding custom rule was loaded, and the reviewed 16 October records leave that question open. Each custom rule covers one event type; Rule 100002 is not expected to fire on creation or deletion.
- **Configuration inspected now is not configuration that ran then.** The on-disk rule file, later rule changes, and the untested matching behavior (Section 5.3) mean path-scope claims remain working assumptions.
- **Tuning is not the same as noise resolved.** v0.8 exclusions and group isolation were implemented and verified with one probe, but residual desktop noise remains and the broader retest is pending.
- **A syntax check is not validation, and validation is not comprehensive coverage.** A syntax check establishes only that the configuration is syntactically valid.
- **Replay is not live monitoring.** Sysmon detections were exercised on replayed telemetry. They show the rule logic matches those samples, not that a live Windows endpoint is monitored or that the rules would fire on live traffic.
- **Keyword-specific rules are brittle.** The v0.7 command-line mutation bypassed Rule `100112` and fell to a Level 0 base rule, so a rule that fires on a sample does not imply it is resilient to variations.
- **A sliding window carries earlier activity forward.** In the v0.6 SSH measurement, the first C2 escalation fired early because failures from C1 were still inside the 60-second window. Escalation timing depends on prior activity, not only on the current burst.
- **Small controlled samples are not rates.** The v0.6 results (for example 3/3, 7/7, 0/3) describe selected samples only and must not be quoted as detection or false-positive rates.
- **Clock skew distorts cross-VM timing.** Negative raw deltas are clock artefacts, not negative detection latency.
- **Triage is not detection or response.** The external Python triage tool prioritises alerts for an analyst. It does not detect, contain, eradicate, or recover.
- **A detection alert does not prove malicious activity.** Whether from a FIM, SSH, or Sysmon rule, an alert is evidence of an event matching rule logic but does not, by itself, establish malicious intent or reliably identify who caused it. That determination requires investigation ([CASE-001](../investigations/CASE-001.md), [CASE-003](../investigations/CASE-003.md), [`06-incident-response.md`](06-incident-response.md)), not inference from the alert alone.

---

## 7. Future Plans

The following are **not yet done**. They are post-closeout engineering and validation work for the open items in Sections 5 and 6, and none of it is a prerequisite for CASE-001 closure. Items that earlier versions of this document listed as planned and that are now implemented (SSH detection, Sysmon replay detection, initial purple-team measurement in v0.6, and mutation testing in v0.7) are described in Section 5 instead.

**Retest and tuning**
- Complete the broader post-v0.8 noise-suppression retest, including the residual `dconf/user` noise
- Design repeatable regression tests for file **creation**, **modification**, and **deletion** events within the configured `/home` scope, with explicit pass/fail criteria
- Test FIM rules for false positives and false negatives against legitimate activity, and tune only after review and approval

**Rule configuration and historical evidence recovery**
- Verify the manager's current active rule configuration on SENTINEL-WAZUH, including which versions of Rules 100002, 100003 and 100004 it is running now
- Attempt to reconstruct the manager's historical loaded configuration for the earlier tests, if available evidence permits; the historical state may not be recoverable, in which case it remains unconfirmed
- Systematically test the matching behavior of the `^/home/` condition against other outside-scope paths and case, beyond the v0.6 `/tmp` negative control, and validate the Tracker3/Nautilus negative conditions with targeted tests
- Determine whether custom Rules 100003 and 100004 were deployed and loaded on 16 October and, if they were, why they are not present in the reviewed records. CASE-001 leaves the historical loaded configuration unknown, and it may not be recoverable
- Keep the documented definitions of Rules 100002–100004 (parents, anchored matching, negative conditions) in step with `local_rules.xml`, and explain the difference between the 16 October and 31 October observations if available evidence permits
- Continue post-closeout historical evidence recovery and attribution work related to unresolved CASE-001 findings, where available evidence permits. This work does not reopen or condition CASE-001 closure

**SSH and Sysmon**
- Test SSH detection beyond the single controlled scenario, including behavior against legitimate authentication activity
- Improve resilience of Sysmon behavioral rules to command-line mutation, including EID10/EID11 correlation
- Review the two EID 7 ImageLoad events that remained uncovered in v0.6 and decide whether coverage is warranted
- Validate Sysmon detections on a live Windows endpoint with real Sysmon telemetry; this requires a Windows/AD endpoint that does not exist yet

**Expansion**
- Add project-level MITRE ATT&CK technique mapping for implemented detections, with care not to treat mappings as proof of attack
- Add broader telemetry sources and detection coverage
- Larger and repeatable purple-team measurement beyond the v0.6 controlled samples (including resolving the endpoint/manager clock skew so timing can be measured), and further mutation testing
- Deeper DFIR capability
- Carefully controlled response automation with human approval; automated containment, eradication, and recovery are not implemented

These remain future work and are not claimed as current capabilities.
