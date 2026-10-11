## investigations/

This directory stores structured SOC investigation records for SENTINEL — the case files produced when a Wazuh alert, suspicious event, controlled attack, or threat-hunting observation is examined in detail.

This README explains how the directory is organized and how investigations should be conducted and recorded. It does not restate SENTINEL's broader incident-response methodology ([`docs/06-incident-response.md`](../docs/06-incident-response.md)), detection-engineering approach ([`docs/05-detection-engineering.md`](../docs/05-detection-engineering.md)), testing methodology ([`docs/07-testing-and-matrices.md`](../docs/07-testing-and-matrices.md)), or failure-driven engineering philosophy ([`docs/08-lessons-and-failures.md`](../docs/08-lessons-and-failures.md)) — see those documents for that material.

---

## Purpose

An investigation begins when there is something worth examining: a Wazuh alert, unexpected endpoint activity, unusual authentication behavior, a controlled attack, a detection test, a threat-hunting finding, a detection anomaly, or any potentially malicious event. The purpose of this directory is to preserve that investigation from initial observation through conclusion, and to turn raw telemetry and alerts into a defensible, evidence-backed understanding of what happened.

The investigation phase sits between detection and response in SENTINEL's core lifecycle:

SIMULATE → DETECT → INVESTIGATE → RESPOND → MEASURE → IMPROVE → RETEST

It is responsible for answering: what happened, when, on which system, based on what evidence, involving which indicators and techniques, along what likely attack path — and what is still unknown.

---

## Investigation Principles

- Evidence first — conclusions are based on observable evidence, not assumption.
- Timeline driven — events are placed into a chronological timeline whenever possible.
- Hypothesis driven — analysts form hypotheses and test them against evidence rather than jumping to an explanation.
- Traceability — important conclusions trace back to specific evidence.
- Separation of fact and inference — observed fact, analyst interpretation, hypothesis, confirmed conclusion, and unresolved unknowns are kept clearly distinct.
- Reproducibility — another analyst should be able to follow how a conclusion was reached.
- Preserve uncertainty — if the evidence is insufficient, the record says so rather than manufacturing certainty.

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
DETERMINE ROOT CAUSE
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

> The exact workflow may vary by scenario — not every investigation will need every stage, and any stage may loop back to an earlier one as evidence develops.

---

## Investigation States

- New
- Triage
- Investigating
- Contained / Awaiting Response
- Resolved
- Closed
- Inconclusive

> "Inconclusive" is a valid, legitimate outcome when the available evidence is insufficient to reach a confirmed conclusion. Investigations are not forced to produce a definitive finding they cannot support.

---

## Case Identifiers

Cases are named `case-001`, `case-002`, `case-003`, and so on.

- IDs are unique and are never reused.
- Once assigned, a case ID remains stable.
- Cases reference related evidence, detections, tests, and response actions where applicable.

> Case numbers are assigned only when a real investigation record is created — this README does not itself define or reserve any case.

---

## Case Record Structure

Each case is a single Markdown file (e.g. `case-001-short-title.md`) using the following structure. Sections are filled in only with what is actually known; unresolved or not-yet-performed items are stated explicitly rather than left implying more progress than exists.

