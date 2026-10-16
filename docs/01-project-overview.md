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

> **Note:** Other project documentation (`investigations/CASE-001.md`) records this agent as ID `002`. This discrepancy has not been resolved through live verification, so neither ID is presented here as newly verified. It should be checked separately against the Wazuh Dashboard or manager.

## 7. Technology Stack

Status labels: ✅ deployed or in use as a tool · 🔄 concept or capability in partial use · ⏳ planned, not yet implemented.

| Category | Technology | Status |
|---|---|---|
| SIEM / Security monitoring | Wazuh (server, indexer, dashboard) | ✅ Deployed |
| Endpoint telemetry | Wazuh Agent 4.14.8 | ✅ Deployed on Linux01 |
| File integrity monitoring | Wazuh FIM (syscheck) | 🔄 In use — exercised in one controlled modification test |
| Custom detection rules | Wazuh custom rule `100002` | 🔄 In use — validated for the tested file modification only |
| Attacker environment | Kali Linux | ✅ Deployed |
| Operating systems | Ubuntu 24.04.5 LTS, Kali Linux | ✅ Deployed |
| Virtualization | Oracle VirtualBox | ✅ In use |
| Networking | Isolated internal lab network (SENTINEL-LAB, 10.10.10.0/24) + NAT | ✅ In use |
| Detection framework | MITRE ATT&CK mapping | ⏳ Planned — comprehensive mapping not yet implemented |
| Automation / engineering | Python | ⏳ Planned — not yet implemented |
| Documentation | Git / GitHub | ✅ In use |

Sysmon is **not** currently deployed anywhere in the lab.

## 8. Development Roadmap

| Version | Focus | Main Objective | Status |
|---|---|---|---|
| v0.1 | Foundation | Isolated lab network, Wazuh deployment, Kali attacker VM, Linux endpoint, agent connectivity | ✅ COMPLETED |
| v0.2 | Detection Engineering | Linux/auth/SSH telemetry, File Integrity Monitoring, detection development and tuning | 🔄 IN PROGRESS — controlled FIM modification test demonstrated; further testing and tuning outstanding |
| v0.3 | SOC Investigation | Alert investigation, evidence collection, timelines, IOCs, MITRE ATT&CK mapping, threat hunting, case management | 🔄 IN PROGRESS — CASE-001 documented and closed for its controlled validation objective |
| v0.4 | Incident Response | Controlled response actions, containment, recovery, incident reporting | ⏳ PLANNED |
| v0.5 | Purple-Team Measurement | Detection rate, missed detections, false positives, timing metrics, before/after comparison | ⏳ PLANNED |
| v0.6 | Attack DNA & Mutation | Attack-chain representation, controlled attacker behavior modification, resilience retesting | ⏳ PLANNED |

**v0.2 progress.** A controlled modification of `/home/sentinel-admin/sentinel-fim-validation.txt` generated a Level 8 alert under custom Wazuh Rule `100002`. This demonstrates detection of the tested modification only. File creation and deletion validation, systematic false-positive and false-negative testing, and detection tuning remain outstanding. This does not indicate comprehensive detection coverage.

**v0.3 progress.** [`investigations/CASE-001.md`](../investigations/CASE-001.md) documents the controlled validation and a review of related FIM events. The case is closed for that validation objective only; the broader v0.3 investigation work remains in progress.

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

Attack DNA, Attack Mutation, Detection Resilience, and the Purple-Team Feedback Loop have not been implemented. Failure-driven detection engineering remains a design goal. The controlled FIM modification validation described in CASE-001 is an existing detection-validation activity, not attack mutation or detection-resilience testing.

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

The version directories show the planned evidence organization. Actual evidence availability depends on completed work, and a listed directory does not mean its evidence set is complete.

## 12. Failure Logging

```
failure-log/
├── detection-failures.md
├── false-positives.md
├── mutation-failures.md
└── infrastructure-issues.md
```

A missed detection or a false positive says something useful about a detection's actual coverage — logging it, rather than omitting it, is what makes the project's later performance claims credible.

This structure describes the intended organization. It does not mean every category already contains validated findings.

## 13. Documentation & Case-Based Learning

Significant investigations—including controlled detection validations, suspicious-event investigations, and confirmed incidents—should produce structured case reports using this format:

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

[`investigations/CASE-001.md`](../investigations/CASE-001.md) documents the controlled FIM modification validation and its supporting evidence. This case validates the tested modification only; it does not establish complete FIM coverage or a comprehensive forensic assessment. The list above is the intended template, and it does not mean every field has been fully validated in the lab.

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

Observed event counts are not the same as formal detection-performance metrics. For example, the CASE-001 review noted 19 matching FIM events in the reviewed period. That count includes the controlled validation event, and the remaining events were not fully attributed to individual processes. It is not a detection rate, a false-positive rate, or evidence of overall detection performance.

No formal detection-performance metrics have been collected yet, and none are presented here. Formal measurement, before/after comparison, and comprehensive metrics remain future work, to be populated starting in v0.5.

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

**Completed milestone:** v0.1 — Foundation
**Current milestones:** v0.2 — Detection Engineering (in progress) and v0.3 — SOC Investigation (in progress)
**Status:** IN PROGRESS — v0.2's controlled FIM modification test is demonstrated; broader validation and tuning remain outstanding. v0.3 includes CASE-001, closed for its controlled validation objective, while broader investigation work remains in progress.
**Next planned milestone:** v0.4 — Incident Response
