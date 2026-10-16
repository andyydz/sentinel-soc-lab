# SENTINEL Detection Engineering

> Does your detection still work when the attacker changes tactics?

This document defines SENTINEL's detection engineering process — how detections are designed, implemented, tested, and validated against real telemetry — and tracks the current state of detections actually built in the lab.

A detection is not considered working because a rule exists. It is considered working only once it has been tested against controlled activity in the lab and the result — pass, fail, or unresolved — has been documented.

---

## 1. Purpose and Scope

SENTINEL treats detection engineering as an evidence-driven discipline: every detection should be observable (grounded in real telemetry), testable (validated against a controlled scenario, not assumed), and explainable (an analyst can state exactly why it fired). This document covers the methodology used to build and validate detections, and documents the current implementation status honestly — including what is confirmed, what is partially confirmed, and what remains unresolved.

---

## 2. Detection Engineering Lifecycle

```
DEFINE → IMPLEMENT → TEST → VALIDATE → TUNE → RETEST
```

| Stage | What happens |
|---|---|
| **Define** | Identify the threat/behavior, the telemetry needed to observe it, and the detection objective |
| **Implement** | Write the detection logic (e.g., a Wazuh rule) against that telemetry |
| **Test** | Execute a controlled, reversible activity in the lab and capture the resulting telemetry |
| **Validate** | Confirm the detection fired as expected, with useful alert context, against that telemetry |
| **Tune** | Adjust the rule based on false positives/negatives or missing context |
| **Retest** | Re-run the same test to confirm the tuning actually fixed the issue |

A detection only reaches **Validated** once Test and Validate have both produced the expected, documented result for the scenario under test. Validation is always scoped to the specific scenario tested — it does not automatically extend to related but untested behavior. Passing a syntax check alone is not the same as passing this lifecycle — see Section 6.

---

## 3. Detection Specification

Every detection should be documented against this template before and after implementation:

| Field | Description |
|---|---|
| Detection ID | Unique project identifier |
| Threat / Technique | What behavior this addresses (MITRE ATT&CK mapping where confidently applicable) |
| Telemetry Source | Required log/event source |
| Detection Logic | Condition(s) that should trigger the alert |
| Expected Alert | What the alert should look like if the logic fires correctly |
| Severity | Intended severity level |
| Test Procedure | The controlled scenario used to validate it |
| Evidence | Supporting artifacts (screenshots, logs, alert output) |

**Current instance — File Integrity Monitoring on `/home`:**

| Field | Value |
|---|---|
| Detection ID | Custom Wazuh Rule `100002` |
| Threat / Technique | Unauthorized or unexpected file modification under `/home`; no MITRE ATT&CK mapping yet |
| Telemetry Source | Wazuh Syscheck (File Integrity Monitoring), real-time, scoped to `/home` on SENTINEL-LINUX01 (`10.10.10.40`, Agent ID `002`) |
| Detection Logic | As reported (not yet checked against the active rule file): parent condition `<if_sid>550</if_sid>` plus a `file` field condition of `/home/`, Level 8, group `sentinel_fim`. The exact matching behavior of the `file` field condition has **not** been verified against the active rule. See Section 5 for an unresolved discrepancy with the parent condition. |
| Expected Alert | Level 8 alert identifying the changed file |
| Severity | Level 8 (custom rule), confirmed for the tested modification scenario. Wazuh's built-in Rule 550 (Level 7, "Integrity checksum changed") was also observed during the same test. |
| Test Procedure | Controlled modification of `/home/sentinel-admin/sentinel-fim-validation.txt` on SENTINEL-LINUX01, confirmed event timestamp `2026-10-11T20:25:14.746+0530`. Additional controlled creation and deletion tests of `/home/sentinel-admin/sentinel-audit-test.txt` were **reported** on 16 October 2026 (see Section 5); they are not yet confirmed against raw alerts. |
| Evidence | `evidence/v0.3/`; full investigation detail in `investigations/CASE-001.md`. Raw alerts for the 16 October creation and deletion tests are still to be captured or reviewed; no artifacts for them are claimed here. |

---

## 4. Testing and Validation Methodology

Every test compares an **expected result** against an **actual result**, and the outcome is recorded regardless of whether it passed:

```
Expected: File modification → Syscheck telemetry → Rule fires → Alert generated
Actual:   [recorded as observed, not assumed]
```

- **Pass** — the expected telemetry and alert were both observed.
- **Fail** — the expected behavior did not occur; the failure is investigated and documented, not hidden.
- **Unresolved / Inconclusive** — part of the chain was confirmed (e.g., telemetry reached the manager) but the specific detection logic under test was not confirmed to fire. This status exists specifically so a partial result isn't overstated as a pass.

This is the standard every detection in this document is held to, including the one currently implemented.

---

## 5. Current Implementation and Status

**Environment:**
- SENTINEL-WAZUH — Ubuntu 24.04, Wazuh 4.14.8, `10.10.10.10`
- SENTINEL-LINUX01 — Ubuntu 24.04, Wazuh Agent 4.14.8, `10.10.10.40`, Agent ID `002`

**What's implemented:**

