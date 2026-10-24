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
| Detection Logic | A read-only inspection of `/var/ossec/etc/rules/local_rules.xml` on SENTINEL-WAZUH showed Rule `100002` with Level 8, parent condition `<if_sid>550</if_sid>`, a `file` field condition of `/home/`, and group `sentinel_fim`. This confirms the on-disk file at inspection time, **not** the version loaded by the running manager during the earlier tests. The exact matching behavior of the `file` field condition has **not** been verified. See Section 5 for the Rule 550 dependency. |
| Expected Alert | Level 8 alert identifying the changed file |
| Severity | Level 8 (custom rule), confirmed for the tested modification scenario. Wazuh's built-in Rule 550 (Level 7, "Integrity checksum changed") was also observed during the same test. |
| Test Procedure | **Confirmed test (11 October 2026):** controlled modification of `/home/sentinel-admin/sentinel-fim-validation.txt` on SENTINEL-LINUX01; custom Rule `100002` fired at `2026-10-11T20:25:14.746+0530`. **Reviewed records (16 October 2026):** controlled creation and deletion of `/home/sentinel-admin/sentinel-audit-test.txt`. The reviewed creation record shows built-in Rule `554` and the reviewed deletion record shows built-in Rule `553`; custom Rule `100002` is absent from each reviewed record. These are reviewed records of individual controlled actions, not successful validations of custom Rule `100002` for creation or deletion (see Section 5). |
| Evidence | `evidence/v0.3/`; full investigation detail in `investigations/CASE-001.md`. The creation and deletion screenshots (`v0.3-oct16-creation-rule-553.png`, `v0.3-oct16-detection-rule-553.png`) have been reviewed. Source alert JSON for the 16 October records still needs to be checked or filed if available. The creation screenshot's filename says `rule-553` although its content shows Rule `554`, and the evidence README reportedly references an older filename (`creation-rule-664`); these remain unresolved. |

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
| Built-in **Rule 554** ("File added to the system") — creation | **Reviewed record** (16 October 2026): the reviewed screenshot for `/home/sentinel-admin/sentinel-audit-test.txt` shows Rule 554. Custom Rule 100002 is **not present** in that record. Timestamp unresolved: the screenshot displays `2026-10-16T11:40:06.007+0530`, while the evidence README lists `2026-10-16T11:40:06.087+0530`; settling it requires the source alert JSON. |
| Built-in **Rule 553** ("File deleted") — deletion | **Reviewed record** (16 October 2026): the reviewed record for the deletion of the same file shows Rule 553 at `2026-10-16T12:31:32.819+0530`. Custom Rule 100002 is **not present** in that record. This remains an open custom-rule coverage question; it is not generalized from this one record. |

**Scope of the confirmed result:** the October 11 controlled test confirmed that a file *modification* under `/home` is correctly detected by Rule 100002 and produces a Level 8 alert. This validates **only the tested modification scenario**. The controlled modification-validation objective of CASE-001 is closed; the overall investigation remains open.

**Reviewed 16 October 2026 records:** creation and deletion were each performed once as an individual controlled action, and the corresponding screenshots have been reviewed. The creation record shows built-in Rule 554 and the deletion record shows built-in Rule 553; custom Rule 100002 is absent from each reviewed record. These are reviewed records, not successful validations of Rule 100002 for creation or deletion. Screenshot review is distinct from source alert JSON review: the source alert JSON for these records has not been reviewed for this document, the creation timestamp discrepancy is unresolved, and the version of Rule 100002 loaded by the manager has not been verified. Rule 100002 depends on parent Rule 550, and the reviewed events were Rules 554 and 553, which is consistent with that dependency in those records. This is not a comprehensive root-cause analysis, and it is not proof that Rule 100002 can never fire on a creation or deletion event. The deletion was still alerted by a built-in rule; whether the custom rule should cover it is an open engineering question. Any ATT&CK mappings carried by built-in events are telemetry metadata, not evidence of malicious intent.

**Unresolved earlier creation claim:** an earlier report stated that Rules 554 and 100002 fired together during the creation. That claim is unsupported by the reviewed creation record and remains unexplained. It is not retained as a positive creation result, no cause is asserted, and the rule has not been changed.

