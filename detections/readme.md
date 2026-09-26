# SENTINEL Detection Library

This directory contains the actual detection definitions, rules, configurations, test references, and supporting artifacts developed for SENTINEL. It is the **implementation layer** of SENTINEL's detection-engineering methodology.

**This file is not:**
- The main project README
- A replacement for `docs/05-detection-engineering.md`

The distinction is deliberate:

| Document | Explains |
|---|---|
| `docs/05-detection-engineering.md` | **How** SENTINEL engineers detections (methodology) |
| `detections/README.md` (this file) | **Where** actual detection implementations live and how they should be organized |

The repository is currently at **v0.1 — infrastructure foundation**. Meaningful detection engineering begins in v0.2. This document contains no invented detection IDs, Wazuh rule IDs, MITRE ATT&CK mappings, alert results, test results, or detection metrics beyond clearly labeled templates and examples.

---

## 1. Purpose

Detections are the operational implementation of the methodology described in `docs/05-detection-engineering.md`. A detection should eventually connect:

```
Threat → Behavior → Telemetry → Detection Logic → Alert →
Investigation → Validation → Measurement → Tuning → Retest
```

This directory holds real detection artifacts as they're built — not theoretical descriptions of detections that don't exist yet.

---

## 2. Current Status

**Current version:** v0.1 — Foundation

### Current infrastructure

| Host | Role | Details |
|---|---|---|
| SENTINEL-WAZUH | SOC / monitoring platform | Wazuh 4.14.8, 10.10.10.10 |
| SENTINEL-KALI | Controlled attacker environment | 10.10.10.20 |
| SENTINEL-LINUX01 | Monitored Linux endpoint | Ubuntu 24.04.5 LTS, 10.10.10.40, Wazuh Agent 4.14.8, Agent ID 001, Active |

### Current state
- Wazuh operational
- Linux endpoint connected
- Lab networking established
- Detection library structure established (this directory)

### Not yet completed
- First validated detection
- First controlled detection test
- Detection performance measurements
- Detection resilience testing
- Attack mutation testing

**No detection in this directory is described as validated unless real test evidence backs that claim.**

---

## 3. Directory Role

This directory is intended to eventually hold:

- Detection definitions
- Detection rule files
- Detection configuration
- Detection metadata
- Detection test references
- Detection documentation
- Supporting scripts, where appropriate

**Never placed here:** large raw logs, VM disks, passwords, API keys, private keys, secrets, large telemetry datasets, or unnecessary packet captures. Those belong outside the repository or in controlled evidence storage.

---

## 4. Detection Lifecycle

```
DRAFT → TELEMETRY VERIFIED → TESTED → TUNED → VALIDATED → MONITORED → RETESTED
```

Also possible at any stage: `FAILED`, `RETIRED`.

| Status | Meaning |
|---|---|
| Draft | Specification written, not yet implemented |
| Telemetry Verified | Required telemetry confirmed available and reliable |
| Tested | A controlled test scenario has been executed at least once |
| Tuned | Logic adjusted based on test results |
| Validated | Meets the validation criteria in `docs/05-detection-engineering.md` |
| Monitored | Running in the lab under ongoing observation |
| Retested | Re-run after tuning or after a mutation attempt |
| Failed | Did not detect as expected; under investigation |
| Retired | No longer maintained or relevant |

**A detection is not Validated merely because the rule exists.** Validation requires actual testing and documented evidence.

---

## 5. Detection Naming Convention

Format: `DET-001`, `DET-002`, `DET-003`, etc. `DET` stands for Detection. No detection IDs beyond illustrative examples are created in this document — real IDs are assigned when a real detection is authored. If the project grows significantly, IDs may later incorporate categories, but unnecessary complexity is avoided for now.

---

## 6. Individual Detection Structure

Recommended structure once real detections exist:

```
detections/
├── README.md
├── DET-001/
│   ├── README.md
│   └── ...
└── DET-002/
    ├── README.md
    └── ...
```

**`DET-001` and `DET-002` above are illustrative only — neither currently exists.** Each detection can get its own directory once the artifact is complex enough (rule file, test script, notes, evidence links). For simple detections, a single file may be sufficient; detections are not forced into a directory structure they don't need.

---

## 7. Detection Metadata

Every real detection should eventually document:

- Detection ID
- Detection Name
- Version
- Status
- Objective
- Threat
- Affected Asset
- Telemetry Source
- Detection Logic
- Expected Behavior
- Severity
- MITRE ATT&CK Mapping
- False Positive Sources
- Test Scenario
- Evidence
- Known Limitations
- Related Investigation
- Related Response
- Last Tested
- Retest Required

No field above is filled with invented values anywhere in this repository — they're left blank or marked "not yet determined" until real information exists.

---

## 8. Detection Template

> **⚠️ TEMPLATE — this is not a real detection. It illustrates the expected format only.**

```markdown
# DET-XXX — Detection Name

## Status
DRAFT

## Objective
What behavior is this detection intended to identify?

## Threat
What threat or suspicious behavior does it address?

## Asset
Which asset is monitored?

## Telemetry Source
What telemetry is required?

## Detection Logic
What conditions should cause the detection to trigger?

## Expected Behavior
What behavior should produce the detection?

## Severity
To be determined based on the actual scenario.

## MITRE ATT&CK
To be mapped after the behavior is defined and verified.

## False Positive Sources
What legitimate behavior may trigger this detection?

## Test Scenario
Which controlled scenario will validate the detection?

## Evidence
Link to actual evidence after testing.

## Investigation
What information should the analyst examine?

## Response
What response procedure may apply?

## Known Limitations
Document known blind spots.

## Test History
Record actual tests only.

## Retest
Document future or completed retesting.
```

