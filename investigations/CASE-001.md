## CASE-001 — Controlled FIM Modification Validation

| Field | Value |
|---|---|
| Case ID | CASE-001 |
| Project | SENTINEL — SOC Lab |
| Version | v0.3 — SOC Investigation |
| Status | Controlled modification-validation objective: Closed. Overall CASE-001 investigation: Open (see Assessment and Disposition) |
| Severity | Low |
| Detection Source | Wazuh File Integrity Monitoring (FIM) |
| Custom Rule | `100002` |
| Endpoint | SENTINEL-LINUX01 (`10.10.10.40`) |
| Wazuh Agent ID | `002` |

---

## Executive Summary

This investigation evaluated a controlled file modification on the SENTINEL-LINUX01 endpoint and verified that the custom Wazuh rule `100002` generated a Level 8 alert.

The investigation also identified additional file-integrity events involving desktop configuration and application-cache files under the user's home directory. These events were reviewed as background activity within the available dataset. Their timing alone does not establish which process caused each change.

> The controlled test demonstrates that the custom rule can detect the tested file modification. It does not establish complete coverage of every file-integrity event or prove that the endpoint is free from threats.

**Addendum (reported 16 October 2026, pending raw-alert review):** a controlled creation was reported to trigger `100002`; a later deletion was reported to alert under built-in Rule `553` but not `100002` (open coverage question); and how `100002` fired on creation while anchored to Rule `550` is unresolved. See Findings 4–6.

---

## Objective

- Validate the custom Wazuh FIM rule `100002`.
- Confirm that a controlled file modification produces the expected alert.
- Review the relevant alert fields and supporting endpoint evidence.
- Document noise, limitations, and follow-up detection-engineering work.

---

## Environment and Scope

| Component | Details |
|---|---|
| Wazuh Manager | SENTINEL-WAZUH — `10.10.10.10` |
| Wazuh Agent | SENTINEL-LINUX01 — `10.10.10.40` |
| Agent ID | `002` |
| Wazuh Version | `4.14.8` |
| Detection Rule | `100002` |
| Monitored test file | `/home/sentinel-admin/sentinel-fim-validation.txt` |
| Additional test file (reported, 16 Oct 2026) | `/home/sentinel-admin/sentinel-audit-test.txt` |

Scope: Review of the controlled file-modification test, the resulting Wazuh alert, and related FIM events available during the investigation. The 16 October 2026 creation/deletion tests and operational events are recorded as reported addenda (see below) and do not change the original modification-validation scope.

---

## Evidence Collected

| Evidence | Purpose |
|---|---|
| [`v0.3-custom-rule-100002.png`](../evidence/v0.3/v0.3-custom-rule-100002.png) | Custom rule validation evidence |
| [`v0.3-custom-rule-100002-dashboard-json.png`](../evidence/v0.3/v0.3-custom-rule-100002-dashboard-json.png) | Alert JSON and event-field evidence |
| [`v0.3-case001-fim-filtered-events.png`](../evidence/v0.3/v0.3-case001-fim-filtered-events.png) | Filtered FIM event view |
| [`v0.3-case001-rule-550-event-details.png`](../evidence/v0.3/v0.3-case001-rule-550-event-details.png) | Built-in Rule 550 event details |
| [`v0.3-case001-endpoint-file-metadata.png`](../evidence/v0.3/v0.3-case001-endpoint-file-metadata.png) | Endpoint file metadata evidence |

All evidence images are stored in [`evidence/v0.3/`](../evidence/v0.3/).

### Primary custom-rule evidence

Custom rule 100002 terminal evidence:

![Custom rule 100002 terminal evidence](../evidence/v0.3/v0.3-custom-rule-100002.png)

Custom rule 100002 dashboard JSON evidence:

![Custom rule 100002 dashboard JSON evidence](../evidence/v0.3/v0.3-custom-rule-100002-dashboard-json.png)

### Additional investigation evidence

- Filtered FIM events:

  ![Filtered FIM events](../evidence/v0.3/v0.3-case001-fim-filtered-events.png)

- Rule 550 event details:

  ![Rule 550 event details](../evidence/v0.3/v0.3-case001-rule-550-event-details.png)

- Endpoint file metadata:

  ![Endpoint file metadata](../evidence/v0.3/v0.3-case001-endpoint-file-metadata.png)

### Evidence still to capture or review (16 October 2026 reported results)

The artifacts below are **not** claimed to exist in the repository. They are listed as evidence to capture or review; no file paths are assigned.

- Raw alert JSON for the creation event (Rules `554` and `100002`).
- Raw alert JSON for the deletion event (Rule `553`; confirmation that `100002` did not fire).
- The active `100002` rule definition from `local_rules.xml` (read-only review), with the relevant built-in definitions for Rules `550`, `553`, and `554` in the installed ruleset.
- Manager startup-failure logs and service status output, if retained.
- Post-restart service, listener, and agent-status output, if retained.

---

## Investigation Timeline

> 11 October 2026 — approximately 20:24–20:30 IST

