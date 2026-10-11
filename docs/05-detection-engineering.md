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

A detection only reaches **Validated** once Test and Validate have both produced the expected, documented result. Passing a syntax check is not the same as passing this lifecycle — see Section 6.

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
| Telemetry Source | Wazuh Syscheck (File Integrity Monitoring), real-time, scoped to `/home` on SENTINEL-LINUX01 |
| Detection Logic | Matches on Syscheck's file-integrity-changed event for the monitored path |
| Expected Alert | Level 8 alert identifying the changed file |
| Severity | Intended: Level 8 (custom rule); Observed: Level 7 via Wazuh's built-in Rule 550 |
| Test Procedure | Controlled file modification performed directly on SENTINEL-LINUX01 within `/home` |
| Evidence | `evidence/v0.2/` |

---

## 4. Testing and Validation Methodology

Every test compares an **expected result** against an **actual result**, and the outcome is recorded regardless of whether it passed:

```
Expected: File modification → Syscheck telemetry → Rule fires → Alert generated
Actual:   [recorded as observed, not assumed]
```

- **Pass** — the expected telemetry and alert were both observed.
- **Fail** — the expected behavior did not occur; the failure is investigated and documented, not hidden.
- **Unresolved / Inconclusive** — part of the chain was confirmed (e.g., telemetry reached the manager) but the specific detection logic under test was not confirmed to fire. This status exists specifically so a partial result isn't overstated as a pass — see Section 5.

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
| Built-in Wazuh **Rule 550** (Level 7, "Integrity checksum changed") | **Observed** during a controlled file-modification test — confirms the FIM telemetry pipeline works end to end |
| Custom **Rule 100002** (target: Level 8) | Implemented in `local_rules.xml`; passed Wazuh's configuration syntax check; **end-to-end validation unresolved** — no confirmed Level 8 alert from this rule yet |

The controlled test confirmed that a file change under `/home` is detected and reaches the Wazuh Manager (via Rule 550). It did **not** confirm that the custom Rule 100002 logic itself fires. These are two separate claims, and only the first is currently supported by evidence.

---

## 6. Known Limitations and Lessons

- **A syntax check is not validation.** Rule 100002 is syntactically valid configuration — Wazuh accepted it without error. That is necessary but not sufficient to call it a working detection; it has not been confirmed to fire against the test activity it was written for.
- **Rule 550 firing does not prove Rule 100002 works.** They are different rules observing related telemetry. One succeeding says nothing about the other's correctness.
- **A FIM alert does not prove malicious activity.** Whether from Rule 550 or (eventually) Rule 100002, a file-integrity alert only confirms a monitored file changed — not who changed it, why, or whether it was legitimate. That determination requires investigation (planned for v0.3), not inference from the alert alone.
- No false-positive or false-negative testing has been performed against Rule 100002, since it has not yet produced a confirmed alert to evaluate.

---

## 7. Future Plans

The following are planned and **not yet implemented**:

- Reproducing and confirming a successful Rule 100002 alert (immediate next step for this detection)
- Broader telemetry sources: authentication activity and process/command execution
- MITRE ATT&CK technique mapping for implemented detections
- Additional detection rules beyond File Integrity Monitoring
- False-positive / false-negative testing at scale
- Purple-team validation (detection rate, detection time, before/after comparison)
- Attack mutation testing (varying attacker technique to test detection resilience)

These remain future work and are not claimed as current capabilities.
