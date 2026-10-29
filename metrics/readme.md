# metrics/

This directory is for **measured results** from SENTINEL's security testing: evidence that a detection or control works, not just that it exists.

**What is here today:** only this README. It defines how SENTINEL intends to measure and record results. **No metric records exist yet, the master results table is unpopulated, and no performance metric has been measured.** A metric definition below is not a measured result.

For the full testing methodology, see [`docs/07-testing-and-metrics.md`](../docs/07-testing-and-metrics.md).

## Where SENTINEL stands

| Area | Current status | Evidence |
|---|---|---|
| Foundation (v0.1) | Complete: Wazuh deployment, Kali attacker VM, Linux monitored endpoint with an active agent, isolated lab network | See `evidence/` |
| Controlled modification detection (v0.2) | **Validated** for the tested scenario: custom Rule `100002` generated a Level 8 alert | 11 Oct 2026 (`2026-10-11T20:25:14.746+0530`): `evidence/v0.3/v0.3-custom-rule-100002.png` and `evidence/v0.3/v0.3-custom-rule-100002-dashboard-json.png`. The original source alert log was not recovered during the 26 Oct review, so this rests on the screenshots. |
| Repeat modification | Two consecutive modifications of one file (`/home/sentinel-admin/sentinel-v02-mod-test.txt`) generated two Rule `100002` Level 8 alerts: `2026-10-26T21:38:27.910+0530` (0 → 23 bytes) and `2026-10-26T21:38:48.473+0530` (23 → 61 bytes). These are **not** two independent test cases or a regression suite. | `evidence/v0.2/v0.2-oct26-controlled-modification-source-alerts-new.png`, referenced from `evidence/v0.3/readme.md` as `../v0.2/v0.2-oct26-controlled-modification-source-alerts-new.png` |
| File creation, 16 Oct 2026 | Reviewed source record showed built-in Rule `554` ("File added to the system"), Level 5, at `2026-10-16T11:40:06.007+0530`. Custom Rule `100002` was **absent** from that record. | `evidence/v0.3/v0.3-oct16-creation-rule-554.png` |
| File deletion, 16 Oct 2026 | Reviewed source record showed built-in Rule `553` ("File deleted"), Level 7, at `2026-10-16T12:31:32.819+0530`. Custom Rule `100002` was **absent** from that record. | `evidence/v0.3/v0.3-oct16-detection-rule-553.png` |
| SOC investigation (v0.3) | **In progress.** CASE-001 evidence reconciliation is closed for the reviewed scope; the overall investigation remains open. | `investigations/CASE-001.md` |

**Reading the 16 October results correctly**
- They are reviewed records of individual controlled actions. They are not custom-rule validations, not a regression test, and not used in any metric or rate.
- The reason Rule `100002` was absent is **unresolved**. It is not established as a detection miss, and no root cause is asserted.
- The source records were reviewed from the Wazuh runtime log `/var/ossec/logs/alerts/2026/Oct/ossec-alerts-16.json`. That raw log is not claimed to be committed to this repository.

**Not yet measured or completed:** detection rate, miss rate, false-positive or false-negative rate, MTTA or MTTR, detection or response time, attack or detection coverage (including complete FIM coverage of `/home` or all event types), response-time statistics, and any resilience or mutation percentage. No containment, eradication, or recovery exercise has been completed, and the full SIMULATE → DETECT → INVESTIGATE → RESPOND → MEASURE → IMPROVE → RETEST workflow has not been completed. Values will be recorded here only as real, controlled tests produce them.

## Measurement principles

SENTINEL does not treat a control as successful because a tool is installed, a rule exists, an alert appears in a screenshot, or a test ran once. Every metric stored here should be:

- **Evidence-backed:** traceable to a specific test, investigation, alert, or other reproducible source.
- **Repeatable:** where practical, tests can be rerun so results can be compared over time.
- **Contextual:** interpreted with its scenario, technique, environment, and available telemetry, never in isolation.
- **Honest:** failed tests and poor results are preserved, not discarded or adjusted.
- **Compared before and after:** improvements are judged against a prior measurement (see below).

