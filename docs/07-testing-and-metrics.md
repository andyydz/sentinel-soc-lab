# SENTINEL Testing & Metrics

> Does your detection still work when the attacker changes tactics?

This document defines how SENTINEL proves its detections actually work — not just that a rule exists — and tracks what has genuinely been tested so far. **"Configured" does not mean "validated."** A control only counts as validated once it has been tested against controlled activity in the lab and the result has been documented, whether that result is a pass, a fail, or an inconclusive outcome. Validation is always scoped to the specific scenario tested.

This is a testing and measurement document. Detection design and implementation are covered separately in `docs/05-detection-engineering.md`; this document focuses on how results are tested, compared, and measured.

---

## 1. Testing Methodology

Every test in SENTINEL follows the same workflow:

```
Define the test → Establish expected results → Execute a controlled test →
Observe actual results → Compare outcomes → Record evidence → Fix and retest
```

| Stage | What happens |
|---|---|
| Define the test | State what's being tested and why |
| Establish expected results | Write down the expected outcome *before* running the test |
| Execute | Run the controlled activity in the isolated lab |
| Observe | Capture what actually happened |
| Compare | Check actual results against the expected results |
| Record evidence | Save proof — screenshots, logs, alert output — regardless of outcome |
| Fix and retest | If it failed or was incomplete, address the cause and run it again |

**Successful, failed, and inconclusive tests are different things:**

- **Successful** — the expected telemetry and alert were both observed, matching what was defined up front.
- **Failed** — the expected behavior did not occur. This is recorded and investigated, not hidden.
- **Inconclusive** — part of the expected chain was confirmed, but the specific thing under test was not. This label exists so a partial result is never overstated as a pass.

---

## 2. Current Testing Evidence

**Environment:**

| Component | Details |
|---|---|
| SENTINEL-WAZUH | Wazuh 4.14.8, `10.10.10.10` |
| SENTINEL-LINUX01 | Wazuh Agent 4.14.8, `10.10.10.40`, Agent ID `002` |
| Lab network | `SENTINEL-LAB`, `10.10.10.0/24` |

**What's actually been verified:**

| Item | Status |
|---|---|
| Wazuh Manager ↔ SENTINEL-LINUX01 communication | Verified |
| Real-time File Integrity Monitoring configured for `/home` | Configured and confirmed working |
| Controlled file **modification** test on `/home/sentinel-admin/sentinel-fim-validation.txt` | Executed; produced observable FIM telemetry at `2026-10-11T20:25:14.746+0530` |
| Built-in Wazuh Rule 550 (Level 7, "Integrity checksum changed") | Observed during the controlled test |
| Custom Rule 100002 (Level 8) | **Confirmed to generate the expected Level 8 alert** for the tested file-modification scenario |

Full detail and screenshots are documented in `investigations/CASE-001.md` and under `evidence/v0.3/`, with the initial telemetry-pipeline evidence under `evidence/v0.2/`.

**Reported, not yet independently reviewed (October 16):**

| Item | Status |
|---|---|
| Controlled file **creation** test on `/home/sentinel-admin/sentinel-audit-test.txt` | Reported: built-in Rule 554 and custom Rule 100002 both fired. Raw-alert review is pending. |
| Controlled file **deletion** test | Reported: built-in Rule 553 fired; custom Rule 100002 did not. Treated as an **open custom-rule coverage question**, pending review of the raw alerts and the active rule definitions. No cause is asserted. |

These two results are individual reported scenarios. Neither is treated as confirmed until the raw alerts have been reviewed, and neither is counted toward any metric in Section 3.

The reported Rule 554 and Rule 553 alerts indicate that FIM events were reportedly generated for the respective creation and deletion tests. Their raw alerts still need review, and their reported firing does not establish whether custom Rule 100002 should cover those events.

**Unresolved discrepancy — creation alert vs. parent condition:** the reported creation result (Rule 100002 firing alongside Rule 554) has not been reconciled with the reported parent condition `<if_sid>550</if_sid>` for Rule 100002. Rule 550 is the rule observed in the October 11 modification test, and the reported creation event was attributed to Rule 554. Neither the active rule definition nor the raw alerts have been independently reviewed, so it is not yet known whether the reported rule definition, the reported creation alert, or both need correction. Until that review is done, neither the creation result nor the reported parent condition is treated as established.

**Scope of results:**

- The October 11 test confirms Rule 100002 works for file *modification* specifically.
- The October 16 creation and deletion results are reported only. They do **not** yet confirm creation coverage, and they leave deletion coverage for Rule 100002 an open question.
- Nothing yet confirms behavior under false-positive conditions (legitimate `/home` activity).
- Nothing yet confirms behavior under false-negative conditions beyond the scenarios above.
- Nothing here confirms complete FIM coverage of `/home`, or anything about malicious activity — these were controlled lab tests.

No controlled attack scenario, response action, or repeatable regression/mutation test has been executed as part of the documented testing to date. The broader investigation and response-engineering work remain open (Section 6).

---

## 3. Metrics Framework

