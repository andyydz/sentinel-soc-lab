# SENTINEL — Requirements

## 1. Purpose

This document defines the actual infrastructure, hardware, software, and network requirements for SENTINEL — a virtual cybersecurity SOC laboratory used for controlled adversary simulation, security telemetry, detection engineering, SOC investigation, incident response, measurement, and detection-resilience testing. It distinguishes what is currently deployed and tested (v0.1) from what is recommended and from what is future/optional expansion.

## 2. v0.1 Scope

The current milestone, **v0.1 — Foundation**, includes the following deployed components:

- SENTINEL-WAZUH — SOC / monitoring platform
- SENTINEL-KALI — attacker / adversary-simulation system
- SENTINEL-LINUX01 — Linux endpoint with a registered, active Wazuh Agent
- SENTINEL-LAB — isolated internal network (`10.10.10.0/24`)

Windows, detection content, investigation workflows, incident response, metrics, and attack mutation are **not** part of v0.1 and are covered under [Future Expansion Requirements](#14-future-expansion-requirements) or later roadmap versions.

## 3. Host Hardware Requirements

### Current development host

| Item | Value |
|---|---|
| Host OS | Windows 11 |
| Hardware | ASUS ExpertBook |
| CPU | 13th Gen Intel Core i5-13420H |
| Host RAM | 16 GB |
| Virtualization platform | Oracle VirtualBox 7.2.20 |

### Practical guidance

The current three VMs together are assigned roughly 16 GB of RAM, which is effectively the entire host's memory. This means:

- **16 GB host RAM** can run the lab, but comfortable simultaneous operation of all three VMs requires active resource management (closing unused VMs, reducing Kali's allocation when idle, or running attack/investigation phases sequentially rather than all at once).
- **32 GB host RAM** is a more comfortable recommendation for running the full environment simultaneously without manual juggling.
- Actual performance also depends on host CPU, storage speed (SSD vs HDD), and how VirtualBox's virtualization mode is configured — no specific benchmark is claimed here.

## 4. Virtualization Requirements

- Oracle VirtualBox (currently version 7.2.20)
- Hardware virtualization (VT-x/AMD-V) enabled in firmware
- 64-bit virtualization support
- Sufficient CPU cores to allocate across guest VMs
- Sufficient RAM to allocate across guest VMs
- Sufficient storage for dynamically allocated virtual disks
- VirtualBox NAT networking support
- VirtualBox Internal Network support (used for SENTINEL-LAB)

Two distinct network concepts are used:

- **NAT** — provides outbound Internet access to a VM (e.g., OS updates, package installation) when required.
- **SENTINEL-LAB** — the isolated internal network used for all communication between the lab's security infrastructure and simulated enterprise systems. This network is not intended to expose any system to the public Internet.

## 5. Current VM Configuration

This is the **current tested configuration** — not a set of minimum requirements.

### SENTINEL-WAZUH

| Setting | Value |
|---|---|
| Platform | VirtualBox VM |
| OS | Ubuntu 24.04 |
| vCPU | 4 |
| RAM | 8192 MB |
| Disk | ~50 GB, dynamically allocated |
| Role | Wazuh all-in-one (server, indexer, dashboard) |
| Lab interface | 10.10.10.10 |
| Other interface | NAT (Internet/package access) |

### SENTINEL-KALI

| Setting | Value |
|---|---|
| Platform | VirtualBox VM |
| OS | Kali Linux 2026.2 |
| vCPU | 2 |
| RAM | ~4 GB |
| Disk | ~80 GB |
| Role | Attacker / adversary-simulation VM |
| Lab interface | 10.10.10.20 |
| Other interface | NAT (Internet/package access) |

### SENTINEL-LINUX01

| Setting | Value |
|---|---|
| Platform | VirtualBox VM |
| OS | Ubuntu 24.04.5 LTS |
| vCPU | 2 |
| RAM | 4096 MB |
| Disk | 40 GB, dynamically allocated |
| Lab interface | 10.10.10.40 |
| Other interface | NAT (Internet/package access) |
| Telemetry agent | Wazuh Agent 4.14.8 |
| Agent ID | 001 |
| Agent status | Active |
| Agent service | Enabled at boot |

## 6. Operating System Requirements

Current v0.1 operating systems:

| Component | OS |
|---|---|
| SENTINEL-WAZUH | Ubuntu 24.04 |
| SENTINEL-KALI | Kali Linux 2026.2 |
| SENTINEL-LINUX01 | Ubuntu 24.04.5 LTS |

**Windows is not a v0.1 requirement.** A Windows endpoint (and optionally Active Directory) may be introduced in a later phase as an optional expansion — see [Future Expansion Requirements](#14-future-expansion-requirements).

## 7. Software Requirements

| Software | Purpose | Current Status |
|---|---|---|
| Oracle VirtualBox | Hypervisor for all lab VMs | ✅ Deployed |
| Wazuh | SIEM / monitoring / detection platform | ✅ Deployed (all-in-one, v4.14.8 agent) |
| Ubuntu | OS for Wazuh host and Linux endpoint | ✅ Deployed |
| Kali Linux | Attacker / adversary-simulation OS | ✅ Deployed |
| Git | Version control | ✅ In use |
| GitHub | Project hosting and documentation | ✅ In use |
| MITRE ATT&CK | Detection/investigation mapping methodology | ⏳ Planned methodology, not deployed software |
| Python | Automation and engineering scripting | ⏳ Planned, not yet used |

The following tools are **future/optional only** and are not currently deployed: Sysmon, Atomic Red Team, CALDERA, TheHive, Shuffle, OpenCTI, Suricata, and a custom SENTINEL console. They are not required for v0.1 and are listed only under [Future Expansion Requirements](#14-future-expansion-requirements) where relevant.

## 8. Network Requirements

**SENTINEL-LAB:** `10.10.10.0/24` — an isolated VirtualBox Internal Network.

| Node | Role | Lab IP |
|---|---|---|
| SENTINEL-WAZUH | SOC / Wazuh | 10.10.10.10 |
| SENTINEL-KALI | Attacker | 10.10.10.20 |
| SENTINEL-LINUX01 | Linux endpoint | 10.10.10.40 |

```
Internet
   |
  NAT
   |
Virtual Machines
```

```
SENTINEL-LAB
10.10.10.0/24
   |
   +-- SENTINEL-WAZUH   (10.10.10.10)
   +-- SENTINEL-KALI    (10.10.10.20)
   +-- SENTINEL-LINUX01 (10.10.10.40)
```

Notes:

- NAT is a separate path from SENTINEL-LAB and is used only when a VM needs outbound Internet access (updates, packages).
- The lab network does not provide inbound exposure from the public Internet.
- All security testing (attacks, exploitation, adversary simulation) must remain inside the authorized SENTINEL-LAB boundary.

## 9. Storage Requirements

Current virtual disk configurations:

| VM | Virtual Disk Size | Type |
|---|---|---|
| SENTINEL-WAZUH | ~50 GB | Dynamically allocated |
| SENTINEL-KALI | ~80 GB | Dynamically allocated/fixed (as configured) |
| SENTINEL-LINUX01 | 40 GB | Dynamically allocated |

These figures are **virtual disk capacities**, not current host disk usage — a dynamically allocated disk only consumes host storage as data is actually written to it, so actual usage on the host is smaller than these maximums, especially early in the project.

Practical considerations:

- Leave free host storage headroom for VM growth over time.
- Wazuh's indexed security data and logs can grow as the lab is used, increasing actual disk consumption on SENTINEL-WAZUH.
- VM disk files are not stored in the Git repository.
- `.vdi`, `.vmdk`, `.ova`, `.iso` files, logs, packet captures, and raw telemetry are not committed unless there is a specific reason and the content has been reviewed as safe to publish.
- The repository's `.gitignore` is intended to exclude VM disks, logs, telemetry, packet captures, credentials, and secrets.

No exact current storage consumption figure is claimed here.

## 10. CPU and Memory Planning

Current resource allocation:

| VM | vCPU | RAM |
|---|---:|---:|
| SENTINEL-WAZUH | 4 | 8 GB |
| SENTINEL-KALI | 2 | ~4 GB |
| SENTINEL-LINUX01 | 2 | 4 GB |

SENTINEL-WAZUH is the most resource-intensive component in the lab, since it runs the Wazuh server, indexer, and dashboard together.

For hosts with limited RAM (such as the current 16 GB host):

- Shut down VMs that are not actively needed for the current task.
- Reduce Kali's allocated resources when it is not being used to actively simulate an attack.
- Run attack simulation and investigation phases sequentially rather than expecting every VM to run at once.
- Avoid overallocating vCPU/RAM to guests beyond what the host can actually spare, since oversubscription can degrade performance for all VMs.

## 11. Laboratory Isolation & Safety Requirements

- Use an isolated lab network (SENTINEL-LAB) for all lab systems.
- Perform attacks and adversary simulation only against authorized lab systems inside SENTINEL-LAB.
- Do not attack external systems, the host machine, or the real LAN.
- Do not use real credentials anywhere in the lab.
- Do not store secrets, passwords, tokens, or keys in GitHub.
- Do not expose intentionally vulnerable lab systems to the public Internet.
- Keep sensitive telemetry and packet captures out of the public repository unless they have been sanitized and are intentionally published.
- Use the NAT interface only when a VM genuinely needs Internet access (updates, package installs).

## 12. GitHub / Development Requirements

**Repository:** `sentinel-soc-lab`
**Visibility:** Private during development.

Current documentation/project structure:

```
sentinel-soc-lab/
├── detections/
├── docs/
├── evidence/
├── failure-log/
├── investigations/
├── metrics/
├── scenarios/
├── .gitignore
├── CHANGELOG.md
├── LICENSE
├── README.md
└── SECURITY.md
```

**GitHub stores:**

- Documentation
- Detection configurations
- Scripts
- Sanitized evidence
- Investigation notes
- Metrics
- Project history

**GitHub must NOT store:**

- VM disks
- Passwords
- API keys
- Private keys
- Tokens
- `.env` files
- Sensitive credentials
- Unsanitized personal information
- Unnecessary raw telemetry

## 13. Evidence Requirements

```
evidence/
├── v0.1/
├── v0.2/
├── v0.3/
├── v0.4/
├── v0.5/
└── v0.6/
```

For **v0.1**, evidence may include:

- Wazuh Dashboard showing SENTINEL-LINUX01 registered
- Agent ID and status confirmation
- Wazuh agent service status
- Final infrastructure verification (connectivity, IPs)

No additional v0.1 evidence beyond what is listed above currently exists. Future phases may add detection alerts, investigation evidence, screenshots, test results, metrics, incident reports, and retest results as those phases are completed.

## 14. Future Expansion Requirements

**None of the items in this section are required for v0.1.** They are potential directions for later phases and will only be introduced if they solve a demonstrated project requirement.

### Windows / Active Directory
Possible future Windows endpoint and Windows Server / AD environment for Windows-specific telemetry and attack scenarios.

### Detection Automation
Possible Python-based automation for detection testing, tuning, or reporting.

### Adversary Emulation
Possible integration of Atomic Red Team or CALDERA for repeatable, mapped attack execution.

### Network Security Telemetry
Possible network monitoring tooling (e.g., Suricata) if it provides meaningful detection value.

### Custom SENTINEL Console
Possible future Python/FastAPI backend and frontend layer that consumes real Wazuh data for a custom view into the lab.

### DFIR / Case Management
Possible future forensic tooling and case-management integration (e.g., TheHive) to support v0.3-and-later investigation workflows.

## 15. v0.1 Readiness Checklist

### v0.1 Foundation

- [x] VirtualBox installed
- [x] SENTINEL-WAZUH deployed
- [x] Wazuh Dashboard operational
- [x] SENTINEL-LAB created
- [x] SENTINEL-KALI deployed
- [x] SENTINEL-LINUX01 deployed
- [x] Linux01 assigned 10.10.10.40
- [x] Wazuh Agent installed
- [x] Wazuh Agent registered
- [x] Agent status verified as Active
- [x] Agent configured to start automatically

### v0.2 Prerequisites

- [ ] Linux telemetry requirements defined
- [ ] Authentication telemetry configured
- [ ] Detection requirements defined
- [ ] First detection scenario prepared
-
