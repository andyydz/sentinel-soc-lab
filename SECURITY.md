# Security Policy

## Purpose

SENTINEL is an isolated virtual cybersecurity SOC laboratory used for defensive security research: detection engineering, security monitoring, SOC investigation, incident response practice, controlled adversary simulation, and purple-team validation. Its lifecycle is:

**SIMULATE → DETECT → INVESTIGATE → RESPOND → MEASURE → IMPROVE → RETEST**

SENTINEL deliberately runs controlled attack scenarios inside an isolated lab to generate telemetry and validate defensive controls. It is **not** intended to be used against real-world systems.

## Scope

This policy applies to:

- SENTINEL virtual machines
- SENTINEL-LAB networking
- Project source code, detection rules, and scripts
- Configuration examples and documentation
- Evidence committed to the repository
- Controlled attack/testing scenarios performed as part of the project

This policy does not grant permission to test any system outside the SENTINEL lab.

## Security Objectives

1. **Lab isolation** — simulated attacks and security testing stay inside the designated SENTINEL laboratory.
2. **Authorization** — only systems owned by the project owner or explicitly authorized for testing are targeted.
3. **Controlled adversary simulation** — attacks are deliberate, reproducible, and limited to designated lab systems.
4. **Defensive purpose** — attack simulation exists to generate telemetry and validate detection, investigation, response, and measurement capabilities.
5. **Evidence integrity** — testing produces reliable evidence without exposing secrets, credentials, or unnecessary sensitive data.
6. **Secrets protection** — credentials, keys, tokens, certificates, and session data are never committed to the repository.
7. **Host and external system protection** — testing must not intentionally affect the host OS, personal devices, unrelated VMs, external networks, cloud systems, third-party infrastructure, or any system outside the authorized lab.

## Laboratory Safety

The current SENTINEL foundation consists of:

| System | Role | Lab IP |
|---|---|---|
| SENTINEL-WAZUH (Ubuntu 24.04) | SOC / monitoring / detection platform (Wazuh all-in-one) | 10.10.10.10 |
| SENTINEL-KALI (Kali Linux) | Controlled attacker / adversary-emulation environment | 10.10.10.20 |
| SENTINEL-LINUX01 (Ubuntu 24.04) | Initial monitored endpoint (active Wazuh agent) | 10.10.10.40 |

All systems communicate over the isolated **SENTINEL-LAB** network (10.10.10.0/24). NAT is used only for legitimate internet access (OS updates, package installation, security tool updates) and does not authorize attacks against external systems.

An earlier design attempted to include a Windows endpoint. Windows and Active Directory are **not** currently part of the SENTINEL environment — they are planned future expansion, and Linux is currently the initial monitored endpoint.

Rules:

- Do not intentionally attack systems outside SENTINEL.
- Do not scan or exploit public IP addresses unless explicitly authorized and required for a separate, legitimate purpose.
- Do not use real or production credentials in attack simulations; use dedicated lab accounts.
- Do not store personal or sensitive information in the repository.
- Do not commit VM disk images or unnecessary raw telemetry containing sensitive information.
- Do not expose host-system information unnecessarily.
- Do not bridge the isolated lab network to an external network without a specific documented reason and appropriate controls.
- Stop testing immediately if activity begins affecting systems outside the intended scope.

## Controlled Attack Simulation

SENTINEL intentionally includes adversary simulation. Attack simulation is permitted **only** when:

- The target is inside the SENTINEL lab.
- The target is owned by, or explicitly authorized for, testing.
- The activity is part of a defined, controlled scenario.
- The activity is documented where appropriate.
- The activity does not intentionally target unrelated systems.

Examples of legitimate SENTINEL testing include controlled authentication attacks against lab systems, controlled network reconnaissance inside SENTINEL-LAB, controlled endpoint attack simulations, and verifying that Wazuh receives expected telemetry and that detection rules behave as intended.

This document does not contain attack instructions or offensive-security tutorials.

## Attack Mutation and Detection Resilience

A planned (not yet implemented) SENTINEL capability is **Attack Mutation**: modifying the behavior of a controlled attack — such as its execution pattern, timing, command structure, process behavior, or network behavior — while preserving its objective, in order to test whether a detection remains effective against changed attacker behavior.

