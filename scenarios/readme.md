# scenarios/

This directory defines SENTINEL's controlled security-testing scenarios — the bridge between adversary simulation and SOC validation.

This README explains how scenarios are designed, organized, executed, and retested. It does not restate SENTINEL's detection-engineering methodology ([`docs/05-detection-engineering.md`](../docs/05-detection-engineering.md)), incident-response methodology ([`docs/06-incident-response.md`](../docs/06-incident-response.md)), or broader testing methodology ([`docs/07-testing-and-metrics.md`](../docs/07-testing-and-metrics.md)) — see those documents for that detail.

## Purpose

A scenario is more than "run an attack." It is a controlled experiment intended to validate whether SENTINEL's defensive capabilities actually work, eventually connecting:

```
ATTACK / EVENT → TELEMETRY → DETECTION → INVESTIGATION →
RESPONSE → MEASUREMENT → IMPROVEMENT → RETEST
```

A scenario definition should specify what is being tested, why, which system is affected, what behavior and telemetry are expected, what detection should occur, what investigation and response should be possible, what should be measured, what evidence should be collected, what happens if detection fails, and how the scenario will be retested.

## Scenario design principles

1. **Controlled** — every scenario runs inside the authorized SENTINEL environment.
2. **Reproducible** — another execution should be possible under the same defined conditions.
3. **Observable** — the activity should generate useful telemetry where detection is expected.
4. **Measurable** — the scenario has defined success criteria.
5. **Evidence-based** — results are supported by evidence, not assertion.
6. **Safe** — the scenario must not intentionally affect systems outside the lab.
7. **Failure-aware** — a missed detection is a valid, documentable result, not a reason to hide the scenario.
8. **Retestable** — after a detection or configuration change, the scenario can be run again.
9. **Minimal scope** — only the systems necessary for the scenario are involved.
10. **No assumptions** — a detection is not assumed to work before it is actually tested.

## Scenario lifecycle

```
DESIGN
  |
SCOPE
  |
PRE-CHECK
  |
EXECUTE
  |
OBSERVE
  |
DETECT
  |
INVESTIGATE
  |
RESPOND
  |
MEASURE
  |
DOCUMENT
  |
IMPROVE
  |
RETEST
```

Not every scenario uses every phase immediately. Early scenarios (v0.2) are expected to focus mainly on EXECUTE → OBSERVE → DETECT → MEASURE; later phases extend into INVESTIGATE → RESPOND → MEASURE → IMPROVE → RETEST as those capabilities mature. The existing test records described under Current status do not imply that every lifecycle phase was completed for every test.

## Scenario identifiers

Scenarios use the naming convention `SCN-001`, `SCN-002`, `SCN-003`, etc.

- IDs are unique and never reused.
- Once assigned, an ID remains stable.
- Related tests, detections, investigations, evidence, and metrics reference the scenario ID.

IDs below (SCN-001 through SCN-004) are reserved concept names for scenario families — they are not yet implemented scenario files, and no fictional scenario directories are created until the corresponding scenario is actually designed. SCN IDs are not assigned retroactively to the existing investigation cases (CASE-001 through CASE-004), and those cases are not renamed as scenario records.

## Scenario record structure

Each scenario is defined using the following structure. Fields describe intent and expectation; nothing here is evidence of an actual result until an execution record confirms it.

```markdown
# Scenario ID — Scenario Name

## Status
Planned | Draft | Ready | Executed | Validated | Failed | Retest Required | Retired
(Never mark Executed or Validated until the scenario has actually been run.)

## Objective
What security capability is being tested.

## Scenario Summary
Short description of the controlled activity.

## Scope
Attacker, target, monitoring system, network, and any other required systems.

## Preconditions
What must be configured before execution (e.g. Wazuh agent active, required telemetry available, detection rule enabled, test account available, connectivity verified). Include only what is actually necessary.

## Expected Behavior
What activity should occur.

## Expected Telemetry
What telemetry should be observable. Not guaranteed until validated.

## Expected Detection
What detection should trigger. Not a claim that the detection already works.

## Investigation Objective
What a SOC analyst should be able to determine.

## Response Objective
What response should be possible, if applicable.

## Success Criteria
Objective pass/fail criteria (e.g. expected telemetry observed, detection triggered, evidence available, investigation possible, response completed, metrics recorded).

## Evidence Requirements
What evidence should be collected (Wazuh alert, screenshot, logs, test output, timeline, detection result).

## Metrics
Relevant measurements to record (detection success, detection time, false positive, missed detection, investigation time, response time).

## Failure Handling
STOP → CAPTURE → DOCUMENT → INVESTIGATE → FIX → RETEST

## Retest
Whether the scenario was rerun after changes, and the result.
```

