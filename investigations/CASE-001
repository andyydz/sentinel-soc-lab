CASE-001 — File Integrity Monitoring Investigation

Project: SENTINEL SOC Lab
Milestone: v0.3
Date: 11 October 2026
Status: Closed — Reviewed Activity Assessed as Non-Malicious

Summary

Reviewed 19 Wazuh file-integrity events from "sentinel-linux01" (agent ID "002"). One controlled modification test successfully triggered custom rule "100002" at Level 8. The other 18 events involved GNOME Tracker and desktop configuration or application-state files.

No malicious indicators were identified in the supplied event dataset. This conclusion is limited to the reviewed evidence.

Scope

- Wazuh Manager: "10.10.10.10"
- Linux endpoint: "10.10.10.40"
- Wazuh version: "4.14.8"
- Review window: 11 October 2026, approximately 20:24–20:30 IST

Key Evidence

Observation| Result
Controlled test file| "/home/sentinel-admin/sentinel-fim-validation.txt"
Custom rule| "100002", Level 8
Test timestamp| "20:25:14.746 IST"
Integrity changes| Size 26 → 52 bytes; hashes changed
Other events| 18 background file-integrity events
Assessment| No malicious indicators identified in the reviewed dataset

Findings

1. Custom rule "100002" detected the controlled file modification.
2. Other alerts were consistent with file indexing and desktop configuration activity.
3. Broad home-directory matching generated unnecessary background alerts.
4. Creation and deletion coverage requires separate validation.

Disposition

Closed as non-malicious observed activity and successful controlled detection validation. No root cause for every background event was independently established, and this review does not prove the endpoint was free of other threats.

Evidence

- "../evidence/v0.3/v0.3-custom-rule-100002.png"
- Add the actual dashboard JSON screenshot filename here.

Follow-up

- Test and validate narrower path matching.
- Validate file creation and deletion rules if required.
- Update the detection-engineering documentation after testing.