---

## 9. Detection Design Principle

**Telemetry comes before detection logic.**

```
Threat
  ↓
Required Behavior
  ↓
Required Telemetry
  ↓
Telemetry Verification
  ↓
Detection Logic
  ↓
Test
  ↓
Validation
```

A detection cannot reliably detect information that the endpoint never generates or the SOC never receives — no amount of clever rule logic compensates for missing telemetry.

---

## 10. Detection Types

SENTINEL may eventually contain multiple detection approaches:

- **Signature / Rule-Based** — matches known event characteristics
- **Threshold / Frequency** — detects repeated behavior within a defined period
- **Correlation** — combines multiple related events into a stronger signal
- **Sequence-Based** — detects a meaningful sequence of events
- **Behavioral** — detects suspicious patterns rather than one fixed event

None of these types are currently implemented — this list describes the range of approaches available once real detections are built.

---

## 11. False Positive Handling

Every important detection should account for legitimate activity that might trigger it. Document potential false-positive sources for each detection.

When a false positive is actually discovered:

```
Detection → Benign Activity → False Positive → Analyze → Tune → Test Again
```

Reference: `failure-log/false-positives.md`. No false positives are invented here — none have occurred yet.

---

## 12. False Negative Handling

If expected malicious test behavior occurs but the detection fails to fire, record it as a detection failure/false negative where the test design supports that classification.

```
Attack → Expected Detection → No Detection → Investigate Telemetry →
Investigate Logic → Fix → Retest
```

Reference: `failure-log/detection-failures.md`. Failed detections are never hidden or omitted from the record.

---

## 13. Detection Testing

Every meaningful detection should eventually have a corresponding controlled test, defined in `docs/07-testing-and-matrices.md`. A test should specify:

- Objective
- Preconditions
- Attack/activity
- Expected telemetry
- Expected detection
- Evidence
- Result
- Failure analysis
- Retest

No fake test IDs or results are created in advance of real testing.

---

## 14. Evidence

Detection evidence lives under `evidence/`, organized by version. Example structure (illustrative only):

```
evidence/
└── v0.2/
    └── detection-tests/
        └── DET-001/
```

Actual evidence directories are created only when actual tests are performed. Possible evidence: Wazuh alerts, relevant logs, screenshots, terminal output, detection configuration, test results, investigation notes, before/after comparisons. Evidence is never fabricated.

---

## 15. Detection → Investigation

A detection should provide enough information to support investigation. A good detection should help answer:

- What happened? When? Which asset? Which account?
- Which process? Which command? Which file?
- Which network connection?
- What happened immediately before? Immediately after?

The exact context actually available depends entirely on the telemetry configured — no context is claimed until it's been verified to exist.

---

## 16. Detection → Response

Detections may eventually connect to incident-response workflows:

```
Detection → Triage → Investigation → Response
```

Potential future response actions: endpoint isolation, process termination, account disablement, indicator blocking, evidence collection. **No automated response currently exists.**

---

## 17. Detection Test Matrix Connection

Every mature detection should eventually appear in `docs/07-testing-and-matrices.md`'s detection coverage matrix, with fields including:

| Field | Description |
|---|---|
| Detection ID | Links back to the artifact in this directory |
| Threat | Threat being addressed |
| Technique | MITRE ATT&CK technique, where confidently applicable |
| Telemetry | Source(s) the detection depends on |
| Expected Result | What should happen when tested |
| Actual Result | What actually happened |
| Status | Current lifecycle status (Section 4) |
| Evidence | Link to supporting evidence |

This keeps the detection library (implementation) and the testing matrix (validation record) in sync — a detection's row in the matrix should never claim a status that this directory's own artifact doesn't support.

---

## 18. Repository Hygiene

- No VM disks, credentials, API keys, tokens, or private keys are ever committed here.
- No large raw telemetry, packet captures, or bulk logs are committed — sanitized excerpts used as evidence go under `evidence/` instead.
- Detection files are documented with enough context (objective, telemetry source, reasoning) that someone unfamiliar with the project could understand why the detection exists, not just what it matches.
- A detection's status label in its own file and its row in the testing matrix should always agree — if one changes, update the other in the same pass.

---

## 19. Current Detection Inventory

| Detection ID | Name | Status | Notes |
|---|---|---|---|
| *(none yet)* | — | — | No detections have been authored as of v0.1 |

This table will be populated starting in v0.2, as real detections are drafted, tested, and validated.

---

## 20. Maintenance

Update this README when:

- The directory structure or naming convention changes.
- A new detection type is introduced.
- The relationship between this directory and `docs/05-detection-engineering.md` or `docs/07-testing-and-matrices.md` changes.
- The repository hygiene rules need revision.

Individual detection files are updated on their own schedule as they move through the lifecycle in Section 4 — this README describes the library's organization, not the status of any single detection.

---

## 21. Final Status

**Current phase:** v0.1 — Foundation. This directory exists and is structured, but contains no completed detections yet.

**Next phase:** v0.2 — Detection Engineering & Linux Telemetry, during which the first detection specifications, telemetry verification, and controlled tests are expected to populate Section 19's inventory.

This file describes where and how SENTINEL's detections are organized. It does not claim any detection is implemented, tested, or validated beyond what Section 19 actually lists.
