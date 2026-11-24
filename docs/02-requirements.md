# SENTINEL — Requirements Specification

This document specifies what the SENTINEL SOC Lab is required to do, the constraints it operates under, how each requirement is verified, and how far each is actually met. It is a requirements specification, not a project overview; the project narrative is in [01-project-overview.md](01-project-overview.md) and the environment design is in [03-architecture.md](03-architecture.md).

SENTINEL is an educational lab. No requirement here implies production readiness, comprehensive detection coverage, or enterprise-grade performance.

---

## 1. Purpose

SENTINEL exists to validate detections, not just to run security tools. The lab is required to:

1. Simulate selected activity in a controlled, isolated environment.
2. Collect telemetry from that activity and evaluate detection rules against it.
3. Support investigation of the resulting alerts, with traceable evidence.
4. Measure results, record gaps as findings, and retest after changes.

Each requirement below has a stable ID, a priority, a status, and acceptance criteria that state how it can be checked and, where evidence is limited to selected scenarios, what that limit is.

## 2. Scope

**In scope:** the isolated Linux-based lab (Wazuh Manager, Kali simulation host, one monitored Linux endpoint), Linux FIM and SSH detection, offline replay of recorded Windows Sysmon telemetry, investigation and evidence documentation, selected controlled measurement and mutation testing, and a separate Python companion project for alert triage.

