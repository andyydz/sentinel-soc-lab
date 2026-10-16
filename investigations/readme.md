investigations/

This directory stores structured SOC investigation records for SENTINEL — the case files produced when a Wazuh alert, suspicious event, controlled attack, or threat-hunting observation is examined in detail.

It explains how the directory is organized and how investigations are recorded. For broader methodology, see [`docs/06-incident-response.md`](../docs/06-incident-response.md), [`docs/05-detection-engineering.md`](../docs/05-detection-engineering.md), [`docs/07-testing-and-metrics.md`](../docs/07-testing-and-metrics.md), and [`docs/08-lessons-and-failures.md`](../docs/08-lessons-and-failures.md).

---

Purpose

Investigation sits between detection and response in SENTINEL's core lifecycle:

SIMULATE → DETECT → INVESTIGATE → RESPOND → MEASURE → IMPROVE → RETEST

It answers: what happened, when, on which system, based on what evidence — and what is still unknown.

---

Investigation Principles

- Evidence first — conclusions rest on observable evidence, not assumption.
- Timeline driven — events are placed in chronological order whenever possible.
- Hypothesis driven — hypotheses are tested against evidence.
- Traceability — important conclusions trace back to specific evidence.
- Separation of fact and inference — fact, interpretation, hypothesis, conclusion, and unknowns stay distinct.
- Reproducibility — another analyst can follow how a conclusion was reached.
- Preserve uncertainty — if evidence is insufficient, the record says so.

---

Investigation Lifecycle

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

Investigation States

v0.3 — SOC Investigation (in progress)

CASE-001 is documented and closed only for its controlled file-modification validation objective. It records the custom Rule "100002" Level 8 alert, supporting FIM evidence, and a review of related endpoint events. Background configuration and cache changes were observed, but process-level attribution for every event and a definitive root cause for those unrelated changes were not established.

Broader investigation and detection-engineering work remains open, including creation and deletion validation, broader false-positive/false-negative testing, and detection tuning. Additional cases remain future work.

> "Inconclusive" is a valid outcome when evidence is insufficient. Investigations are not forced to produce a finding they cannot support.

---

Case Identifiers

Cases are named `CASE-001`, `CASE-002`, `CASE-003`, and so on.

- IDs are unique and are never reused.
- Once assigned, a case ID remains stable.
- Cases reference related evidence, detections, tests, and response actions where applicable.

> Case numbers are assigned only when a real investigation record is created.

---

Case Record Structure

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

Working Guidelines

- **Triage:** decide whether the event is worth investigating, what asset is involved, whether the activity is expected or part of a controlled SENTINEL test, and what to examine next. Do not declare an incident confirmed before the evidence supports it.
- **Timeline:** use only telemetry actually available; never invent timestamps. Distinguish event, detection, investigation, and response time where possible.
- **IOCs:** collect only from actual evidence, with type, value, source, observed time, and context. Avoid unnecessary sensitive data.
- **MITRE ATT&CK:** map only observed, traceable behavior. No validated mapping is an acceptable outcome.
- **Threat hunting:** planned future work, not a current capability.
- **Evidence:** store under the matching version directory in [`evidence/`](../evidence/). Keep it relevant, sanitized, and traceable.

> Never commit passwords, API keys, tokens, private keys, real credentials, personal information, production data, or unnecessary sensitive telemetry.

---

Relationship to Other SENTINEL Documentation

Document	Role	
[`investigations/README.md`](README.md) (this file)	Directory-level guide for how investigation records are organized	
[`investigations/CASE-001.md`](CASE-001.md)	CASE-001 — controlled validation of custom Wazuh FIM rule 100002 and review of related file-integrity events	
[`docs/06-incident-response.md`](../docs/06-incident-response.md)	Incident-response methodology and workflow	
[`docs/05-detection-engineering.md`](../docs/05-detection-engineering.md)	How detections are designed and validated	
[`docs/07-testing-and-metrics.md`](../docs/07-testing-and-metrics.md)	Testing, validation, and measurement methodology	
[`docs/08-lessons-and-failures.md`](../docs/08-lessons-and-failures.md)	Failure-driven engineering approach	
[`failure-log/`](../failure-log/)	Meaningful failures during development and testing	
[`evidence/`](../evidence/)	Supporting investigation and testing evidence	
[`detections/`](../detections/)	Detection implementations	
[`metrics/`](../metrics/)	Measured performance and validation results	
[`CHANGELOG.md`](../CHANGELOG.md)	Project-level milestones and architecture changes	

---

Investigation Index

Case ID	Investigation	Status	Primary Detection	
[CASE-001](CASE-001.md)	Controlled FIM Modification Validation	✅ Closed — controlled validation completed	Wazuh FIM, custom Rule 100002	

---

CASE-001 Summary

CASE-001 documents a controlled modification of `/home/sentinel-admin/sentinel-fim-validation.txt` on SENTINEL-LINUX01, which generated a Wazuh Level 8 alert under custom Rule 100002.

Additional file-integrity events involving desktop configuration, application state, and cache files were documented as observed background activity within the reviewed dataset; individual process attribution was not conclusively established.

> The case is closed for its controlled validation objective. Creation and deletion testing, broader false-positive/false-negative testing, and detection-rule tuning remain follow-up tasks.

Supporting evidence: stored in [`evidence/v0.3/`](../evidence/v0.3/).

---

Investigation → Response and Detection Improvement

Detection → Investigation → Findings → Response → Measurement → Improvement → Retest

An investigation should not automatically trigger destructive response actions. Response actions are deliberate and documented separately; the investigation provides the evidence base for those decisions.

Investigations feed back into detection engineering: a detection gap leads to identifying missing telemetry or weak logic, improving the detection, testing it, and retesting the original scenario. CASE-001 confirmed the tested modification-detection behavior of custom Rule 100002 and identified broad home-directory matching as an area for further evaluation. Proposed tuning must be tested before its effectiveness is claimed.

> Attack DNA and Attack Mutation are not currently implemented in SENTINEL. A future use of this directory may be to record how attacker behavior and detection performance change under mutation.

---

Current Status

- ✅ Investigation methodology and directory structure are documented.
- ✅ SENTINEL-WAZUH and SENTINEL-LINUX01 provide the telemetry foundation for the current investigation workflow.
- ✅ CASE-001 has been documented in [`investigations/CASE-001.md`](CASE-001.md), with supporting evidence under [`evidence/v0.3/`](../evidence/v0.3/).
- ✅ Custom Rule 100002 successfully detected the controlled file modification tested in CASE-001.
- ✅ Additional home-directory FIM events were reviewed, and potential noise from routine desktop activity was documented with appropriate attribution limitations.
- ⬜ Creation and deletion validation, broader false-positive/false-negative testing, detection tuning, and validation of tuning effectiveness remain outstanding.
- ⬜ Future investigations should receive unique case IDs and follow the evidence-first principles described in this guide.
