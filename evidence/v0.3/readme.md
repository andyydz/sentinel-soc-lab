# SENTINEL v0.3 — SOC Investigation Evidence

## Controlled FIM detection validation for CASE-001: modification, creation, and deletion

This directory contains screenshots supporting the SENTINEL v0.3 SOC investigation checkpoint: endpoint file metadata, Wazuh File Integrity Monitoring (FIM) events, validation of custom detection Rule `100002`, and follow-up file-creation and deletion tests that generated built-in Wazuh alerts.

The evidence supports the specific results described below. It does not establish complete FIM coverage or a comprehensive endpoint forensic assessment.

---

## Evidence Overview

| # | Evidence | File | What it supports |
|---|----------|------|------------------|
| 1 | CASE-001 endpoint file metadata | [`v0.3-case001-endpoint-file-metadata.png`](v0.3-case001-endpoint-file-metadata.png) | Metadata for the controlled test file |
| 2 | CASE-001 filtered FIM events | [`v0.3-case001-fim-filtered-events.png`](v0.3-case001-fim-filtered-events.png) | FIM events reviewed during the investigation |
| 3 | CASE-001 Rule 550 event details | [`v0.3-case001-rule-550-event-details.png`](v0.3-case001-rule-550-event-details.png) | Built-in integrity-checksum-change alert |
| 4 | Custom Rule 100002 alert | [`v0.3-custom-rule-100002.png`](v0.3-custom-rule-100002.png) | Custom Level 8 alert from the Oct 11 modification test |
| 5 | Custom Rule 100002 dashboard JSON | [`v0.3-custom-rule-100002-dashboard-json.png`](v0.3-custom-rule-100002-dashboard-json.png) | Event fields used to verify the alert |
| 6 | Oct 16 creation, Rule 554 | [`v0.3-oct16-creation-rule-664.png`](v0.3-oct16-creation-rule-664.png) | Built-in "File added to the system" alert |
| 7 | Oct 16 creation, file path | [`v0.3-oct16-creation-file-path.png`](v0.3-oct16-creation-file-path.png) | Test-file path on the creation event |
| 8 | Oct 16 deletion, Rule 553 | [`v0.3-oct16-detection-rule-553.png`](v0.3-oct16-detection-rule-553.png) | Built-in "File deleted" alert |
| 9 | Oct 16 deletion, file path | [`v0.3-oct16-detection-file-path.png`](v0.3-oct16-detection-file-path.png) | Test-file path on the deletion event |
| 10 | Rule 100002 definition | [`v0.3-rule-100002-definition.png`](v0.3-rule-100002-definition.png) | Configuration of the custom rule |
| 11 | Investigation report on GitHub | [`v0.3-fim-rule-100002-investigation-github.png`](v0.3-fim-rule-100002-investigation-github.png) | How the report appears on GitHub; not independent proof of detection |

---

## 1. CASE-001: Endpoint File Metadata

![CASE-001 endpoint file metadata](v0.3-case001-endpoint-file-metadata.png)

- **Purpose:** Records metadata for the controlled test file in the investigation scenario.
- **Evidence value:** Documents the test artifact and provides context for the file-integrity investigation.

---

## 2. CASE-001: Filtered FIM Events

![CASE-001 filtered FIM events](v0.3-case001-fim-filtered-events.png)

- **Purpose:** Shows the filtered Wazuh FIM events reviewed during CASE-001.
- **Evidence value:** Demonstrates the event-review stage and helps identify the relevant integrity-change activity.

---

## 3. CASE-001: Built-in Rule 550 Event Details

![CASE-001 Rule 550 event details](v0.3-case001-rule-550-event-details.png)

- **Purpose:** Captures a built-in Wazuh Rule `550` (integrity checksum changed) alert.
- **Evidence value:** Provides context for the underlying FIM event and shows the built-in detection path observed during testing.

> **Note:** Rule 550 and custom Rule 100002 are distinct rules. Evidence of one does not independently validate the other.

---

## 4. Custom Rule 100002: October 11 Modification Test

![Custom Rule 100002 alert](v0.3-custom-rule-100002.png)

| Field | Value |
|-------|-------|
| Rule ID | `100002` |
| Alert level | `8` |
| Description | SENTINEL: File integrity modification detected in monitored home directory. |
| Test objective | Confirm that the controlled file modification triggers the custom detection. |

- **Evidence value:** Supports successful validation of the custom modification-detection path for this controlled test.

### Dashboard event JSON

![Custom Rule 100002 dashboard JSON](v0.3-custom-rule-100002-dashboard-json.png)