**Out of scope:** see [Section 9](#9-out-of-scope--deferred-requirements).

## 3. System Context and Constraints

| Item | Constraint / fact |
|---|---|
| Lab network | Isolated VirtualBox network `10.10.10.0/24` |
| SENTINEL-WAZUH | Ubuntu 24.04, Wazuh 4.14.8, `10.10.10.10` |
| SENTINEL-KALI | Kali Linux, `10.10.10.20`, used for controlled attack simulation |
| SENTINEL-LINUX01 | Ubuntu 24.04.5 LTS, `10.10.10.40`, Wazuh Agent 4.14.8, Agent ID `002` |
| FIM scope | `/home` on SENTINEL-LINUX01 |
| Telemetry paths | Kali generates controlled SSH traffic to Linux01. Linux01's Wazuh Agent forwards Linux01's telemetry to the manager. Kali does not forward its own SSH authentication logs to Wazuh |
| NAT | The Wazuh Manager has a separate NAT interface for outbound updates and package access. NAT is not part of the isolated attack or telemetry paths |
| Windows telemetry | Offline replay of recorded Sysmon data only: EVTX (Python EVTX-to-NDJSON conversion, ingested by logcollector through Linux01) and JSON (ingested by manager-side logcollector). No live Windows endpoint and no Active Directory |
| Python triage | `python-soc-automation` is a separate companion project that parses Wazuh alert JSON and supports severity-based triage. It is not a native Wazuh component, not a SOAR platform, and not a continuously integrated detection pipeline |
| Response | Human-in-the-loop. No automated containment, eradication, or recovery is implemented |

---

## 4. Functional Requirements

**Priority:** Must / Should / Could. **Status:** Implemented / Partially Implemented / Planned / Not Implemented. A requirement is not marked Implemented merely because it is documented; see [Section 7](#7-verification-and-acceptance-criteria).

| ID | Requirement | Priority | Status | Verification / Acceptance Criteria | Evidence / Reference |
|---|---|---|---|---|---|
| FR-01 | The lab shall support controlled simulation of selected activity: SSH authentication attempts originating from SENTINEL-KALI against SENTINEL-LINUX01, and controlled FIM file operations performed on the monitored SENTINEL-LINUX01 endpoint, within the isolated network | Must | Implemented | Controlled SSH password-guessing attempts originating from Kali and targeting Linux01 have been run and recorded (CASE-003). Controlled FIM file operations were performed on the monitored Linux01 endpoint itself, not from Kali, and recorded (CASE-001). Limited to those selected scenarios | [CASE-003](../investigations/CASE-003.md), [CASE-001](../investigations/CASE-001.md) |
| FR-02 | Linux endpoint security telemetry shall be collected through the enrolled Wazuh Agent `002` and forwarded to the manager | Must | Implemented | Agent `002` is the active endpoint; Linux01 FIM and SSH authentication events appear as alerts on the manager. Kali's own logs are not forwarded | [03-architecture.md](03-architecture.md), [CASE-003](../investigations/CASE-003.md) |
| FR-03 | Wazuh FIM shall monitor `/home` on SENTINEL-LINUX01 | Must | Partially Implemented | FIM is configured and has produced events in controlled tests. Complete monitoring of every relevant file change is **not** established, and FIM noise has not been fully eliminated | [05-detection-engineering.md](05-detection-engineering.md), [CASE-001](../investigations/CASE-001.md) |
| FR-04 | Custom Rules `100002` (modification), `100003` (creation), and `100004` (deletion) shall detect the corresponding file lifecycle events within the FIM scope | Must | Partially Implemented | Each rule has been observed matching in controlled probes on selected files. Committed v0.11 evidence (pending reconciliation) contains three Level 8 records for one controlled creation/modification/deletion lifecycle on `/home/sentinel-admin/v011_fim_probe.txt`, matching Rules `100003`, `100002`, and `100004`. These are limited controlled tests, not a repeatable regression suite or comprehensive FIM coverage. The on-disk rule XML does not establish which configuration the manager had loaded during historical events | [05-detection-engineering.md](05-detection-engineering.md), [v0.6 measurement](../metrics/v0.6-purple-team-measurement.md), [v011_fim_alerts.json](../evidence/v0.11/v011_fim_alerts.json), [October 26 alerts screenshot](../evidence/v0.2/screenschots/v0.2-oct26-controlled-modification-source-alerts-new.png) |
| FR-05 | Rule `100200` shall produce an alert for matching SSH authentication events on SENTINEL-LINUX01 | Must | Partially Implemented | In the CASE-003 controlled simulation, 21 failed SSH authentication attempts over 2 minutes 46 seconds produced 21 Rule `100200` Level 5 alerts. This is a single controlled test and is not comprehensive SSH detection coverage. Behavior on legitimate authentication activity is untested | [CASE-003](../investigations/CASE-003.md), [05-detection-engineering.md](05-detection-engineering.md) |
| FR-06 | Rule `100201` shall escalate when matching Rule `100200` events from the same source IP occur within its configured frequency window | Must | Partially Implemented | In CASE-003, one Rule `100201` Level 10 escalation was produced; manual investigation found zero successful logins. The rule counts matching `100200` events from the same source IP within its window; it is not specified as counting unique failed-password attempts. Threshold behavior is covered only by the selected observations in CASE-003 and CASE-004 | [CASE-003](../investigations/CASE-003.md), [CASE-004](../investigations/CASE-004.md) |
| FR-07 | The lab shall support offline replay of recorded Windows Sysmon EVTX telemetry (EVTX converted to NDJSON by Python, ingested by logcollector through Linux01) into Wazuh detection | Must | Implemented | Selected recorded EVTX data has been converted, ingested, and evaluated by Wazuh rules. Replay of selected recordings only; not live Windows monitoring | [CASE-002](../investigations/CASE-002.md) |
| FR-08 | The lab shall support offline replay of Sysmon JSON telemetry through manager-side Wazuh logcollector | Should | Implemented | Selected JSON replay data has been ingested and evaluated. Replay only; not live Windows monitoring | [05-detection-engineering.md](05-detection-engineering.md), [CHANGELOG.md](../CHANGELOG.md) |
| FR-09 | Custom Sysmon-based rules shall detect selected replayed Windows behaviors | Must | Partially Implemented | The v0.6 report (Section 3) states that seven committed alert records represent seven custom rule IDs, but these are not a complete, independently reproducible 7/7 coverage measurement: the reported 12-event input was not committed. The report also records 0/3 benign events alerting and two uncovered Event ID 7 ImageLoad events; these observations are operator-recorded and cannot be reconstructed from the seven committed alert records. CASE-004 documents a bypassing mutation (#24) that produced no custom alert. Small controlled samples; not a measure of live Windows detection | [v0.6 measurement](../metrics/v0.6-purple-team-measurement.md), [CASE-004](../investigations/CASE-004.md) |
| FR-10 | FIM alert noise from benign desktop/configuration activity shall be reduced without suppressing relevant events | Should | Partially Implemented | FIM exclusions and rule group isolation were applied (v0.8) and residual noise remains. The v0.11 evidence includes seven desktop/configuration-path records whose origin and benign status are **not** conclusively established; the evidence does not show that exclusions succeeded or failed. Acceptance requires reconciled evidence and broader retesting, both outstanding | [05-detection-engineering.md](05-detection-engineering.md), [v011_fim_alerts.json](../evidence/v0.11/v011_fim_alerts.json) |
| FR-11 | Alerts shall be investigated and documented in case files with timelines and evidence, limited to each case's stated scope | Must | Implemented | CASE-001 to CASE-004 exist with defined scopes. CASE-001 was closed on 18 November 2026 for its defined reviewed scope; remaining FIM engineering and noise tuning do not reopen it | [CASE-001](../investigations/CASE-001.md), [CASE-002](../investigations/CASE-002.md), [CASE-003](../investigations/CASE-003.md), [CASE-004](../investigations/CASE-004.md), [06-incident-response.md](06-incident-response.md) |
| FR-12 | The lab shall record controlled measurements of selected detections | Should | Partially Implemented | v0.6 records selected FIM, Sysmon replay, and SSH measurements. Samples are small and controlled; they are not statistically meaningful detection or false-positive rates. Response time has not been measured | [v0.6 measurement](../metrics/v0.6-purple-team-measurement.md), [07-testing-and-metrics.md](07-testing-and-metrics.md) |
| FR-13 | The lab shall test selected detections against modified (mutated) attacker behavior and record gaps as findings | Should | Partially Implemented | CASE-004 documents selected mutation, evasion, FIM, and SSH threshold testing, including a recorded detection gap. Coverage is limited to those scenarios | [CASE-004](../investigations/CASE-004.md) |
| FR-14 | The separate Python SOC Automation Engine shall parse exported Wazuh alert JSON and support severity-based triage | Should | Partially Implemented | Used on Sysmon replay alerts and Linux FIM alerts, and on SSH alerts in CASE-003, as file-based processing. Not a live Wazuh integration and takes no response action. In the v0.11 triage report, process, target-process, and event-time enrichment fields are `None`. The tool's own test suite is not SENTINEL detection validation | [CASE-003](../investigations/CASE-003.md), [triage_report.md](../evidence/v0.11/triage_report.md) |
| FR-15 | A repeatable regression test shall confirm that detection rules, including FIM exclusions, still behave as intended after changes | Should | Planned | Acceptance requires defined pass/fail criteria, a repeatable procedure, and reconciled results. The v0.11 aggregate `regression_summary.json` does not establish a completed regression suite, its full test criteria, or successful exclusion validation | [regression_summary.json](../evidence/v0.11/regression_summary.json), [07-testing-and-metrics.md](07-testing-and-metrics.md) |

---

## 5. Non-Functional Requirements

| ID | Requirement | Priority | Status | Verification / Acceptance Criteria | Evidence / Reference |
|---|---|---|---|---|---|
| NFR-01 | Attack-simulation and telemetry traffic shall remain on the isolated `10.10.10.0/24` network, separate from external networks | Must | Implemented | VirtualBox network configuration reviewed; baseline checks covered isolated networking. The manager's separate NAT interface (updates and packages only) is not part of the attack or telemetry paths. Verified by configuration review, not by traffic capture | [03-architecture.md](03-architecture.md), [01-project-overview.md](01-project-overview.md) |
| NFR-02 | Evidence shall be traceable to its source and preserved, with the evidence level of each result stated | Must | Partially Implemented | Evidence is stored per milestone. Gaps: the original source record for the 11 October result was not recovered, the v0.10 archive is external to the repository, and v0.11 evidence is committed but pending reconciliation. A milestone folder does not imply a complete evidence set | [06-incident-response.md](06-incident-response.md), [01-project-overview.md](01-project-overview.md) |
| NFR-03 | Documentation shall distinguish observed behavior, validated behavior, and untested assumptions | Must | Partially Implemented | Reviewed documents state evidence levels and unresolved questions explicitly. Applied through ongoing review, not enforced by tooling | [06-incident-response.md](06-incident-response.md), [08-lessons-and-failures.md](08-lessons-and-failures.md) |
| NFR-04 | Documentation shall distinguish current implementation from planned work, and shall not claim detection coverage, regression coverage, or production readiness that is not demonstrated | Must | Partially Implemented | Reviewers can check that every capability statement has matching evidence and that future work is labelled not implemented. Corrections to earlier overstated claims (for example v0.11 verification) are applied through documentation review | [01-project-overview.md](01-project-overview.md), [CHANGELOG.md](../CHANGELOG.md) |
| NFR-05 | Reported measurements shall state their sample size and limits | Must | Partially Implemented | v0.6 results are labelled small controlled samples and not enterprise detection or false-positive rates. Applies to any future measurement report | [v0.6 measurement](../metrics/v0.6-purple-team-measurement.md), [07-testing-and-metrics.md](07-testing-and-metrics.md) |
| NFR-06 | Tests shall be reproducible where source artifacts and procedures are available | Should | Partially Implemented | Replay inputs and several evidence artifacts are available; some historical records are not recoverable and the historical loaded Wazuh configuration may not be reconstructable. Reproducibility is therefore not claimed for all results | [05-detection-engineering.md](05-detection-engineering.md), [06-incident-response.md](06-incident-response.md) |

---

## 6. Operational and Security Requirements

| ID | Requirement | Priority | Status | Verification / Acceptance Criteria | Evidence / Reference |
|---|---|---|---|---|---|
| OR-01 | Controlled simulations shall be run only within the lab boundary | Must | Implemented | Case records show simulations originating from SENTINEL-KALI against SENTINEL-LINUX01 on the isolated network. Procedural control; verified by case review | [CASE-003](../investigations/CASE-003.md), [03-architecture.md](03-architecture.md) |
| OR-02 | Response procedures shall be human-in-the-loop; a person shall decide before any destructive or disruptive action | Must | Implemented | Documented decision and escalation path requires human review; no automated response exists | [06-incident-response.md](06-incident-response.md) |
| OR-03 | The lab shall not implement or claim automated containment, eradication, or recovery | Must | Implemented | Review confirms no automated response component exists. The Python project performs triage only and takes no response action | [06-incident-response.md](06-incident-response.md), [01-project-overview.md](01-project-overview.md) |
| OR-04 | Repository documentation and evidence shall not expose credentials, secrets, or sensitive raw telemetry | Must | Partially Implemented | Intended and applied when committing evidence; no systematic audit is documented. Acceptance requires a recorded review of committed evidence | [01-project-overview.md](01-project-overview.md), [06-incident-response.md](06-incident-response.md) |
| OR-05 | A manual, source-scoped containment procedure shall be documented for the SSH scenario | Should | Partially Implemented | The procedure is documented for CASE-003. It is a documented procedure only; it has not been exercised as a containment exercise, and its application is not claimed | [CASE-003](../investigations/CASE-003.md), [06-incident-response.md](06-incident-response.md) |
| OR-06 | A controlled containment exercise shall be performed and recorded | Should | Planned | Acceptance: a recorded exercise with scope, human approval, outcome, and evidence | [06-incident-response.md](06-incident-response.md) |
| OR-07 | Eradication and recovery shall be exercised, including confirming detection and telemetry still work afterwards | Should | Planned | Acceptance: recorded exercises covering eradication and recovery. Verifying that the SSH service is running is not treated as a recovery exercise | [06-incident-response.md](06-incident-response.md) |
| OR-08 | Response metrics (for example time to detect, triage, and contain) shall be measured | Could | Planned | Acceptance: measured values with method and sample size. None has been measured | [07-testing-and-metrics.md](07-testing-and-metrics.md) |
| OR-09 | The manager's currently active rule configuration shall be verified, and the historical loaded configuration reconstructed where evidence permits | Should | Planned | Acceptance: recorded comparison of the running configuration with on-disk rules. The historical state may not be recoverable and would then remain unconfirmed | [05-detection-engineering.md](05-detection-engineering.md), [06-incident-response.md](06-incident-response.md) |
| OR-10 | Any future response automation shall require human approval before destructive or disruptive steps | Could | Not Implemented | Applies only if automation is introduced. None exists | [06-incident-response.md](06-incident-response.md) |

---

## 7. Verification and Acceptance Criteria

### 7.1 Verification methods

| Method | Use |
|---|---|
| Controlled test | A defined activity is run in the lab and the expected alert is observed |
| Replay test | Recorded EVTX or JSON telemetry is ingested and evaluated; this is not live endpoint verification |
| Evidence inspection | A committed or reviewed artifact is examined against the claim |
| Configuration review | Lab or rule configuration is inspected. On-disk configuration does not by itself show what the running manager had loaded at a past time |
| Documentation review | Statements are checked against evidence and against the limitations in this document |

### 7.2 Status rules

- **Implemented:** the capability exists and evidence shows it working for the scope stated in the requirement. If evidence covers only selected scenarios, the requirement is worded for those scenarios.
- **Partially Implemented:** some of the requirement is met, or it has been tested only in limited controlled scenarios; the gap is stated in the acceptance criteria.
- **Planned:** intended future work with nothing yet exercised.
- **Not Implemented:** the capability does not exist.

A configuration file, a screenshot, or a documented procedure alone does not make a requirement Implemented where stronger evidence is needed.

### 7.3 Evidence caveats

- v0.11 artifacts are committed evidence pending reconciliation. They do not constitute an official changelog release, a verified regression suite, or confirmation that FIM exclusions passed or failed.
- CASE-001 is closed for its defined reviewed scope; follow-up work does not reopen it.
- v0.6 figures are small controlled samples.

---

## 8. Requirements Status Summary

| Status | Count | IDs |
|---|---|---|
| Implemented | 9 | FR-01, FR-02, FR-07, FR-08, FR-11, NFR-01, OR-01, OR-02, OR-03 |
| Partially Implemented | 16 | FR-03, FR-04, FR-05, FR-06, FR-09, FR-10, FR-12, FR-13, FR-14, NFR-02, NFR-03, NFR-04, NFR-05, NFR-06, OR-04, OR-05 |
| Planned | 5 | FR-15, OR-06, OR-07, OR-08, OR-09 |
| Not Implemented | 1 | OR-10 |

These counts describe the status of the requirements in this document, not detection coverage or performance.

---

## 9. Out of Scope / Deferred Requirements

These are not current requirements and are not claimed as capability.

| ID | Deferred item | Status | Note |
|---|---|---|---|
| DR-01 | Live Windows endpoint monitoring | Not Implemented | Windows detection is replay-only |
| DR-02 | Active Directory environment | Not Implemented | None deployed |
| DR-03 | SOAR-style automated response; automated containment, eradication, or recovery | Not Implemented | Not part of the lab; Python triage is advisory only |
| DR-04 | Production deployment and production-grade guarantees | Not Implemented | The lab is educational and isolated |
| DR-05 | Comprehensive detection coverage and statistically meaningful detection or false-positive rates | Not Implemented | Current measurements are small controlled samples |
| DR-06 | Additional mutation scenarios and coverage of the uncovered Event ID 7 cases | Planned | Future work, not committed |
| DR-07 | Deeper DFIR workflows | Planned | Future work, not committed |

---

## 10. Related Documentation

| Document | Role |
|---|---|
| [01-project-overview.md](01-project-overview.md) | Project concept and narrative |
| [03-architecture.md](03-architecture.md) | Environment and component architecture |
| [05-detection-engineering.md](05-detection-engineering.md) | Detection methodology and rule status |
| [06-incident-response.md](06-incident-response.md) | Investigation and response methodology and status |
| [07-testing-and-metrics.md](07-testing-and-metrics.md) | Testing approach and measurement |
| [08-lessons-and-failures.md](08-lessons-and-failures.md) | Failures and lessons |
| [CASE-001](../investigations/CASE-001.md) | FIM investigation, closed 18 November 2026 for its defined scope |
| [CASE-002](../investigations/CASE-002.md) | Sysmon EVTX replay validation |
| [CASE-003](../investigations/CASE-003.md) | Controlled SSH testing, investigation, and Python-assisted triage |
| [CASE-004](../investigations/CASE-004.md) | Selected mutation, evasion, FIM, and SSH threshold testing |
| [v0.6 purple-team measurement](../metrics/v0.6-purple-team-measurement.md) | Small-sample controlled measurements |
| [`evidence/v0.11/`](../evidence/v0.11/) | Committed v0.11 evidence, pending reconciliation |
| [CHANGELOG.md](../CHANGELOG.md) | Official release history |