- Reviewed FIM events generated on the monitored endpoint.
- Examined the built-in Rule 550 event details.
- Performed a controlled modification of `/home/sentinel-admin/sentinel-fim-validation.txt`.
- Confirmed a custom Rule `100002` alert for the modified file.
- Reviewed the corresponding dashboard JSON and file-integrity metadata.
- Observed additional events involving desktop configuration, application state, and cache files.

Confirmed controlled-test alert timestamp: `2026-10-11T20:25:14.746+0530`

> The broader review window is approximate; it should not be interpreted as the exact timestamp of every event.

### 16 October 2026 — reported addendum (pending evidence review)

Timestamps below are as reported and have not been checked against raw alerts.

| Reported time | Event |
|---|---|
| `2026-10-16T11:40:06.105+0530` | Controlled creation of `/home/sentinel-admin/sentinel-audit-test.txt`; Rules `554` and `100002` reported. |
| `2026-10-16T12:31:32.819+0530` | Controlled deletion of the same file; Rule `553` (Level 7) reported; `100002` did not fire. |

No timestamps are recorded for the Manager startup incident or the restart-persistence test.

---

## Technical Findings

### Finding 1 — Custom Rule 100002 triggered

Result: Confirmed for the tested modification.

The controlled modification generated a Wazuh alert with:

| Field | Value |
|---|---|
| Rule ID | `100002` |
| Severity level | `8` |
| Event type | `modified` |
| File | `/home/sentinel-admin/sentinel-fim-validation.txt` |
| Decoder | `syscheck_integrity_changed` |
| Event location | `syscheck` |

The event included file-integrity metadata, including size and hash information.

> This confirms that the tested modification matched the custom rule.

### Finding 2 — Additional home-directory FIM events

Result: Additional activity observed; attribution remains limited.

The dashboard contained 19 matching events in the reviewed period. The controlled validation event was identified among them. Other events included paths associated with GNOME Tracker cache, desktop configuration, and application state.

> These paths are consistent with ordinary desktop activity, but the available evidence does not independently establish the process responsible for every event. They should be treated as observed background activity rather than conclusively attributed events.

### Finding 3 — Detection scope requires further tuning

Result: Follow-up work required.

As reported, the rule is configured with a `file` field condition of `/home/` (parent `<if_sid>550</if_sid>`, Level 8, group `sentinel_fim`). This is the configured definition as supplied; it has not been re-checked against the active `local_rules.xml` for this review. The exact matching behavior of the field condition (for example, whether it acts as an unanchored substring or regular-expression match, or how it treats case) has **not** been verified. Describing the rule as matching "paths containing `/home/`" is therefore a working assumption, not a confirmed behavior.

If the condition is broad, it may generate noise from routine user-session activity; this has not been quantified.

Further testing is needed to determine whether narrower path matching or carefully validated exclusions would improve signal quality without suppressing relevant activity.

> The original controlled test validated modification detection only. Creation and deletion results subsequently reported on 16 October 2026 are recorded in Findings 4 and 5; they are reported single-test observations and do not establish complete coverage of these event types.

### Finding 4 — Controlled file creation (reported, 16 October 2026)

Result: **Reported** — pending review of the raw alert and supporting evidence.

- Test file: `/home/sentinel-admin/sentinel-audit-test.txt`
- Custom Rule `100002` (Level 8) was reported to fire.
- Built-in Rule `554` ("File added to the system") was also reported.
- The event was reported as real-time FIM activity.

This is a positive result for this specific controlled creation test only. It is not generalized to other paths, file types, or complete creation coverage. See Finding 6 regarding the unresolved rule-anchor discrepancy.

### Finding 5 — Controlled file deletion: custom-rule coverage question (reported, 16 October 2026)

Result: **Reported** — open custom-rule coverage question, pending review of the raw alert and active rule definitions.

- The same test file was subsequently deleted.
- Built-in Rule `553` ("File deleted", Level 7) was reported to generate an alert, so the deletion was still alerted on by a built-in rule.
- Custom Rule `100002` was reported **not** to fire for the deletion.
- Rule `100002` is anchored to built-in Rule `550`; deletion coverage is therefore an open engineering issue requiring investigation and appropriate testing. The rule has not been modified.

The deletion was a controlled test action and is not indicative of malicious activity. If the alert carries MITRE ATT&CK mappings (not confirmed here), they are telemetry metadata from the built-in rule and are not evidence of malicious intent.

### Finding 6 — Unresolved discrepancy: creation event vs. rule anchor

Result: **Unresolved.**

The reported definition of `100002` (see Finding 3; not yet checked against the active configuration) is anchored to built-in Rule `550` via `<if_sid>550</if_sid>`, yet the creation event was reported to trigger `100002`. This has not been explained. No cause is asserted here, the rule has not been changed, and the discrepancy is not considered resolved. The raw creation alert and the active rule definition must be reviewed (see Follow-Up Actions); until then, neither the reported anchor nor the reported creation match should be relied on for coverage claims.

---