**On-disk XML vs loaded rule:** the `local_rules.xml` inspection shows the file as it was at inspection time. It does not establish which version of Rule 100002 the running manager had loaded during the earlier tests. That version has not been verified.

**Evidence discrepancies (unresolved):** the creation screenshot's filename contains `creation-rule-553` although its content shows Rule 554; the evidence README reportedly references an older filename, `creation-rule-664`; and the creation timestamp differs between the screenshot and the evidence README (above). None of these has been fixed.

**Field-condition matching:** the exact matching behavior of the `file` field condition `/home/` (for example, whether it acts as an unanchored substring or regular-expression match, and how it treats case) has not been verified. Descriptions of the rule as matching "paths under `/home/`" are a working assumption.

The current results do **not** establish:

- Verified coverage for file *creation* or *deletion* events — each has one reviewed record in which Rule 100002 is absent, and deletion is an open coverage question for the custom rule
- Broader false-positive or false-negative behavior (not yet tested)
- That the rule has been tuned or hardened — no tuning has occurred
- Complete FIM coverage of `/home`, or any claim about malicious activity — these were controlled lab tests, not attacks

These results are further reviewed as part of investigation `CASE-001` (`investigations/CASE-001.md`), whose controlled modification-validation objective is closed while the overall investigation remains open: broader review, source-timestamp and loaded-rule-version verification, false-positive analysis, and tuning remain ongoing.

---

## 6. Known Limitations and Lessons

- **A single validated scenario is not complete coverage.** Rule 100002 is confirmed to work for the tested file modification. The reviewed creation and deletion records are records of individual controlled actions, not successful validations of Rule 100002 for those event types; they do not establish coverage for creation, deletion, other paths, or other file types.
- **Screenshot review is not source-alert review.** The 16 October records have been reviewed as screenshots, but the source alert JSON has not been checked, the creation timestamp is unresolved, and the loaded rule version is unconfirmed.
- **A built-in rule alert is not a custom rule alert.** The reviewed creation record showed built-in Rule 554, and the reviewed deletion record showed built-in Rule 553; custom Rule 100002 was absent from both. Rule 100002's documented parent dependency is `<if_sid>550</if_sid>`; Rules 553 and 554 are not its parent rules. A built-in alert for one FIM event type should not be read as coverage by the custom rule, and a rule that matches one event type should not be assumed to match the others.
- **Matching semantics are unverified.** The behavior of the `/home/` field condition has not been confirmed, so path-scope claims remain working assumptions.
- **A syntax check is not validation, and validation is not comprehensive coverage.** Rule 100002 moved from "syntax-valid only" to "confirmed firing" for one scenario — a meaningful step, but still a narrow one; the two should not be conflated with "the detection is done."
- **A FIM alert does not prove malicious activity.** Whether from Rule 550, 553, 554, or Rule 100002, a file-integrity alert only confirms a monitored file changed — not who changed it, why, or whether it was legitimate. That determination requires investigation (CASE-001, `docs/06-incident-response.md`), not inference from the alert alone.
- No false-positive or false-negative testing has been performed against Rule 100002 yet, and no tuning has occurred — both remain open work.

---

## 7. Future Plans

The following are planned and **not yet implemented**:

- Reviewing or obtaining the source alert JSON for the 16 October creation and deletion records, and settling the creation timestamp
- Verifying which version of Rule 100002 the manager had loaded during testing, if historical evidence permits
- Reviewing built-in Rules 550, 553, and 554 and verifying the matching behavior of the `file` field condition
- Reconciling the creation screenshot filename and the evidence README references in a later, separately approved documentation pass
- Investigating the deletion coverage question and, after review and approval, designing and testing any rule change
- Designing repeatable regression tests for file **creation**, **modification**, and **deletion** events under `/home`, with explicit pass/fail criteria
- False-positive / false-negative testing for Rule 100002 against legitimate `/home` activity, and tuning, only after review and approval
- Completing CASE-001's broader review, timeline, root-cause, and attribution work
- Broader telemetry sources: authentication activity and process/command execution
- MITRE ATT&CK technique mapping for implemented detections
- Additional detection rules beyond File Integrity Monitoring
- Purple-team validation (detection rate, detection time, before/after comparison)
- Attack mutation testing (varying attacker technique to test detection resilience)

These remain future work and are not claimed as current capabilities.
