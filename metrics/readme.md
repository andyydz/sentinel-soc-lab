# metrics/

This directory is for **measured results** from SENTINEL's security testing: evidence that a detection or control works, not just that it exists.

**What is here today:** this README and [`v0.6-purple-team-measurement.md`](v0.6-purple-team-measurement.md). The v0.6 report is the current committed formal measurement report; it contains measured controlled results for FIM, Sysmon replay and SSH testing. Its test populations are small and controlled, so they are **not** statistically representative detection or false-positive rates. The master test metrics table in this README remains unpopulated because no consolidated rows have been added to it. Other investigation cases contain measured test outcomes, but those are not automatically converted into broad detection-rate or MTTR claims. A metric definition below is not a measured result.

For the full testing methodology, see [`docs/07-testing-and-metrics.md`](../docs/07-testing-and-metrics.md).

## Where SENTINEL stands

| Area | Current status | Evidence |
|---|---|---|
| Foundation (v0.1) | Complete: Wazuh deployment, Kali attacker VM, Linux monitored endpoint with an active agent, isolated lab network | See [`evidence/`](../evidence/) |
| Controlled modification detection (v0.2) | **Validated** for the tested scenario: custom Rule `100002` generated a Level 8 alert | 11 Oct 2026 (`2026-10-11T20:25:14.746+0530`): [alert screenshot](../evidence/v0.3/screenshots/v0.3-custom-rule-100002.png) and [dashboard fields](../evidence/v0.3/screenshots/v0.3-custom-rule-100002-dashboard-json.png). The original source alert log was not recovered during the 26 Oct review, so this rests on the screenshots. |
| Repeat modification | Two consecutive modifications of one file (`/home/sentinel-admin/sentinel-v02-mod-test.txt`) generated two Rule `100002` Level 8 alerts: `2026-10-26T21:38:27.910+0530` (0 → 23 bytes) and `2026-10-26T21:38:48.473+0530` (23 → 61 bytes). These are **not** two independent test cases or a regression suite. | [26 Oct controlled modification screenshot](../evidence/v0.2/screenschots/v0.2-oct26-controlled-modification-source-alerts-new.png) |
| File creation, 16 Oct 2026 | Reviewed source record showed built-in Rule `554` ("File added to the system"), Level 5, at `2026-10-16T11:40:06.007+0530`. Custom Rule `100002` was absent from that record, which is consistent with its design as the modification rule. | [16 Oct creation screenshot](../evidence/v0.3/screenshots/v0.3-oct16-creation-rule-554.png) |
| File deletion, 16 Oct 2026 | Reviewed source record showed built-in Rule `553` ("File deleted"), Level 7, at `2026-10-16T12:31:32.819+0530`. Custom Rule `100002` was absent from that record, which is consistent with its design as the modification rule. | [16 Oct deletion screenshot](../evidence/v0.3/screenshots/v0.3-oct16-detection-rule-553.png) |
| SOC investigation (v0.3) / [CASE-001](../investigations/CASE-001.md) | **Closed** on 18 November 2026 for its defined investigation scope. Broader FIM validation and detection-engineering follow-up remain open. | [`CASE-001.md`](../investigations/CASE-001.md) |
| Sysmon replay ([CASE-002](../investigations/CASE-002.md)) | Selected Windows Sysmon detections tested using replayed `.evtx` telemetry, not a live Windows endpoint | [`CASE-002.md`](../investigations/CASE-002.md), [raw Sysmon alerts](../evidence/sysmon-replay/sysmon_alerts_raw.json) |
| SSH ([CASE-003](../investigations/CASE-003.md)) | Controlled SSH password-guessing detection, Python triage and documented manual response procedures | [`CASE-003.md`](../investigations/CASE-003.md), [evidence index](../evidence/v0.5/readme.md) |
| v0.6 | Controlled purple-team measurement across FIM, Sysmon replay and SSH (small samples) | [`v0.6-purple-team-measurement.md`](v0.6-purple-team-measurement.md) |
| v0.7 / [CASE-004](../investigations/CASE-004.md) | Controlled mutation, evasion and benign-noise testing | [`CASE-004.md`](../investigations/CASE-004.md) |
| v0.8 | Selected FIM tuning and one controlled live probe; residual desktop noise and the broader retest remain | See [`detections/readme.md`](../detections/readme.md) |
| v0.9 and v0.9.1 | Manager-side JSON replay and Python triage integration/documentation | [evidence index](../evidence/v0.9/readme.md) |
| v0.10 | Live Linux FIM probe and Python triage validation; its evidence archive is external to this repository (`~/soc-evidence/v0.10-fim-probe/`) | External archive, not committed |
| v0.11 | Committed alert, triage and regression-summary artifacts; milestone reconciliation is pending. Not described as a completed regression suite | [`v011_fim_alerts.json`](../evidence/v0.11/v011_fim_alerts.json), [`triage_report.md`](../evidence/v0.11/triage_report.md), [`regression_summary.json`](../evidence/v0.11/regression_summary.json) |

