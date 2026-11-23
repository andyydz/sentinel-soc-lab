# SENTINEL — Requirements

## 1. Purpose

This document defines the infrastructure, hardware, software and network requirements for SENTINEL, an isolated virtual SOC laboratory. It distinguishes the **tested configuration** from **recommended resources** and from **future/optional expansion**. For project scope, lifecycle and status, see [`01-project-overview.md`](01-project-overview.md).

## 2. Scope and Milestone Context

**v0.1 (Foundation)** established the infrastructure: Wazuh, Kali, a Linux endpoint with a registered agent, and the isolated lab network. That infrastructure remains the base of the lab.

Development has continued through **v0.10** per [`CHANGELOG.md`](../CHANGELOG.md): detection engineering, SOC investigation, offline Sysmon replay detection, documented manual incident-response procedures and SSH triage, purple-team measurement, attack mutation, FIM tuning, Sysmon JSON replay with Python triage, and Linux FIM / Python triage validation. The incident-response work is manual and documented; it does not include automated containment, eradication or recovery.

Current capabilities, each limited to its documented scope:

- Linux file integrity monitoring (FIM) with Wazuh syscheck
- SSH detection and controlled SSH testing
- Offline replay of pre-recorded Sysmon EVTX telemetry
- Investigations (CASE-001 to CASE-004) and small-sample measurement (v0.6)
- Controlled mutation testing (CASE-004)
- Python-assisted alert parsing and severity-based triage (separate companion project)

None of this implies comprehensive detection coverage or production readiness. There is no live Windows endpoint and no Active Directory deployment.

## 3. Host Hardware

### Tested development host

| Item | Value |
|---|---|
| Host OS | Windows 11 |
| Hardware | ASUS ExpertBook |
| CPU | 13th Gen Intel Core i5-13420H |
| Host RAM | 16 GB |
| Virtualization platform | Oracle VirtualBox 7.2.20 *(owner to confirm current version)* |

### Practical guidance (recommendations, not minimums)

The three VMs together are assigned roughly the host's full 16 GB. Therefore:

- **16 GB** can run the lab, but needs active resource management: close unused VMs, reduce Kali's allocation when idle, and run attack and investigation phases sequentially.
- **32 GB** is the more comfortable recommendation for running everything at once.
- Performance also depends on CPU, storage speed and VirtualBox configuration. No benchmark is claimed.

No minimum CPU, RAM or disk requirement has been established or is claimed here.

## 4. Virtualization Requirements

- Oracle VirtualBox
- Hardware virtualization (VT-x/AMD-V) enabled in firmware, and 64-bit support
- Enough CPU cores, RAM and storage to allocate across guests
- VirtualBox Internal Network support (SENTINEL-LAB)
- VirtualBox NAT support (outbound updates and package access on SENTINEL-WAZUH)

Two network concepts are used:

- **SENTINEL-LAB:** the isolated Internal Network `10.10.10.0/24`. All three VMs are attached to it, and all lab traffic (SSH testing, Wazuh Agent communication) uses this network.
- **NAT:** separate outbound access for updates and package installs. Per [`03-architecture.md`](03-architecture.md), NAT is documented on **SENTINEL-WAZUH only**. SENTINEL-KALI and SENTINEL-LINUX01 use SENTINEL-LAB only, unless the owner confirms a different current VirtualBox configuration. NAT is **not** part of the isolated lab traffic path.

## 5. VM Configuration

This is the **documented tested configuration**, not a set of minimum requirements. Values marked ⚠ come from earlier documentation and could not be independently corroborated; they need owner confirmation.

### SENTINEL-WAZUH

| Setting | Value |
|---|---|
| OS | Ubuntu 24.04 |
| Software | Wazuh 4.14.8 (all-in-one: server, indexer, dashboard) |
| Lab IP | 10.10.10.10 |
| vCPU / RAM / Disk | 4 / 8192 MB / ~50 GB dynamic ⚠ |
| Other interface | NAT (outbound updates and packages), per `03-architecture.md` |

### SENTINEL-KALI

| Setting | Value |
|---|---|
| OS | Kali Linux 2026.2 ⚠ |
| Lab IP | 10.10.10.20 |
| vCPU / RAM / Disk | 2 / ~4 GB / ~80 GB ⚠ |
| Role | Attacker / adversary simulation |
| Other interface | None documented (SENTINEL-LAB only) ⚠ owner to confirm current VirtualBox adapters |

