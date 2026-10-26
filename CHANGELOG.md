## ChangeLog

All notable changes to SENTINEL are documented here.

This file records meaningful project-level changes, architecture decisions, validated milestones, and important lessons learned during development.

## This file is not:

- a Git commit history
- a technical tutorial
- a replacement for detailed project documentation (architecture, threat model, detection engineering, incident response, testing matrices, and lessons/failure logs are maintained separately)

SENTINEL is a virtual cybersecurity SOC lab built around the lifecycle:

SIMULATE → DETECT → INVESTIGATE → RESPOND → MEASURE → IMPROVE → RETEST

The project's guiding question is: does your detection still work when the attacker changes tactics?

---

[Unreleased]

## Architecture

- Replaced the original Windows-first architecture with a Linux-first initial monitored endpoint.

- A Windows VM (SENTINEL-WIN01) was attempted as the initial monitored endpoint but encountered repeated deployment/boot issues that made it unsuitable as a dependency for the core v0.1 build. This is recorded as an infrastructure/deployment issue, not an attributed technical root cause.

- Decision made to proceed with Linux telemetry as the foundation for the core SENTINEL v0.1–v0.6 path, and to treat Windows and Active Directory as a future expansion capability rather than a blocking requirement.

- Current initial lab topology established:
  
  INTERNET
   |
  NAT
   |
SENTINEL-WAZUH (10.10.10.10) — SOC / Wazuh
   |
SENTINEL-LAB (10.10.10.0/24)
   |
   +----------------------+
   |                      |
SENTINEL-KALI          SENTINEL-LINUX01
10.10.10.20             10.10.10.40
Attacker                Monitored Endpoint

## Infrastructure

- Deployed SENTINEL-WAZUH (Ubuntu 24.04) as the SOC host, lab IP 10.10.10.10.
- Deployed SENTINEL-KALI as the controlled attacker/adversary-emulation system, lab IP 10.10.10.20.
- Deployed SENTINEL-LINUX01 (Ubuntu 24.04) as the initial monitored endpoint, lab IP 10.10.10.40.
- Established the isolated SENTINEL-LAB network (10.10.10.0/24) connecting all three systems.
- Verified connectivity between Wazuh and Linux01.
- Verified connectivity between Kali and Wazuh.
- Upgraded VirtualBox from 7.2.8 to 7.2.20 during infrastructure troubleshooting.

## Wazuh

- Completed Wazuh all-in-one deployment (version 4.14.8) on SENTINEL-WAZUH.
- Wazuh Dashboard is operational.
- Installed and enabled the Wazuh agent on SENTINEL-LINUX01; agent is actively running.
- Confirmed SENTINEL-LINUX01 appears as an active endpoint in the Wazuh Dashboard.
- Disabled the Wazuh package repository after installation to reduce the risk of accidental package upgrades.

## Documentation

- Established repository documentation covering: project overview, requirements, architecture, threat model, detection engineering, incident response, and testing/matrices.
- Established a lessons/failures record for capturing project issues as they occur.
- Established repository structure for future work: "detections/", "investigations/", "metrics/", "scenarios/", "evidence/", "failure-log/".
- Documented CASE-001, an investigation into controlled FIM validation and related home-directory file-integrity events.
- Updated the investigation directory guide to index CASE-001 and reflect the current investigation status.
- Updated detection-engineering documentation to distinguish confirmed modification detection from outstanding testing and tuning work.

## Evidence

- Captured initial v0.1 infrastructure verification evidence, including the Wazuh Dashboard showing the active SENTINEL-LINUX01 endpoint and confirmation of a running Wazuh agent.
- Captured v0.2 detection-engineering evidence for the built-in Rule 550 and custom Rule 100002 validation.
- Captured v0.3 investigation evidence for the 11 October 2026 modification test and CASE-001, including custom-rule alert details, dashboard JSON, filtered FIM events, Rule 550 event details, and endpoint file metadata.
- Evidence is organized under "evidence/v0.2/" and "evidence/v0.3/" as applicable.
- The original source alert log for the 11 October 2026 modification test was not recovered during the 26 October 2026 review. That result is supported by the existing screenshots only.
- CASE-001 documents the controlled modification test and the limitations of the reviewed dataset.
- The 16 October 2026 creation and deletion source records were reviewed from "/var/ossec/logs/alerts/2026/Oct/ossec-alerts-16.json". Reviewing a source record is separate from storing it in the repository: this Wazuh runtime log is not claimed to be committed to GitHub, and no raw-alert files are claimed as repository artifacts. The 16 October screenshots remain referenced in "evidence/v0.3/readme.md". See "Reviewed Records and Reported Observations" below for what the records show.
- The 26 October 2026 modification results are recorded below. No repository evidence path is linked for them.
- Operational artifacts from the reported Wazuh Manager startup observation have not been independently reviewed or confirmed saved in the repository.

