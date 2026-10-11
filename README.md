## SENTINEL — SOC Lab

## Does your detection still work when the attacker changes tactics?

SENTINEL is a controlled virtual Security Operations Center (SOC) lab built with VirtualBox, Wazuh, Kali Linux, and an Ubuntu endpoint. It is designed to practice and document a defensive engineering workflow—not simply install security tools.

## Objective

SIMULATE → DETECT → INVESTIGATE → RESPOND → MEASURE → IMPROVE → RETEST

Each stage should be supported by evidence before its results are trusted. A detection is not considered fully validated just because a rule exists: it must be tested, its outcome recorded, and its limitations understood.

## Architecture

                INTERNET
                   |
                  NAT
                   |
          +----------------+
          | SENTINEL-WAZUH |
          | 10.10.10.10    |
          +----------------+
                   |
            SENTINEL-LAB
            10.10.10.0/24
                   |
        +----------+----------+
        |                     |
+---------------+     +------------------+
| SENTINEL-KALI |     | SENTINEL-LINUX01 |
| 10.10.10.20   |     | 10.10.10.40      |
+---------------+     +------------------+

- SENTINEL-WAZUH — Ubuntu 24.04, Wazuh 4.14.8; monitoring and security analysis platform.
- SENTINEL-KALI — Kali Linux; controlled adversary-emulation VM.
- SENTINEL-LINUX01 — Ubuntu 24.04, Wazuh Agent 4.14.8; monitored endpoint with File Integrity Monitoring (FIM) configured for "/home".
- SENTINEL-LAB — internal lab network, "10.10.10.0/24"; NAT is used for legitimate package and update traffic.

An earlier Windows endpoint ("SENTINEL-WIN01") was dropped after repeated boot and deployment failures. Windows and Active Directory integration remain future work rather than dependencies for the current milestones.

## Current status

## v0.1 — Foundation: Complete

- Wazuh deployed and operational.
- Kali and the Ubuntu Linux endpoint deployed.
- Lab networking established.
- Wazuh agent enrolled and communicating with the manager.

## v0.2 — Telemetry and detection engineering: In progress

- Real-time FIM configured for "/home".
- Built-in Wazuh Rule 550 observed during file-integrity testing.
- Custom Wazuh Rule "100002" created and configuration syntax validated.
- A controlled file-modification test successfully generated the expected Level 8 Rule 100002 alert.
- Supporting terminal and dashboard evidence recorded.

The controlled modification test validates this specific detection path. Broader validation remains outstanding, including file-creation and deletion behavior, detection-noise tuning, and systematic false-positive/false-negative testing.

## v0.3 — SOC investigation: In progress

The CASE-001 checkpoint has been documented using controlled FIM activity and supporting alert evidence.

The investigation includes review of the custom Rule 100002 alert and related FIM events. The reviewed events included benign-looking background configuration and cache changes; temporal proximity alone does not establish their process-level cause. No malicious indicators were identified in the reviewed dataset, but this is not a comprehensive endpoint forensic assessment.

The controlled-validation checkpoint is complete. Broader investigation, hunting, and SOC workflow development remain ongoing.

Not yet fully implemented or validated

- Broader authentication and process-execution telemetry.
- Systematic false-positive and false-negative test matrices.
- Completed detection tuning and broader FIM coverage validation.
- A complete incident-response exercise.
- Performance and detection-quality metrics.
- Purple-team validation and attack-mutation testing.
- A custom SENTINEL console.

## Roadmap

Version| Focus| Status
v0.1| Foundation — infrastructure, networking, Wazuh| Complete
v0.2| Telemetry and detection engineering| In progress; controlled modification detection validated
v0.3| SOC investigation — CASE-001| In progress; checkpoint documented
v0.4| Incident response| Planned
v0.5| Purple-team measurement| Planned
v0.6| Attack DNA and mutation testing| Planned
Future| Custom SENTINEL console and visualization layer| Not started

A completed test or checkpoint does not automatically mean its entire version is complete. Version status will be updated as the remaining agreed scope is tested and documented.

What makes SENTINEL valuable

SENTINEL is evaluated by evidence and repeatability—not tool count.

The project documents what worked, what remains untested, and where further tuning is needed. Its central differentiator is the intended engineering loop:

Simulate → Detect → Investigate → Respond → Measure → Improve → Retest

The validated Rule 100002 modification test demonstrates one working detection path. It does not imply complete FIM coverage or a fully operational end-to-end SOC workflow.

## Documentation and evidence

Resource| Purpose
"Detection engineering" (docs/05-detection-engineering.md)| Detection methodology, custom Rule 100002, validation results, and remaining work
"Incident response" (docs/06-incident-response.md)| Response methodology and planned exercises
"Testing and metrics" (docs/07-testing-and-metrics.md)| Testing, validation, and measurement methodology
"v0.1 evidence" (evidence/v0.1/)| Foundation evidence and artifacts
"v0.2 evidence" (evidence/v0.2/)| Telemetry and detection-engineering evidence
"v0.3 evidence" (evidence/v0.3/readme.md)| Investigation checkpoint and screenshots
"Detection guide" (detections/readme.md)| Detection directory organization
"Investigation guide" (investigations/readme.md)| Investigation process and case organization
"CASE-001" (investigations/CASE-001.md)| Controlled FIM validation investigation
"Security policy" (SECURITY.md)| Authorized testing boundaries
"Changelog" (CHANGELOG.md)| Version history and project changes

## Security and safety

SENTINEL is an authorized, controlled lab.

- Testing is restricted to the intended lab environment.
- No production targets or unauthorized external systems are tested.
- Real credentials, secrets, and VM disk images are not committed to the repository.
- Attack simulations and detection tests are conducted for defensive learning and validation.

See "SECURITY.md" (SECURITY.md) for the full testing boundaries and security policy.