| Component | Status |
|---|---|
| Real-time FIM on `/home` (Wazuh Syscheck) | Implemented and confirmed working |
| Built-in Wazuh **Rule 550** (Level 7, "Integrity checksum changed") | **Observed** during a controlled file-modification test |
| Custom **Rule 100002** (Level 8) — modification | **Confirmed to generate the expected Level 8 alert** for the tested controlled file-modification scenario (`/home/sentinel-admin/sentinel-fim-validation.txt`, `2026-10-11T20:25:14.746+0530`) |
| Custom **Rule 100002** (Level 8) — creation | **Reported** (16 October 2026): Rules 554 ("File added to the system") and 100002 reportedly fired for `/home/sentinel-admin/sentinel-audit-test.txt`, as real-time FIM activity. Raw-alert review pending. |
| Built-in **Rule 553** (Level 7, "File deleted") — deletion | **Reported** (16 October 2026): built-in Rule 553 reportedly fired for the deletion of the same file, while custom Rule 100002 did **not**. This remains an open custom-rule coverage question pending review of the raw alerts and active rule definitions; the cause has not been established. |

**Scope of the confirmed result:** the October 11 controlled test confirmed that a file *modification* under `/home` is correctly detected by Rule 100002 and produces a Level 8 alert. This validates **only the tested modification scenario**.

**Reported 16 October 2026 observations:** creation and deletion have each been exercised once in a controlled test, with the results above. These are reported observations, not verified detection coverage: the raw alerts and the active rule definition have not been independently reviewed for this document. The creation result is a positive result for that one test only. The deletion result was not unalerted — built-in Rule 553 reportedly fired — but the custom rule reportedly did not elevate it, and the reason has not been established. Any ATT&CK mappings carried by built-in events are telemetry metadata, not evidence of malicious intent.

**Unresolved discrepancy:** the reported definition of Rule 100002 is anchored to built-in Rule 550 via `<if_sid>550</if_sid>`, yet the creation event was reported to trigger Rule 100002. This is unexplained. No cause is asserted, and the rule has not been changed. Resolving it requires review of the raw creation alert, the active `local_rules.xml` definition, and the relevant built-in rule definitions (550, 553, 554) in the installed ruleset. Until then, neither the reported anchor nor the reported creation match should be relied on for coverage claims.

**Field-condition matching:** the exact matching behavior of the `file` field condition `/home/` (for example, whether it acts as an unanchored substring or regular-expression match, and how it treats case) has not been verified against the active rule. Descriptions of the rule as matching "paths under `/home/`" are a working assumption.

The current results do **not** establish:

- Verified coverage for file *creation* or *deletion* events — each has one reported, unreviewed test, and deletion is an open coverage question for the custom rule
- Broader false-positive or false-negative behavior (not yet tested)
- That the rule has been tuned or hardened — no tuning has occurred
- Complete FIM coverage of `/home`, or any claim about malicious activity — these were controlled lab tests, not attacks

These results are further reviewed as part of investigation `CASE-001` (`investigations/CASE-001.md`), whose controlled modification-validation objective is closed while the overall investigation remains open: broader review, rule-discrepancy verification, false-positive analysis, and tuning remain ongoing.

---

## 6. Known Limitations and Lessons

- **A single validated scenario is not complete coverage.** Rule 100002 is confirmed to work for the tested file modification. The reported creation and deletion tests are single, unreviewed observations; they do not establish verified coverage for those event types, other paths, or other file types.
- **Reported results are not verified coverage.** Until raw alerts and the active rule definition are reviewed, the October 16 results stay reported observations, and the creation-match discrepancy against the `<if_sid>550</if_sid>` parent stays unresolved.
- **A built-in parent rule match is not a custom rule match.** In the reported deletion test, built-in Rule 553 fired while custom Rule 100002 did not. A rule that matches one FIM event type should not be assumed to match the others.
- **A syntax check is not validation, and validation is not comprehensive coverage.** Rule 100002 moved from "syntax-valid only" to "confirmed firing" for one scenario — a meaningful step, but still a narrow one; the two should not be conflated with "the detection is done."
- **A FIM alert does not prove malicious activity.** Whether from Rule 550, 553, 554, or Rule 100002, a file-integrity alert only confirms a monitored file changed — not who changed it, why, or whether it was legitimate. That determination requires investigation (CASE-001, `docs/06-incident-response.md`), not inference from the alert alone.
- No false-positive or false-negative testing has been performed against Rule 100002 yet, and no tuning has occurred — both remain open work.

---

## 7. Future Plans

The following are planned and **not yet implemented**:

- Reviewing the raw alerts for the reported 16 October creation and deletion tests and the active Rule 100002 definition, resolving the `<if_sid>550</if_sid>` creation discrepancy, and verifying the matching behavior of the `file` field condition
- Investigating the deletion coverage question and, after review and approval, designing and testing any rule change
- Repeatable regression tests for file **creation**, **modification**, and **deletion** events under `/home`, with explicit pass/fail criteria
- False-positive / false-negative testing for Rule 100002 against legitimate `/home` activity
- Tuning Rule 100002 based on the results of the above
- Completing CASE-001's broader review, timeline, root-cause, and attribution work
- Broader telemetry sources: authentication activity and process/command execution
- MITRE ATT&CK technique mapping for implemented detections
- Additional detection rules beyond File Integrity Monitoring
- Purple-team validation (detection rate, detection time, before/after comparison)
- Attack mutation testing (varying attacker technique to test detection resilience)

These remain future work and are not claimed as current capabilities.
