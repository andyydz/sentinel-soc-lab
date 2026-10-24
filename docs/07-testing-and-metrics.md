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
| Real-time File Integrity Monitoring configured for `/home` | Configured; telemetry confirmed for the tested scenarios. Complete coverage has not been established. |
| Controlled file **modification** test on `/home/sentinel-admin/sentinel-fim-validation.txt` (11 October 2026) | Executed; produced observable FIM telemetry at `2026-10-11T20:25:14.746+0530` |
| Built-in Wazuh Rule 550 (Level 7, "Integrity checksum changed") | Observed during the controlled test |
| Custom Rule 100002 (Level 8) | **Confirmed to generate the expected Level 8 alert** for the tested file-modification scenario only |

Full detail and screenshots are documented in `investigations/CASE-001.md` and under `evidence/v0.3/`, with the initial telemetry-pipeline evidence under `evidence/v0.2/`.

**Reviewed records from 16 October 2026** (controlled actions on `/home/sentinel-admin/sentinel-audit-test.txt`; the screenshots have been reviewed, the source alert JSON has not):

| Item | Reviewed record |
|---|---|
| Controlled file **creation** | The reviewed screenshot shows built-in Rule 554. Custom Rule 100002 is **absent** from that record. Timestamp unresolved (see below). |
| Controlled file **deletion** | The reviewed record shows built-in Rule 553 at `2026-10-16T12:31:32.819+0530`. Custom Rule 100002 is **absent** from that record. |

These are reviewed records of individual controlled actions. They are **not** successful validations of Rule 100002 for creation or deletion, and neither is counted toward any metric in Section 3. For deletion, a built-in alert appeared and the custom rule's absence is an **unresolved custom-rule coverage question** — not a confirmed detection miss and not a definitive root cause. An earlier claim that Rules 554 and 100002 fired together during creation is unsupported by the reviewed screenshot and remains unexplained; it is not treated as a result.

**Rule 550 dependency (unresolved):** a read-only inspection of the on-disk `local_rules.xml` showed Rule 100002 at Level 8 with parent `<if_sid>550</if_sid>`, a `file` field condition of `/home/`, and group `sentinel_fim`. The reviewed creation and deletion records show built-in Rules 554 and 553, respectively, and do not show Rule 550 as the matching parent rule for those records. This is consistent with Rule 100002 being absent, but it does not explain the earlier creation claim or establish a definitive root cause. The inspection shows the file as it was at inspection time, not necessarily the version loaded by the manager during the earlier tests, and the exact matching semantics of the `/home/` condition remain unverified. The rule has not been changed.

**Open evidence-reconciliation items:**

- **Creation timestamp:** the reviewed screenshot shows `2026-10-16T11:40:06.007+0530`, while the evidence README contains `2026-10-16T11:40:06.087+0530`. Unresolved pending review of the source alert JSON.
- **Creation screenshot filename:** it contains `creation-rule-553` although its content shows Rule 554, and the evidence README references `creation-rule-664`. Unresolved pending filename review.

**Scope of results:**

- The October 11 test confirms Rule 100002 works for file *modification* specifically.
- The October 16 records do **not** confirm creation coverage, and they leave deletion coverage for Rule 100002 an open question.
- Nothing yet confirms behavior under false-positive conditions (legitimate `/home` activity).
- Nothing yet confirms behavior under false-negative conditions beyond the scenarios above.
- Nothing here confirms complete FIM coverage of `/home`, or anything about malicious activity — these were controlled lab tests.

No controlled attack scenario, response action, or repeatable regression/mutation test has been executed as part of the documented testing to date. The broader investigation and response-engineering work remain open (Section 6).

---

## 3. Metrics Framework

| Metric | What it measures | Status |
|---|---|---|
| Detection Rate / Coverage | Successful detections ÷ applicable test executions | Not measured — one confirmed scenario (modification); the 16 October reviewed records are not counted; insufficient for a rate |
| Missed Detections | Malicious test activity that should have triggered a detection but didn't | Not measured — the absence of Rule 100002 from the reviewed creation and deletion records is an open coverage question, not a confirmed miss |
| False-Positive Rate | Legitimate activity incorrectly flagged ÷ applicable benign events tested | Not measured — no false-positive testing performed yet |
| Mean Time to Detect (MTTD) | Time between activity occurring and a detection firing | Not measured |
| Mean Time to Respond (MTTR) | Time between a confirmed detection and a response action | Not measured — response capability not yet implemented |
| Detection-Rule Validation Status | Whether a specific rule has passed its full test lifecycle (not just syntax check) | Rule 100002: **validated for the file-modification scenario only**. Creation: not validated — reviewed record shows built-in Rule 554 with Rule 100002 absent. Deletion: not validated — reviewed record shows built-in Rule 553 with Rule 100002 absent; open coverage question. Broader FP/FN testing not yet performed. |
| MITRE ATT&CK Coverage | Proportion of relevant techniques with a validated, mapped detection | Planned — no mappings exist yet |

