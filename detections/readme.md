# SENTINEL Detection Library

This directory documents the detection content implemented in the SENTINEL lab: what each detection is, where it lives, how it was tested, and what remains untested. A rule that exists is not a rule that works. Every detection listed here is labeled by its actual validation status, scoped to the specific scenario that was tested.

Design methodology is covered in `../docs/05-detection-engineering.md`; test results and metrics are tracked in `../docs/07-testing-and-metrics.md`. This README is the index between the two and does not duplicate either document.

---

## 1. Current Detections

| ID | Detection | Status | Validated scenario |
|---|---|---|---|
| — | Wazuh custom Rule 100002 (Level 8): FIM file-modification alert on monitored paths | Validated (modification scenarios tested only) | Controlled modifications of `/home/sentinel-admin/sentinel-fim-validation.txt` (11 October 2026) and `/home/sentinel-admin/sentinel-v02-mod-test.txt` (26 October 2026); expected Level 8 alerts observed |

Implementation details (Rule 100002):

- Configured on the Wazuh Manager at `/var/ossec/etc/rules/local_rules.xml`
- Tested on SENTINEL-LINUX01
- Test record and investigation: `../investigations/CASE-001.md` and `../investigations/fim-rule-100002-investigation.md`
- Evidence directories: `../evidence/v0.3/` (earlier pipeline evidence: `../evidence/v0.2/`)

**Confirmed validation scope (modification only):**

- **11 October 2026:** existing screenshots support a Level 8 Rule 100002 alert for a controlled modification of `/home/sentinel-admin/sentinel-fim-validation.txt`. The original source alert log could not be recovered during the 26 October review.
- **26 October 2026:** two Level 8 Rule 100002 modification alerts were observed in terminal output for `/home/sentinel-admin/sentinel-v02-mod-test.txt`: `2026-10-26T21:38:27.910+0530` (size 0 → 23 bytes) and `2026-10-26T21:38:48.473+0530` (size 23 → 61 bytes). A screenshot was reported as uploaded to `evidence/v0.2/v0.2-oct26-controlled-modification-source-alerts.png`; that path has not been verified here.

These validate the tested modification scenarios only. They do not establish complete `/home` coverage or validated creation/deletion detection.

**16 October 2026 reviewed records** (`/home/sentinel-admin/sentinel-audit-test.txt`):

| Event | Rule shown in reviewed record | Timestamp | Rule 100002 |
|---|---|---|---|
| Creation | Built-in Rule 554 | `2026-10-16T11:40:06.007+0530` | Absent from the reviewed record |
| Deletion | Built-in Rule 553 | `2026-10-16T12:31:32.819+0530` | Absent from the reviewed record |

- These statements are limited to the two reviewed records. They do not show how Rule 100002 behaves for other creation or deletion events.
- The reason Rule 100002 was absent from these records is **unresolved**. Rule 100002 has been described as depending on parent Rule 550 (`<if_sid>550</if_sid>`), but the active rule definition and its matching behavior have not been re-verified, and that dependency is not asserted as the cause.
- Rule 100002 has not been changed.
- Earlier versions of this document recorded Rule 100002 as firing on creation; that is not supported by the reviewed records.

What "validated" does not mean here:

- Creation and deletion detection by the custom rule: not validated. Only built-in Rules 554 and 553 were observed in the reviewed records.
- False-positive behavior against legitimate `/home` activity: not yet tested.
- Systematic false-negative testing: not yet performed. The absence of Rule 100002 from the two reviewed records is an open question, not a measured miss rate.
- Repeatable regression testing: not yet established. Individual tests are not a regression suite.
- Tuning: not performed. Broad `/home` matching remains an area for further noise evaluation.
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
- Validated: confirmed firing on at least one controlled scenario.
- Planned: designed or intended, not yet implemented.
- Untested: implemented but never exercised.

---

## 3. Testing Evidence

Per-detection test results are not restated here. The sources are:

- `../investigations/CASE-001.md`: controlled Rule 100002 validation, the 16 October creation/deletion records, and the 26 October modification results
- `../investigations/fim-rule-100002-investigation.md`: Rule 100002 lifecycle-event scope investigation
- `../docs/07-testing-and-metrics.md`: methodology, metrics framework, and validation records
- `../evidence/v0.3/`, `../evidence/v0.2/`: screenshots and alert output

The 11 October result rests on existing screenshots, as the original alert log could not be recovered. The 16 October results come from reviewed source records on the Wazuh Manager; the raw records are not claimed to be committed to this repository. The 26 October screenshot path above is reported but not verified.

Note: the Testing & Metrics document currently records the Rule 100002 validation in its general evidence section. A dedicated per-detection inventory entry (e.g., `DET-001`) has not been established there yet.

---

## 4. Limitations

- Coverage today is a single custom rule validated on modification scenarios only, on a single agent.
- Rule 100002 was absent from the two reviewed 16 October creation/deletion records, and the reason is unresolved.
- Built-in Wazuh rules (e.g., Rules 550, 553, 554) generate telemetry but are not counted as SENTINEL detections until a scenario has been tested against them. A built-in rule firing does not establish whether custom Rule 100002 should cover the same event.
- No detection has been tuned yet, so no before/after comparison exists.
- No repeatable regression testing, false-positive/false-negative measurement, or detection metrics exist yet.
- All limitations above are documented rather than hidden; an honest gap list is more useful to reviewers than implied completeness.

---

## 5. Maintenance

- Rule changes are made in `local_rules.xml` on the Wazuh Manager and mirrored here only once committed as artifacts.
- Any rule change resets that detection's status to "implemented" until a controlled retest is documented. This includes any change made to resolve the open Rule 100002 questions above.
- This README is updated whenever a detection changes status; the Testing & Metrics document is updated in the same commit.
- Evidence is never edited retroactively; a changed result is recorded as a new test.
