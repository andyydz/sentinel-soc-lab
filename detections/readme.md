# SENTINEL Detection Library

This directory documents the detection content implemented in the SENTINEL lab: what each detection is, where it lives, how it was tested, and what remains untested. A rule that exists is not a rule that works. Every detection listed here is labeled by its actual validation status, scoped to the specific scenario that was tested.

Design methodology is covered in `../docs/05-detection-engineering.md`; test results and metrics are tracked in `../docs/07-testing-and-metrics.md`. This README is the index between the two and does not duplicate either document.

---

## 1. Current Detections

| ID | Detection | Status | Scenario and evidence basis |
|---|---|---|---|
| — | Wazuh custom Rule 100002 (Level 8): FIM file-modification alert on monitored paths | Validated (modification scenarios tested only) | Controlled modifications of `/home/sentinel-admin/sentinel-fim-validation.txt` (11 October 2026) and `/home/sentinel-admin/sentinel-v02-mod-test.txt` (26 October 2026); expected Level 8 alerts observed |
| — | Wazuh custom Rule 100003 (Level 8): FIM file-creation alert | Observed, not validated through controlled testing | Alert observed on 31 October 2026 (~18:51:56 IST) under `/home/sentinel-admin/snap/firmware-updater/262/.config/bus/`; trigger origin not established |
| — | Wazuh custom Rule 100004 (Level 8): FIM file-deletion alert | Observed, not validated through controlled testing | Alert observed on 31 October 2026 (~18:51:56 IST) under `/home/sentinel-admin/snap/firmware-updater/262/.config/bus/`; trigger origin not established |

Implementation details (Rule 100002):

- Configured on the Wazuh Manager at `/var/ossec/etc/rules/local_rules.xml`
- Tested on SENTINEL-LINUX01
- Test record and investigation: `../investigations/CASE-001.md` and `../investigations/fim-rule-100002-investigation.md`
- Evidence directories: `../evidence/v0.3/` (earlier pipeline evidence: `../evidence/v0.2/`)

The definitions of Rules 100003 and 100004 have not been reviewed for this README, and their configuration location and matching behavior are not documented here.

**Confirmed validation scope (Rule 100002, modification only):**

- **11 October 2026:** existing screenshots support a Level 8 Rule 100002 alert for a controlled modification of `/home/sentinel-admin/sentinel-fim-validation.txt`. The original source alert log could not be recovered during the 26 October review.
- **26 October 2026:** two Level 8 Rule 100002 modification alerts were observed in terminal output for `/home/sentinel-admin/sentinel-v02-mod-test.txt`: `2026-10-26T21:38:27.910+0530` (size 0 → 23 bytes) and `2026-10-26T21:38:48.473+0530` (size 23 → 61 bytes). These are two alerts from consecutive modifications of one file, not two independent test cases. The screenshot is referenced in CASE-001 and the v0.3 evidence index at `../evidence/v0.2/screenschots/v0.2-oct26-controlled-modification-source-alerts-new.png` (existing directory spelling preserved); its presence has not been independently verified here.

These validate the tested modification scenarios only. They do not establish complete `/home` coverage or validated creation/deletion detection.

**Observed detections (Rules 100003 and 100004, 31 October 2026):**

- Rule 100003 (creation, Level 8) and Rule 100004 (deletion, Level 8) were observed at approximately 18:51:56 IST, with paths under `/home/sentinel-admin/snap/firmware-updater/262/.config/bus/`.
- The evidence is a single terminal screenshot showing both alerts: `../evidence/v0.3/screenshots/v0.3-fim-lifecycle-custom-detections.png`. It is not a raw alert record and not a repeatable test. Raw alert records are not committed.
- The paths are in an application configuration directory. Whether the events were deliberately triggered or ordinary application activity has not been established, and no process attribution or root cause exists.
- These are **observed alerts**, not controlled-test validations. They show that each rule fired in the observed instance only; they do not establish repeatability, behavior for other paths or file types, or complete FIM coverage.
- The 11/26 October, 16 October and 31 October observations are separate sessions and are not one end-to-end lifecycle test. Rule 100002 is not claimed to handle creation or deletion.

**16 October 2026 reviewed records** (`/home/sentinel-admin/sentinel-audit-test.txt`):

| Event | Rule shown in reviewed record | Timestamp | Rule 100002 |
|---|---|---|---|
| Creation | Built-in Rule 554 (Level 5) | `2026-10-16T11:40:06.007+0530` | Absent from the reviewed record |
| Deletion | Built-in Rule 553 (Level 7) | `2026-10-16T12:31:32.819+0530` | Absent from the reviewed record |

