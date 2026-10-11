CASE-001 — File Integrity Monitoring Investigation

Case ID: CASE-001
Project: SENTINEL — SOC Lab
Version: v0.3 — Detection Engineering
Status: Closed — Controlled Validation Completed
Severity: Low
Detection Source: Wazuh File Integrity Monitoring (FIM)
Custom Rule: 100002
Endpoint: "SENTINEL-LINUX01" ("10.10.10.40")
Wazuh Agent ID: "002"

---

1. Executive Summary

This investigation evaluated a controlled file modification on the "SENTINEL-LINUX01" endpoint and verified that the custom Wazuh rule 100002 generated a Level 8 alert.

The investigation also identified additional file-integrity events involving desktop configuration and application-cache files under the user's home directory. These events were reviewed as background activity within the available dataset. Their timing alone does not establish which process caused each change.

The controlled test demonstrates that the custom rule can detect the tested file modification. It does not establish complete coverage of every file-integrity event or prove that the endpoint is free from threats.

2. Objective

- Validate the custom Wazuh FIM rule "100002".
- Confirm that a controlled file modification produces the expected alert.
- Review the relevant alert fields and supporting endpoint evidence.
- Document noise, limitations, and follow-up detection-engineering work.

3. Environment and Scope

Component| Details
Wazuh Manager| "SENTINEL-WAZUH" — "10.10.10.10"
Wazuh Agent| "SENTINEL-LINUX01" — "10.10.10.40"
Agent ID| "002"
Wazuh Version| "4.14.8"
Detection Rule| "100002"
Monitored test file| "/home/sentinel-admin/sentinel-fim-validation.txt"

Scope: Review of the controlled file-modification test, the resulting Wazuh alert, and related FIM events available during the investigation.

4. Evidence Collected

Evidence| Purpose
"v0.3-custom-rule-100002.png"| Custom rule validation evidence
"v0.3-custom-rule-100002-dashboard-json.png"| Alert JSON and event-field evidence
"v0.3-case001-fim-filtered-events.png"| Filtered FIM event view
"v0.3-case001-rule-550-event-details.png"| Built-in Rule 550 event details
"v0.3-case001-endpoint-file-metadata.png"| Endpoint file metadata evidence

All evidence images are stored in ""evidence/v0.3/"" (../evidence/v0.3/).

Primary custom-rule evidence

"Custom rule 100002 terminal evidence" (../evidence/v0.3/v0.3-custom-rule-100002.png)

"Custom rule 100002 dashboard JSON evidence" (../evidence/v0.3/v0.3-custom-rule-100002-dashboard-json.png)

Additional investigation evidence

- "Filtered FIM events" (../evidence/v0.3/v0.3-case001-fim-filtered-events.png)
- "Rule 550 event details" (../evidence/v0.3/v0.3-case001-rule-550-event-details.png)
- "Endpoint file metadata" (../evidence/v0.3/v0.3-case001-endpoint-file-metadata.png)

5. Investigation Timeline

11 October 2026 — approximately 20:24–20:30 IST

- Reviewed FIM events generated on the monitored endpoint.
- Examined the built-in Rule 550 event details.
- Performed a controlled modification of "/home/sentinel-admin/sentinel-fim-validation.txt".
- Confirmed a custom Rule 100002 alert for the modified file.
- Reviewed the corresponding dashboard JSON and file-integrity metadata.
- Observed additional events involving desktop configuration, application state, and cache files.

Confirmed controlled-test alert timestamp: "2026-10-11T20:25:14.746+0530"

The broader review window is approximate; it should not be interpreted as the exact timestamp of every event.

6. Technical Findings

Finding 1 — Custom Rule 100002 triggered

Result: Confirmed for the tested modification.

The controlled modification generated a Wazuh alert with:

- Rule ID: "100002"
- Severity level: "8"
- Event type: "modified"
- File: "/home/sentinel-admin/sentinel-fim-validation.txt"
- Decoder: "syscheck_integrity_changed"
- Event location: "syscheck"

The event included file-integrity metadata, including size and hash information.

This confirms that the tested modification matched the custom rule.

Finding 2 — Additional home-directory FIM events

Result: Additional activity observed; attribution remains limited.

The dashboard contained 19 matching events in the reviewed period. The controlled validation event was identified among them. Other events included paths associated with GNOME Tracker cache, desktop configuration, and application state.

These paths are consistent with ordinary desktop activity, but the available evidence does not independently establish the process responsible for every event. They should be treated as observed background activity rather than conclusively attributed events.

Finding 3 — Detection scope requires further tuning

Result: Follow-up work required.

The rule matches file-integrity events associated with paths containing "/home/". This broad scope can generate noise from routine user-session activity.

Further testing is needed to determine whether narrower path matching or carefully validated exclusions would improve signal quality without suppressing relevant activity.

The current test validates modification detection only. File creation and deletion behavior have not been independently validated against this custom rule.

7. Assessment and Disposition

Disposition: Closed for the controlled validation objective.

The custom rule successfully detected the tested file modification at Level 8. Additional home-directory events were observed and reviewed within the available evidence.

No malicious indicators were identified in the reviewed dataset. This finding is limited to the events and artifacts examined; it is not a comprehensive forensic assessment and does not establish that the endpoint was free from compromise.

8. Limitations

- Validation covered a controlled file modification, not every FIM event type.
- Creation and deletion detection require separate testing.
- Additional background events were not fully attributed to individual processes.
- The broad home-directory matching scope can produce noisy alerts.
- No completed false-positive or false-negative test matrix is claimed.
- Detection tuning and its effectiveness remain unverified until tested.

9. Follow-Up Actions

- [ ] Test file creation and deletion behavior separately.
- [ ] Evaluate narrower path matching for the custom rule.
- [ ] Test any proposed exclusions against both benign and controlled test events.
- [ ] Document false-positive and false-negative test results.
- [ ] Confirm that tuning preserves detection of the intended file modifications.
- [ ] Update the detection-engineering documentation and changelog after validation.

10. Conclusion

CASE-001 documents a successful controlled validation of SENTINEL's custom Wazuh FIM rule "100002". The test demonstrates modification detection for the specified home-directory file and records the additional noise and coverage questions discovered during investigation.

The next phase should focus on improving signal quality and validating creation and deletion scenarios while preserving the existing working detection.
