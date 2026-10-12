# SENTINEL Detection Library.

This directory documents the detection content implemented in the SENTINEL lab: what each detection is, where it lives, how it was tested, and what remains untested. A rule that exists is not a rule that works — every detection listed here is labeled by its actual validation status, scoped to the specific scenario that was tested.

Design methodology is covered in "../docs/05-detection-engineering.md"; test results and metrics are tracked in "../docs/07-testing-and-metrics.md". This README is the index between the two — it does not duplicate either document.

---

## 1. Current Detections

ID| Detection| Status| Validated scenario
—| Wazuh custom Rule 100002 (Level 8) — FIM file-modification alert on monitored paths| Validated (one scenario)| Controlled modification of "/home/sentinel-admin/sentinel-fim-validation.txt"; expected Level 8 alert observed

Implementation details (Rule 100002):

- Configured on the Wazuh Manager at "/var/ossec/etc/rules/local_rules.xml"
- Triggered during a controlled file-modification test on SENTINEL-LINUX01
- Full test record, screenshots, and alert output: "../investigations/CASE-001.md"
- Raw evidence: "../evidence/v0.3/" (earlier pipeline evidence: "../evidence/v0.2/")

What "validated" does not mean here:

- File creation and deletion events — not yet tested
- False-positive behavior against legitimate "/home" activity — not yet tested
- Systematic false-negative testing — not yet performed. Only the single positive scenario above has been exercised; the absence of recorded misses reflects untested coverage, not confirmed coverage.
- MITRE ATT&CK mapping — planned, none exists yet

No portable rule artifact has been committed to this directory, and no per-detection subdirectory (e.g., "DET-001/") exists yet. Both are planned once the detection content matures past single-scenario validation.

---

## 2. Detection Lifecycle

Every detection in this library moves through the same stages:

Design → Implement → Test (controlled scenario) → Evaluate → Tune → Retest → Document

- Design — define the detection logic and the expected alert behavior before implementing.
- Implement — configure the rule on the Wazuh Manager and verify it loads without errors.
- Test — run a controlled activity in the lab and capture actual results. Syntax validation alone does not advance a detection past "implemented."
- Evaluate — compare actual vs. expected outcomes; a result is recorded as successful, failed, or inconclusive.
- Tune / Retest — adjust the rule based on results; any change resets the validation status until retested.
- Document — the test record lands in "../docs/07-testing-and-metrics.md" (or a case file for investigations), and this README's status table is updated.

Validation is always scoped to the scenario tested. Status labels in this README mean:

- Implemented — configured and syntax-validated, but not yet validated through a controlled test.
- Validated — confirmed firing on at least one controlled scenario.
- Planned — designed or intended, not yet implemented.
- Untested — implemented but never exercised.

---

## 3. Testing Evidence

Per-detection test results are not restated here — the source of truth is:

- "../docs/07-testing-and-metrics.md" — methodology, metrics framework, and validation records
- "../investigations/CASE-001.md" — the controlled Rule 100002 validation and initial investigation
- "../evidence/v0.3/", "../evidence/v0.2/" — screenshots, log excerpts, and alert output

Note: the Testing & Metrics document currently records the Rule 100002 validation in its general evidence section. A dedicated per-detection inventory entry (e.g., "DET-001") has not been established there yet.

---

## 4. Limitations

- Coverage today is a single custom rule validated on a single scenario, on a single agent.
- Built-in Wazuh rules (e.g., Rule 550) generate telemetry but are not counted as SENTINEL detections until a scenario has been tested against them.
- No detection has been tuned yet, so no before/after comparison exists.
- All limitations above are documented rather than hidden; an honest gap list is more useful to reviewers than implied completeness.

---

## 5. Maintenance

- Rule changes are made in "local_rules.xml" on the Wazuh Manager and mirrored here only once committed as artifacts.
- Any rule change resets that detection's status to "implemented" until a controlled retest is documented.
- This README is updated whenever a detection changes status; the Testing & Metrics document is updated in the same commit.
- Evidence is never edited retroactively — a changed result is recorded as a new test.