## Scenario status model

```
PLANNED → DRAFT → READY → EXECUTED → VALIDATED
```

with possible branches:

- EXECUTED → FAILED
- EXECUTED → RETEST REQUIRED
- VALIDATED → REGRESSION
- VALIDATED → RETIRED

"Executed" does not mean "successful" — a scenario can be executed and still fail its success criteria.

## Scenario categories

Broad categories a scenario may fall into, not all of which are currently implemented:

- **Authentication** — controlled authentication-related behavior.
- **Network Reconnaissance** — controlled reconnaissance inside SENTINEL-LAB.
- **Endpoint Execution** — controlled execution behavior on the monitored endpoint.
- **Persistence** *(future)* — controlled persistence scenarios.
- **Privilege / Access** *(future)* — controlled privilege-related scenarios.
- **Discovery** — controlled discovery behavior.
- **File / System Activity** — controlled file or system modifications that generate telemetry.
- **Command and Control** *(future)* — controlled C2 simulation, where appropriate.
- **Response Validation** — scenarios designed to validate response actions.
- **Detection Resilience** *(future)* — scenarios that deliberately vary attacker behavior to test detection resilience.
- **Regression** — scenarios rerun after a detection or configuration change.

## Initial scenario prioritization

Early scenarios are chosen for safe execution, clear telemetry, a clear expected detection, reproducibility, relevance to SOC work, investigability of the resulting alert, measurability, and the ability to improve and retest — not for how technically impressive they look. The goal of the first scenarios is to establish a reliable testing methodology.

## Four core scenario families

These four families define the direction of formal scenario development. **No formal SCN-ID-based scenario file or execution record exists for any of them yet.** Related controlled testing has already occurred and is documented in the investigation and measurement records, as noted for each family. Those records are not SCN records.

### SCN-001 — Authentication Abuse
**Purpose:** test whether controlled authentication abuse against the lab endpoint generates expected telemetry and can be detected.
Potential flow: controlled authentication activity → Linux telemetry → Wazuh → detection → investigation → measurement.
Key questions: was the activity logged, did Wazuh receive the relevant telemetry, did the expected detection trigger, was the alert actionable, could the source and affected account be identified, how quickly was it detected, did false positives occur.
**Related existing testing:** authentication abuse has been tested through [CASE-003](../investigations/CASE-003.md): 21 controlled failed SSH attempts from SENTINEL-KALI against SENTINEL-LINUX01, exercising Rules `100200` and `100201`, with Python triage and documented manual, source-scoped containment procedures. CASE-003 was not assigned SCN-001, and no formal SCN-001 scenario file or execution record exists. CASE-003 documents manual procedures, not automated containment or production SOAR.

### SCN-002 — Network Reconnaissance
**Purpose:** test whether controlled reconnaissance within SENTINEL-LAB produces observable network behavior with available telemetry/detection.
Potential flow: controlled reconnaissance → network activity → available telemetry → detection → investigation → measurement.
Key questions: was the activity observable, which telemetry source captured it, was detection available, could the source be identified, could the activity be reconstructed, what detection gaps exist. Strictly confined to SENTINEL-LAB.
**Status:** planned future work. It has not been executed.

### SCN-003 — Endpoint Execution / Suspicious Process Activity
**Purpose:** test whether controlled suspicious execution behavior on SENTINEL-LINUX01 produces useful endpoint telemetry the SOC can identify and investigate.
Potential flow: controlled execution → process/system telemetry → Wazuh → detection → investigation → measurement.
Key questions: was the process activity recorded, was parent/child context available (if supported), did detection trigger, could the analyst reconstruct the activity, what evidence was available.
**Related existing testing:** related process-detection testing exists in [CASE-002](../investigations/CASE-002.md), through replayed Windows Sysmon telemetry, and in [CASE-004](../investigations/CASE-004.md), through `wazuh-logtest` mutation testing. CASE-002 did not use a live Windows endpoint or exercise the Sysmon kernel driver, and no live Windows process telemetry is claimed. No formal SCN-003 scenario file exists; the formal scenario concept remains future work.