No aggregate numerical values are reported above beyond the single confirmed test result, because there isn't yet enough test data to support a rate or trend. As more scenarios are tested, this table will be populated with real figures — never estimated or interpolated ones.

---

## 4. Evidence and Reproducibility

Every test should leave behind enough to reproduce it later: the exact procedure, the expected outcome (written before execution), the actual outcome, a timestamp, and supporting artifacts — a screenshot, a relevant log excerpt, or alert output.

Evidence for the Rule 100002 validation and CASE-001 is stored under `evidence/v0.3/`; earlier infrastructure/telemetry-pipeline evidence is under `evidence/v0.2/`. This document references those paths without restating their contents — the evidence directories themselves are the source of truth for what was actually captured.

**October 16 evidence status:**

- **Reviewed:** the creation and deletion screenshots, which are referenced in the v0.3 evidence index and stored under `evidence/v0.3/`.
- **Not confirmed located or reviewed:** the source alert JSON for those records, and any operational artifacts from the same period. No evidence path is claimed for them here.
- **Open reconciliation:** the creation timestamp and filename discrepancies listed in Section 2.

Screenshot review is not the same as source-alert review; until the source JSON is located, reviewed, and saved, the creation timestamp stays unresolved. Evidence is never edited to make a failed or inconclusive test look like a pass. If a result changes on retest, both the original and the retest are kept on record.

---

## 5. Lessons and Limitations

A few distinctions matter enough to call out directly:

- **Tool availability is not agent connectivity.** Wazuh being installed and running doesn't mean an agent is enrolled and reporting.
- **Agent connectivity is not telemetry validation.** An active agent doesn't guarantee the specific telemetry a detection needs is actually being generated or collected correctly.
- **A rule passing syntax validation is not a validated detection — and one validated scenario is not complete coverage.** Rule 100002 moved from "syntax-valid only" to "confirmed firing on a controlled modification test" — a real step forward, but it validates one specific scenario.
- **A reviewed record is not validated coverage.** The October 16 creation and deletion records each show a built-in rule with Rule 100002 absent. They do not establish that Rule 100002 covers creation, and they do not establish why it was absent for deletion.
- **A built-in rule alert is not a custom rule alert.** The reviewed creation record showed built-in Rule 554 and the reviewed deletion record showed built-in Rule 553; custom Rule 100002 was absent from both. Rule 100002's documented parent dependency is `<if_sid>550</if_sid>`; Rules 553 and 554 are not its parent rules. A built-in alert for one FIM event type should not be read as coverage by the custom rule.
- **A single test run is not repeatable regression testing.** One execution per scenario, on one asset, is not a documented, repeatable test that can be rerun after a rule change.
- **One passing test is not production readiness.** A single successful result, on one asset, under one set of conditions, doesn't generalize to other environments, other event types, or attacker behavior.

Documenting failed and inconclusive tests matters as much as documenting passes — a missing or incomplete result is information about where the lab's current coverage actually ends, and hiding it would make every other claim in this document less trustworthy.

---

## 6. Future Plans

The following are planned and **not yet completed**:

- Reviewing or obtaining the source alert JSON for the 16 October creation and deletion records, if available, and settling the creation timestamp
- Resolving the creation screenshot filename and evidence README discrepancies in a separately approved documentation pass
- Verifying the Rule 100002 version loaded by the manager during testing, if historical evidence permits
- Reviewing built-in Rules 550, 553, and 554, and verifying the field-condition matching behavior of the `/home/` condition
- Determining whether Rule 100002 is intended to cover creation and deletion, without presuming a cause for its absence from the reviewed records
- Broader investigation and response-engineering work, which remains open
- Repeatable, documented creation, modification, and deletion test procedures, with expected results written in advance, so they can serve as regression tests
- False-positive and false-negative testing for Rule 100002 against legitimate `/home` activity
- Tuning Rule 100002 based on the above, only after review and approval, and retesting after any change
- Broader telemetry sources: authentication activity and process execution
- Repeatable, documented detection test scenarios beyond the FIM tests performed so far
- MITRE ATT&CK mapping for implemented detections
- Purple-team testing (red/blue/purple loop) and attack mutation testing
- Before-and-after comparisons following detection tuning, once a detection has actually been tuned

These are labeled planned or unresolved because none of them have produced a documented result yet — this section exists so the roadmap stays visible without being mistaken for current capability.
