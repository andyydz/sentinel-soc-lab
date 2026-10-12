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
| Detection Logic | Matches on Syscheck's file-integrity-changed event for the monitored path |
| Expected Alert | Level 8 alert identifying the changed file |
| Severity | Level 8 (custom rule), confirmed for the tested modification scenario. Wazuh's built-in Rule 550 (Level 7, "Integrity checksum changed") was also observed during the same test. |
| Test Procedure | Controlled modification of `/home/sentinel-admin/sentinel-fim-validation.txt` on SENTINEL-LINUX01, confirmed event timestamp `2026-10-11T20:25:14.746+0530` |
| Evidence | `evidence/v0.3/`; full investigation detail in `investigations/CASE-001.md` |

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
| Custom **Rule 100002** (Level 8) | **Confirmed to generate the expected Level 8 alert** for the tested controlled file-modification scenario (`/home/sentinel-admin/sentinel-fim-validation.txt`, `2026-10-11T20:25:14.746+0530`) |

**Scope of this result:** the controlled test confirmed that a file *modification* under `/home` is correctly detected by Rule 100002 and produces a Level 8 alert. This validates **only the tested modification scenario**. It does **not** establish:

- Coverage for file *creation* or *deletion* events (not yet tested)
- Broader false-positive or false-negative behavior (not yet tested)
- That the rule has been tuned or hardened — no tuning has occurred
- Complete FIM coverage of `/home`, or any claim about malicious activity — this was a controlled lab test, not an attack

This result is further reviewed as part of investigation `CASE-001` (`investigations/CASE-001.md`), whose controlled-validation objective is closed while broader review, false-positive analysis, and tuning remain ongoing.

---

## 6. Known Limitations and Lessons

- **A single validated scenario is not complete coverage.** Rule 100002 is now confirmed to work for file modification specifically — that result does not extend to file creation, deletion, or other behaviors until each is independently tested.
- **A syntax check is not validation, and validation is not comprehensive coverage.** Rule 100002 moved from "syntax-valid only" to "confirmed firing" for one scenario — a meaningful step, but still a narrow one; the two should not be conflated with "the detection is done."
- **A FIM alert does not prove malicious activity.** Whether from Rule 550 or Rule 100002, a file-integrity alert only confirms a monitored file changed — not who changed it, why, or whether it was legitimate. That determination requires investigation (CASE-001, `docs/06-incident-response.md`), not inference from the alert alone.
- No false-positive or false-negative testing has been performed against Rule 100002 yet, and no tuning has occurred — both remain open work.

---

## 7. Future Plans

The following are planned and **not yet implemented**:

- Extending Rule 100002 validation to file **creation** and **deletion** events under `/home`
- False-positive / false-negative testing for Rule 100002 against legitimate `/home` activity
- Tuning Rule 100002 based on the results of the above
- Completing CASE-001's broader review, timeline, root-cause, and attribution work
- Broader telemetry sources: authentication activity and process/command execution
- MITRE ATT&CK technique mapping for implemented detections
- Additional detection rules beyond File Integrity Monitoring
- Purple-team validation (detection rate, detection time, before/after comparison)
- Attack mutation testing (varying attacker technique to test detection resilience)

These remain future work and are not claimed as current capabilities.
