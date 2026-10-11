# SENTINEL Testing & Metrics

> Does your detection still work when the attacker changes tactics?

This document defines how SENTINEL proves its detections actually work — not just that a rule exists — and tracks what has genuinely been tested so far. **"Configured" does not mean "validated."** A control only counts as validated once it has been tested against controlled activity in the lab and the result has been documented, whether that result is a pass, a fail, or an inconclusive outcome.

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
- **Inconclusive** — part of the expected chain was confirmed, but the specific thing under test was not. For example, confirming telemetry reached the manager doesn't confirm a *specific* rule fired. This label exists so a partial result is never overstated as a pass.

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
| Controlled file creation/modification test on `/home` | Executed; produced observable FIM telemetry |
| Built-in Wazuh Rule 550 (Level 7, "Integrity checksum changed") | Observed during the controlled test |
| Custom Rule 100002 | Passed configuration syntax validation; **end-to-end validation unresolved** — no confirmed Level 8 alert yet |

**Important:** Rule 550 firing confirms the FIM telemetry pipeline works end to end. It does **not** confirm that custom Rule 100002 works — they are separate rules, and one succeeding says nothing about the other. This distinction is tracked explicitly rather than treating "FIM telemetry observed" and "custom rule validated" as the same claim.

No controlled attack scenario, investigation, response action, or regression/mutation test has been executed yet. Those remain future work (Section 6).

---

## 3. Metrics Framework

| Metric | What it measures | Status |
|---|---|---|
| Detection Rate / Coverage | Successful detections ÷ applicable test executions | Not measured — insufficient test data |
| Missed Detections | Malicious test activity that should have triggered a detection but didn't | Not measured |
| False-Positive Rate | Legitimate activity incorrectly flagged ÷ applicable benign events tested | Not measured |
| Mean Time to Detect (MTTD) | Time between activity occurring and a detection firing | Not measured |
| Mean Time to Respond (MTTR) | Time between a confirmed detection and a response action | Not measured — response capability not yet implemented |
| Detection-Rule Validation Status | Whether a specific rule has passed its full test lifecycle (not just syntax check) | Rule 100002: syntax-valid, end-to-end validation unresolved |
| MITRE ATT&CK Coverage | Proportion of relevant techniques with a validated, mapped detection | Planned — no mappings exist yet |

No numerical values are reported above because there isn't yet enough test data to support one. As detections are tested and validated, this table will be populated with real figures — never estimated or interpolated ones.

---

## 4. Evidence and Reproducibility

Every test should leave behind enough to reproduce it later: the exact procedure, the expected outcome (written before execution), the actual outcome, a timestamp, and supporting artifacts — a screenshot, a relevant log excerpt, or alert output.

Evidence for work completed so far is stored under `evidence/v0.2/`, organized by project version. This document references that path without restating its contents — the evidence directory itself is the source of truth for what was actually captured.

Evidence is never edited to make a failed or inconclusive test look like a pass. If a result changes on retest, both the original and the retest are kept on record.

---

## 5. Lessons and Limitations

A few distinctions matter enough to call out directly:

- **Tool availability is not agent connectivity.** Wazuh being installed and running doesn't mean an agent is enrolled and reporting.
- **Agent connectivity is not telemetry validation.** An active agent doesn't guarantee the specific telemetry a detection needs is actually being generated or collected correctly.
- **A rule passing syntax validation is not a validated detection.** Wazuh accepting a rule's configuration only means the configuration is well-formed — it says nothing about whether the rule fires correctly against real activity. This is exactly where Rule 100002 currently stands: syntax-valid, not yet proven to work.
- **One passing test is not production readiness.** A single successful result, on one asset, under one set of conditions, doesn't generalize to other environments or attacker behavior.

Documenting failed and inconclusive tests matters as much as documenting passes — a missing or incomplete result is information about where the lab's current coverage actually ends, and hiding it would make every other claim in this document less trustworthy.

---

## 6. Future Plans

The following are planned and **not yet completed**:

- End-to-end validation of custom Rule 100002 (immediate next step)
- Broader telemetry sources: authentication activity and process execution
- Repeatable, documented detection test scenarios beyond the single FIM test performed so far
- MITRE ATT&CK mapping for implemented detections
- Purple-team testing (red/blue/purple loop) and attack mutation testing
- Before-and-after comparisons following detection tuning, once a detection has actually been tuned

These are labeled planned or unresolved because none of them have produced a documented result yet — this section exists so the roadmap stays visible without being mistaken for current capability.
