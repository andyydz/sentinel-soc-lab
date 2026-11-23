# SENTINEL — Project Overview

SENTINEL is an evidence-driven SOC detection, investigation and response lab built on an isolated virtual network. It is used to simulate controlled attacks, collect telemetry, engineer detections, investigate alerts, measure results and retest after changes. It is a validation framework for detections, not a tool collection and not a production system.

---

## 1. Purpose and Core Question

Many home labs stop when a SIEM alert fires once. That shows a tool works; it does not show a *detection* works, or that it survives an attacker who changes behavior slightly.

> **Does your detection still work when the attacker changes tactics?**

SENTINEL treats the gap between "detected once" and "detected reliably" as its central engineering problem, and records gaps as findings rather than hiding them.

## 2. Project Concept

A deliberately small enterprise-style environment: a monitoring platform, an attacker system and a Linux target endpoint on a private network. All simulation stays inside that boundary.

## 3. Security Lifecycle

```
SIMULATE → DETECT → INVESTIGATE → RESPOND → MEASURE → IMPROVE → RETEST
```

| Stage | Meaning |
|---|---|
| Simulate | Run a controlled attack or behavior inside the lab |
| Detect | Telemetry is collected; a detection fires or does not |
| Investigate | Analyze the alert: timeline, evidence, technique mapping |
| Respond | Triage and response documentation (human-in-the-loop) |
| Measure | Record detection performance as data |
| Improve | Tune detections or telemetry based on findings |
| Retest | Re-run the same or a mutated behavior to check the fix |

## 4. Current Architecture

The live lab is Linux-based and runs on an isolated VirtualBox network, `10.10.10.0/24`.

```
        Isolated VirtualBox network 10.10.10.0/24

  +-------------+   controlled SSH testing   +------------------+
  | SENTINEL-   | -------------------------> | SENTINEL-LINUX01 |
  | KALI        |                            | 10.10.10.40      |
  | 10.10.10.20 |                            | Wazuh Agent 002  |
  +-------------+                            +------------------+
                                                      |
                                           Wazuh Agent communication
                                                      v
                                             +----------------+
                                             | SENTINEL-WAZUH |
                                             | 10.10.10.10    |
                                             +----------------+
```

Kali does not communicate directly with the Wazuh manager in the documented architecture. The lab traffic paths shown above (controlled SSH testing and Wazuh Agent communication) use the isolated lab network only. This overview does not document NAT adapter details; if a separate NAT adapter is configured in VirtualBox, it is separate from the isolated lab traffic path and is not part of the documented lab traffic flow.

### Offline Sysmon pipeline (separate from the live topology)

```
Pre-recorded Windows EVTX → Python EVTX conversion → NDJSON → logcollector → Wazuh detection
```

Recorded Sysmon telemetry is replayed through the Linux01 agent's logcollector. This is offline replay, **not** live Windows monitoring. There is no live Windows endpoint and no Active Directory deployment.

## 5. Infrastructure and Technology Stack

| Component | Role | Details |
|---|---|---|
| SENTINEL-WAZUH | SIEM / detection platform | Ubuntu 24.04, `10.10.10.10`, Wazuh 4.14.8 |
| SENTINEL-KALI | Attacker / simulation | Kali Linux, `10.10.10.20` |
| SENTINEL-LINUX01 | Monitored Linux endpoint | Ubuntu 24.04, `10.10.10.40`, Wazuh Agent ID `002` |

Supporting technology: Oracle VirtualBox (isolated networking), Wazuh FIM (syscheck), Wazuh log analysis for SSH and replayed Sysmon data, a Python EVTX-to-NDJSON converter, and Git/GitHub for documentation.

The baseline was checked for VirtualBox isolated networking, Agent ID `002` against the active endpoint, v0.11 FIM regression and exclusion behavior, and EVTX-to-NDJSON converter output against the intended Sysmon rule structure.

## 6. Development Roadmap

Milestones follow [`CHANGELOG.md`](../CHANGELOG.md), which holds per-release detail.