- **Purpose:** Captures the event details used to inspect and verify the alert.
- **Evidence value:** Supports verification of the rule ID, alert level, file path, event details, and integrity information visible in the captured event.
- **Timestamp:** The controlled validation event was recorded at `2026-10-11T20:25:14.746+0530`.

> Interpret the screenshots together with the investigation report, not as proof of broader detection coverage.

---

## 5. October 16 File-Creation Test: Built-in Rule 554

![Oct 16 creation, Rule 554](v0.3-oct16-creation-rule-553.png)

![Oct 16 creation, file path](v0.3-oct16-creation-file-path.png)

- **Rule:** Built-in Wazuh Rule `554`, "File added to the system."
- **Test file:** `/home/sentinel-admin/sentinel-audit-test.txt`
- **Reviewed event timestamp:** `2026-10-16T11:40:06.087+0530`
- **Observed result:** The reviewed creation record shows built-in Rule 554. It did not show custom Rule `100002` firing for this event.

---

## 6. October 16 File-Deletion Test: Built-in Rule 553

![Oct 16 deletion, Rule 553](v0.3-oct16-detection-rule-553.png)

![Oct 16 deletion, file path](v0.3-oct16-detection-file-path.png)

- **Rule:** Built-in Wazuh Rule `553`, "File deleted."
- **Test file:** `/home/sentinel-admin/sentinel-audit-test.txt` (same path as the creation test)
- **Reviewed event timestamp:** `2026-10-16T12:31:32.819+0530`
- **Observed result:** The reviewed deletion record shows built-in Rule 553. It did not show custom Rule `100002` firing for this event.

> These are observed results for the reviewed records only. They do not show that no creation or deletion event could ever trigger the custom rule.

---

## 7. Custom Rule 100002: Rule Definition

![Rule 100002 definition](v0.3-rule-100002-definition.png)

- **Purpose:** Shows the configuration of the custom rule.
- **Dependency:** The rule uses `<if_sid>550</if_sid>`, so it is evaluated only for events already matched by built-in Rule 550. Its scope is therefore tied to qualifying Rule 550 modification events.
- **Path condition:** The rule matches on `/home/`, limiting it to files in the monitored home directory.
- **Relation to Oct 16 results:** Because of the Rule 550 dependency, the absence of Rule 100002 in the reviewed creation (554) and deletion (553) records is consistent with the rule's design, but this README does not claim it as a general guarantee.

---

## 8. Investigation Report

![Investigation report on GitHub](v0.3-fim-rule-100002-investigation-github.png)

- The detailed findings are in the [FIM Rule 100002 investigation report](../../investigations/fim-rule-100002-investigation.md).
- This screenshot documents how the report appears on GitHub. It is not independent proof of the underlying detection; the supporting evidence is in sections 1–7.

---

## Investigation Outcome

- The controlled October 11 modification test generated the expected custom Rule `100002` Level 8 alert.
- The October 16 creation and deletion tests generated built-in Rules `554` and `553`. In the reviewed records, custom Rule `100002` did not fire for either event.
- The CASE-001 reviewed event set also contained background configuration and cache changes. No malicious indicators were identified in that dataset, but the evidence does not establish process-level attribution for every event or prove that the endpoint was free of threats.
- Findings are documented in [CASE-001](../../investigations/CASE-001.md) and the [FIM Rule 100002 investigation report](../../investigations/fim-rule-100002-investigation.md).

---

## Limitations and Remaining Work

- Creation and deletion were each reviewed for a single test file path; other directories, multiple files, and repeated events remain untested.
- Decide whether file creation and deletion in `/home/` warrant custom detections, since Rule 100002 depends on Rule 550 modification events.
- Review and tune noisy FIM events where appropriate.
- Develop systematic false-positive and false-negative test cases.
- Expand telemetry and investigation coverage as the project progresses.

---

## Scope Statement

These screenshots document specific, controlled detection-validation and investigation checkpoints. They are not evidence that every detection scenario has been tested, that FIM coverage is complete, or that the SENTINEL SOC workflow is finished.

---

## Related Documentation

| Document | Path |
|----------|------|
| Investigation findings and disposition (CASE-001) | [`CASE-001`](../../investigations/CASE-001.md) |
| FIM Rule 100002 investigation report | [`fim-rule-100002-investigation`](../../investigations/fim-rule-100002-investigation.md) |
| Detection methodology and remaining validation work | [`Detection Engineering`](../../docs/05-detection-engineering.md) |

---

SENTINEL v0.3 — SOC Investigation Evidence
