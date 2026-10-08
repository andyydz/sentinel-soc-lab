# ChangeLog

All notable changes to SENTINEL are documented here.

This file records meaningful project-level changes, architecture decisions, validated milestones, and important lessons learned during development.

This file is **not**:
- a Git commit history
- a technical tutorial
- a replacement for detailed project documentation (architecture, threat model, detection engineering, incident response, testing matrices, and lessons/failure logs are maintained separately)

SENTINEL is a virtual cybersecurity SOC lab built around the lifecycle:

**SIMULATE → DETECT → INVESTIGATE → RESPOND → MEASURE → IMPROVE → RETEST**

The project's guiding question is: *does your detection still work when the attacker changes tactics?*

---

## [Unreleased]

### Architecture
- Replaced the original Windows-first architecture with a Linux-first initial monitored endpoint.
- A Windows VM (SENTINEL-WIN01) was attempted as the initial monitored endpoint but encountered repeated deployment/boot issues that made it unsuitable as a dependency for the core v0.1 build. This is recorded as an infrastructure/deployment issue, not an attributed technical root cause.
- Decision made to proceed with Linux telemetry as the foundation for the core SENTINEL v0.1–v0.6 path, and to treat Windows and Active Directory as a future expansion capability rather than a blocking requirement.
- Current initial lab topology established:

  ```
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
  ```

### Infrastructure
- Deployed SENTINEL-WAZUH (Ubuntu 24.04) as the SOC host, lab IP 10.10.10.10.
- Deployed SENTINEL-KALI as the controlled attacker/adversary-emulation system, lab IP 10.10.10.20.
- Deployed SENTINEL-LINUX01 (Ubuntu 24.04) as the initial monitored endpoint, lab IP 10.10.10.40.
- Established the isolated SENTINEL-LAB network (10.10.10.0/24) connecting all three systems.
- Verified connectivity between Wazuh and Linux01.
- Verified connectivity between Kali and Wazuh.
- Upgraded VirtualBox from 7.2.8 to 7.2.20 during infrastructure troubleshooting.

### Wazuh
- Completed Wazuh all-in-one deployment (version 4.14.8) on SENTINEL-WAZUH.
- Wazuh Dashboard is operational.
- Installed and enabled the Wazuh agent on SENTINEL-LINUX01; agent is actively running.
- Confirmed SENTINEL-LINUX01 appears as an active endpoint in the Wazuh Dashboard.
- Disabled the Wazuh package repository after installation to reduce the risk of accidental package upgrades.

### Documentation
- Established repository documentation covering: project overview, requirements, architecture, threat model, detection engineering, incident response, and testing/matrices.
- Established a lessons/failures record for capturing project issues as they occur.
- Established repository structure for future work: `detections/`, `investigations/`, `metrics/`, `scenarios/`, `evidence/`, `failure-log/`.

### Evidence
- Captured initial v0.1 infrastructure verification evidence, including the Wazuh Dashboard showing the active SENTINEL-LINUX01 endpoint and confirmation of a running Wazuh agent.
- No detection, attack, investigation, response, mutation, or metrics evidence existed at the time of the v0.1 Foundation phase; detection evidence is now being captured under v0.2 (see below).

### Engineering Principles
- Adopted the development philosophy: **BUILD → UNDERSTAND → TEST → BREAK → FIX → MEASURE → DOCUMENT → EXPLAIN**.
- A security control is not considered successful simply because it exists; detections must eventually be tested, evidenced, measured, improved when necessary, and retested.
- Adopted a failure-handling process: **STOP → CAPTURE → DOCUMENT → CONTINUE**. Significant failures and architecture changes are recorded rather than hidden.
- Lesson recorded from the Windows VM issue: SENTINEL should continue developing even when an optional environment component is unreliable, rather than allowing it to block progress.

### Roadmap
Project phase status:

- **v0.1 — Foundation**: Complete. See `[0.1.0]` below.
- **v0.2 — Detection Engineering**: In progress. Linux telemetry validation and a first custom detection (File Integrity Monitoring) have been built and validated; further detection scenarios, additional telemetry sources, and false-positive/missed-detection analysis remain ongoing. See `[0.2.0]` below.
- **v0.3 — SOC Investigation** *(Next, planned)*: Alert investigation, timeline reconstruction, IOC collection, threat hunting, incident case development, first complete incident case, formal investigation report.
- **v0.4 — Incident Response** *(Planned)*: Controlled response actions, containment workflow, eradication/recovery workflow, response validation, human-in-the-loop response, response performance measurement.
- **v0.5 — Purple-Team Validation** *(Planned)*: Detection coverage measurement, detection rate, detection time, response time, false-positive/false-negative analysis, regression testing, before/after comparison, purple-team feedback loop.
- **v0.6 — Attack DNA & Mutation** *(Planned)*: Attack-chain representation, Attack DNA, controlled attack variation, attack mutation, detection resilience testing, detection failure analysis, detection improvement, retesting against modified attacker behavior.

### Future Expansion
- Windows and Active Directory monitored endpoints (deferred from the core v0.1–v0.6 path).
- A custom SENTINEL console, planned for a later stage after the core security engine is working. It is intended to sit on top of Wazuh rather than replace it, with potential future functionality including incident visualization, detection timelines, MITRE ATT&CK mapping, IOC visualization, detection metrics, Attack DNA visualization, mutation results, detection coverage, and response/case reporting. Not currently implemented.

---

## [0.2.0] - Unreleased

**v0.2 — Detection Engineering phase.**

Purpose: move beyond infrastructure foundation into building, testing, and validating an actual security detection on top of the Wazuh/Linux01 telemetry pipeline established in v0.1. This release documents the first validated detection; it does **not** represent complete detection coverage, investigation workflows, or response workflows.

### Detection Engineering
- Configured Wazuh Syscheck (File Integrity Monitoring) on SENTINEL-LINUX01.
- Scoped FIM monitoring to the `/home` directory.
- Authored a custom Wazuh detection rule, Rule ID `100002`, to flag file-integrity modification events within the monitored scope.
- Detection flow: SENTINEL-LINUX01 → Wazuh Agent → Syscheck/FIM → telemetry event → custom Rule `100002` → Level 8 alert.

### Validation / Testing
- Performed a controlled file modification test against the monitored `/home` directory.
- Confirmed Wazuh generated a `syscheck_integrity_changed` event in response to the test modification.
- Confirmed the custom Rule `100002` correctly matched the event and produced a Level 8 alert.
- Confirmed the alert text correctly identifies the event as a SENTINEL file-integrity modification detection.
- The detection was validated end-to-end through this controlled test: telemetry generation → rule match → alert.

### Evidence
- Captured evidence of the configured FIM rule, the controlled test execution, the resulting `syscheck_integrity_changed` event, and the Level 8 alert generated by Rule `100002`.
- This is the first detection-specific evidence in the project, building on the infrastructure evidence captured in v0.1.

### Lessons Learned
- A file modification alert is not automatically evidence of malicious activity. It must be correlated with the user, process, file path, timestamp, and surrounding events/context before being treated as suspicious — this distinction will inform how FIM-based alerts are triaged in later investigation work (v0.3).

### Not yet included in v0.2 (planned for v0.3+)
- Additional detection scenarios beyond File Integrity Monitoring
- Expanded telemetry sources (authentication, process execution, command execution)
- False-positive and missed-detection analysis beyond the single validated test above
- MITRE ATT&CK technique mapping
- Alert investigation and case workflows
- Detection metrics, coverage measurement, and purple-team validation
- Attack DNA / mutation testing

---

## [0.1.0] - Unreleased

**v0.1 — Foundation phase.**

Purpose: establish the infrastructure required for later security testing (detection engineering, investigation, response, and purple-team validation). This release does **not** represent a complete detection, investigation, or response system.

Completed in this phase:
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
- 