## Operational Events — Manager Incident and Restart Test (reported, 16 October 2026)

> This section records operational recovery. It is separate from, and is not evidence for, detection-rule validation. All items are reported observations; raw logs have not been supplied or independently reviewed.

### Wazuh Manager startup timeout

- Reported: Wazuh Manager startup timed out (approximately 45 seconds, per earlier session notes; to be confirmed).
- Reported: `/var/ossec/var/start-script-lock` was inspected and found to be a directory containing a PID file for PID `1440`, which at the time was associated with the Wazuh Indexer Java process (per earlier session notes; to be confirmed).
- Reported: no active Wazuh Manager processes were found during the relevant check.
- Reported: the lock directory was removed after that check.
- Reported: `systemctl daemon-reload` was run, and the Manager subsequently started successfully.
- Reported: later checks showed the Manager and Dashboard active, the API and agent-communication ports listening, and Agent `002` reconnecting to Active.

**Root cause: not established.** The original reason for the startup timeout and how the lock directory came to be present are unconfirmed. Calling the lock "stale" reflects the observation that no Manager process was found, not a confirmed history, and successful startup after its removal does not prove that the lock caused the failure. Possibilities such as PID reuse have not been established and are not asserted. Recovery was a response to observed conditions; the lock directory should not be deleted automatically or repeatedly without fresh diagnostic evidence.

### Restart-persistence test

A separate graceful shutdown-and-restart test of the Manager and Linux endpoint VMs was reported successful when the Manager VM (`SENTINEL-WAZUH`) was started before `SENTINEL-LINUX01`. Reported post-boot checks: `wazuh-manager` active, `wazuh-dashboard` active, listeners on `0.0.0.0:55000` (API), `0.0.0.0:1514` (agent communication) and `0.0.0.0:1515` (enrollment), and Agent `002` initially shown as Disconnected before returning to Active.

This is one reported successful cycle for the checks performed. It does not demonstrate resilience under other failures, boot orders, or future restarts.

---

## Assessment and Disposition

Disposition: Closed for the controlled modification-validation objective. The overall CASE-001 investigation remains open.

This closure applies only to the controlled file-modification validation. The custom rule successfully detected the tested file modification at Level 8. Additional home-directory events were observed and reviewed within the available evidence.

No malicious indicators were identified in the reviewed dataset. This finding is limited to the events and artifacts examined; it is not a comprehensive forensic assessment and does not establish that the endpoint was free from compromise.

Broader investigation and detection-engineering work remains open. Timeline reconstruction, attribution of background events, broader event review, verification of the Rule `100002`/Rule `550` discrepancy, deletion-rule engineering, systematic false-positive/false-negative testing, and detection tuning remain outstanding.

---

## Limitations

- The original validation covered a controlled file modification; the creation and deletion results are single reported tests and do not represent every FIM event type or path.
- Custom Rule `100002` did not fire for the reported deletion; custom-rule deletion coverage is an open coverage question.
- It is unresolved how `100002` reportedly fired on creation while anchored to Rule `550`.
- Additional background events were not fully attributed to individual processes.
- The `/home/` field condition may be broad enough to produce noisy alerts, and its exact matching behavior is unverified.
- No completed false-positive or false-negative test matrix is claimed; no detection rates are established; complete FIM coverage is not claimed.
- Detection tuning and its effectiveness remain unverified until tested.
- The Manager startup-timeout root cause is unconfirmed, and the restart test is a single reported cycle.
- The 16 October 2026 raw alerts and operational logs have not been supplied for review; all results from that date are reported observations.

---

## Follow-Up Actions

- Review the raw creation and deletion alerts and attach them as evidence (new files to be captured; none are claimed to exist yet).
- Review the active Rule `100002` definition and the built-in Rule `550`/`553`/`554` definitions (read-only) to resolve the creation-event discrepancy and to confirm how the `file` field condition actually matches.
- Design and, after review and approval, test a safe change for deletion coverage; do not alter the rule before that review.
- Define repeatable creation, modification, and deletion regression tests with explicit pass/fail criteria.
- Evaluate narrower path matching for the custom rule.
- Test any proposed exclusions against both benign and controlled test events.
- Document false-positive and false-negative test results.
- Confirm that tuning preserves detection of the intended file modifications.
- Capture diagnostics (service status, logs, process list) before any change if the Manager startup failure recurs.
- Update the detection-engineering, incident-response, and testing/metrics documentation and changelog after validation.

---

## Conclusion

CASE-001 documents a successful controlled validation of SENTINEL's custom Wazuh FIM rule `100002` for the specified modification scenario, and records the additional noise and coverage questions discovered during investigation. Reported 16 October 2026 observations add a creation test that triggered the rule, a deletion that built-in Rule `553` alerted on but `100002` did not, and an unresolved discrepancy about the rule's anchor.

The next phase should focus on verifying the 16 October 2026 evidence, resolving the rule discrepancy, improving signal quality, and validating creation and deletion scenarios while preserving the existing working detection.

---

CASE-001 — evidence first, uncertainty preserved.
