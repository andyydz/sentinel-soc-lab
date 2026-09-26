# SENTINEL — Project Overview

SENTINEL is a virtual cybersecurity SOC laboratory built inside an isolated environment to model a small enterprise network — a place where attacks can be simulated, telemetry collected, detections engineered, incidents investigated, responses tested, and defensive controls continuously validated. It is not a Wazuh installation, an attacker VM, or a tool collection; it is a framework for proving that a detection actually works, and for finding out when it stops working.

---

## 1. Project Purpose

Most home security labs stop once a SIEM is installed and a single alert fires. That proves a tool works — it doesn't prove a *detection* works, and it says nothing about whether that detection survives an attacker who behaves even slightly differently next time.

SENTINEL exists to close that gap. Its purpose is to build a small, controlled enterprise-like environment where the full defensive lifecycle — from attack simulation through measurable detection improvement — can be practiced and documented end to end, rather than stopping at "an alert appeared."

## 2. Core Question

> **Does your detection still work when the attacker changes tactics?**

This question matters because most detections are written and tested against one specific version of an attack. A rule tuned to catch one exact command line, encoding, or tool often breaks the moment an attacker changes any of those details while keeping the same objective. SENTINEL treats that gap — between "detected once" and "detected reliably" — as the central engineering problem worth solving, and is designed so every future detection is eventually tested against a mutated form of the attack it was built for.

## 3. Project Concept

SENTINEL models a miniature enterprise: a monitoring/SOC platform, an attacker system, and one or more target endpoints, all connected on a private, isolated lab network. Everything relevant to the project — the attacks, the telemetry, the alerts, the investigations — happens inside this boundary. The lab is deliberately small so that every component's purpose is understood, rather than accumulating tools for their own sake.

## 4. Security Lifecycle

```
SIMULATE → DETECT → INVESTIGATE → RESPOND → MEASURE → IMPROVE → RETEST
```

| Stage | What it means |
|---|---|
| **Simulate** | Execute a controlled attack or adversary behavior inside the lab |
| **Detect** | Telemetry is collected and a detection either fires or doesn't |
| **Investigate** | The resulting alert is analyzed: timeline, evidence, IOCs, technique mapping |
| **Respond** | A containment or remediation action is taken (human-in-the-loop) |
| **Measure** | Detection and response performance is recorded as data |
| **Improve** | Detections or telemetry are tuned based on what measurement showed |
| **Retest** | The same — or a mutated — attack is run again to confirm the fix holds |

## 5. Current Architecture

The current lab is Linux-based. There is no Windows endpoint in the environment at this stage.

```
                    INTERNET
                       |
                      NAT
                       |
              +----------------+
              | SENTINEL-WAZUH |
              | 10.10.10.10    |
              | Wazuh SOC      |
              +----------------+
                       |
                SENTINEL-LAB
                10.10.10.0/24
                       |
              +--------+--------+
              |                 |
       +-------------+   +-------------+
       | SENTINEL-   |   | SENTINEL-   |
       | KALI        |   | LINUX01     |
       | 10.10.10.20 |   | 10.10.10.40 |
       | Attacker    |   | Target      |
       +-------------+   +-------------+
```

## 6. Current Infrastructure

| Component | Role | OS / Technology | Lab IP | Status |
|---|---|---|---|---|
| SENTINEL-WAZUH | SOC / monitoring / detection platform | Wazuh (all-in-one) | 10.10.10.10 | ✅ Deployed |
| SENTINEL-KALI | Attacker / adversary simulation system | Kali Linux | 10.10.10.20 | ✅ Deployed |
| SENTINEL-LINUX01 | Linux endpoint / target | Ubuntu 24.04.5 LTS, Wazuh Agent 4.14.8 | 10.10.10.40 | ✅ Deployed, agent active |

SENTINEL-LINUX01's Wazuh Agent (ID `001`) is registered, appears in the Wazuh Dashboard, and is running as an enabled, automatically-starting service. The Wazuh package repository was disabled after installation to avoid unintended package upgrades.

## 7. Technology Stack

| Category | Technology | Status |
|---|---|---|
| SIEM / Security monitoring | Wazuh (server, indexer, dashboard) | ✅ Deployed |
| Endpoint telemetry | Wazuh Agent 4.14.8 | ✅ Deployed on Linux01 |
| Attacker environment | Kali Linux | ✅ Deployed |
| Operating systems | Ubuntu 24.04.5 LTS, Kali Linux | ✅ Deployed |
| Virtualization | Oracle VirtualBox | ✅ In use |
| Networking | Isolated internal lab network (SENTINEL-LAB, 10.10.10.0/24) + NAT | ✅ In use |
| Detection framework | MITRE ATT&CK mapping | ⏳ Planned |
| Automation / engineering | Python | ⏳ Planned |
| Documentation | Git / GitHub | ✅ In use |

