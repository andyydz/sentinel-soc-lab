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

CASE-001 remains open overall. Its controlled file-modification validation objective is closed: on 11 October 2026, custom Rule "100002" generated a Level 8 alert for the controlled modification test, with supporting FIM evidence and a review of related endpoint events. Background configuration and cache changes were observed, but process-level attribution for every event and a definitive root cause for those unrelated changes were not established.

File creation and deletion tests were reportedly performed on 16 October 2026, but their results remain unverified pending independent review of the raw alerts and the active rule definitions. Deletion coverage by custom Rule "100002" is an open question.

Broader investigation and detection-engineering work remains open, including review of the reported creation/deletion results, broader false-positive/false-negative testing, and detection tuning. Additional cases remain future work.

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
| [`investigations/CASE-001.md`](CASE-001.md) | CASE-001 — controlled validation of custom Wazuh FIM rule 100002 and review of related file-integrity events |
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
| [CASE-001](CASE-001.md) | Controlled FIM Modification Validation | 🟡 Open — modification-validation objective closed | Wazuh FIM, custom Rule 100002 |

---

## CASE-001 Summary

CASE-001 documents a controlled modification of `/home/sentinel-admin/sentinel-fim-validation.txt` on SENTINEL-LINUX01.

**Confirmed:** On 11 October 2026, custom Rule 100002 generated a Level 8 alert for that controlled modification. This confirms the tested modification scenario only.

**Reported, pending review:** On 16 October 2026, creation of `/home/sentinel-admin/sentinel-audit-test.txt` reportedly triggered built-in Rule 554 and custom Rule 100002.

**Reported, pending review:** Deletion of that file reportedly triggered built-in Rule 553, while custom Rule 100002 reportedly did not. This is an open custom-rule coverage question; no cause is asserted, and no rule change or tuning has been made.

**Unresolved:** The reported creation alert is inconsistent with the reported parent condition `<if_sid>550</if_sid>`. The raw alerts and active rule definitions have not yet been independently reviewed.

The creation and deletion tests were reportedly performed, but their results remain unverified pending raw-alert and active-rule review. A built-in rule firing does not by itself establish whether custom Rule 100002 should cover the same event.

Additional file-integrity events involving desktop configuration, application state, and cache files were documented as observed background activity within the reviewed dataset; individual process attribution was not conclusively established.

> The case remains open. Its controlled modification-validation objective is closed. Review of the reported creation/deletion results, broader false-positive/false-negative testing, and detection-rule tuning remain follow-up tasks.

Supporting evidence: stored in [`evidence/v0.3/`](../evidence/v0.3/). This covers the confirmed 11 October modification test; the 16 October raw alerts and related artifacts are not confirmed as saved in the repository.

---

## Investigation → Response and Detection Improvement

Detection → Investigation → Findings → Response → Measurement → Improvement → Retest

An investigation should not automatically trigger destructive response actions. Response actions are deliberate and documented separately; the investigation provides the evidence base for those decisions.

Investigations feed back into detection engineering: a detection gap leads to identifying missing telemetry or weak logic, improving the detection, testing it, and retesting the original scenario. CASE-001 confirmed the tested modification-detection behavior of custom Rule 100002 and identified broad home-directory matching as an area for further evaluation. Proposed tuning must be tested before its effectiveness is claimed.

> Attack DNA and Attack Mutation are not currently implemented in SENTINEL. A future use of this directory may be to record how attacker behavior and detection performance change under mutation.

---

## Current Status

- ✅ Investigation methodology and directory structure are documented.
- ✅ SENTINEL-WAZUH and SENTINEL-LINUX01 provide the telemetry foundation for the current investigation workflow.
- ✅ CASE-001 is documented in [`investigations/CASE-001.md`](CASE-001.md), with existing supporting evidence for the confirmed 11 October modification test under [`evidence/v0.3/`](../evidence/v0.3/).
- ✅ Custom Rule 100002 successfully detected the controlled file modification tested in CASE-001 (11 October 2026).
- ✅ Additional home-directory FIM events were reviewed, and potential noise from routine desktop activity was documented with appropriate attribution limitations.
- 🟡 Reported, pending review (16 October 2026): creation reportedly triggered Rules 554 and 100002; deletion reportedly triggered Rule 553 but not Rule 100002. Raw alerts and active rule definitions have not been independently reviewed, and the creation alert remains inconsistent with the reported `<if_sid>550</if_sid>` parent condition.
- 🟡 Open: whether custom Rule 100002 covers file deletion.
- ⬜ Review of the reported creation/deletion results, broader false-positive/false-negative testing, detection tuning, and validation of tuning effectiveness remain outstanding.
- ⬜ Threat hunting and additional investigation cases remain planned; future investigations should receive unique case IDs and follow the evidence-first principles described in this guide.
- ⬜ Attack Mutation is not implemented.