When implemented, the same constraints as any other attack simulation apply:

- Mutation stays inside the isolated lab.
- Mutation targets only authorized systems.
- Mutation is never used against real-world targets.
- Mutation results are treated as security-testing evidence.
- Failed detections are documented and used to improve defensive controls.

Attack Mutation is a future methodology and is **not currently implemented** in SENTINEL.

## Data and Evidence Security

Allowed repository evidence includes sanitized screenshots, detection results, investigation notes, test results, sanitized logs, metrics, and configuration examples free of secrets.

The repository must **never** contain:

- Passwords, API keys, or access tokens
- Private SSH keys or certificates containing private material
- Session cookies or other authentication material
- Personal information
- Production logs or unnecessary raw telemetry containing sensitive data
- VM disk images or large unnecessary binary artifacts
- Sensitive host information

When evidence contains sensitive information, it must be removed, redacted, or replaced with safe example data before committing — never commit the original sensitive artifact.

## Credentials and Secrets

Never commit passwords, API keys, tokens, SSH private keys, cloud or database credentials, certificates/private keys, browser or session credentials, Wazuh administrative credentials, or any other authentication material.

Preferred practices:

- Use environment variables where appropriate.
- Use local configuration files excluded via `.gitignore`.
- Use dedicated lab-only credentials.
- Use secret-management mechanisms if and when future integrations require them.

Real production credentials must never be reused inside SENTINEL.

## Network Security

The SENTINEL-LAB network (10.10.10.0/24) provides an isolated environment for controlled testing:

- Wazuh: 10.10.10.10
- Kali: 10.10.10.20
- Linux01: 10.10.10.40

The lab remains separated from unrelated systems. NAT may be used for legitimate internet access (updates, package installation, tool updates), but this does not authorize attacks against external systems. No dedicated firewall or gateway appliance is currently implemented beyond the lab's network isolation.

## Virtualization Security

SENTINEL uses virtual machines to create controlled security-testing environments. Principles followed:

- Keep VM networking intentional; prefer isolated/internal networking for attack traffic.
- Avoid unnecessary bridged networking.
- Keep host/guest boundaries in mind.
- Do not expose unnecessary services from lab VMs.
- Keep snapshots/backups controlled when used.
- Do not commit VM disks to the repository.
- Do not expose VM credentials or configuration secrets.

No advanced hypervisor-level security controls beyond these practices are currently implemented.

## Failure and Incident Handling

SENTINEL treats unexpected failures as engineering evidence, using the process:

**STOP → CAPTURE → DOCUMENT → CONTINUE**

If a security test behaves unexpectedly and may affect systems outside the intended lab scope:

1. Stop the activity immediately.
2. Disconnect or disable the relevant test activity.
3. Assess what systems were affected.
4. Preserve relevant evidence.
5. Document the issue.
6. Correct the environment before continuing.

Infrastructure failures, detection failures, false positives, missed detections, investigation failures, and response failures are documented as part of SENTINEL's engineering process rather than hidden.

## Reporting Security Issues

If you identify a security issue in SENTINEL itself:

- Do not publicly disclose exploit details that could expose credentials, infrastructure information, or other sensitive material.
- Non-sensitive issues may be reported via the project's GitHub issue tracker.
- Issues involving sensitive information should not be publicly disclosed; contact the repository owner privately instead.

This project does not currently maintain a dedicated security contact address, bug bounty, private disclosure portal, security team, or response-time guarantee.

## Current and Future Security Capabilities

**Current:**
- Isolated virtual lab (SENTINEL-LAB)
- Wazuh monitoring and detection platform
- Kali attacker VM
- Linux monitored endpoint
- Controlled testing practices
- Evidence-handling practices
- Repository secret protection
- Internal lab network isolation

**Future (not yet implemented):**
- Windows endpoint and Active Directory environment
- Attack DNA and Attack Mutation
- Expanded purple-team testing
- Advanced response automation
- Additional forensic capabilities
- Custom SENTINEL Console

Future capabilities are not represented as currently deployed.