### SCN-004 — Detection Resilience / Attack Variation
**Purpose:** test whether a validated detection continues to work when attacker behavior changes while preserving the same objective.
Concept: original behavior → detection result, compared against modified behavior → detection result, across telemetry, detection, investigation, detection time, detection failure, and coverage. If the modified behavior bypasses detection: FAILURE → ANALYZE → IMPROVE → RETEST.
**Related existing testing:** mutation and evasion testing has already been conducted under [CASE-004](../investigations/CASE-004.md) / v0.7. Examples include the `comsvcs.dll, #24` variation bypassing keyword-specific Rule `100112` and matching Level 0 base Rule `100101`, hidden-file FIM testing, and SSH sub-threshold testing. This is bounded testing, not comprehensive detection-resilience coverage. No formal SCN-004 scenario file exists, and broader mutation coverage and repeatable detection-resilience testing remain future work. A broader, repeatable Attack DNA / Attack Mutation framework is not established.

## Scenario safety

- Target only SENTINEL systems, using only authorized lab accounts.
- Never use real or production credentials or secrets.
- Never target public systems, the host operating system, unrelated VMs, or external networks.
- Never commit sensitive evidence.
- Stop immediately if activity leaves the intended scope.

NAT access exists for legitimate updates only and does not authorize external testing. The presence of SENTINEL-KALI inside the lab does not authorize attacking anything outside SENTINEL-LAB.

## Scenario pre-check

Before executing any scenario, verify:

- **Infrastructure** — required VMs running, interfaces connected, IPs correct, lab connectivity working.
- **Monitoring** — Wazuh operational, required endpoint agent active, expected telemetry source available.
- **Detection** — expected detection enabled if the scenario requires one, configuration documented.
- **Evidence** — evidence location known, sensitive information will not be captured unnecessarily.
- **Safety** — target is inside SENTINEL-LAB, no unrelated systems are in scope.

Do not execute a scenario if the safety boundary is unclear.

## Scenario execution records

Each execution records, where applicable: scenario ID, date/time, version, attacker system, target system, expected behavior, actual behavior, telemetry observed, detection result, investigation result, response result, evidence references, failures, metrics, and retest requirement. None of these values are invented — an execution record only reports what actually happened.

Executed tests to date are recorded in the investigation cases [CASE-001](../investigations/CASE-001.md), [CASE-002](../investigations/CASE-002.md), [CASE-003](../investigations/CASE-003.md) and [CASE-004](../investigations/CASE-004.md), the [v0.6 measurement report](../metrics/v0.6-purple-team-measurement.md), and the relevant evidence documents. These records document actual testing, findings and limitations, but they are not formal scenario execution records. Formal execution records keyed to `SCN-001` and so on have not yet been established. A future SCN execution record should distinguish expected behavior from actual behavior and link to the relevant case or evidence where applicable, without duplicating entire investigation reports.

## Scenario results

- **PASS** — expected behavior occurred and defined success criteria were satisfied.
- **FAIL** — a defined success criterion was not satisfied.
- **PARTIAL** — some objectives satisfied, others not.
- **BLOCKED** — the scenario could not be executed because a prerequisite was unavailable.
- **INCONCLUSIVE** — available evidence was insufficient to determine the result.
- **RETEST REQUIRED** — the scenario needs another execution after an improvement or configuration change.

Not every scenario is expected to result in PASS.

## Scenario design vs. scenario execution

A scenario document defines *what should happen*. An execution record documents *what actually happened*. These are never the same statement — "Detection should trigger" (expected) is distinct from "Detection triggered" (actual), and planned behavior is never treated as evidence.

## Scenario versioning

Scenario definitions may evolve. When a scenario changes significantly: preserve the scenario ID where appropriate, document the change, update related detection/test documentation, retest the scenario, and record the change in [`CHANGELOG.md`](../CHANGELOG.md) if it affects project architecture or a milestone. Scenario objectives are not silently changed after seeing results.

## Downstream connections

- **Scenario → Detection**: scenario → expected telemetry → detection hypothesis → detection implementation → controlled execution → alert → validation → measurement.
- **Scenario → Investigation**: scenario → alert → triage → evidence → timeline → IOC extraction → technique mapping → root cause → conclusion, feeding [`investigations/`](../investigations/).
- **Scenario → Response**: detection → investigation → response decision → controlled containment → validation → measurement (future work; no automated response exists, and destructive response instructions are not documented here).
- **Scenario → Metrics**: every meaningful scenario is expected to eventually connect to detection success, detection time, missed detection, false positive, investigation time, response time, coverage, regression, or mutation-resilience metrics in [`metrics/`](../metrics/) — generated only from actual test results.
- **Scenario → Failure Log**: a failed scenario follows STOP → CAPTURE → DOCUMENT → INVESTIGATE → FIX → RETEST and links to the corresponding record in [`failure-log/`](../failure-log/) (e.g. a scenario failure, detection miss, or regression) using a real `FAIL-*` ID, never a fictional one.
- **Scenario → Evidence**: relevant evidence is stored under the matching version directory in [`evidence/`](../evidence/) (e.g. `evidence/v0.2/`), and never includes passwords, API keys, tokens, private keys, real credentials, personal information, production data, VM disks, or unnecessary sensitive telemetry.
- **Scenario → MITRE ATT&CK**: scenarios may be mapped to ATT&CK techniques where the mapping is technically justified and verified — mapping behavior, not tool names, and never added merely for presentation. A scenario may legitimately have no ATT&CK mapping.