- These statements are limited to the two reviewed records. They do not show how Rule 100002 behaves for other creation or deletion events.
- The reason Rule 100002 was absent from these records is **unresolved**. This is an observation, not a confirmed detection failure, and no root cause is established. Rule 100002 has been described as depending on parent Rule 550 (`<if_sid>550</if_sid>`), but the active rule definition and its matching behavior have not been re-verified, and that dependency is not asserted as the cause.
- Rule 100002 has not been changed.
- Why Rules 100003 and 100004 were observed on 31 October when built-in Rules 554 and 553 appeared on 16 October is also unresolved.
- Earlier versions of this document recorded Rule 100002 as firing on creation; that is not supported by the reviewed records.

What "validated" does not mean here:

- Creation and deletion detection by the custom rules: not validated. Rules 100003 and 100004 have each been observed once, without an established trigger; on 16 October only built-in Rules 554 and 553 appeared in the reviewed records.
- False-positive behavior against legitimate `/home` activity: not yet tested.
- Systematic false-negative testing: not yet performed. The absence of Rule 100002 from the two reviewed records is an open question, not a measured miss rate.
- Repeatable regression testing: not yet established. Individual tests and observations are not a regression suite.
- Tuning: not performed. The reported `/home/` matching scope remains an area for further noise evaluation.
- MITRE ATT&CK mapping: planned, none exists yet.

No portable rule artifact has been committed to this directory, and no per-detection subdirectory (e.g., `DET-001/`) exists yet. Both are planned once the detection content matures past single-scenario validation.

---

## 2. Detection Lifecycle

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
- Validated: confirmed firing on at least one controlled scenario, with a known deliberate trigger.
- Planned: designed or intended, not yet implemented.
- Untested: implemented but never exercised.

---

## 3. Testing Evidence

Per-detection test results are not restated here. The sources are:

- `../investigations/CASE-001.md`: Rule 100002 validation, the 16 October creation/deletion records, the 26 October modification results, and the 31 October observation of Rules 100003 and 100004
- `../investigations/fim-rule-100002-investigation.md`: Rule 100002 lifecycle-event scope investigation
- `../docs/07-testing-and-metrics.md`: methodology, metrics framework, and validation records
- `../evidence/v0.3/`, `../evidence/v0.2/`: screenshots and alert output
  - `../evidence/v0.3/screenshots/v0.3-fim-lifecycle-custom-detections.png`: single terminal screenshot showing Rules 100003 and 100004 (31 October)
  - `../evidence/v0.2/screenschots/v0.2-oct26-controlled-modification-source-alerts-new.png`: terminal output of the two 26 October Rule 100002 alerts (existing directory spelling preserved)

The 11 October result rests on existing screenshots, as the original alert log could not be recovered. The 16 October results come from reviewed source records on the Wazuh Manager; the raw records are not claimed to be committed to this repository. The 31 October result rests on one terminal screenshot; raw alert records are not committed. Screenshot paths above are as referenced in the investigation and evidence documents and have not been independently verified here.

Note: the Testing & Metrics document currently records the Rule 100002 validation in its general evidence section. A dedicated per-detection inventory entry (e.g., `DET-001`) has not been established there yet.

---

## 4. Limitations

- Coverage today is three custom rules on a single agent: one (Rule 100002) validated on modification scenarios only, and two (Rules 100003 and 100004) observed once without validation through controlled testing.
- Rule 100002 was absent from the two reviewed 16 October creation/deletion records, and the reason is unresolved.
- The trigger origin of the 31 October creation/deletion alerts is not established, and no complete `/home` coverage is claimed.
- Built-in Wazuh rules (e.g., Rules 550, 553, 554) generate telemetry but are not counted as SENTINEL detections until a scenario has been tested against them. A built-in rule firing does not establish whether a custom rule should cover the same event.
- No detection has been tuned yet, so no before/after comparison exists.
- No repeatable regression testing, false-positive/false-negative measurement, or detection metrics exist yet.
- All limitations above are documented rather than hidden; an honest gap list is more useful to reviewers than implied completeness.

---

## 5. Maintenance

- Rule changes are made in `local_rules.xml` on the Wazuh Manager and mirrored here only once committed as artifacts.
- Any rule change resets that detection's status to "implemented" until a controlled retest is documented. This includes any change made to resolve the open Rule 100002 questions above.
- This README is updated whenever a detection changes status; the Testing & Metrics document is updated in the same commit.
- Evidence is never edited retroactively; a changed result is recorded as a new test.
