## SENTINEL v0.3 — SOC Investigation Evidence

##  Controlled file-modification test & FIM detection validation for CASE-001

This directory contains screenshots supporting the SENTINEL v0.3 SOC investigation checkpoint, including endpoint file metadata, Wazuh File Integrity Monitoring (FIM) events, and validation of custom detection Rule `100002`.

The evidence documents a controlled file-modification test and the investigation of related FIM events. It supports the specific validation results described below; it does not establish complete FIM coverage or a comprehensive endpoint forensic assessment.

---

## Evidence Overview

#	Evidence	File	Purpose	
1	CASE-001 endpoint file metadata	[`v0.3-case001-endpoint-file-metadata.png`](v0.3-case001-endpoint-file-metadata.png)	Records metadata for the controlled test file	
2	CASE-001 filtered FIM events	[`v0.3-case001-fim-filtered-events.png`](v0.3-case001-fim-filtered-events.png)	Shows FIM events reviewed during investigation	
3	CASE-001 Rule 550 event details	[`v0.3-case001-rule-550-event-details.png`](v0.3-case001-rule-550-event-details.png)	Provides details of a built-in Wazuh integrity-change alert	
4	Custom Rule 100002 alert	[`v0.3-custom-rule-100002.png`](v0.3-custom-rule-100002.png)	Shows the custom Level 8 detection alert	
5	Custom Rule 100002 dashboard JSON	[`v0.3-custom-rule-100002-dashboard-json.png`](v0.3-custom-rule-100002-dashboard-json.png)	Provides the underlying event fields used for validation	

---

## 1 CASE-001 — Endpoint File Metadata

![CASE-001 endpoint file metadata](v0.3-case001-endpoint-file-metadata.png)

File: `v0.3-case001-endpoint-file-metadata.png`

- Purpose: Records the endpoint file metadata associated with the controlled investigation scenario.
- Evidence value: Helps document the test artifact and provides supporting context for the file-integrity investigation.

---

## 2 CASE-001 — Filtered FIM Events

![CASE-001 filtered FIM events](v0.3-case001-fim-filtered-events.png)

File: `v0.3-case001-fim-filtered-events.png`

- Purpose: Shows the filtered Wazuh FIM events reviewed during CASE-001.
- Evidence value: Demonstrates the event-review stage of the investigation and helps identify the relevant integrity-change activity for further analysis.

---

## 3 CASE-001 — Built-in Rule 550 Event Details

![CASE-001 Rule 550 event details](v0.3-case001-rule-550-event-details.png)

File: `v0.3-case001-rule-550-event-details.png`

- Purpose: Captures details of a built-in Wazuh Rule 550 integrity-checksum-change alert.
- Evidence value: Provides context for the underlying FIM event and shows the built-in detection path observed during testing.
  
>  Note: Rule 550 and custom Rule 100002 are distinct rules; evidence of one does not independently validate the other.

---

## 4 Custom Rule 100002 — Alert Validation

![Custom Rule 100002 alert](v0.3-custom-rule-100002.png)

File: `v0.3-custom-rule-100002.png`

- Purpose: Shows the custom SENTINEL Rule `100002` alert generated during a controlled file-modification test.

## Observed result:

Field	Value	
Rule ID	`100002`	
Alert level	`8`	
Description	SENTINEL: File integrity modification detected in monitored home directory.	
Test objective	Confirm that the controlled file modification triggers the custom detection.	

- Evidence value: Supports successful validation of the custom modification-detection path. It does not establish detection coverage for file creation, deletion, or every possible modification scenario.

---

## 5 Custom Rule 100002 — Dashboard Event JSON

![Custom Rule 100002 dashboard JSON](v0.3-custom-rule-100002-dashboard-json.png)

File: `v0.3-custom-rule-100002-dashboard-json.png`

- Purpose: Captures the event details used to inspect and verify the custom detection alert.
- Evidence value: Supports verification of the rule ID, alert level, file path, event details, and associated integrity information visible in the captured event.

>  The controlled validation event was recorded at `2026-10-11T20:25:14.746+0530`. The screenshot and event fields should be interpreted together with the investigation report rather than as proof of broader detection coverage.

---

## Investigation Outcome

The controlled file-modification test successfully generated the expected custom Rule `100002` Level 8 alert. The associated evidence was reviewed and documented in CASE-001 ([`../../investigations/CASE-001.md`](../../investigations/CASE-001.md)).

The reviewed event set also contained background configuration and cache changes. No malicious indicators were identified in the reviewed dataset, but the available evidence does not establish process-level attribution for every event or prove that the endpoint was free of threats.

---

## Limitations and Remaining Work

- Validate file-creation and deletion behavior separately.
- Review and tune noisy FIM events where appropriate.
- Develop systematic false-positive and false-negative test cases.
- Expand telemetry and investigation coverage as the project progresses.

---

## Scope Statement

These screenshots document a specific, controlled detection-validation and investigation checkpoint. They are not evidence that every detection scenario has been tested or that the complete SENTINEL SOC workflow is finished.

---

## Related Documentation

Document	Path	
 Investigation findings and disposition	[`CASE-001`](../../investigations/CASE-001.md)	
 Detection methodology and remaining validation work	[`Detection Engineering`](../../docs/05-detection-engineering.md)	

---

SENTINEL v0.3 — SOC Investigation Evidence
