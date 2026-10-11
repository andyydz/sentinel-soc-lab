## SENTINEL Detection Engineering

«Does your detection still work when the attacker changes tactics?»

This document defines SENTINEL's detection engineering process — how detections are designed, implemented, tested, and validated against real telemetry — and tracks the current state of detections actually built in the lab.

A detection is not considered working because a rule exists. It is considered working only once it has been tested against controlled activity in the lab and the result — pass, fail, or unresolved — has been documented.

---

## 1. Purpose and Scope

SENTINEL treats detection engineering as an evidence-driven discipline: every detection should be observable (grounded in real telemetry), testable (validated against a controlled scenario, not assumed), and explainable (an analyst can state exactly why it fired). This document covers the methodology used to build and validate detections, and documents the current implementation status honestly — including what is confirmed, what is partially confirmed, and what remains unresolved.

---

## 2. Detection Engineering Lifecycle

DEFINE → IMPLEMENT → TEST → VALIDATE → TUNE → RETEST

Stage| What happens
Define| Identify the threat/behavior, the telemetry needed to observe it, and the detection objective
Implement| Write the detection logic (e.g., a Wazuh rule) against that telemetry
Test| Execute a controlled, reversible activity in the lab and capture the resulting telemetry
Validate| Confirm the detection fired as expected, with useful alert context, against that telemetry
Tune| Adjust the rule based on false positives/negatives or missing context
Retest| Re-run the same test to confirm the tuning actually fixed the issue

A detection only reaches Validated once Test and Validate have both produced the expected, documented result. Passing a syntax check is not the same as passing this lifecycle — see Section 6.

---

## 3. Detection Specification

Every detection should be documented against this template before and after implementation:

Field| Description
Detection ID| Unique project identifier
Threat / Technique| What behavior this addresses (MITRE ATT&CK mapping where confidently applicable)
Telemetry Source| Required log/event source
Detection Logic| Condition(s) that should trigger the alert
Expected Alert| What the alert should look like if the logic fires correctly
Severity| Intended severity level
Test Procedure| The controlled scenario used to validate it
Evidence| Supporting artifacts (screenshots, logs, alert output)

## Current instance — File Integrity Monitoring on "/home":

Field| Value
Detection ID| Custom Wazuh Rule "100002"
Threat / Technique| Unexpected file modification under "/home"; no MITRE ATT&CK mapping yet
Telemetry Source| Wazuh Syscheck (File Integrity Monitoring), real-time, scoped to "/home" on SENTINEL-LINUX01
Detection Logic| Matches a Syscheck file-integrity-changed event for a path containing "/home/"
Expected Alert| Level 8 alert identifying the changed file
Severity| Intended: Level 8 (custom rule); Observed during controlled validation: Level 8 from Rule 100002
Test Procedure| Controlled file modification performed directly on SENTINEL-LINUX01 within "/home"
Evidence| "evidence/v0.3/v0.3-custom-rule-100002.png"; "evidence/v0.3/v0.3-custom-rule-100002-dashboard-json.png"

---

## 4. Testing and Validation Methodology

Every test compares an expected result against an actual result, and the outcome is recorded regardless of whether it passed:

Expected: File modification → Syscheck telemetry → Rule fires → Alert generated
Actual:   Controlled modification → Syscheck event → Rule 100002 Level 8 alert confirmed

- Pass — the expected telemetry and alert were both observed for the scenario under test.
- Fail — the expected behavior did not occur; the failure is investigated and documented, not hidden.
- Unresolved / Inconclusive — part of the chain was confirmed, but the specific detection logic or behavior under test was not fully confirmed.

A successful controlled modification test does not automatically validate file creation, deletion, every monitored path, or detection performance across other scenarios. Those require separate tests.

---

## 5. Current Implementation and Status

Environment:

- SENTINEL-WAZUH — Ubuntu 24.04, Wazuh 4.14.8, "10.10.10.10"
- SENTINEL-LINUX01 — Ubuntu 24.04, Wazuh Agent 4.14.8, "10.10.10.40", Agent ID "002"