## Metric categories

Categories describe what SENTINEL intends to measure. None has measured values yet.

- **Detection:** detection status, rate, latency, successful and missed detections, coverage, alert quality.
- **False positive:** count or rate, which benign events triggered a detection, tuning changes, post-tuning results.
- **False negative / missed detection:** attacks executed, expected detections, missed detections, miss rate, gaps, corrective action, retest result.
- **Investigation:** time to triage and investigate, completion status, evidence completeness, timeline reconstruction, IOC identification, root-cause determination. Used only once the investigation methodology supports them.
- **Response:** time to response and containment, success, recovery status, failures, manual intervention. Automated-response metrics are not used unless automated response is implemented.
- **Coverage:** attack scenario, detection, telemetry, MITRE ATT&CK, investigation, and response coverage, always against clearly defined test cases.
- **Regression:** whether a change caused a previously passing test to fail: previous result, what changed, rerun result, regression detected or not.
- **Detection resilience (future):** original vs. modified attack detection and an overall resilience measure. Not applicable: Attack Mutation is not implemented.
- **Purple team (future):** attack executions, detections and misses, detection and response latency, false positives, improvements, retest results. Not applicable: purple-team validation has not begun.

## Core metric definitions

These are intended definitions. None currently has a measured value.

**Detection Rate**
```
Detection Rate = Successful Detections / Total Expected Detection Opportunities × 100
```
The denominator must be defined per test set before the rate is calculated.

**Miss Rate**
```
Miss Rate = Missed Detections / Total Expected Detection Opportunities × 100
```

**False-Positive Rate**
Calculated only once the test population and the definition of a false positive for that population are established, never against an arbitrary or undefined denominator.

**Detection Time**
The interval between relevant activity occurring and detection becoming available to the SOC. Attack/event time, telemetry ingestion time, alert creation time, and analyst awareness time are kept as separate points, not one blended number.

**Response Time**
The interval between a confirmed or accepted incident and the corresponding response action, with explicit start and end points defined per test.

**Time to Investigation**
The interval from detection/triage start to investigation conclusion, where the investigation methodology supports measuring it.

**Time to Containment** *(future)*
Used once controlled response workflows exist. Not currently measured.

## Metric record format

Each measured result is stored as an individual record. Fields contain only real, verified values; an unmeasured field is marked as such, not omitted or guessed. No records exist yet.

```markdown
# Metric Record

## Test ID
Assigned only when a real test occurs (do not invent test IDs).

## Scenario
Description of the controlled scenario.

## Version
e.g. v0.2

## Date
Only an actual date.

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

A master table may summarize completed tests. It will be populated only with real, completed tests. No test-result rows have been recorded yet.

| Test ID | Scenario | Technique | Expected | Result | Detection Time | Response Time | Evidence |
|---|---|---|---|---|---|---|---|

## Before / after measurement

When a detection or control is changed to fix a gap, tune a false positive, or respond to a missed detection, performance is recorded before and after the change using matching records (same scenario, same technique, comparable conditions where possible). A comparison exists only once a real "before" measurement and a real "after" retest are both recorded.


## Related documentation

- [`docs/07-testing-and-metrics.md`](../docs/07-testing-and-metrics.md): full testing and validation methodology.
- [`docs/05-detection-engineering.md`](../docs/05-detection-engineering.md): detection design and validation.
- [`docs/06-incident-response.md`](../docs/06-incident-response.md): incident response methodology.
- [`investigations/`](../investigations/): investigation case records.
- [`failure-log/`](../failure-log/): documented failures, misses, and regressions.
- [`evidence/`](../evidence/): supporting evidence and screenshots.
- [`CHANGELOG.md`](../CHANGELOG.md): project milestones and changes.