```markdown
# Case ID / Title

## Incident Summary
Short factual description of what triggered the investigation.

## Status
New | Triage | Investigating | Contained / Awaiting Response | Resolved | Closed | Inconclusive

## Severity
Only assign when supported by the project's severity methodology.

## Affected Assets
e.g. SENTINEL-LINUX01, SENTINEL-WAZUH, SENTINEL-KALI

## Detection / Trigger
What caused the investigation (Wazuh alert, controlled attack test,
threat-hunting observation, suspicious telemetry). Do not invent an alert ID.

## Investigation Objective
What the investigation is trying to determine.

## Initial Hypothesis
What is suspected at the outset — explicitly labeled as a hypothesis,
not a conclusion.

## Evidence Collected
Wazuh alerts, logs, process information, authentication events, network
observations, file information, screenshots, test results. Use
repository-relative links where appropriate.

## Timeline
Chronological sequence of relevant events (timestamp, event, source,
interpretation/significance). Do not fabricate timestamps.

## Indicators of Compromise
IP addresses, domains, URLs, file hashes, filenames, processes, user
accounts, commands, or other indicators — only those actually observed.

## MITRE ATT&CK Mapping
Only where the mapping is technically justified and traceable to observed
behavior. If none is validated, state that explicitly.

## Analysis
What the evidence shows, separating facts, interpretation, hypotheses,
and confirmed findings.

## Attack / Activity Chain
Initial Activity → Execution → Persistence → Discovery →
Privilege/Access Changes → Collection → Command/Control → Impact.
Include only stages actually supported by evidence — do not assume
the full chain occurred.

## Root Cause
Only when supported by evidence. If unknown: "Root cause not determined."

## Impact Assessment
Affected VM, service, account, data, and detection impact.
Do not exaggerate impact.

## Response
Link to response actions when applicable. If none yet:
"Response not yet performed."

## Detection Performance
Detection triggered? Detection time, relevant rule, telemetry source,
false positive?, missed detection?, limitations. Do not invent metrics.

## Lessons Learned
What the investigation revealed.

## Improvements
Detection, telemetry, investigation, response, or documentation
improvements identified.

## Retest
Passed | Failed | Partial | Not yet retested
```

---

## Triage

Triage is the first stage of any investigation and should answer:

1. Is the event worth investigating?
2. What asset is involved?
3. What happened?
4. When did it happen?
5. Is the activity expected?
6. Is this part of a controlled SENTINEL test?
7. What evidence is immediately available?
8. What should be investigated next?

> Triage should avoid prematurely declaring an incident confirmed before the evidence supports it.

---

## Timeline Reconstruction

A timeline connects related events across whatever telemetry is actually available — this may include Wazuh alerts, Linux logs, authentication events, process information, network observations, or file activity. Only sources genuinely available in the given scenario should be listed; timestamps are never invented. Where possible, a timeline should distinguish event time, detection time, investigation time, and response time.

---

## IOC Handling

Indicators of compromise are collected only from actual evidence, not inferred or assumed. Useful categories include IP, domain, URL, hash, filename, process, username, command, and file path. Where practical, each IOC records its type, value, source, first/last observed time, and context. Real-world sensitive data is not included unnecessarily.

---

## MITRE ATT&CK Mapping

ATT&CK mapping describes observed attacker behavior and should be evidence-driven, specific, justified, and traceable to what was actually observed — not applied to every investigation simply for presentation. The absence of a validated mapping is an acceptable, honest outcome.

---

## Threat Hunting

Threat hunting is planned future investigation work, not a currently implemented capability. When introduced, it will follow a hypothesis-driven process:

```text
Hypothesis → Search telemetry → Identify suspicious behavior →
Validate evidence → Investigate → Confirm / Reject hypothesis → Document result
```

---

## Investigation Evidence

Supporting evidence for a case belongs in the appropriate version directory under [`evidence/`](../evidence/) (e.g. Wazuh alerts, screenshots, logs, timeline evidence, command output, detection results, IOC evidence, network observations, before/after comparisons). Evidence should be relevant, sanitized, traceable, and reproducible where possible.

>  Never commit passwords, API keys, tokens, private keys, real credentials, personal information, production data, or unnecessary sensitive telemetry.

---

## Relationship to Other SENTINEL Documentation

