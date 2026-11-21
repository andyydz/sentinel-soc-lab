# SENTINEL Detection Library

This directory documents the detection content implemented in the SENTINEL lab: what each detection is, where it lives, how it was tested, and what remains untested. A rule that exists is not a rule that works. Every detection listed here is labeled by its actual validation status, scoped to the specific scenario that was tested.

Design methodology is covered in `../docs/05-detection-engineering.md`; test results and metrics are tracked in `../docs/07-testing-and-metrics.md`. This README is the index between the two and does not duplicate either document.

---

## 1. Current Detections

The table lists the three custom Linux FIM rules. SSH and Sysmon rules are covered in the inventory below and in Sections 2 and 3.

| ID | Detection | Status | Scenario and evidence basis |
|---|---|---|---|
| — | Wazuh custom Rule 100002 (Level 8, parent Rule 550): FIM file-modification alert on monitored paths | Validated for the controlled scenarios listed (modification and lifecycle sessions); v0.8 tuned and probe-verified | Controlled modifications of `/home/sentinel-admin/sentinel-fim-validation.txt` (11 October 2026, screenshot-supported) and `/home/sentinel-admin/sentinel-v02-mod-test.txt` (26 October 2026); modification step of the 2 November, 20 November (v0.6 measurement) and 21 November (v0.8 probe) lifecycle sessions |
| — | Wazuh custom Rule 100003 (Level 8, parent Rule 554): FIM file-creation alert | Observed (31 Oct, not a controlled test); validated in three controlled lifecycle sessions only (2 Nov, 20 Nov, 21 Nov); v0.8 tuned and probe-verified | 2 Nov: `/home/sentinel-admin/sentinel-v03-final-test.txt`. 20 Nov (v0.6): `~/sentinel-v06-pt-fim.txt`. 21 Nov: `/home/sentinel-admin/.v08-check/probe.txt`. Separate 31 Oct alert under `/home/sentinel-admin/snap/firmware-updater/262/.config/bus/` had unestablished trigger origin |
| — | Wazuh custom Rule 100004 (Level 8, parent Rule 553): FIM file-deletion alert | Observed (31 Oct, not a controlled test); validated in three controlled lifecycle sessions only (2 Nov, 20 Nov, 21 Nov); v0.8 tuned and probe-verified | Same sessions and 31 Oct observation as Rule 100003 |

All three rules now have controlled lifecycle evidence from three separate controlled sessions (2 November, 20 November v0.6 measurement, 21 November v0.8 probe), and validation is limited to those sessions. The 31 October observation (screenshot-only, not a controlled test) and the three controlled sessions are separate records and are not merged into one test. Three sessions are not a regression suite and do not establish comprehensive coverage.

### Consolidated Detection Inventory

| Family | Rules | Telemetry | Validation & Scope Notes |
|---|---|---|---|
| Linux FIM | `100002`–`100004` (`detections/local_rules.xml`) | Wazuh Syscheck (`SENTINEL-LINUX01`, Agent `002`) | Controlled evidence: Rule 100002 modification tests (11 Oct, 26 Oct); three controlled single-file lifecycle sessions (2 Nov; 20 Nov v0.6 measurement, 3/3 selected lifecycle events detected with Rules 100003/100002/100004 at Level 8, plus 0/3 `/tmp` negative-control alerts; 21 Nov v0.8 probe). 31 Oct alerts are observations only, not a controlled test. v0.8 tuning implemented and probe-verified; broader noise-suppression retest pending. Not comprehensive `/home` coverage |
| SSH | `100200`–`100201` (`detections/sentinel_ssh_bruteforce_rules.xml`) | `sshd` authentication logs on `SENTINEL-LINUX01` (Agent `002`); failures generated from `SENTINEL-KALI` | `CASE-003` (21 failed attempts), v0.6 controlled measurement (C1/C2), and a v0.8 `wazuh-logtest` check of the threshold behavior. One source; not tested against legitimate authentication activity |
| Windows Sysmon | `100100`–`100140` (`detections/sentinel_sysmon_replay_rules.xml`) | Replayed Sysmon telemetry: EVTX replay (`CASE-002`) and JSON replay (v0.9); no live Windows endpoint | Selected detections fired on replayed samples (v0.6: 7/7 selected). v0.9 JSON replay produced alerts for `100110`, `100130` and `100140` only; not every Sysmon rule was independently validated by v0.9 |