## Reconciliation Update (26 October 2026)

- The 16 October creation and deletion records were reviewed at source level. The creation timestamp is "2026-10-16T11:40:06.007+0530"; the earlier ".007" versus ".087" discrepancy no longer applies.
- Two further controlled modifications on 26 October 2026 produced Rule "100002" Level 8 alerts (details below).
- CASE-001 evidence reconciliation for the reviewed scope is closed. The overall CASE-001 investigation and broader detection-engineering work remain open.
- Earlier entries below are preserved as development history; where they conflict with this update, this update and the "Reviewed Records and Reported Observations" section govern.

## Reviewed Records and Reported Observations

Detection — reviewed source records, 16 October 2026 (test file "/home/sentinel-admin/sentinel-audit-test.txt"):

- Source: "/var/ossec/logs/alerts/2026/Oct/ossec-alerts-16.json". This file is not claimed to be committed to the repository.
- Creation: the reviewed source record shows built-in Rule "554" ("File added to the system") at "2026-10-16T11:40:06.007+0530". Custom Rule "100002" is absent from that record.
- Deletion: the reviewed source record shows built-in Rule "553" ("File deleted") at "2026-10-16T12:31:32.819+0530". Custom Rule "100002" is absent from that record.
- These are reviewed records of individual controlled actions. They are not successful custom-rule validations, not repeatable regression tests, and not counted toward any metric.
- An earlier claim that Rules "554" and "100002" fired together during creation is unsupported by the reviewed records and remains unexplained.
- The reason Rule "100002" was absent from the reviewed creation and deletion records is unresolved. It is a coverage question, not a confirmed detection miss or an established root cause.

Detection — controlled modification, 26 October 2026 (test file "/home/sentinel-admin/sentinel-v02-mod-test.txt"):

- Two controlled modifications each generated a custom Rule "100002" Level 8 alert:
  - "2026-10-26T21:38:27.910+0530" — file size 0 → 23 bytes.
  - "2026-10-26T21:38:48.473+0530" — file size 23 → 61 bytes.
- These results support the modification scenario only. They do not validate creation or deletion, establish coverage of other paths or event types, or constitute a regression suite or a detection rate.

Rule 100002 dependency:

- A read-only inspection of the on-disk "/var/ossec/etc/rules/local_rules.xml" showed Rule "100002" at Level 8, group "sentinel_fim", with parent "<if_sid>550</if_sid>" and a "file" field condition of "/home/". This establishes what was in the on-disk file at inspection time, not which rule version the manager had loaded during the historical tests.
- The reviewed creation and deletion records show Rules "554" and "553", respectively, and do not show Rule "550" as the matching parent rule. The parent condition is recorded as a dependency still to be examined; it is not established as the cause of Rule "100002" being absent.
- The current loaded rule configuration, the rule version loaded during the historical tests, and the exact matching semantics of "/home/" have not been reverified. The rule has not been changed.

Evidence discrepancies:

- Creation timestamp: resolved. The reviewed source record shows "2026-10-16T11:40:06.007+0530". The ".087" value previously recorded in the evidence README is superseded.
- Creation screenshot filename: remains unresolved. It contains "creation-rule-553" even though the content shows Rule "554", and the evidence README reportedly references "creation-rule-664". This is a naming/documentation discrepancy and is separate from the reviewed alert finding.

Operations (reported; logs and outputs not independently reviewed or confirmed saved in the repository):

- A Wazuh Manager startup reportedly timed out at approximately 45 seconds.
- A lock directory was removed after a check reportedly found no active Manager processes; the Manager subsequently started. The root cause of the original startup failure is unconfirmed, and the lock is not claimed to have caused it.
- One graceful Manager/endpoint VM restart cycle was reported successful, with Agent "002" reconnecting to Active. This is a single observation and is not evidence of general resilience.

Status: no Wazuh rule changes, tuning, or metric measurements are claimed. No definitive root cause, complete FIM coverage, measured detection rate, or comprehensive false-positive/false-negative result has been established. CASE-001 evidence reconciliation for the reviewed scope is closed; the overall CASE-001 investigation remains open.

## Engineering Principles