### SENTINEL-LINUX01

| Setting | Value |
|---|---|
| OS | Ubuntu 24.04 (24.04.5 LTS in earlier documentation ⚠) |
| Lab IP | 10.10.10.40 |
| vCPU / RAM / Disk | 2 / 4096 MB / 40 GB dynamic ⚠ |
| Telemetry agent | Wazuh Agent, version 4.14.8 per earlier documentation ⚠ |
| Agent ID | **002** (current documented ID). Earlier v0.1 evidence referenced `001`; this historical discrepancy has not been reconciled. |
| Agent status | Active, enabled at boot per earlier documentation ⚠ (re-check current state) |
| Other interface | None documented (SENTINEL-LAB only) ⚠ owner to confirm current VirtualBox adapters |

## 6. Software Requirements

| Software | Purpose | Status |
|---|---|---|
| Oracle VirtualBox | Hypervisor | ✅ In use |
| Wazuh 4.14.8 | SIEM, detection, FIM (syscheck) | ✅ Deployed |
| Ubuntu 24.04 | Wazuh host and Linux endpoint | ✅ Deployed |
| Kali Linux | Attacker / simulation | ✅ Deployed |
| Python 3 | EVTX conversion script and companion project | ✅ In use |
| `python-evtx` (`Evtx`) | Parse `.evtx` files | ✅ Dependency of `scripts/evtx_to_wazuh.py` |
| `xmltodict` | Convert event XML to dictionaries | ✅ Dependency of `scripts/evtx_to_wazuh.py` |
| Git / GitHub | Version control, hosting | ✅ In use |
| MITRE ATT&CK | Mapping methodology, not software | Methodology only |

Python 3 is required by the script but its exact version was not verified. No other dependencies are claimed; confirm against the script's imports.

### Python components

- **`scripts/evtx_to_wazuh.py`** converts pre-recorded Sysmon `.evtx` files to NDJSON for replay.
- **`python-soc-automation`** is a separate companion repository for Wazuh alert parsing and severity-based triage. Python-assisted triage has been demonstrated, including Sysmon replay and Wazuh Linux FIM alert-triage workflows. It is not a SOAR platform, performs no automated containment, eradication or recovery, and is not continuously or fully integrated with the Wazuh pipeline.

### Sysmon

Offline replay of recorded Sysmon EVTX telemetry is **implemented**. A **live Sysmon deployment is not**: there is no live Windows endpoint.

Not documented as deployed: Atomic Red Team, CALDERA, TheHive, Shuffle, OpenCTI, Suricata, and a custom SENTINEL console.

## 7. Network Requirements

**SENTINEL-LAB:** `10.10.10.0/24`, an isolated VirtualBox Internal Network.

| Node | Role | Lab IP |
|---|---|---|
| SENTINEL-WAZUH | Wazuh manager | 10.10.10.10 |
| SENTINEL-KALI | Attacker | 10.10.10.20 |
| SENTINEL-LINUX01 | Linux endpoint, Wazuh Agent 002 | 10.10.10.40 |

```
Kali (10.10.10.20) --controlled SSH testing--> Linux01 (10.10.10.40)
Linux01 --Wazuh Agent 002 communication--> Wazuh manager (10.10.10.10)
```

SENTINEL-KALI has network connectivity to the Wazuh manager over SENTINEL-LAB, but it does not send its own logs or telemetry to the manager. During controlled SSH testing, the resulting sshd authentication logs are collected on SENTINEL-LINUX01 by Wazuh Agent 002 and forwarded to the manager.

### Offline Sysmon replay pipeline

```
Pre-recorded Windows EVTX → scripts/evtx_to_wazuh.py → NDJSON → Linux01 logcollector → Wazuh detection
```

This is offline replay, not live Windows monitoring.

Notes:

- NAT is documented on SENTINEL-WAZUH only, for outbound updates and packages. SENTINEL-KALI and SENTINEL-LINUX01 use SENTINEL-LAB only, unless the owner confirms a different current configuration. NAT is not part of the isolated lab traffic path.
- No inbound exposure from the public Internet is intended.
- All attack simulation stays inside SENTINEL-LAB.

## 8. Storage Requirements