Implementation details (Rule 100002):

- Configured on the Wazuh Manager at `/var/ossec/etc/rules/local_rules.xml`
- Tested on SENTINEL-LINUX01
- Test record and investigation: `../investigations/CASE-001.md` and `../investigations/fim-rule-100002-investigation.md`
- Evidence directories: `../evidence/v0.3/` (earlier pipeline evidence: `../evidence/v0.2/`)

Custom FIM rules `100002`–`100004` are maintained in `detections/local_rules.xml` (`<group name="local,syscheck,sentinel_fim,">`), SSH rules `100200`–`100201` in `detections/sentinel_ssh_bruteforce_rules.xml`, and Sysmon replay rules `100100`–`100140` in `detections/sentinel_sysmon_replay_rules.xml`.

**Confirmed validation scope (Rule 100002, modification):**

- **11 October 2026:** existing screenshots support a Level 8 Rule 100002 alert for a controlled modification of `/home/sentinel-admin/sentinel-fim-validation.txt`. The original source alert log could not be recovered during the 26 October review.
- **26 October 2026:** two Level 8 Rule 100002 modification alerts were observed in terminal output for `/home/sentinel-admin/sentinel-v02-mod-test.txt`: `2026-10-26T21:38:27.910+0530` (size 0 → 23 bytes) and `2026-10-26T21:38:48.473+0530` (size 23 → 61 bytes). These are two alerts from consecutive modifications of one file, not two independent test cases. The screenshot is referenced in CASE-001 and the v0.3 evidence index at `../evidence/v0.2/screenschots/v0.2-oct26-controlled-modification-source-alerts-new.png` (existing directory spelling preserved); its presence has not been independently verified here.

**Controlled lifecycle sessions (Rules 100002, 100003, 100004):**

- **2 November 2026:** one controlled session on one dedicated file, `/home/sentinel-admin/sentinel-v03-final-test.txt`, created, modified and deleted. Creation matched Rule 100003, modification Rule 100002, deletion Rule 100004, each at Level 8. Evidence is a terminal screenshot (`../evidence/v0.3/screenshots/v0.3-fim-full-lifecycle-custom-rules.png`, path as referenced in `../docs/05-detection-engineering.md` and not verified here); raw alert JSON is not committed.
- **20 November 2026 (v0.6 measurement):** a separate controlled FIM lifecycle measurement on `~/sentinel-v06-pt-fim.txt`: creation matched Rule 100003, modification Rule 100002, deletion Rule 100004, each at Level 8 (3/3 selected lifecycle events). Details in Section 4.
- **21 November 2026 (v0.8 live Agent `002` probe):** `/home/sentinel-admin/.v08-check/probe.txt` created, modified and deleted; all three rules fired at Level 8. Details in Section 10.

These are three separate controlled sessions, each one lifecycle on one file. These results validate only those scenarios. Three sessions are not a regression suite or repeatability test and do not establish complete `/home` coverage.

**Observed detections (Rules 100003 and 100004, 31 October 2026):**

- Rule 100003 (creation, Level 8) and Rule 100004 (deletion, Level 8) were observed at approximately 18:51:56 IST, with paths under `/home/sentinel-admin/snap/firmware-updater/262/.config/bus/`.
- The evidence is a single terminal screenshot showing both alerts: `../evidence/v0.3/screenshots/v0.3-fim-lifecycle-custom-detections.png`. It is not a raw alert record and not a repeatable test. Raw alert records are not committed.
- The paths are in an application configuration directory. Whether the events were deliberately triggered or ordinary application activity has not been established, and no process attribution or root cause exists.
- These are **observed alerts**, not controlled tests. They show that each rule fired in the observed instance only; they do not establish repeatability, behavior for other paths or file types, or complete FIM coverage. The later 2 November session does not retroactively validate them.
- The 11 October and 26 October modification tests, the 16 October built-in-rule observations, the 31 October custom-rule observations, the 2 November session, the v0.6 measurement and the 21 November probe were separate sessions. They do not constitute one end-to-end lifecycle test. Rule 100002 is the modification rule and is not claimed to handle creation or deletion.