## Relationship to other SENTINEL documentation

- **`scenarios/readme.md`** (this file) — how controlled scenarios are designed and organized.
- **[`docs/05-detection-engineering.md`](../docs/05-detection-engineering.md)** — how detections are engineered and validated.
- **[`docs/06-incident-response.md`](../docs/06-incident-response.md)** — response methodology.
- **[`docs/07-testing-and-metrics.md`](../docs/07-testing-and-metrics.md)** — the broader testing methodology.
- **[`docs/08-lessons-and-failures.md`](../docs/08-lessons-and-failures.md)** — failure-driven engineering approach.
- **[`detections/`](../detections/)** — actual detection implementations.
- **[`investigations/`](../investigations/)** — investigation records.
- **[`metrics/`](../metrics/)** — measured results.
- **[`evidence/`](../evidence/)** — supporting evidence.
- **[`failure-log/`](../failure-log/)** — meaningful failure records.
- **[`CHANGELOG.md`](../CHANGELOG.md)** — major project-level milestones and architecture decisions.

## Portfolio value

The value of SENTINEL's scenarios is not "I ran an attack." It is: defining what to test, establishing expected telemetry and detection, executing the activity in a controlled environment, collecting evidence, investigating the result, measuring performance, documenting failures, improving the defense, and retesting it — a complete security-engineering feedback loop.

## Current status

Controlled security testing has occurred and is documented in the investigation, measurement and evidence records. These are existing test and investigation records, not necessarily formal scenario records with `SCN-*` identifiers. Formal SCN-ID-based scenario files and execution records have not yet been created.

**Existing testing and investigation history:**
- **v0.2** — initial controlled FIM detection testing: a controlled Linux FIM modification test using custom Rule `100002`.
- **v0.3** — SOC investigation and FIM evidence reconciliation: [CASE-001](../investigations/CASE-001.md), including controlled lifecycle validations.
- **v0.4** — Sysmon replay detection validation: [CASE-002](../investigations/CASE-002.md), Windows Sysmon `.evtx` replay and selected Wazuh detection-rule validation. This was replayed telemetry on Linux, not a live Windows endpoint.
- **v0.5** — SSH brute-force detection, triage and manual response documentation: [CASE-003](../investigations/CASE-003.md), a controlled SSH password-guessing simulation from Kali against Linux01, Python triage, and documented manual source-scoped containment procedures. This is not automated containment or production SOAR.
- **v0.6** — controlled purple-team measurement across FIM, Sysmon replay and SSH ([report](../metrics/v0.6-purple-team-measurement.md)). This is small controlled measurement, not statistically representative performance data.
- **v0.7** — attack mutation, evasion and benign-noise testing: [CASE-004](../investigations/CASE-004.md), across FIM, Sysmon rule logic and SSH. This is bounded testing, not comprehensive detection-resilience coverage.
- **v0.8 onward** — subsequent tuning, replay, triage and probe milestones:
  - v0.8: selected FIM tuning and a controlled live probe.
  - v0.9 and v0.9.1: manager-side JSON replay and Python triage integration/documentation (v0.9 [evidence index](../evidence/v0.9/readme.md)).
  - v0.10: live Linux FIM probe and Python triage validation; its evidence archive is external to this repository.
  - v0.11: committed FIM alert ([`v011_fim_alerts.json`](../evidence/v0.11/v011_fim_alerts.json)), triage ([`triage_report.md`](../evidence/v0.11/triage_report.md)) and regression-summary ([`regression_summary.json`](../evidence/v0.11/regression_summary.json)) artifacts, with milestone reconciliation still pending.

**Planned:** formal SCN-ID-based scenario definitions and execution records. No version numbers are assigned to them, and the scenario framework is not complete.

## Directory structure

Current:

```
scenarios/
└── readme.md
```

No scenario subdirectories exist yet. A structure such as:

```
scenarios/
├── readme.md
├── SCN-001/
├── SCN-002/
├── SCN-003/
└── SCN-004/
```

is the conceptual future shape of this directory, and individual scenario directories are created only once that specific scenario is actually designed and implemented — not in advance.
