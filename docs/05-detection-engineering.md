# SENTINEL Detection Engineering

> Does your detection still work when the attacker changes tactics?

This document defines SENTINEL's detection engineering process — how detections are designed, implemented, tested, and validated against real telemetry — and tracks the current state of detections actually built in the lab.

A detection is not considered working because a rule exists. It is considered working only once it has been tested against controlled activity in the lab and the result — pass, fail, or unresolved — has been documented.

---

## 1. Purpose and Scope

SENTINEL treats detection engineering as an evidence-driven discipline: every detection should be observable (grounded in real telemetry), testable (validated against a controlled scenario, not assumed), and explainable (an analyst can state exactly why it fired). This document covers the methodology used to build and validate detections, and documents the current implementation status honestly — including what is confirmed, what is partially confirmed, and what remains unresolved.

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

**Current instance — File Integrity Monitoring on `/home`:**

| Field | Value |
|---|---|
| Detection ID | Custom Wazuh Rule `100002` |
| Threat / Technique | Unauthorized or unexpected file modification within the configured `/home` monitoring scope; no MITRE ATT&CK mapping yet |
| Telemetry Source | Wazuh Syscheck (File Integrity Monitoring), real-time, with `/home` as the configured monitoring scope on SENTINEL-LINUX01 (`10.10.10.40`, Agent ID `002`) |
| Detection Logic | A read-only inspection of `/var/ossec/etc/rules/local_rules.xml` on SENTINEL-WAZUH showed Rule `100002` with Level 8, parent condition `<if_sid>550</if_sid>`, a `file` field condition containing `/home/`, and group `sentinel_fim`. This establishes the on-disk file at inspection time, **not** the version loaded by the running manager during the earlier tests. The exact matching behavior of the `file` field condition has **not** been verified. See Section 5 for the Rule 550 dependency. |
| Expected Alert | Level 8 alert identifying the changed file |
| Severity | Level 8 (custom rule), observed for the documented controlled modification tests. Wazuh's built-in Rule 550 (Level 7, "Integrity checksum changed") was also observed during the 11 October test. |
| Test Procedure | **Controlled modifications:** (1) 11 October 2026 — `/home/sentinel-admin/sentinel-fim-validation.txt`; screenshot evidence supports custom Rule `100002` firing at `2026-10-11T20:25:14.746+0530`. (2) 26 October 2026 — `/home/sentinel-admin/sentinel-v02-mod-test.txt`; two modifications each recorded a custom Rule `100002` Level 8 alert: `2026-10-26T21:38:27.910+0530` (file size 0 → 23 bytes) and `2026-10-26T21:38:48.473+0530` (file size 23 → 61 bytes). **Controlled creation and deletion (16 October 2026):** `/home/sentinel-admin/sentinel-audit-test.txt`. The reviewed source alert record shows built-in Rule `554` for creation and built-in Rule `553` for deletion; custom Rule `100002` is absent from each. These are reviewed records of individual controlled actions, not validations of custom Rule `100002` for creation or deletion (see Section 5). |
| Evidence | `evidence/v0.3/`; full investigation detail in `investigations/CASE-001.md`. **11 October:** supported by screenshot evidence; the original source alert record was not recovered during the later review, so this result is not source-log verified. **16 October:** reviewed from the source alert record at `/var/ossec/logs/alerts/2026/Oct/ossec-alerts-16.json`; this document does not claim that the raw log is committed to the repository. **26 October:** two alerts from two consecutive modifications of one file (not a regression suite); screenshot: [October 26 controlled-modification source alerts](../evidence/v0.2/v0.2-oct26-controlled-modification-source-alerts-new.png). |

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

This is the standard every detection in this document is held to, including the one currently implemented.

---

## 5. Current Implementation and Status