**16 October 2026 reviewed records** (`/home/sentinel-admin/sentinel-audit-test.txt`):

| Event | Rule shown in reviewed record | Timestamp | Custom rule designed for this event |
|---|---|---|---|
| Creation | Built-in Rule 554 (Level 5) | `2026-10-16T11:40:06.007+0530` | Rule 100003 (child of 554): absent from the reviewed record |
| Deletion | Built-in Rule 553 (Level 7) | `2026-10-16T12:31:32.819+0530` | Rule 100004 (child of 553): absent from the reviewed record |

- These statements are limited to the two reviewed records, each a single controlled action. They do not validate Rules 100003 or 100004.
- Rule 100002 is the modification rule (parent Rule 550) and is not the rule designed to cover creation or deletion, so its absence from these records is not itself a finding.
- **Unresolved:** whether custom Rules 100003 and 100004 were deployed and loaded on 16 October and, if they were, why they are not present in the reviewed records. CASE-001 leaves the historical loaded configuration unknown, and no explanation is asserted. Their later matches (31 Oct, 2 Nov, 20 Nov, 21 Nov) do not answer this.
- Rules 100002–100004 were changed after the early tests (v0.2 standardisation per project history; v0.8 tuning), so the configuration loaded during earlier sessions may differ from the current on-disk definition. The historical loaded configuration has not been reconstructed.
- Earlier versions of this document recorded Rule 100002 as firing on creation; that is not supported by the reviewed records.

What "validated" does not mean here:

- Creation and deletion detection by the custom rules: validated only for the three controlled single-file lifecycle sessions (2 Nov, 20 Nov v0.6 measurement, 21 Nov probe). The 31 October observations had no established trigger, and on 16 October only built-in Rules 554 and 553 appeared in the reviewed records.
- False-positive behavior against legitimate `/home` activity: not comprehensively tested. The v0.6 `/tmp` negative control produced 0/3 alerts, but `/tmp` is outside the monitored scope and this is not a false-positive rate. v0.7 raw alert telemetry showed Tracker3 and Nautilus activity that motivated the v0.8 exclusions.
- Systematic false-negative testing: not yet performed. The absence of Rules 100003 and 100004 from the 16 October records is an open question, not a measured miss rate.
- Repeatable regression testing: not yet established. Individual tests and observations, including the three controlled lifecycle sessions, are not a regression suite.
- Tuning: v0.8 tuning is implemented and probe-verified for one lifecycle on one file. Residual desktop noise remains, the exclusions have not been independently validated through dedicated tests, and the broader noise-suppression retest is pending. Tuning is not the same as noise resolved.
- MITRE ATT&CK mapping: documented as candidate/contextual mappings in rule files, detection docs, and investigation records (not standalone proof of malicious intent).

Rule definitions are committed as XML files in this directory (`local_rules.xml`, `sentinel_ssh_bruteforce_rules.xml`, `sentinel_sysmon_replay_rules.xml`). Packaged per-detection artifacts and dedicated per-detection subdirectories (e.g., `DET-001/`) have not yet been established and are planned once the detection content matures past single-scenario validation.

---

## 2. Sysmon Replay Ruleset (`sentinel_sysmon_replay_rules.xml`)

Defined in `sentinel_sysmon_replay_rules.xml` (`100100`–`100140`) and exercised via Sysmon replay telemetry (`CASE-002` EVTX replay and `v0.9` JSON replay):