## What's implemented:

Component| Status
Real-time FIM on "/home" (Wazuh Syscheck)| Implemented and confirmed working for the tested file modification
Built-in Wazuh Rule 550 (Level 7, "Integrity checksum changed")| Observed during file-modification testing; confirms the built-in FIM detection path
Custom Rule 100002 (target: Level 8)| Controlled modification validation confirmed — a Level 8 alert was observed for the test file
Review of additional home-directory FIM events| Completed for the reviewed dataset; background desktop/cache activity observed, with process attribution limitations
Rule tuning and broader validation| Pending

The controlled modification of "/home/sentinel-admin/sentinel-fim-validation.txt" generated a custom Rule 100002 alert at Level 8. The corresponding event identified the modified file and included file-integrity metadata. This confirms that the custom rule fired for the tested modification.

The reviewed dashboard data contained 19 matching events during the investigation window. The controlled validation event was identified among them. Other events included changes to desktop configuration, application state, and cache files. These were documented as observed background activity; the available evidence does not conclusively attribute every event to a specific process.

## Primary validation evidence:

- "Custom Rule 100002 validation screenshot" (../evidence/v0.3/v0.3-custom-rule-100002.png)
- "Custom Rule 100002 dashboard JSON" (../evidence/v0.3/v0.3-custom-rule-100002-dashboard-json.png)
- "Filtered FIM events" (../evidence/v0.3/v0.3-case001-fim-filtered-events.png)
- "Rule 550 event details" (../evidence/v0.3/v0.3-case001-rule-550-event-details.png)
- "Endpoint file metadata" (../evidence/v0.3/v0.3-case001-endpoint-file-metadata.png)
- "CASE-001 investigation report" (../investigations/CASE-001.md)

The confirmed result is limited to the tested file modification. It does not establish that all file-integrity scenarios are covered or that the endpoint is free from malicious activity.

---

## 6. Known Limitations and Lessons

- A syntax check is not validation. Rule 100002 passed the configuration syntax check, and subsequent controlled testing confirmed that it generated a Level 8 alert for the tested file modification. These are separate validation steps.
- Rule 550 and Rule 100002 are different detections. Rule 550 was observed during testing, and the custom Rule 100002 alert was independently confirmed. Evidence for one rule should not be substituted for evidence of the other.
- A FIM alert does not prove malicious activity. A file-integrity alert confirms a monitored file changed; it does not, by itself, establish who changed it, why it changed, or whether the activity was malicious. Investigation and additional telemetry may be required.
- Broad path matching can introduce noise. The custom rule matches file-integrity events associated with paths containing "/home/". Additional desktop configuration, application-state, and cache events were observed. Any proposed narrowing or exclusions must be tested to ensure useful detection is preserved.
- Validation coverage is limited. The controlled modification scenario was confirmed, but separate creation and deletion tests remain outstanding.
- Broader false-positive and false-negative testing remains incomplete. The reviewed events revealed potential noise, but no comprehensive false-positive/false-negative test matrix has been completed. Individual events have not all been attributed to a process.

---

## 7. Future Plans

The following work is planned and not yet completed:

- Validate file creation and deletion behavior separately.
- Evaluate narrower path matching and potential noise-reduction changes for Rule 100002.
- Test any proposed rule changes against controlled modifications and relevant benign activity before claiming improvement.
- Expand telemetry sources to authentication activity and process/command execution.
- Add MITRE ATT&CK technique mappings where observed behavior supports them.
- Implement and validate additional detection rules beyond File Integrity Monitoring.
- Conduct broader false-positive / false-negative testing.
- Perform purple-team validation, including detection rate, detection time, and before/after comparisons where measurable.
- Implement attack mutation testing to assess detection resilience when behavior changes.

These remain future work and are not claimed as current capabilities. The confirmed Rule 100002 modification test is the starting point for improving detection quality and expanding validation coverage.