**Environment:**
- SENTINEL-WAZUH — Ubuntu 24.04, Wazuh 4.14.8, `10.10.10.10`
- SENTINEL-LINUX01 — Ubuntu 24.04, Wazuh Agent 4.14.8, `10.10.10.40`, Agent ID `002`

**What's implemented:**

| Component | Status |
|---|---|
| Real-time FIM with `/home` as the configured monitoring scope (Wazuh Syscheck) | Implemented; generated events in the documented controlled tests |
| Built-in Wazuh **Rule 550** (Level 7, "Integrity checksum changed") | **Observed** during the 11 October controlled modification test (screenshot-supported) |
| Custom **Rule 100002** (Level 8) — modification | **Confirmed for the documented controlled modification tests.** 11 October 2026: `/home/sentinel-admin/sentinel-fim-validation.txt`, `2026-10-11T20:25:14.746+0530` — screenshot-supported; original source alert record not recovered. 26 October 2026: `/home/sentinel-admin/sentinel-v02-mod-test.txt`, two Level 8 alerts at `2026-10-26T21:38:27.910+0530` (0 → 23 bytes) and `2026-10-26T21:38:48.473+0530` (23 → 61 bytes). |
| Built-in **Rule 554** ("File added to the system") — creation | **Reviewed source record** (16 October 2026): `/home/sentinel-admin/sentinel-audit-test.txt` shows Rule 554 at `2026-10-16T11:40:06.007+0530`. Custom Rule 100002 is **absent** from the reviewed record. |
| Built-in **Rule 553** ("File deleted") — deletion | **Reviewed source record** (16 October 2026): the same file shows Rule 553 at `2026-10-16T12:31:32.819+0530`. Custom Rule 100002 is **absent** from the reviewed record. |

**Scope of the confirmed result:** the controlled modification tests (11 and 26 October) show that Rule 100002 fires a Level 8 alert for modification of the test files within the configured `/home` monitoring scope in the scenarios tested. This validates **only those tested modification scenarios**. `/home` is the configured monitoring scope; that configuration does not guarantee that every change under the path is detected. Two modification tests on two files are not a regression suite and do not establish a detection rate.

**Reviewed 16 October 2026 records:** creation and deletion were each performed once as an individual controlled action. The source alert record at `/var/ossec/logs/alerts/2026/Oct/ossec-alerts-16.json` was reviewed; it shows built-in Rule 554 for creation and built-in Rule 553 for deletion, with custom Rule 100002 absent from each. These records do **not** validate custom Rule 100002 for creation or deletion. Why Rule 100002 was absent is **unresolved**. Rule 100002's on-disk definition depends on parent Rule 550, which is relevant context, but this is not a root-cause analysis and does not show that Rule 100002 can never fire on a creation or deletion event. Both events were alerted by built-in rules; whether the custom rule should also cover them is an open engineering question. Any ATT&CK mappings carried by built-in events are telemetry metadata, not evidence of malicious intent.

**Superseded earlier creation claim:** an earlier report stated that Rules 554 and 100002 fired together during creation. The reviewed source alert record does not support that claim. It is not retained as a positive creation result, and no cause for the earlier report is asserted.

**Rule configuration caveats:**
- **On-disk vs loaded rule:** the `local_rules.xml` inspection shows the file as it was at inspection time. It does not establish which version of Rule 100002 the running manager had loaded during the historical tests. That version has not been verified, and the rule has not been changed.
- **Field-condition matching:** the exact matching behavior of the `file` field condition containing `/home/` (for example, whether it acts as an unanchored substring or regular-expression match, and how it treats case) has not been verified. Descriptions of the rule as matching "paths under `/home/`" are a working assumption.

**Evidence reconciliation:** CASE-001 evidence reconciliation is closed for the reviewed scope. That closure covers the evidence reviewed; it does not mean the broader investigation or detection-engineering work is complete. The 11 October result remains screenshot-supported only, because its original source alert record was not recovered.

The current results do **not** establish:

- Validated coverage of custom Rule 100002 for file *creation* or *deletion* events — each has one reviewed source record in which Rule 100002 is absent, and the reason is unresolved
- Complete FIM coverage of the configured `/home` scope, or coverage of all lifecycle event types or file types
- Measured detection rates
- Broader false-positive or false-negative behavior (not yet tested)
- A repeatable regression suite (none exists)
- That the rule has been tuned or hardened — no tuning has occurred
- Any malicious activity — these were controlled lab tests, not attacks

These results are further reviewed in investigation `CASE-001` (`investigations/CASE-001.md`). Its evidence reconciliation for the reviewed scope is closed; the broader investigation and detection-engineering work remain open (follow-up work is listed in Section 7). SENTINEL v0.3 is not complete.

---

## 6. Known Limitations and Lessons

Current status, scope, and the unresolved 16 October finding are recorded in Section 5; the lessons below are the general takeaways.

- **A limited set of validated scenarios is not complete coverage.** Rule 100002 is confirmed only for the documented controlled modification scenarios of 11 and 26 October 2026 (one test file each). Other paths, file types, and event types are not established by these results.
- **Screenshots and source records are different levels of evidence.** The 16 October results were reviewed from the source alert record; the 11 October result is supported by screenshots only. Claims should state which level of evidence supports them.
- **A built-in rule alert is not a custom rule alert.** In the inspected on-disk definition, Rule 100002's parent condition is `<if_sid>550</if_sid>`; Rules 553 and 554 are not named as its parent. This does not establish the historically loaded configuration and is not offered as the cause of the 16 October absence. A built-in alert for one FIM event type should not be read as coverage by the custom rule, and a rule that matches one event type should not be assumed to match the others.
- **Configuration inspected now is not configuration that ran then.** The on-disk rule file and the unverified `/home/` matching behavior (Section 5) mean path-scope claims remain working assumptions.
- **A syntax check is not validation, and validation is not comprehensive coverage.** A syntax check establishes only that the configuration is syntactically valid. Rule 100002 moved from "syntax-valid only" to "confirmed firing" for the documented modification scenarios — a meaningful step, but still a narrow one.
- **A FIM alert does not prove malicious activity.** Whether from Rule 550, 553, 554, or Rule 100002, a file-integrity alert is evidence of a file-integrity event but does not, by itself, establish malicious intent or reliably identify who caused the change. That determination requires investigation (CASE-001, `docs/06-incident-response.md`), not inference from the alert alone.

---

## 7. Future Plans

The following are planned and **not yet implemented**. They are the follow-up work for the open items in Sections 5 and 6.

**Rule configuration and the 16 October finding**
- Verify the manager's current active rule configuration on SENTINEL-WAZUH, including which version of Rule 100002 it is running now
- Attempt to reconstruct the manager's historical loaded configuration for the earlier tests, if available evidence permits; the historical state may not be recoverable, in which case it remains unconfirmed
- Verify the matching behavior of the `file` field condition containing `/home/`
- Review built-in Rules 550, 553, and 554 and determine why Rule 100002 was absent from the reviewed creation and deletion records
- Decide whether custom Rule 100002 should cover creation and deletion and, after review and approval, design and test any rule change

**Testing and tuning**
- Design repeatable regression tests for file **creation**, **modification**, and **deletion** events within the configured `/home` scope, with explicit pass/fail criteria
- Test Rule 100002 for false positives and false negatives against legitimate activity within the configured `/home` scope, and tune only after review and approval

**Investigation and expansion**
- Complete CASE-001's broader review, timeline, root-cause, and attribution work
- Add broader telemetry sources: authentication activity and process/command execution
- Add MITRE ATT&CK technique mapping for implemented detections
- Add detection rules beyond File Integrity Monitoring
- Purple-team validation (detection rate, detection time, before/after comparison)
- Attack mutation testing (varying attacker technique to test detection resilience)

These remain future work and are not claimed as current capabilities.