- **Base filters (`100100`–`100104`, Level 0):** Match `Microsoft-Windows-Sysmon` JSON events for EID 1 (`100101`), EID 3 (`100102`), EID 10 (`100103`), and EID 11 (`100104`) without generating alerts. Rule `100101` suppresses benign `services.exe` → `svchost.exe` process-creation events.
- **Candidate behavioral detections (`100110`, `100111`, `100112`, `100120`, `100130`, `100131`, `100140`):** Mapped to candidate MITRE ATT&CK techniques (`T1059.003`/`T1059.001`, `T1059.005`, `T1003.001`/`T1218.011`, `T1105`) as triage hypotheses from replayed Sysmon fields—not standalone proof of confirmed malicious execution or complete post-exploitation activity.
- **EVTX replay (v0.4, `CASE-002`):** pre-recorded `.evtx` captures converted to NDJSON and replayed through `SENTINEL-LINUX01` (`Agent 002`) into `SENTINEL-WAZUH`; seven selected detections were observed and three benign `services.exe` → `svchost.exe` events were suppressed by Level 0 Rule `100101`.
- **JSON replay (v0.9):** replay JSON tailed by manager-side logcollector on `SENTINEL-WAZUH` (`/var/ossec/logs/sentinel-sysmon-replay.json`); alerts were produced for Rules `100110`, `100130` and `100140`. This does not mean every Sysmon rule was independently validated by v0.9.
- **Known gaps:** two EID 7 ImageLoad events remained uncovered by the ruleset (v0.6). A v0.7 command-line mutation (`CASE-004`) bypassed keyword-specific Rule `100112` and matched base EID 1 Rule `100101` at Level 0; correlation with EID 10/EID 11 events is a potential improvement and is not implemented.
- **Scope boundary:** exercised on replayed telemetry, not a live Windows endpoint or live `SysmonDrv.sys` kernel stream. A rule firing on a replayed sample shows the rule logic matched that sample, not that an attack occurred.

---

## 3. SSH Authentication Rules (`sentinel_ssh_bruteforce_rules.xml`)

- **Rule `100200` (Level 5):** matches SSH authentication failures from `sshd` logs on `SENTINEL-LINUX01` (`Agent 002`).
- **Rule `100201` (Level 10):** frequency-based escalation after six matching failures within 60 seconds from the same source IP.
- **Evidence:** `CASE-003` documented 21 failed attempts from `SENTINEL-KALI`, baseline `100200` alerts, `100201` escalation, and manual investigation confirming zero successful logins. v0.8 also verified the six-failure/60-second threshold in a stateful `wazuh-logtest` session (Section 9).
- **Scope:** one controlled source. Behavior against legitimate authentication activity has not been tested, and no detection or false-positive rate is established.

---

## 4. v0.6 Controlled Measurement Summary

Source report: `../metrics/v0.6-purple-team-measurement.md` (path as referenced in `../docs/05-detection-engineering.md`; not inspected here).

- **FIM (20 November 2026, `~/sentinel-v06-pt-fim.txt`):** 3/3 selected lifecycle events detected: creation matched Rule `100003` (Level 8), modification Rule `100002` (Level 8) and deletion Rule `100004` (Level 8). 0/3 alerts for `/tmp` negative-control operations (outside the monitored scope). This is the second of three separate controlled FIM lifecycle sessions (2 Nov, 20 Nov, 21 Nov).
- **Sysmon (replayed telemetry):** 7/7 selected detections fired; 0/3 benign `svchost.exe` events alerted because of Level 0 suppression; two EID 7 ImageLoad events remained uncovered.
- **SSH:** C1 produced four Rule `100200` alerts and zero Rule `100201` escalations. C2 produced eight Rule `100200` alerts and two Rule `100201` escalations. The first C2 escalation occurred early because four C1 failures carried over into the 60-second sliding window and combined with two C2 failures; the second was triggered by the C2 burst.

**Caveats:** these are small controlled samples, not statistically meaningful detection or false-positive rates, and no rates are calculated here. Endpoint and manager clocks were skewed, so raw cross-VM timing deltas are unreliable; a negative raw delta is a clock artefact, not negative detection latency. No detection-latency figure is claimed.

---

## 5. Detection Lifecycle

Every detection in this library moves through the same stages:

Design → Implement → Test (controlled scenario) → Evaluate → Tune → Retest → Document

- Design: define the detection logic and the expected alert behavior before implementing.
- Implement: configure the rule on the Wazuh Manager and verify it loads without errors.
- Test: run a controlled activity in the lab and capture actual results. Syntax validation alone does not advance a detection past "implemented."
- Evaluate: compare actual vs. expected outcomes; a result is recorded as successful, failed, or inconclusive.
- Tune / Retest: adjust the rule based on results; any change resets the validation status until retested.
- Document: the test record lands in `../docs/07-testing-and-metrics.md` (or a case file for investigations), and this README's status table is updated.

