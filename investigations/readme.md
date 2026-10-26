# investigations/

This directory stores structured SOC investigation records for SENTINEL — the case files produced when a Wazuh alert, suspicious event, controlled attack, or threat-hunting observation is examined in detail.

It explains how the directory is organized and how investigations are recorded. For broader methodology, see [`docs/06-incident-response.md`](../docs/06-incident-response.md), [`docs/05-detection-engineering.md`](../docs/05-detection-engineering.md), [`docs/07-testing-and-metrics.md`](../docs/07-testing-and-metrics.md), and [`docs/08-lessons-and-failures.md`](../docs/08-lessons-and-failures.md).

---

## Purpose

Investigation sits between detection and response in SENTINEL's core lifecycle:

SIMULATE → DETECT → INVESTIGATE → RESPOND → MEASURE → IMPROVE → RETEST

It answers: what happened, when, on which system, based on what evidence — and what is still unknown.

---

## Investigation Principles

- Evidence first — conclusions rest on observable evidence, not assumption.
- Timeline driven — events are placed in chronological order whenever possible.
- Hypothesis driven — hypotheses are tested against evidence.
- Traceability — important conclusions trace back to specific evidence.
- Separation of fact and inference — fact, interpretation, hypothesis, conclusion, and unknowns stay distinct.
- Reproducibility — another analyst can follow how a conclusion was reached.
- Preserve uncertainty — if evidence is insufficient, the record says so.

---

## Investigation Lifecycle

```text
ALERT / EVENT
      |
   TRIAGE
      |
    SCOPE
      |
COLLECT EVIDENCE
      |
BUILD TIMELINE
      |
ANALYZE ACTIVITY
      |
 IDENTIFY IOCs
      |
 MAP TECHNIQUES
      |
FORM / TEST HYPOTHESES
      |
ASSESS ROOT CAUSE / DOCUMENT UNKNOWN
      |
 ASSESS IMPACT
      |
   CONCLUDE
      |
RESPONSE / IMPROVEMENT
      |
  DOCUMENT
      |
   RETEST
```

> The workflow may vary by scenario — not every investigation needs every stage, and any stage may loop back as evidence develops.

---

## Investigation States

**v0.3 — SOC Investigation (in progress)**

CASE-001 remains open overall. Evidence reconciliation for the reviewed CASE-001 scope is closed: the controlled modification tests (11 and 26 October 2026) are recorded, and the 16 October creation/deletion observations have been reconciled against the reviewed source records. Background configuration and cache changes were observed in the 11 October review, but process-level attribution for every event was not established.

Broader investigation and detection-engineering work remains open, including resolving why custom Rule "100002" was absent from the reviewed 16 October creation/deletion records, broader false-positive/false-negative testing, repeatable regression testing, and detection tuning. Additional cases remain future work.

> "Inconclusive" is a valid outcome when evidence is insufficient. Investigations are not forced to produce a finding they cannot support.

---

## Case Identifiers

Cases are named `CASE-001`, `CASE-002`, `CASE-003`, and so on.

- IDs are unique and are never reused.
- Once assigned, a case ID remains stable.
- Cases reference related evidence, detections, tests, and response actions where applicable.

> Case numbers are assigned only when a real investigation record is created.

---

## Case Record Structure

Each case is a single Markdown file (e.g. `CASE-001.md`). Sections contain only what is actually known; unresolved or not-yet-performed items are stated explicitly.

```markdown
# Case ID / Title
## Incident Summary
## Status        (New | Triage | Investigating | Contained / Awaiting Response | Resolved | Closed | Inconclusive)
## Severity      (only when supported by the severity methodology)
## Affected Assets
## Detection / Trigger      (do not invent an alert ID)
## Investigation Objective
## Initial Hypothesis       (labeled as a hypothesis)
## Evidence Collected       (repository-relative links)
## Timeline                 (do not fabricate timestamps)
## Indicators of Compromise (only those actually observed)
## MITRE ATT&CK Mapping     (only if justified; otherwise state none validated)
## Analysis                 (separate fact, interpretation, hypothesis, conclusion)
## Attack / Activity Chain  (only stages supported by evidence)
## Root Cause               (only when supported; else "Root cause not determined.")
## Impact Assessment        (do not exaggerate)
## Response                 (else "Response not yet performed.")
## Detection Performance    (do not invent metrics)
## Lessons Learned
## Improvements
## Retest                   (Passed | Failed | Partial | Not yet retested)
```