Sysmon is **not** currently deployed anywhere in the lab.

## 8. Development Roadmap

| Version | Focus | Main Objective | Status |
|---|---|---|---|
| v0.1 | Foundation | Isolated lab network, Wazuh deployment, Kali attacker VM, Linux endpoint, agent connectivity | ✅ COMPLETED |
| v0.2 | Detection Engineering | Linux/auth/SSH telemetry, File Integrity Monitoring, detection development and tuning | ⏳ PLANNED |
| v0.3 | SOC Investigation | Alert investigation, evidence collection, timelines, IOCs, MITRE ATT&CK mapping, threat hunting, case management | ⏳ PLANNED |
| v0.4 | Incident Response | Controlled response actions, containment, recovery, incident reporting | ⏳ PLANNED |
| v0.5 | Purple-Team Measurement | Detection rate, missed detections, false positives, timing metrics, before/after comparison | ⏳ PLANNED |
| v0.6 | Attack DNA & Mutation | Attack-chain representation, controlled attacker behavior modification, resilience retesting | ⏳ PLANNED |

## 9. Differentiation

Traditional home SOC:

```
Attack → Alert → Screenshot
```

SENTINEL's intended workflow:

```
Attack → Detection → Investigation → Response → Measurement → Improvement → Retest
```

The difference isn't the tools — a home SOC and SENTINEL can both run Wazuh. The difference is what happens after the alert fires: whether the detection's performance is ever measured, and whether it's ever tested again after the attacker changes something. This isn't a claim that SENTINEL is better than other projects — it's a description of the additional stages this project is designed to build out over time.

## 10. Signature Engineering Concepts

These are **design goals for later project stages**, not current capabilities:

- **Attack DNA** — representing a full attack chain as a sequence of behaviors, rather than judging a single isolated alert.
- **Attack Mutation** — changing how an attacker achieves an objective (tooling, encoding, timing) while keeping the objective the same, then retesting.
- **Detection Resilience** — whether a detection keeps catching the underlying malicious behavior after mutation.
- **Purple-Team Feedback Loop** — Attack → Detect → Investigate → Measure → Improve → Retest, run repeatedly.
- **Failure-Driven Detection Engineering** — a missed detection or false positive is recorded and treated as engineering evidence, not hidden.

None of these have been implemented yet; they describe the direction v0.2 onward is building toward.

## 11. Evidence-Driven Development

Each meaningful phase of the project is intended to produce evidence rather than just a claim of completion:

```
evidence/
├── v0.1/
├── v0.2/
├── v0.3/
├── v0.4/
├── v0.5/
└── v0.6/
```

Screenshots, detection test results, alerts, investigation notes, metrics, and reports may be stored here as each phase produces them. No secrets, credentials, or sensitive raw telemetry are stored in this structure.

## 12. Failure Logging

```
failure-log/
├── detection-failures.md
├── false-positives.md
├── mutation-failures.md
└── infrastructure-issues.md
```

A missed detection or a false positive says something useful about a detection's actual coverage — logging it, rather than omitting it, is what makes the project's later performance claims credible.

## 13. Documentation & Case-Based Learning

Once real incidents are investigated, each significant one is intended to produce a structured case report using this format:

- Incident Summary
- Severity
- Affected Assets
- Timeline
- Initial Detection
- Evidence
- IOCs
- MITRE ATT&CK Mapping
- Investigation
- Root Cause
- Response
- Detection Performance
- Failure / False Positive Analysis
- Improvements
- Retest Results
- Lessons Learned

No case report exists yet — this format will apply starting in v0.3.

## 14. Metrics Philosophy

Once detections exist, SENTINEL intends to measure them rather than just display alerts. Planned metrics include:

- Attack executions
- Successful detections
- Missed detections
- False positives
- Detection rate
- Detection time
- Response time
- Before/after detection performance

No metrics have been collected yet, and none are presented here — this section describes the intended measurement model, to be populated starting in v0.5.

## 15. Future Expansion

**The following are future possibilities only — none are currently part of the lab:**

- Windows endpoint
- Active Directory / Windows Server
- Deception / honeypot capabilities
- Deeper DFIR workflows
- Threat intelligence integrations
- A custom SENTINEL console
- A Python/FastAPI automation layer

These will only be added if and when they provide clear security or engineering value — they are not commitments on a timeline.

## 16. Security & Lab Safety

SENTINEL runs entirely inside an isolated laboratory network. All adversary simulation stays inside that boundary; nothing in this project targets external systems, the host machine, or a real LAN. No real credentials, personal information, API keys, tokens, private keys, or production data are used anywhere in the lab. VM disks, sensitive telemetry, credentials, and secrets are not committed to the repository.

## 17. Project Status

**Current milestone:** v0.1 — Foundation
**Status:** COMPLETED
**Next milestone:** v0.2 — Detection Engineering & Linux Telemetry