Validation is always scoped to the scenario tested. Status labels in this README mean:

- Implemented: configured and syntax-validated, but not yet validated through a controlled test.
- Observed: an alert was seen firing, but the trigger origin is not established (it may be ordinary activity rather than a deliberate test). This confirms the rule fired in that instance only; it is not a controlled-test validation and does not establish repeatability.
- Validated: confirmed firing on at least one controlled scenario, with a known deliberate trigger. Scoped to that scenario.
- Tuned: configuration was changed to address noise or gaps. This is not the same as the noise being resolved.
- Pending retest: tuning exists, but the broader retest that would confirm its effect has not been completed.
- Planned: designed or intended, not yet implemented.
- Untested: implemented but never exercised.

---

## 6. Testing Evidence

Per-detection test results are not restated here. The sources are:

- `../investigations/CASE-001.md`: Rule 100002 validation, the 16 October creation/deletion records, the 26 October modification results, and the 31 October observation of Rules 100003 and 100004
- `../investigations/fim-rule-100002-investigation.md`: Rule 100002 lifecycle-event scope investigation
- `../investigations/CASE-002.md`, `../investigations/CASE-003.md`, `../investigations/CASE-004.md`: Sysmon EVTX replay, SSH brute-force scenario, and v0.7 mutation testing
- `../metrics/v0.6-purple-team-measurement.md`: v0.6 controlled measurements
- `../docs/07-testing-and-metrics.md`: methodology, metrics framework, and validation records
- `../evidence/v0.3/`, `../evidence/v0.2/`, `../evidence/v0.9/`, `../evidence/sysmon-replay/`: screenshots and alert output
  - `../evidence/v0.3/screenshots/v0.3-fim-lifecycle-custom-detections.png`: single terminal screenshot showing Rules 100003 and 100004 (31 October)
  - `../evidence/v0.3/screenshots/v0.3-fim-full-lifecycle-custom-rules.png`: terminal screenshot of the 2 November lifecycle session
  - `../evidence/v0.2/screenschots/v0.2-oct26-controlled-modification-source-alerts-new.png`: terminal output of the two 26 October Rule 100002 alerts (existing directory spelling preserved)

The 11 October result rests on existing screenshots, as the original alert log could not be recovered. The 16 October results come from reviewed source records on the Wazuh Manager; the raw records are not claimed to be committed to this repository. The 31 October and 2 November results rest on terminal screenshots; raw alert records are not committed. Screenshot and report paths above are as referenced in the investigation, evidence and design documents and have not been independently verified here.

Note: the Testing & Metrics document currently records the Rule 100002 validation in its general evidence section. A dedicated per-detection inventory entry (e.g., `DET-001`) has not been established there yet.

---

## 7. Limitations

- FIM coverage today is three custom rules on a single agent (`Agent 002`). Rule 100002 is validated for the controlled modification scenarios and lifecycle sessions above. Rules 100003 and 100004 are validated only in three controlled single-file lifecycle sessions (2 Nov, 20 Nov v0.6 measurement, 21 Nov) and were separately observed once on 31 Oct without an established trigger (not a controlled test). Three sessions are not a regression suite, and no complete `/home` coverage is claimed.
- Whether custom Rules 100003 and 100004 were deployed and loaded on 16 October is unresolved; the reviewed records show only built-in Rules 554 and 553, and CASE-001 leaves the historical loaded configuration unknown.
- The current on-disk rule definitions are not evidence of what the manager had loaded during earlier tests. The `^/home/` matching behavior against other outside-scope paths and case has not been systematically tested (the v0.6 `/tmp` negative control produced no alerts), and the Tracker3/Nautilus negative conditions have not been independently validated through targeted tests.
- Built-in Wazuh rules (e.g., Rules 550, 553, 554) generate telemetry but are not counted as SENTINEL detections until a scenario has been tested against them. A built-in rule firing does not establish whether a custom rule was loaded.
- v0.8 tuning has been implemented and verified with one live probe (one lifecycle, one file). Residual desktop noise under `/home/sentinel-admin/.config/dconf/user` still triggers Rule 100002, and the broader noise-suppression retest is pending. No before/after noise measurement is recorded here.
- v0.6 recorded small controlled measurements (Section 4). They are not statistically meaningful detection or false-positive rates, and cross-VM timing is subject to clock skew. No repeatable regression suite and no comprehensive false-positive or false-negative measurement exist.
- Sysmon detections were exercised on replayed telemetry only; a rule firing on a sample is not a confirmed attack, and keyword-specific rules can be bypassed by mutation (Rule `100112`, CASE-004).
- SSH detection was tested from one controlled source and not against legitimate authentication activity.
- All limitations above are documented rather than hidden; an honest gap list is more useful to reviewers than implied completeness.