| VM | Virtual disk | Type |
|---|---|---|
| SENTINEL-WAZUH | ~50 GB ⚠ | Dynamic |
| SENTINEL-KALI | ~80 GB ⚠ | Dynamic or fixed, as configured |
| SENTINEL-LINUX01 | 40 GB ⚠ | Dynamic |

These are virtual capacities, not host usage. Keep free host storage headroom; Wazuh indexed data grows with use. No current consumption figure is claimed.

VM disks (`.vdi`, `.vmdk`, `.ova`, `.iso`), logs, packet captures and raw telemetry are not intended to be committed unless reviewed as safe to publish. `.gitignore` reduces the risk of committing such files but does **not** guarantee that sensitive files can never be committed; review changes before pushing.

## 9. CPU and Memory Planning

| VM | vCPU | RAM |
|---|---:|---:|
| SENTINEL-WAZUH | 4 ⚠ | 8 GB ⚠ |
| SENTINEL-KALI | 2 ⚠ | ~4 GB ⚠ |
| SENTINEL-LINUX01 | 2 ⚠ | 4 GB ⚠ |

SENTINEL-WAZUH is the most resource-intensive component. On a 16 GB host, shut down idle VMs, reduce Kali's allocation when idle, run phases sequentially, and avoid oversubscribing the host.

## 10. Isolation and Safety Requirements

- Keep all lab systems on SENTINEL-LAB.
- Run attacks only against authorized lab systems inside SENTINEL-LAB.
- Do not attack external systems, the host or the real LAN.
- Do not use real credentials in the lab.
- Do not store secrets, passwords, tokens or keys in GitHub.
- Do not expose intentionally vulnerable systems to the Internet.
- Keep sensitive telemetry and packet captures out of the public repository unless sanitized and intentionally published.
- Use the NAT interface (documented on SENTINEL-WAZUH only) solely for updates and package installs.

## 11. GitHub and Repository Requirements

**Repository:** `andyydz/Sentinel-SOC-Lab`
**Visibility:** Public. Content must therefore be reviewed before commit.

Root structure (⚠ owner to verify against the live root; `failure-log/` and `SECURITY.md` come from the earlier listing):

```
Sentinel-SOC-Lab/
├── .github/
├── detections/
├── docs/
├── evidence/
├── failure-log/
├── investigations/
├── metrics/
├── scenarios/
├── scripts/
├── .gitignore
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
└── SECURITY.md
```

**Intended to be stored:** documentation, detection configurations, scripts, sanitized evidence, investigation notes, metrics, project history.

**Must not be stored:** VM disks, passwords, API keys, private keys, tokens, `.env` files, sensitive credentials, unsanitized personal information, unnecessary raw telemetry.

## 12. Evidence Requirements

Evidence is organized per milestone under [`evidence/`](../evidence/). Availability varies by milestone, and the presence of a directory does not mean its evidence set is complete. The exact directory list should be taken from the repository.

- **Foundation (v0.1) evidence:** Wazuh Dashboard showing the Linux endpoint registered and active, the agent service running, and infrastructure verification. The original v0.1 evidence README identifies the captured agent as ID "001"; current documentation uses "002". This historical discrepancy remains unreconciled.
- **Later milestones:** detection, investigation, replay, measurement and mutation evidence is documented in [`investigations/`](../investigations/), [`metrics/`](../metrics/) and the per-milestone evidence folders, where supplied.

## 13. Current Readiness Summary

Documented release history runs through **v0.10** per [`CHANGELOG.md`](../CHANGELOG.md). The v0.11 FIM regression and exclusion checks are implementation-baseline verification, not an official changelog release.

The infrastructure foundation (VirtualBox, isolated lab network, Wazuh, Kali, Linux01 with Agent 002) is the working base. Detection, mutation and measurement work is selective and small-sample (see [`07-testing-and-metrics.md`](07-testing-and-metrics.md)). Detection gaps and FIM noise-tuning remain open.

## 14. Future Expansion (Optional, Not Committed)

- Live Windows endpoint and Active Directory / Windows Server
- Additional adversary-emulation platforms (e.g. Atomic Red Team, CALDERA)
- Network security telemetry (e.g. Suricata)
- Optional case management (e.g. TheHive)
- Optional custom SENTINEL console (Python/FastAPI)
- Additional mutation scenarios and coverage of known uncovered detections

Already implemented and therefore removed from this list: Python-based EVTX conversion, Python-assisted alert triage and offline Sysmon replay.