**Reading the 16 October results correctly**
- They are reviewed records of individual controlled actions. They are not custom-rule validations, not a regression test, and not used in any metric or rate.
- Rule `100002` is the custom modification rule (parent Rule `550`). Its absence from creation and deletion records is consistent with its design and is not a confirmed detection failure.
- The unresolved historical question is whether custom Rules `100003` and `100004` were deployed and loaded on 16 October. No historical loaded configuration or root cause has been established.
- The source records were reviewed from the Wazuh runtime log `/var/ossec/logs/alerts/2026/Oct/ossec-alerts-16.json`. That raw log is not claimed to be committed to this repository.

## v0.6 measurement summary

Source: [`v0.6-purple-team-measurement.md`](v0.6-purple-team-measurement.md). These are small controlled test results, not statistically meaningful rates or a broad effectiveness claim. No aggregate percentages are calculated here, and results from different tests are not merged into one rate.

- **FIM:** 3/3 selected lifecycle events detected; the `/tmp` negative control produced 0/3 alerts.
- **Sysmon replay:** 7/7 selected covered detections fired; 3 benign events generated no alerts (they matched the Level 0 base rule); 2 Event ID 7 ImageLoad events remained uncovered.
- **SSH:** baseline and threshold-escalation behavior were observed. The first threshold escalation occurred early because the 60-second sliding window carried four failures from the earlier C1 test into C2.
- **Timing:** cross-VM clock skew made raw detection-time deltas negative, so reliable detection latency was not established.
- **Response:** no automated containment or response time was measured.

## v0.11 artifacts (milestone reconciliation pending)

- [`v011_fim_alerts.json`](../evidence/v0.11/v011_fim_alerts.json) contains 10 FIM alert records from Agent `002`. Three records correspond to creation, modification and deletion of `v011_fim_probe.txt`, matching custom Rules `100003`, `100002` and `100004` at Level 8. The other seven records concern desktop/configuration paths and are not labeled confirmed benign noise.
- [`triage_report.md`](../evidence/v0.11/triage_report.md) shows `None` for the process, target-process and event-time enrichment fields.
- [`regression_summary.json`](../evidence/v0.11/regression_summary.json) contains pre/post-cutoff counts and path counts. It does not establish that a defined regression suite passed.
- Milestone reconciliation remains pending, and no metric from these artifacts is entered in the master table.

**Not yet measured or completed:** statistically meaningful detection rate, miss rate, false-positive or false-negative rate, MTTA or MTTR, reliable detection or response latency, attack or detection coverage (including complete FIM coverage of `/home` or all event types), response-time statistics, and any resilience or mutation percentage. Broader mutation coverage and repeatable regression testing also remain future work or unestablished. CASE-003 documents manual, source-scoped containment procedures and post-test SSH service-health verification; this does not establish automated containment, production SOAR capability, or a comprehensive production incident-response exercise, and no response-time statistics were measured. The full SIMULATE → DETECT → INVESTIGATE → RESPOND → MEASURE → IMPROVE → RETEST workflow has not been completed as a repeatable program. Values will be recorded here only as real, controlled tests produce them.

