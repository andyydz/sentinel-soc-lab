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
- Captured v0.3 investigation evidence, including custom-rule alert details, dashboard JSON, filtered FIM events, Rule 550 event details, and endpoint file metadata.
- Evidence is organized under "evidence/v0.2/" and "evidence/v0.3/" as applicable.
- CASE-001 documents the confirmed controlled modification test and the limitations of the reviewed dataset.
- No evidence has been confirmed as saved in the repository for the 16 October 2026 reported observations below.

## Reported Observations (pending review)

Detection (reported 16 October 2026; raw alerts and active rule definitions not yet independently reviewed):

- File creation test on "/home/sentinel-admin/sentinel-audit-test.txt": built-in Rule "554" and custom Rule "100002" were reported to fire.
- File deletion test on the same file: built-in Rule "553" was reported to fire; custom Rule "100002" reportedly did not. This is recorded as an open custom-rule coverage question. No cause is asserted.
- The reported creation alert for Rule "100002" is inconsistent with the reported parent condition "<if_sid>550</if_sid>". This discrepancy is unresolved.
- These are individual reported results. They are not verified coverage, not repeatable regression tests, and not counted toward any metric.

Operations (reported; logs and outputs not independently reviewed or confirmed saved in the repository):

- A Wazuh Manager startup reportedly timed out at approximately 45 seconds.
- A lock directory was removed after a check reportedly found no active Manager processes; the Manager subsequently started. The root cause of the original startup failure is unconfirmed, and the lock is not claimed to have caused it.
- One graceful Manager/endpoint VM restart cycle was reported successful, with Agent "002" reconnecting to Active. This is a single observation and is not evidence of general resilience.

Status: no Wazuh rule changes, tuning, or metric measurements are claimed.

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
- v0.2 — Detection Engineering: Core controlled file-modification detection validated. Creation/deletion tests have been reportedly performed but remain unverified pending raw-alert and rule-definition review. Broader detection scenarios, additional telemetry sources, and systematic false-positive/missed-detection analysis remain ongoing. See "[0.2.0]" below.
- v0.3 — SOC Investigation (In progress): CASE-001 documented for controlled FIM validation and review of related events. The controlled modification-validation objective is closed; the overall CASE-001 investigation remains open. Broader investigation capabilities, additional cases, threat-hunting validation, and investigation workflow improvements remain future work within this phase.
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
- Distinguished the confirmed controlled test result from other observed events whose individual process attribution was not established.
- Recorded the investigation scope, findings, limitations, disposition, and follow-up actions in "investigations/CASE-001.md".
- Status: the controlled modification-validation objective is closed; the overall CASE-001 investigation remains open.

## Detection Validation

Confirmed (11 October 2026):

- Custom Wazuh Rule "100002" generated a Level 8 alert for the controlled modification of "/home/sentinel-admin/sentinel-fim-validation.txt" (alert timestamp "2026-10-11T20:25:14.746+0530").
- The event identified the modified file and included file-integrity metadata.
- Recorded the successful controlled modification test without treating it as proof that all FIM event types or paths are covered. This confirms the tested modification scenario only.

Reported, pending raw-alert review (16 October 2026):

- Creation of "/home/sentinel-admin/sentinel-audit-test.txt": built-in Rule "554" and custom Rule "100002" were reported to fire.
- Deletion of the same file: built-in Rule "553" was reported to fire; custom Rule "100002" reportedly did not.
- These creation/deletion tests were reportedly performed; their results remain unverified until the raw alerts and active rule definitions are independently reviewed. Earlier wording that creation/deletion had not been tested is superseded by this status.

Open questions:

- Custom-rule coverage of file deletion is an open question. No cause is asserted.
- The reported creation alert from Rule "100002" is inconsistent with the reported parent condition "<if_sid>550</if_sid>". This discrepancy is unresolved, and neither the reported creation result nor the reported rule definition is treated as established.

Other:

- Identified broad home-directory matching as an area for further noise evaluation.
- Systematic false-positive/false-negative testing and detection-rule tuning remain outstanding. No rule change or tuning is claimed.

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
- Linked the evidence artifacts from the CASE-001 investigation report.
- The 16 October 2026 raw creation/deletion alerts, active rule definitions, and operational logs have not been confirmed as saved in the repository. No evidence files are claimed for them.

## Lessons Learned

- A successful controlled detection test confirms only the behavior exercised by that test.
- A FIM alert establishes that a monitored file changed; it does not independently establish malicious intent or identify the responsible process.
- Broad path matching can capture routine desktop activity alongside the intended validation event.
- Investigation conclusions must distinguish observed facts, interpretations, and unresolved questions.
- Rule tuning must be followed by testing to ensure that noise is reduced without suppressing the intended detection.
- A built-in rule firing (for example Rule 554 or 553) does not establish whether custom Rule 100002 should cover, or does cover, the same event.
- A reported result is not a verified result until the raw alerts and active rule definitions have been reviewed.

## Not yet included in v0.3

- Comprehensive threat hunting across multiple telemetry sources
- Verified file creation and deletion validation for custom Rule 100002 (tests reportedly performed; pending raw-alert and rule-definition review)
- Resolution of the Rule "100002" / "<if_sid>550</if_sid>" discrepancy and the deletion coverage question
- Repeatable regression tests for creation and deletion
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
- This validation does not establish coverage of file creation, file deletion, every monitored path, or other detection scenarios. Later reported creation/deletion results are recorded under "[0.3.0]" and remain pending review.

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