- Adopted the development philosophy: BUILD → UNDERSTAND → TEST → BREAK → FIX → MEASURE → DOCUMENT → EXPLAIN.
- A security control is not considered successful simply because it exists; detections must eventually be tested, evidenced, measured, improved when necessary, and retested.
- Adopted a failure-handling process: STOP → CAPTURE → DOCUMENT → CONTINUE. Significant failures and architecture changes are recorded rather than hidden.
- Lesson recorded from the Windows VM issue: SENTINEL should continue developing even when an optional environment component is unreliable, rather than allowing it to block progress.
- Confirmed that configuration syntax validation, telemetry observation, custom-rule validation, and broader detection coverage are distinct engineering claims and must be documented separately.
- Identified broad home-directory FIM matching as an area for further noise evaluation; proposed tuning must be tested before its effectiveness is claimed.

## Roadmap

## Project phase status:

- v0.1 — Foundation: Complete. See "[0.1.0]" below.
- v0.2 — Detection Engineering: Core controlled file-modification detection validated (11 and 26 October 2026 tests). The reviewed 16 October creation/deletion source records show built-in Rules 554/553 with custom Rule 100002 absent; they are not custom-rule validations. Broader detection scenarios, additional telemetry sources, and systematic false-positive/missed-detection analysis remain ongoing. See "[0.2.0]" below.
- v0.3 — SOC Investigation (In progress): CASE-001 documented for controlled FIM validation and review of related events. The reviewed-scope evidence reconciliation is closed; the overall CASE-001 investigation and broader detection-engineering work remain open. Broader investigation capabilities, additional cases, threat-hunting validation, and investigation workflow improvements remain future work within this phase.
- v0.4 — Incident Response (Planned): Controlled response actions, containment workflow, eradication/recovery workflow, response validation, human-in-the-loop response, and response performance measurement.
- v0.5 — Purple-Team Validation (Planned): Detection coverage measurement, detection rate, detection time, response time, false-positive/false-negative analysis, regression testing, before/after comparison, and purple-team feedback loop.
- v0.6 — Attack DNA & Mutation (Planned): Attack-chain representation, Attack DNA, controlled attack variation, attack mutation, detection resilience testing, detection failure analysis, detection improvement, and retesting against modified attacker behavior.

## Future Expansion

- Windows and Active Directory monitored endpoints (deferred from the core v0.1–v0.6 path).
- A custom SENTINEL console, planned for a later stage after the core security engine is working. It is intended to sit on top of Wazuh rather than replace it, with potential future functionality including incident visualization, detection timelines, MITRE ATT&CK mapping, IOC visualization, detection metrics, Attack DNA visualization, mutation results, detection coverage, and response/case reporting. Not currently implemented.

---

[0.3.0] - Unreleased

## v0.3 — SOC Investigation phase.

Purpose: investigate relevant security telemetry, validate detection results, document evidence, and produce a traceable investigation record. This phase builds on the FIM detection implemented in v0.2. It does not represent a complete threat-hunting, incident-response, or purple-team capability.

## Investigation

- Created CASE-001 to document a controlled file-integrity modification test on SENTINEL-LINUX01 and the review of related FIM events.
- Recorded the controlled test file: "/home/sentinel-admin/sentinel-fim-validation.txt".
- Documented the custom Rule 100002 alert and its supporting file-integrity metadata.
- Reviewed additional home-directory events involving desktop configuration, application state, and cache files.
- Distinguished the controlled test result from other observed events whose individual process attribution was not established.
- Recorded the investigation scope, findings, limitations, disposition, and follow-up actions in "investigations/CASE-001.md".
- Status: CASE-001's controlled modification-validation objective is closed, and evidence reconciliation for the reviewed scope is closed. The overall CASE-001 investigation and broader detection-engineering work remain open.

## Detection Validation

Controlled modification, 11 October 2026 (supported by existing screenshots):

- Custom Wazuh Rule "100002" generated a Level 8 alert for the controlled modification of "/home/sentinel-admin/sentinel-fim-validation.txt" (alert timestamp "2026-10-11T20:25:14.746+0530"). Built-in Rule "550" was also observed.
- The event identified the modified file and included file-integrity metadata.
- The original source alert log was not recovered during the 26 October 2026 review.
- Recorded the controlled modification test without treating it as proof that all FIM event types or paths are covered. This supports the tested modification scenario only.

Controlled modification, 26 October 2026:

- Two controlled modifications of "/home/sentinel-admin/sentinel-v02-mod-test.txt" each generated a custom Rule "100002" Level 8 alert:
  - "2026-10-26T21:38:27.910+0530" — file size 0 → 23 bytes.
  - "2026-10-26T21:38:48.473+0530" — file size 23 → 61 bytes.
- These results support the modification scenario only. They are not a regression suite and do not establish creation/deletion coverage, other paths, or a detection rate.

Reviewed source records (16 October 2026), from "/var/ossec/logs/alerts/2026/Oct/ossec-alerts-16.json" (not claimed to be committed to the repository):

- Creation of "/home/sentinel-admin/sentinel-audit-test.txt": built-in Rule "554" shown at "2026-10-16T11:40:06.007+0530"; custom Rule "100002" absent.
- Deletion of the same file: built-in Rule "553" shown at "2026-10-16T12:31:32.819+0530"; custom Rule "100002" absent.
- These are not custom-rule validations for creation or deletion. Earlier wording that creation/deletion had not been tested, and the earlier claim that Rule "100002" fired on creation, are superseded; see "Reviewed Records and Reported Observations" above for the full findings and discrepancies.

Open questions:

- Why Rule "100002" was absent from the reviewed creation and deletion records, and whether it is intended to cover those events, is unresolved. It is an open coverage question, not a confirmed detection miss. No cause is asserted, and the "<if_sid>550</if_sid>" parent condition is not claimed as the cause. The on-disk rule definition does not establish the version the manager had loaded during the historical tests (details under "[Unreleased]").

Other outstanding work:

- Inspection of the current loaded rule configuration, and verification of the "/home/" matching behavior; historical runtime configuration remains unconfirmed.
- Repeatable regression testing for creation, modification, and deletion.
- Systematic false-positive/false-negative testing.
- Broad home-directory matching identified as an area for further noise evaluation, and detection-rule tuning with regression validation. No rule change or tuning is claimed.

## Operational Incident (reported; root cause unconfirmed)

- A Wazuh Manager startup reportedly timed out at approximately 45 seconds.
- A lock directory was removed after a check reportedly found no active Manager processes; the Manager subsequently started. The root cause of the original startup failure is unconfirmed; the lock is not claimed to be the cause.
- One graceful Manager/endpoint VM restart cycle was reported successful, with Agent "002" reconnecting to Active. This is a single observation, not proof of general resilience.
- Operational logs and outputs have not been independently reviewed or confirmed saved in the repository.

## Evidence

- Captured "evidence/v0.3/v0.3-custom-rule-100002.png".
- Captured "evidence/v0.3/v0.3-custom-rule-100002-dashboard-json.png".
- Captured "evidence/v0.3/v0.3-case001-fim-filtered-events.png".
- Captured "evidence/v0.3/v0.3-case001-rule-550-event-details.png".
- Captured "evidence/v0.3/v0.3-case001-endpoint-file-metadata.png".
- Linked the evidence artifacts above from the CASE-001 investigation report.
- The 16 October creation and deletion records were reviewed from the Wazuh alert log path given above. The screenshots remain referenced in "evidence/v0.3/readme.md". The raw alert log is not claimed to be a committed repository artifact. The creation timestamp is resolved ("2026-10-16T11:40:06.007+0530"); the creation screenshot-filename discrepancy remains unresolved (see "[Unreleased]").
- The original source alert log for the 11 October 2026 test was not recovered during the 26 October 2026 review.
- No repository evidence path is linked for the 26 October 2026 modification results.
- Operational logs have not been confirmed as located, reviewed, or saved in the repository. No such files are claimed.

## Lessons Learned

- A successful controlled detection test confirms only the behavior exercised by that test.
- A FIM alert establishes that a monitored file changed; it does not independently establish malicious intent or identify the responsible process.
- Broad path matching can capture routine desktop activity alongside the intended validation event.
- Investigation conclusions must distinguish observed facts, interpretations, and unresolved questions.
- Rule tuning must be followed by testing to ensure that noise is reduced without suppressing the intended detection.
- A built-in rule alert (for example Rule 554 or 553) is not a custom Rule 100002 alert, and does not establish whether the custom rule should cover, or does cover, the same event.
- Screenshots and source records provide different levels of evidence. Claims that require source-level detail should be checked against the source record where available; the 16 October creation timestamp was resolved through that review.
- Reviewing a source record is not the same as committing it as a repository artifact; the two are documented separately.

## Not yet included in v0.3