---

## Working Guidelines

- **Triage:** decide whether the event is worth investigating, what asset is involved, whether the activity is expected or part of a controlled SENTINEL test, and what to examine next. Do not declare an incident confirmed before the evidence supports it.
- **Timeline:** use only telemetry actually available; never invent timestamps. Distinguish event, detection, investigation, and response time where possible.
- **IOCs:** collect only from actual evidence, with type, value, source, observed time, and context. Avoid unnecessary sensitive data.
- **MITRE ATT&CK:** map only observed, traceable behavior. No validated mapping is an acceptable outcome.
- **Threat hunting:** planned future work, not a current capability.
- **Evidence:** store under the matching version directory in [`evidence/`](../evidence/). Keep it relevant, sanitized, and traceable.

> Never commit passwords, API keys, tokens, private keys, real credentials, personal information, production data, or unnecessary sensitive telemetry.

---

## Relationship to Other SENTINEL Documentation

| Document | Role |
|---|---|
| [`investigations/README.md`](README.md) (this file) | Directory-level guide for how investigation records are organized |
| [`investigations/CASE-001.md`](CASE-001.md) | CASE-001 — controlled validation of custom Wazuh FIM rule 100002, creation/deletion evidence reconciliation, and review of related file-integrity events |
| [`investigations/fim-rule-100002-investigation.md`](fim-rule-100002-investigation.md) | Rule 100002 lifecycle-event scope investigation |
| [`docs/06-incident-response.md`](../docs/06-incident-response.md) | Incident-response methodology and workflow |
| [`docs/05-detection-engineering.md`](../docs/05-detection-engineering.md) | How detections are designed and validated |
| [`docs/07-testing-and-metrics.md`](../docs/07-testing-and-metrics.md) | Testing, validation, and measurement methodology |
| [`docs/08-lessons-and-failures.md`](../docs/08-lessons-and-failures.md) | Failure-driven engineering approach |
| [`failure-log/`](../failure-log/) | Meaningful failures during development and testing |
| [`evidence/`](../evidence/) | Supporting investigation and testing evidence |
| [`detections/`](../detections/) | Detection implementations |
| [`metrics/`](../metrics/) | Measured performance and validation results |
| [`CHANGELOG.md`](../CHANGELOG.md) | Project-level milestones and architecture changes |

---

## Investigation Index

| Case ID | Investigation | Status | Primary Detection |
|---|---|---|---|
| [CASE-001](CASE-001.md) | Controlled FIM Validation and Evidence Reconciliation (modification, creation, deletion) | 🟡 Open — evidence reconciliation for the reviewed scope closed | Wazuh FIM, custom Rule 100002 |

---

## CASE-001 Summary

CASE-001 documents controlled file-integrity tests on SENTINEL-LINUX01. Details are in [`CASE-001.md`](CASE-001.md) and [`fim-rule-100002-investigation.md`](fim-rule-100002-investigation.md); this is a short summary.

**Observed — modification:**

- 11 October 2026: existing screenshots support a Level 8 custom Rule 100002 alert for a controlled modification of `/home/sentinel-admin/sentinel-fim-validation.txt` (`2026-10-11T20:25:14.746+0530`). The original source alert log was not recovered during the 26 October review.
- 26 October 2026: two controlled modifications of `/home/sentinel-admin/sentinel-v02-mod-test.txt` produced Rule 100002 Level 8 alerts at `2026-10-26T21:38:27.910+0530` (size 0 → 23 bytes) and `2026-10-26T21:38:48.473+0530` (size 23 → 61 bytes).
- These validate the tested modification scenarios only. They say nothing about creation or deletion coverage.