---

## 8. Maintenance

- Rule changes are made on the Wazuh Manager; the XML files in this directory are the maintained definitions and should be kept in step with the manager's active configuration (not verified here).
- Any rule change resets that detection's status to "implemented" until a controlled retest is documented. This includes any change made to resolve the open 16 October questions above. For v0.8, the 21 November probe is the retest for one lifecycle on one file; the broader retest is pending.
- This README is updated whenever a detection changes status; the Testing & Metrics document is updated in the same commit.
- Evidence is never edited retroactively; a changed result is recorded as a new test.

---

## 9. v0.8 Reliability Tuning Notes (Implemented & Manager-Validated)

- **FIM group isolation (`detections/local_rules.xml`):** Moved custom FIM rules `100002` (modify, `T1565.001`), `100003` (create, `T1105`), and `100004` (delete, `T1070.004`) out of the `sshd` group block into `<group name="local,syscheck,sentinel_fim,">` so FIM alerts no longer inherit `sshd`.
- **Surgical noise exclusion vs. hidden-path coverage:** Added negated PCRE2 `file` conditions on `100002`–`100004` to filter `^/home/[^/]+/(\.cache/tracker3/|\.local/share/nautilus/tags/meta\.db-(?:shm|wal)$)` based on `v0.7` raw alert telemetry (`evidence/v0.7/fim_mutation_alerts_raw.json`), while deliberately preserving hidden dot-directory/file monitoring (such as `/home/sentinel-admin/.v07-hidden-dir/.v07-payload.sh`). Anchored `^/home/` matching was retained.
- **SSH frequency/window check (`sentinel_ssh_bruteforce_rules.xml`):** Verified in a stateful `wazuh-logtest` session that six sequential SSH authentication failures (`100200`, Level 5) from `10.10.10.20` within `60s` trigger `100201` (Level 10, `T1110`/`T1110.001`).
- **Validation boundary:** `wazuh-analysisd -t` and `wazuh-manager` reload succeeded on `SENTINEL-WAZUH`. Live endpoint verification on `SENTINEL-LINUX01` was later performed for one lifecycle (Section 10). The Tracker3/Nautilus exclusions have not been independently validated through dedicated tests, and suppression effectiveness beyond the probe is not established.

## 10. v0.8 Live Endpoint Verification (2026-11-21, Agent 002)

- **Controlled probe lifecycle (`sentinel-linux01`, Agent `002`):** Created, modified, and deleted `/home/sentinel-admin/.v08-check/probe.txt` and confirmed live alerts on `SENTINEL-WAZUH`:
  - `100003` (`fim_create`, Level 8) at `2026-11-21T11:39:20.241+0530`
  - `100002` (`fim_modify`, Level 8) at `2026-11-21T11:39:22.462+0530`
  - `100004` (`fim_delete`, Level 8) at `2026-11-21T11:39:24.483+0530`
- **Group & path check:** All three probe alerts carried `sentinel_fim` with `sshd` absent, and hidden dot-directory monitoring remained active without adding VMs.
- **Residual desktop noise noted:** `/home/sentinel-admin/.config/dconf/user` still triggered `100002` (`2026-11-21T11:39:16.756+0530`), recorded as normal desktop session activity rather than an intrusion indicator.
- **Status:** verified for this probe only. It is one lifecycle on one file, not a regression suite, and does not measure overall noise reduction; the broader noise-suppression retest remains pending.