| Version | Focus |
|---|---|
| v0.1 | Foundation |
| v0.2 | Detection Engineering |
| v0.3 | SOC Investigation |
| v0.4 | Sysmon Replay Detection |
| v0.5 | Incident Response and SSH Triage |
| v0.6 | Purple-Team Measurement |
| v0.7 | Attack DNA and Mutation |
| v0.8 | FIM Tuning |
| v0.9 | Sysmon JSON Replay and Python Triage |
| v0.9.1 | Follow-up |
| v0.10 | Live Linux FIM and Python Triage Validation |

The v0.11 FIM regression and exclusion behavior has been verified as part of the current implementation baseline. This overview does not describe it as a changelog release.

## 7. Detection Engineering and Mutation Testing

Detections are built, tested against controlled activity, and then challenged with modified behavior. Mutation testing has been performed and is documented in CASE-004. For example, Sysmon command-line mutation #24 bypassed the keyword-based Rule `100112` and matched only the general Level 0 base rule, so no custom alert fired. This exposed a detection gap. CASE-004 also records selected FIM, Sysmon and SSH threshold observations.

Mutation coverage is limited to the scenarios documented there. Additional mutation scenarios remain future work. Rule logic and implementation details are in [`docs/05-detection-engineering.md`](05-detection-engineering.md).

## 8. Investigations

| Case | Scope |
|---|---|
| CASE-001 | FIM investigation, closed 18 November 2026 for its defined scope. Closure does not mean all FIM engineering or noise tuning is complete. |
| CASE-002 | Validates selected detections against replayed Sysmon EVTX telemetry. |
| CASE-003 | Controlled SSH testing, investigation and Python-assisted triage. |
| CASE-004 | Selected mutation, evasion, FIM and SSH threshold testing. |

Each case is limited to its documented scope. Timelines and evidence are in the case files under [`investigations/`](../investigations/).

## 9. Python SOC Automation Engine

A separate companion repository. It has been used for Wazuh alert parsing and severity-based triage, including documented Sysmon replay and Wazuh Linux FIM alert-triage workflows. It is not a SOAR platform, performs no automated containment, eradication or recovery, and is not continuously or fully integrated with the Wazuh detection pipeline.

## 10. Measurement

The v0.6 report ([`metrics/v0.6-purple-team-measurement.md`](../metrics/v0.6-purple-team-measurement.md)) records:

- **FIM:** 3/3 selected lifecycle events detected; 0/3 `/tmp` negative-control operations alerted.
- **Sysmon replay:** 7/7 selected detections fired; 0/3 benign events alerted; two Event ID 7 ImageLoad events remained uncovered.
- **SSH:** baseline and threshold escalation measured; sliding-window carry-over affected the first escalation in C2.

These are small controlled samples. They are not statistically meaningful detection rates or enterprise false-positive rates. Response time has not been measured, and regression coverage is not comprehensive. Details: [`docs/07-testing-and-metrics.md`](07-testing-and-metrics.md).

## 11. Evidence and Limitations

Evidence is stored per milestone where work produced it; availability varies and a milestone folder does not imply a complete evidence set. The repository is intended to exclude secrets, credentials and sensitive raw telemetry. Detection gaps, such as mutation #24, are documented as findings.

Limitations:

- No live Windows endpoint and no Active Directory.
- Sysmon coverage is offline replay of selected recorded telemetry.
- Detection coverage is selective, not comprehensive.
- FIM noise has not been fully eliminated.
- Lab only, not production-ready.

Future expansion (not committed): additional mutation scenarios, coverage of the uncovered Event ID 7 cases, a live Windows endpoint, Active Directory, and deeper DFIR workflows.

## 12. Current Status

In progress.

- **Latest documented release history:** v0.10 (Live Linux FIM and Python Triage Validation), per [`CHANGELOG.md`](../CHANGELOG.md).
- **Implementation-baseline checks (v0.11):** FIM regression and exclusion behavior verified. v0.11 is not represented as an official changelog release.
- **Open work:** detection gaps and noise-tuning work remain open.