Document	Role	
[`investigations/README.md`](README.md) (this file)	Directory-level guide for how investigation records are organized	
[`investigations/CASE-001.md`](CASE-001.md)	CASE-001 — controlled validation of custom Wazuh FIM rule 100002 and review of related file-integrity events	
[`docs/06-incident-response.md`](../docs/06-incident-response.md)	Broader incident-response methodology and response workflow	
[`docs/05-detection-engineering.md`](../docs/05-detection-engineering.md)	How detections are designed and validated	
[`docs/07-testing-and-matrices.md`](../docs/07-testing-and-matrices.md)	Testing, validation, and measurement methodology	
[`docs/08-lessons-and-failures.md`](../docs/08-lessons-and-failures.md)	Broader failure-driven engineering approach	
[`failure-log/`](../failure-log/)	Meaningful failures encountered during development and testing	
[`evidence/`](../evidence/)	Supporting investigation and testing evidence	
[`detections/`](../detections/)	Detection implementations	
[`metrics/`](../metrics/)	Measured performance and validation results	
[`CHANGELOG.md`](../CHANGELOG.md)	Major project-level milestones and architecture changes	

---

## Investigation Index

Case ID	Investigation	Status	Primary Detection	
[CASE-001](CASE-001.md)	File Integrity Monitoring Investigation	✅ Closed — controlled validation completed	Wazuh FIM, custom Rule 100002	

---

## CASE-001 Summary

CASE-001 documents a controlled modification of `/home/sentinel-admin/sentinel-fim-validation.txt` on SENTINEL-LINUX01. The modification generated a Wazuh Level 8 alert under custom Rule 100002.

The investigation also reviewed additional file-integrity events involving desktop configuration, application state, and cache files. These events were documented as observed background activity within the reviewed dataset; individual process attribution was not conclusively established.

> The case is closed for its controlled validation objective. Creation and deletion testing, broader false-positive/false-negative testing, and detection-rule tuning remain follow-up tasks.

## Supporting evidence is stored in [`evidence/v0.3/`](../evidence/v0.3/).

---

## Investigation → Response

Detection → Investigation → Findings → Response → Measurement → Improvement → Retest

An investigation should not automatically trigger destructive response actions. In the controlled SENTINEL environment, response actions are deliberate and documented separately. The investigation's job is to determine what happened and provide the evidence base that supports response decisions.

---

## Investigation → Detection Improvement

Investigations are expected to feed back into detection engineering. An investigation may surface a detection gap, which leads to identifying missing telemetry or weak logic, improving the detection, testing it, and retesting the original scenario.

CASE-001 confirmed the tested modification-detection behavior of custom Rule 100002 and identified broad home-directory matching as an area for further evaluation. Proposed tuning must be tested before its effectiveness is claimed.

---

## Investigation → Attack DNA / Mutation (future)

A future use of this directory is to record how attacker behavior and detection performance change under Attack Mutation — which behaviors remained observable, which changed, which detections survived, which failed, and what improvements are required.

> Attack DNA and Attack Mutation are not currently implemented in SENTINEL. This section describes intended future use only.

---

## Investigation Quality

A useful investigation is evidence-backed, chronological, reproducible, explicit about uncertainty, traceable to telemetry, clear about which statements are hypotheses versus conclusions, and linked to relevant detections, evidence, response actions, and lessons learned. Quality is not judged by report length.

---

## Current Status

- ✅ Investigation methodology and directory structure are documented.
- ✅ SENTINEL-WAZUH and SENTINEL-LINUX01 provide the telemetry foundation for the current investigation workflow.
- ✅ CASE-001 has been documented in [`investigations/CASE-001.md`](CASE-001.md), with supporting evidence under [`evidence/v0.3/`](../evidence/v0.3/).
- ✅ Custom Rule 100002 successfully detected the controlled file modification tested in CASE-001.
- ✅ Additional home-directory FIM events were reviewed, and potential noise from routine desktop activity was documented with appropriate attribution limitations.
- ⬜ Creation and deletion validation, detection tuning, and broader false-positive/false-negative testing remain outstanding.
- ⬜ Future investigations should receive unique case IDs and follow the evidence-first principles described in this guide.
