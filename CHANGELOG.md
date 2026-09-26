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
- No detection, attack, investigation, response, mutation, or metrics evidence exists yet — this is expected at this stage and is planned for v0.2 and later.

### Engineering Principles
- Adopted the development philosophy: **BUILD → UNDERSTAND → TEST → BREAK → FIX → MEASURE → DOCUMENT → EXPLAIN**.
- A security control is not considered successful simply because it exists; detections must eventually be tested, evidenced, measured, improved when necessary, and retested.
- Adopted a failure-handling process: **STOP → CAPTURE → DOCUMENT → CONTINUE**. Significant failures and architecture changes are recorded rather than hidden.
- Lesson recorded from the Windows VM issue: SENTINEL should continue developing even when an optional environment component is unreliable, rather than allowing it to block progress.

### Roadmap
Planned phases (not yet completed):

- **v0.2 — Detection Engineering**: Linux telemetry validation, first controlled attack scenarios, initial detection rules, detection testing, false-positive analysis, missed detection analysis, MITRE ATT&CK mapping where technically verified, detection evidence.
- **v0.3 — SOC Investigation**: Alert investigation, timeline reconstruction, IOC collection, threat hunting, incident case development, first complete incident case, formal investigation report.
- **v0.4 — Incident Response**: Controlled response actions, containment workflow, eradication/recovery workflow, response validation, human-in-the-loop response, response performance measurement.
- **v0.5 — Purple-Team Validation**: Detection coverage measurement, detection rate, detection time, response time, false-positive/false-negative analysis, regression testing, before/after comparison, purple-team feedback loop.
- **v0.6 — Attack DNA & Mutation**: Attack-chain representation, Attack DNA, controlled attack variation, attack mutation, detection resilience testing, detection failure analysis, detection improvement, retesting against modified attacker behavior.

### Future Expansion
- Windows and Active Directory monitored endpoints (deferred from the core v0.1–v0.6 path).
- A custom SENTINEL console, planned for a later stage after the core security engine is working. It is intended to sit on top of Wazuh rather than replace it, with potential future functionality including incident visualization, detection timelines, MITRE ATT&CK mapping, IOC visualization, detection metrics, Attack DNA visualization, mutation results, detection coverage, and response/case reporting. Not currently implemented.

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