| Metric | What it measures | Status |
|---|---|---|
| Detection Rate / Coverage | Successful detections ÷ applicable test executions | Not measured — one confirmed scenario plus two reported, unreviewed scenarios; insufficient for a rate |
| Missed Detections | Malicious test activity that should have triggered a detection but didn't | Not measured — the reported deletion result is an open question, not a confirmed miss |
| False-Positive Rate | Legitimate activity incorrectly flagged ÷ applicable benign events tested | Not measured — no false-positive testing performed yet |
| Mean Time to Detect (MTTD) | Time between activity occurring and a detection firing | Not measured |
| Mean Time to Respond (MTTR) | Time between a confirmed detection and a response action | Not measured — response capability not yet implemented |
| Detection-Rule Validation Status | Whether a specific rule has passed its full test lifecycle (not just syntax check) | Rule 100002: **validated for the file-modification scenario**. Creation: reported to fire, pending raw-alert review and reconciliation with the reported `<if_sid>550</if_sid>` condition. Deletion: reported not to fire, open pending review. Broader FP/FN testing not yet performed. |
| MITRE ATT&CK Coverage | Proportion of relevant techniques with a validated, mapped detection | Planned — no mappings exist yet |

No aggregate numerical values are reported above beyond the single confirmed test result, because there isn't yet enough test data to support a rate or trend. As more scenarios are tested, this table will be populated with real figures — never estimated or interpolated ones.

---

## 4. Evidence and Reproducibility

Every test should leave behind enough to reproduce it later: the exact procedure, the expected outcome (written before execution), the actual outcome, a timestamp, and supporting artifacts — a screenshot, a relevant log excerpt, or alert output.

Evidence for the Rule 100002 validation and CASE-001 is stored under `evidence/v0.3/`; earlier infrastructure/telemetry-pipeline evidence is under `evidence/v0.2/`. This document references those paths without restating their contents — the evidence directories themselves are the source of truth for what was actually captured.

**October 16 evidence status:** the raw alerts and operational artifacts from the creation and deletion tests have **not been confirmed as saved in the repository**. No evidence path is claimed for them here. Until those artifacts are located, reviewed, and saved, the October 16 results remain reported observations rather than documented evidence.

Evidence is never edited to make a failed or inconclusive test look like a pass. If a result changes on retest, both the original and the retest are kept on record.

---

## 5. Lessons and Limitations

A few distinctions matter enough to call out directly:

- **Tool availability is not agent connectivity.** Wazuh being installed and running doesn't mean an agent is enrolled and reporting.
- **Agent connectivity is not telemetry validation.** An active agent doesn't guarantee the specific telemetry a detection needs is actually being generated or collected correctly.
- **A rule passing syntax validation is not a validated detection — and one validated scenario is not complete coverage.** Rule 100002 moved from "syntax-valid only" to "confirmed firing on a controlled modification test" — a real step forward, but it validates one specific scenario.
- **A reported test is not verified coverage.** The October 16 creation and deletion results are individual reported scenarios. Without reviewed raw alerts and a checked rule definition, they do not establish that Rule 100002 covers creation, and they do not establish why it did not fire on deletion.
- **A built-in rule firing is not a custom-rule firing.** The reported Rule 554 and Rule 553 alerts indicate FIM events were reportedly generated, but their raw alerts still need review, and their reported firing does not establish whether custom Rule 100002 should cover those events.
- **A single test run is not repeatable regression testing.** One execution per scenario, on one asset, is not a documented, repeatable test that can be rerun after a rule change.
- **One passing test is not production readiness.** A single successful result, on one asset, under one set of conditions, doesn't generalize to other environments, other event types, or attacker behavior.

Documenting failed and inconclusive tests matters as much as documenting passes — a missing or incomplete result is information about where the lab's current coverage actually ends, and hiding it would make every other claim in this document less trustworthy.

---

## 6. Future Plans

The following are planned and **not yet completed**:

- Reviewing the raw alerts and the active Rule 100002 definition to resolve the creation-alert vs. `<if_sid>550</if_sid>` discrepancy
- Reviewing the reported deletion result (Rule 553 fired, Rule 100002 did not) against the raw alerts and active rule definitions, and determining whether Rule 100002 is intended to cover deletion
- Locating and saving the October 16 raw-alert and operational artifacts in the repository, then confirming or correcting the reported creation and deletion results
- Broader investigation and response-engineering work, which remains open
- Repeatable, documented creation and deletion test procedures, with expected results written in advance, so they can serve as regression tests
- False-positive and false-negative testing for Rule 100002 against legitimate `/home` activity
- Tuning Rule 100002 based on the above, and retesting after any change
- Broader telemetry sources: authentication activity and process execution
- Repeatable, documented detection test scenarios beyond the FIM tests performed so far
- MITRE ATT&CK mapping for implemented detections
- Purple-team testing (red/blue/purple loop) and attack mutation testing
- Before-and-after comparisons following detection tuning, once a detection has actually been tuned

These are labeled planned or unresolved because none of them have produced a documented result yet — this section exists so the roadmap stays visible without being mistaken for current capability.