- Comprehensive threat hunting across multiple telemetry sources
- Custom-rule validation of file creation and deletion for Rule 100002 (the reviewed records show built-in Rules 554/553 with Rule 100002 absent)
- Resolution of the creation screenshot-filename discrepancy
- Resolution of why Rule "100002" was absent from the reviewed creation and deletion records, including the "<if_sid>550</if_sid>" question
- Inspection of the current loaded rule configuration and verification of the "/home/" matching behavior; historical runtime configuration remains unconfirmed
- Repeatable regression tests for creation, modification, and deletion
- Systematic false-positive and false-negative testing
- Tested noise-reduction tuning and regression validation
- Multiple investigation cases covering different security scenarios
- Full incident-response workflow, response engineering, and response performance measurement
- Detection coverage metrics and purple-team validation
- MITRE ATT&CK technique mapping
- Attack DNA / mutation testing

---

[0.2.0] - Unreleased

## v0.2 — Detection Engineering phase.

Purpose: move beyond infrastructure foundation into building, testing, and validating an actual security detection on top of the Wazuh/Linux01 telemetry pipeline established in v0.1. This release documents the first validated detection; it does not represent complete detection coverage, investigation workflows, or response workflows.

## Detection Engineering

- Configured Wazuh Syscheck (File Integrity Monitoring) on SENTINEL-LINUX01.
- Scoped FIM monitoring to the "/home" directory.
- Authored a custom Wazuh detection rule, Rule ID "100002", to flag file-integrity modification events within the monitored scope.
- Detection flow: SENTINEL-LINUX01 → Wazuh Agent → Syscheck/FIM → telemetry event → custom Rule "100002" → Level 8 alert.

## Validation / Testing

- Performed a controlled file modification test against the monitored "/home" directory.
- Confirmed Wazuh generated a "syscheck_integrity_changed" event in response to the test modification.
- Confirmed the custom Rule "100002" matched the tested event and produced a Level 8 alert.
- Confirmed the alert identified the modified file and included file-integrity metadata.
- Validated the modification-detection path end-to-end for the controlled scenario: telemetry generation → custom-rule match → Level 8 alert.
- The modification scenario is the confirmed custom-rule validation. This validation does not establish coverage of file creation, file deletion, every monitored path, or other detection scenarios. The reviewed 16 October creation/deletion records do not validate custom Rule "100002" for creation or deletion; see "[Unreleased]" and "[0.3.0]".

## Evidence

- Captured evidence of the configured FIM rule, the controlled test, the resulting "syscheck_integrity_changed" event, and the Level 8 alert generated by Rule "100002".
- Supporting v0.3 investigation evidence is also available under "evidence/v0.3/".
- This is the project's first confirmed custom detection validation, building on the infrastructure evidence captured in v0.1.

## Lessons Learned

- A file modification alert is not automatically evidence of malicious activity. It must be correlated with available user, process, file path, timestamp, and surrounding event context before being treated as suspicious.
- Rule 550 and custom Rule 100002 are distinct detections; validation evidence for one should not be substituted for the other.
- Broad path matching can introduce noise from normal user-session activity, making careful investigation and evidence-backed tuning important.

Not yet included in v0.2 (planned for v0.3+)

- Additional detection scenarios beyond File Integrity Monitoring
- Expanded telemetry sources (authentication, process execution, command execution)
- Systematic false-positive and missed-detection analysis beyond the controlled modification test
- MITRE ATT&CK technique mapping
- Broader alert investigation and case workflows
- Detection metrics, coverage measurement, and purple-team validation
- Attack DNA / mutation testing

---

[0.1.0] - Unreleased

## v0.1 — Foundation phase.

Purpose: establish the infrastructure required for later security testing (detection engineering, investigation, response, and purple-team validation). This release does not represent a complete detection, investigation, or response system.

## Completed in this phase:

- Virtual SOC infrastructure (SENTINEL-WAZUH) deployed and operational.
- Isolated lab network (SENTINEL-LAB) established.
- Kali attacker environment (SENTINEL-KALI) deployed.
- Linux monitored endpoint (SENTINEL-LINUX01) deployed with an enrolled, running Wazuh agent visible in the dashboard.
- Initial telemetry pipeline established (agent-to-manager connectivity verified).
- Documentation structure and evidence structure established.
- Failure-tracking structure established.
- Architecture decision made to proceed Linux-first, deferring Windows/AD to future expansion.

Not yet included in v0.1 (planned for v0.2+):

- Detection rules and detection testing
- Controlled attack scenarios
- Investigation workflows
- Response workflows
- Metrics, coverage measurement, and purple-team validation
- Attack DNA / mutation testing
- SENTINEL console
