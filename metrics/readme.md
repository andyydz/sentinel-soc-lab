# metrics/

This directory stores the measured results produced by SENTINEL's security testing — the evidence that defensive controls actually work, rather than merely exist.

This README explains how measurement is organized in this directory. It does not restate SENTINEL's broader testing and validation methodology (`docs/07-testing-and-matrices.md`) — see that document for the full methodology this directory's records are built from.

## Purpose

SENTINEL does not consider a security control successful simply because a tool is installed, a detection rule exists, an alert appears in a screenshot, or a test was run once. The purpose of `metrics/` is to record the actual, evidence-backed answers to questions such as:

- Did the detection trigger?
- How quickly was the activity detected?
- How much relevant telemetry was available?
- Was the alert actionable?
- Was the event investigated successfully?
- How quickly was incident response initiated?
- Did the response achieve its intended result?
- Did the detection produce false positives?
- Were any controlled attacks missed?
- Did a detection improve after tuning?
- Did the detection survive a change in attacker behavior?
- Did a previously working detection regress?

Every metric stored here should be traceable to a specific test, investigation, alert, or other reproducible piece of evidence.

## Metrics philosophy

- **Measure, don't assume** — a control isn't considered effective just because it exists.
- **Evidence first** — every metric traces back to a test, investigation, alert, or other reproducible source.
- **Repeatability** — where practical, tests are repeatable so results can be compared over time.
- **Before / after** — when a detection or control is improved, performance is compared before and after the change.
- **Context matters** — a metric is always interpreted alongside the scenario, technique, environment, and telemetry available, not read in isolation.
- **Honest results** — failed tests and poor results are preserved, not discarded or adjusted to make SENTINEL look better.

## Metric categories

- **Detection metrics** — detection status, detection rate, detection latency, number of successful/missed detections, detection coverage, alert quality.
- **False-positive metrics** — false-positive count/rate, which benign events triggered a detection, tuning changes made, and post-tuning results.
- **False-negative / missed-detection metrics** — controlled attacks executed, expected detections, missed detections, miss rate, detection gaps, corrective action, and retest result.
- **Investigation metrics** — time to triage, time to investigate, investigation completion status, evidence completeness, timeline reconstruction success, IOC identification, root-cause determination. Used only once the investigation methodology actually supports them.
- **Response metrics** — time to response, time to containment, response success, recovery status, response failures, manual intervention required. Automated-response metrics are not used unless automated response is actually implemented.
- **Coverage metrics** — attack scenario coverage, detection coverage, telemetry coverage, MITRE ATT&CK technique coverage, investigation coverage, response coverage — always based on clearly defined test cases.
- **Regression metrics** — whether a change (e.g. a detection improvement) caused a previously passing test to fail: previous result, what changed, rerun result, regression detected or not.
- **Detection resilience metrics (future)** — for Attack Mutation testing: whether the original attack was detected, whether the modified attack was detected, whether detection behavior changed, and an overall resilience measure. **Not currently applicable — Attack Mutation is not yet implemented.**
- **Purple-team metrics (future)** — attack executions, successful/missed detections, detection latency, response latency, false positives, detection improvements, retest results. **Not currently applicable — purple-team validation has not yet begun.**

## Core metric definitions

These are the metrics SENTINEL intends to use once real test data exists. None of them currently have a measured value.

**Detection Rate**
```
Detection Rate = Successful Detections / Total Expected Detection Opportunities × 100
```
The denominator (total expected detection opportunities) must be clearly defined per test set before this is calculated.

**Miss Rate**
```
Miss Rate = Missed Detections / Total Expected Detection Opportunities × 100
```

**False-Positive Rate**
Calculated only once the test population and the definition of a "false positive" for that population are clearly established — never against an arbitrary or undefined denominator.

**Detection Time**
The interval between relevant activity occurring and detection becoming available to the SOC. This should distinguish attack/event time, telemetry ingestion time, alert creation time, and analyst awareness time as separate points, not a single blended number.

**Response Time**
The interval between a confirmed/accepted incident and the corresponding response action, with explicit start and end points defined per test.

**Time to Investigation**
The interval from detection/triage start to investigation conclusion, where the investigation methodology supports measuring it.

**Time to Containment** *(future)*
Used once controlled response workflows exist to measure. Not currently measured.

## Metric record format

Each measured result is stored as an individual record using the following structure. Fields are filled in only with real, verified values — an unmeasured field is marked as such rather than omitted or guessed.

```markdown
# Metric Record

## Test ID
e.g. TEST-001 (do not invent test IDs; assign only when a real test occurs)

## Scenario
Description of the controlled scenario.

## Version
e.g. v0.2

## Date
Only an actual date. Never invented.

## Environment
Affected systems, e.g. SENTINEL-KALI, SENTINEL-LINUX01, SENTINEL-WAZUH.

## Technique / Behavior
The behavior under test.

## MITRE ATT&CK
Only included when technically validated.

## Expected Result
What should happen.

## Actual Result
What actually happened.

## Metric
Name of the measurement.

## Value
The actual measured value.

## Unit
seconds | minutes | count | percentage

## Evidence
Link to supporting evidence (repository-relative where appropriate).

## Test Result
Pass | Fail | Partial | Not Measured

## Notes
Important context or limitations.
```

## Master test metrics table (future)

Future versions of this directory may maintain a master table summarizing completed tests:

| Test ID | Scenario | Technique | Expected | Result | Detection Time | Response Time | Evidence |
|---|---|---|---|---|---|---|---|

This table is only populated with real, completed tests as they occur. It does not currently contain any rows.

## Before / after measurement

When a detection or control is changed to fix a gap, tune a false positive, or respond to a missed detection, SENTINEL records performance both before and after the change using matching metric records (same scenario, same technique, comparable test conditions where possible). This lets a change be judged by its actual effect on measured performance rather than by assumption. Before/after comparisons are only produced once an initial "before" measurement and a corresponding "after" retest both exist as real records.

## Relationship to other SENTINEL documentation

- **`metrics/README.md`** (this file) — directory-level guide for how measurement is organized and recorded.
- **`docs/07-testing-and-matrices.md`** — the full testing and validation methodology this directory implements.
- **`docs/05-detection-engineering.md`** — how detections are designed, which metrics here help validate.
- **`docs/06-incident-response.md`** — the response methodology that response metrics measure against.
- **`investigations/`** — case records that investigation metrics are drawn from.
- **`failure-log/`** — failures (including detection misses and regressions) that may also appear here as measured results.
- **`evidence/`** — the underlying supporting evidence that metric records link to.
- **`CHANGELOG.md`** — project-level milestones and architecture changes.

## Current status

SENTINEL is currently in **v0.1 Foundation**. Verified current capabilities include the Wazuh deployment and dashboard, the Kali attacker VM, the Linux monitored endpoint with an active Wazuh agent, the initial telemetry pipeline, the isolated lab network, and initial infrastructure evidence.

The project has **not** yet completed a detection, investigation, or response cycle, so this directory does not currently contain — and this README does not claim — any of the following:

- a measured detection rate
- measured MTTA or MTTR
- a false-positive or false-negative rate
- an attack coverage percentage
- response-time statistics
- a detection resilience or mutation percentage
- any other performance result

These values will be produced from real, controlled tests beginning in v0.2 Detection Engineering and later phases, and recorded here as they occur.