## Measurement principles

SENTINEL does not treat a control as successful because a tool is installed, a rule exists, an alert appears in a screenshot, or a test ran once. Every metric stored here should be:

- **Evidence-backed:** traceable to a specific test, investigation, alert, or other reproducible source.
- **Repeatable:** where practical, tests can be rerun so results can be compared over time.
- **Contextual:** interpreted with its scenario, technique, environment, and available telemetry, never in isolation.
- **Honest:** failed tests and poor results are preserved, not discarded or adjusted.
- **Compared before and after:** improvements are judged against a prior measurement (see below).

A measured result is not a broad performance claim: each result applies only to the scenario and sample that produced it.

## Metric categories

Categories describe what SENTINEL measures or intends to measure. Small controlled v0.6 results exist for some categories (see the summary above); none is a statistically meaningful rate.

- **Detection:** detection status, rate, latency, successful and missed detections, coverage, alert quality.
- **False positive:** count or rate, which benign events triggered a detection, tuning changes, post-tuning results.
- **False negative / missed detection:** attacks executed, expected detections, missed detections, miss rate, gaps, corrective action, retest result.
- **Investigation:** time to triage and investigate, completion status, evidence completeness, timeline reconstruction, IOC identification, root-cause determination. Used only once the investigation methodology supports them.
- **Response:** time to response and containment, success, recovery status, failures, manual intervention. Automated-response metrics are not applicable until an automated response workflow exists.
- **Coverage:** attack scenario, detection, telemetry, MITRE ATT&CK, investigation, and response coverage, always against clearly defined test cases.
- **Regression:** whether a change caused a previously passing test to fail: previous result, what changed, rerun result, regression detected or not.
- **Detection resilience (limited):** original vs. modified attack detection and an overall resilience measure. Controlled mutation, evasion and benign-noise testing is documented in v0.7 / [CASE-004](../investigations/CASE-004.md); no resilience percentage is established, and broader mutation coverage remains future work.
- **Purple team (limited):** attack executions, detections and misses, detection and response latency, false positives, improvements, retest results. Controlled measurement is documented in v0.6 using small samples; reliable latency and response time were not established.

## Core metric definitions

These are intended definitions. No rate computed from them is claimed; v0.6 reports small controlled counts only.

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

Each measured result is stored as an individual record. Fields contain only real, verified values; an unmeasured field is marked as such, not omitted or guessed. No individual records in this format have been created yet; the v0.6 report is a formal measurement report rather than a set of such records.

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

A master table may summarize completed tests. It will be populated only with real, completed tests. No consolidated test-result rows have been recorded in it yet; v0.6 results are reported in [`v0.6-purple-team-measurement.md`](v0.6-purple-team-measurement.md).

| Test ID | Scenario | Technique | Expected | Result | Detection Time | Response Time | Evidence |
|---|---|---|---|---|---|---|---|

## Before / after measurement

When a detection or control is changed to fix a gap, tune a false positive, or respond to a missed detection, performance is recorded before and after the change using matching records (same scenario, same technique, comparable conditions where possible). A comparison exists only once a real "before" measurement and a real "after" retest are both recorded.


## Related documentation

- [`v0.6-purple-team-measurement.md`](v0.6-purple-team-measurement.md): the current committed formal measurement report.
- [`docs/07-testing-and-metrics.md`](../docs/07-testing-and-metrics.md): full testing and validation methodology.
- [`docs/05-detection-engineering.md`](../docs/05-detection-engineering.md): detection design and validation.
- [`docs/06-incident-response.md`](../docs/06-incident-response.md): incident response methodology.
- [`investigations/`](../investigations/): investigation case records.
- [`failure-log/`](../failure-log/): documented failures, misses, and regressions.
- [`evidence/`](../evidence/): supporting evidence and screenshots.
- [`CHANGELOG.md`](../CHANGELOG.md): project milestones and changes.