**Observed — creation and deletion (16 October 2026, `/home/sentinel-admin/sentinel-audit-test.txt`):**

- The reviewed creation record showed built-in Rule 554 at `2026-10-16T11:40:06.007+0530`. Rule 100002 was absent from that record.
- The reviewed deletion record showed built-in Rule 553 at `2026-10-16T12:31:32.819+0530`. Rule 100002 was absent from that record.
- These statements are limited to the two reviewed records and do not show how Rule 100002 behaves for other creation or deletion events. Earlier versions of this guide recorded Rule 100002 as firing on creation; that is not supported by the reviewed records.

**Unresolved:** why Rule 100002 was absent from the two reviewed records. Rule 100002 has been described as depending on parent Rule 550 (`<if_sid>550</if_sid>`), but the active rule definition and its matching behavior have not been re-verified, and that dependency is not asserted as the cause. No rule change or tuning has been made. A built-in rule firing does not by itself establish whether custom Rule 100002 should cover the same event.

Additional file-integrity events involving desktop configuration, application state, and cache files were documented as observed background activity within the 11 October reviewed dataset; individual process attribution was not conclusively established.

> The case remains open. Evidence reconciliation for the reviewed scope is closed. Resolution of the Rule 100002 absence, broader false-positive/false-negative testing, and detection-rule tuning remain follow-up tasks.

Supporting evidence: existing screenshots for the 11 October modification test are stored in [`evidence/v0.3/`](../evidence/v0.3/). A screenshot of the 26 October terminal output was reported as uploaded to `evidence/v0.2/v0.2-oct26-controlled-modification-source-alerts-new.png`; that path has not been verified here. The 11 October original source log and the 16 October raw records are not claimed to be committed to the repository.

---

## Investigation → Response and Detection Improvement

Detection → Investigation → Findings → Response → Measurement → Improvement → Retest

An investigation should not automatically trigger destructive response actions. Response actions are deliberate and documented separately; the investigation provides the evidence base for those decisions.

Investigations feed back into detection engineering: a detection gap leads to identifying missing telemetry or weak logic, improving the detection, testing it, and retesting the original scenario. CASE-001 confirmed the tested modification-detection behavior of custom Rule 100002, left the absence of Rule 100002 from the reviewed creation/deletion records unresolved, and identified broad home-directory matching as an area for further evaluation. Proposed tuning must be tested before its effectiveness is claimed.

> Attack DNA and Attack Mutation are not currently implemented in SENTINEL. A future use of this directory may be to record how attacker behavior and detection performance change under mutation.

---

## Current Status

- ✅ Investigation methodology and directory structure are documented.
- ✅ SENTINEL-WAZUH and SENTINEL-LINUX01 provide the telemetry foundation for the current investigation workflow.
- ✅ CASE-001 is documented in [`investigations/CASE-001.md`](CASE-001.md) and [`investigations/fim-rule-100002-investigation.md`](fim-rule-100002-investigation.md); existing supporting evidence for the 11 October modification test is under [`evidence/v0.3/`](../evidence/v0.3/).
- ✅ Custom Rule 100002 detected the controlled file modifications tested on 11 and 26 October 2026 (tested scenarios only).
- ✅ The 16 October creation and deletion records were reviewed: built-in Rules 554 and 553 were observed, and Rule 100002 was absent from both records.
- ✅ Additional home-directory FIM events were reviewed, and potential noise from routine desktop activity was documented with appropriate attribution limitations.
- 🟡 Open: why Rule 100002 was absent from the reviewed creation/deletion records. The active rule definition and matching behavior have not been re-verified, and no root cause is asserted.
- ⬜ Broader false-positive/false-negative testing, repeatable regression testing, detection tuning, and validation of tuning effectiveness remain outstanding.
- ⬜ Threat hunting and additional investigation cases remain planned; future investigations should receive unique case IDs and follow the evidence-first principles described in this guide.
- ⬜ Attack Mutation is not implemented.
