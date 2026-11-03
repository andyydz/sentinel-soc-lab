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

**v0.3 — SOC Investigation (phase milestone complete)**

CASE-001 remains open overall. Evidence reconciliation for the reviewed CASE-001 scope is closed: the controlled modification tests (11 and 26 October 2026) are recorded, the 16 October creation/deletion observations have been reconciled against the reviewed source records, and the 31 October custom creation/deletion alerts are recorded as observations. Background configuration and cache changes were observed in the 11 October review, but process-level attribution for every event was not established.

A single controlled creation, modification and deletion lifecycle validation on one dedicated test file was recorded on 2 November 2026 as an additional validation milestone. It is one session, not a regression suite or repeatability test, and it does not resolve the 16 October observations or retroactively validate the 31 October events. A read-only check of the on-disk Rule 100002 definition on SENTINEL-WAZUH was recorded on 3 November 2026; it verifies the on-disk definition and analysis-engine service state only, not the rule definition loaded in memory.

Broader investigation and detection-engineering work remains open, including investigating why custom Rule "100002" was absent from the reviewed 16 October creation/deletion records, investigating the differences between the 16 and 31 October observations (no explanation is established), broader false-positive/false-negative testing, repeatable regression testing, and detection tuning. Additional cases remain future work. No containment, eradication, or recovery exercise has been completed.

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
## Status        (Open | New | Triage | Investigating | Contained / Awaiting Response | Resolved | Closed | Inconclusive)
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
| [`investigations/readme.md`](readme.md) (this file) | Directory-level guide for how investigation records are organized |
| [`investigations/CASE-001.md`](CASE-001.md) | CASE-001 — FIM detection validation and evidence reconciliation: custom Wazuh FIM Rules 100002, 100003 and 100004, creation/deletion evidence reconciliation, and review of related file-integrity events |
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
| [CASE-001](CASE-001.md) | FIM Detection Validation and Evidence Reconciliation (modification, creation, deletion) | 🟡 Open — evidence reconciliation for the reviewed scope closed | Wazuh FIM, custom Rules 100002 (modification), 100003 (creation), 100004 (deletion) |

---

## CASE-001 Summary

CASE-001 documents Wazuh FIM detection observations on SENTINEL-LINUX01 across separate sessions on 11, 16, 26 and 31 October and 2 November 2026, plus a read-only rule-configuration check on SENTINEL-WAZUH on 3 November 2026. Details are in [`CASE-001.md`](CASE-001.md) and [`fim-rule-100002-investigation.md`](fim-rule-100002-investigation.md); this is a short summary.

Evidence types differ and are kept distinct: the 16 October findings rest on reviewed source alert records, while the 11 October, 26 October, 31 October and 2 November results rest on screenshots (including terminal screenshots). A terminal screenshot is not a raw alert JSON or source record.

**Observed — modification (custom Rule 100002, Level 8):**

- 11 October 2026: existing screenshots support a Level 8 custom Rule 100002 alert for a controlled modification of `/home/sentinel-admin/sentinel-fim-validation.txt` (`2026-10-11T20:25:14.746+0530`). The original source alert log was not recovered during the 26 October review.
- 26 October 2026: two consecutive modifications of one file, `/home/sentinel-admin/sentinel-v02-mod-test.txt`, produced two Level 8 Rule 100002 alerts at `2026-10-26T21:38:27.910+0530` (size 0 → 23 bytes) and `2026-10-26T21:38:48.473+0530` (size 23 → 61 bytes). These are not two independent test cases and not a regression suite.
- These validate the tested modification scenarios only. They say nothing about creation or deletion coverage.

**Observed — creation and deletion (16 October 2026, `/home/sentinel-admin/sentinel-audit-test.txt`):**

- The reviewed creation record showed built-in Rule 554 (Level 5) at `2026-10-16T11:40:06.007+0530`. Rule 100002 was absent from that record.
- The reviewed deletion record showed built-in Rule 553 (Level 7) at `2026-10-16T12:31:32.819+0530`. Rule 100002 was absent from that record.
- These statements are limited to the two reviewed records and do not show how Rule 100002 behaves for other creation or deletion events. This is an observation, not a confirmed detection failure, and its cause is unresolved. Earlier versions of this guide recorded Rule 100002 as firing on creation; that is not supported by the reviewed records.

**Observed — custom creation and deletion (31 October 2026):**

- Custom Rule 100003 (file creation, Level 8) and custom Rule 100004 (file deletion, Level 8) were observed at approximately 18:51:56 IST, with paths under `/home/sentinel-admin/snap/firmware-updater/262/.config/bus/`.
- These are observed detections, not established deliberate or controlled tests. The paths are in an application configuration directory, and whether the events were deliberately triggered or ordinary application activity has not been established.
- The evidence is a single terminal screenshot covering both alerts. Raw alert records are not committed.
- Process attribution, trigger and root cause have not been established. No repeatability, completed regression test, or comprehensive FIM coverage is claimed.
- The 11 October and 26 October modification tests, the 16 October built-in-rule observations, and the 31 October custom-rule observations were separate sessions. They do not constitute one end-to-end lifecycle test, and Rule 100002 is not claimed to handle creation or deletion.

**Controlled lifecycle validation (2 November 2026) — separate from the 31 October observations:**

Evidence: [`v0.3-fim-full-lifecycle-custom-rules.png`](../evidence/v0.3/screenshots/v0.3-fim-full-lifecycle-custom-rules.png) (E16)

| Event | Custom rule | Level |
|---|---|---|
| Creation | `100003` | 8 |
| Modification | `100002` | 8 |
| Deletion | `100004` | 8 |

- One dedicated test file, `/home/sentinel-admin/sentinel-v03-final-test.txt`, was created, modified and deleted in one controlled session. All three event types were observed on that same file, each matched by the corresponding custom rule at Level 8.
- This is one controlled lifecycle session on one dedicated file. It is not a regression suite or repeatability test, and it does not establish comprehensive FIM coverage (other paths, file types, sizes or repeated events remain untested).
- The evidence is a terminal screenshot, not a raw alert JSON or source record. Raw 2 November alert records are not committed.
- It is a separate session from the 16 and 31 October observations. It does not explain why Rule 100002 was absent from the 16 October records, and it does not retroactively validate the 31 October events, whose trigger and attribution remain unestablished.
- Level 8 is the Wazuh alert level assigned by each rule definition. It is distinct from the administrative investigation classification of CASE-001 and is not an assessment of case severity or impact.

**Configuration evidence (kept separate):** two Syscheck configurations are committed as repository evidence and indexed in [`evidence/v0.3/`](../evidence/v0.3/). Both are screenshots of local configuration files, are not interchangeable, and are not combined.

- E14 — endpoint SENTINEL-LINUX01: [`v0.3-e14-endpoint-syscheck-configuration.png`](../evidence/v0.3/screenshots/v0.3-e14-endpoint-syscheck-configuration.png). The visible local `/var/ossec/etc/ossec.conf` shows Syscheck enabled (`<disabled>no</disabled>`), real-time monitoring of `/home`, startup scanning enabled, and a scheduled scan frequency of 43,200 seconds (12 hours).
- E15 — manager SENTINEL-WAZUH: [`v0.3-e15-manager-syscheck-configuration.png`](../evidence/v0.3/screenshots/v0.3-e15-manager-syscheck-configuration.png). The visible local `/var/ossec/etc/ossec.conf` shows Syscheck enabled, startup scanning enabled, new-file alerts enabled, and manager directories `/etc,/usr/bin,/bin,/usr/sbin`.
- E15 is manager-side configuration only and is not evidence of endpoint `/home` monitoring; endpoint `/home` monitoring is documented only by E14.
- Both show local configuration as captured. Neither independently establishes which configuration was loaded during the historical 16 October tests.

**Configuration verification — Rule 100002 on-disk definition and service state (3 November 2026):** a read-only check of `/var/ossec/etc/rules/local_rules.xml` on SENTINEL-WAZUH confirmed the following **on-disk** definition:

```xml
<rule id="100002" level="8">
  <if_sid>550</if_sid>
  <field name="file">^/home/</field>
  <description>SENTINEL: File integrity modification detected in monitored home directory.</description>
  <group>sentinel_fim,</group>
</rule>
```

Confirmed:

- The on-disk definition above (Rule 100002, Level 8, parent `<if_sid>550</if_sid>`, file condition `^/home/`).
- `wazuh-analysisd` was running during the check.
- The rule file modification time preceded the analysis engine's start time on 3 November 2026. This chronology is consistent with the engine starting after the file was modified.
- The check was read-only; no configuration change or restart was performed. It is recorded as a maintainer-run check, and no screenshot of it is indexed in the evidence directory.

Not verified:

- The exact rule definition loaded in memory by the analysis engine. The chronology is consistent with, but does not prove, the engine having loaded this definition, so the active rule version is not claimed as definitively verified.
- Which rule definition and Syscheck configuration were loaded during the 16 October tests.
- Why Rule 100002 was absent from the reviewed 16 October records.
- The definitions of Rules 100003 and 100004, which this check did not cover.

**Unresolved:**

- Why Rule 100002 was absent from the two 16 October records. The on-disk Rule 100002 definition depends on parent Rule 550, but the in-memory rule, the rule and Syscheck configurations loaded on 16 October, and the rule's matching behavior have not been verified, and that dependency is not asserted as the cause. No root cause is confirmed. No rule change or tuning has been made. A built-in rule firing does not by itself establish whether a custom rule should cover the same event.
- Why custom Rules 100003 and 100004 were observed on 31 October when built-in Rules 554 and 553 appeared on 16 October. No explanation is established.
- Whether the 31 October events were deliberate or ordinary application activity.

Additional file-integrity events involving desktop configuration, application state, and cache files were documented as observed background activity within the 11 October reviewed dataset only; this does not describe all endpoint activity or all `/home` events. Individual process attribution was not conclusively established.

> The case remains open. Evidence reconciliation for the reviewed scope is closed. Resolution of the unresolved items above, broader false-positive/false-negative testing, repeatable regression testing, and detection-rule tuning remain follow-up tasks. These FIM alerts do not establish malicious activity. No containment, eradication, or recovery exercise has been completed.

Supporting evidence: screenshots for the 11 October modification test, the 31 October observation, the 2 November lifecycle validation, and the E14/E15 configuration evidence are stored in [`evidence/v0.3/`](../evidence/v0.3/). The 26 October terminal output is supported by the screenshot [`v0.2-oct26-controlled-modification-source-alerts-new.png`](../evidence/v0.2/screenschots/v0.2-oct26-controlled-modification-source-alerts-new.png), stored in `evidence/v0.2/` rather than the v0.3 evidence directory; it supports the two Level 8 alerts from consecutive modifications of one file. The 11 October original source log and the raw 16, 31 October and 2 November records are not claimed to be committed to the repository.

---

## Investigation → Response and Detection Improvement

Detection → Investigation → Findings → Response → Measurement → Improvement → Retest

An investigation should not automatically trigger destructive response actions. Response actions are deliberate and documented separately; the investigation provides the evidence base for those decisions.

Investigations feed back into detection engineering: a detection gap leads to identifying missing telemetry or weak logic, improving the detection, testing it, and retesting the original scenario. CASE-001 confirmed the tested modification-detection behavior of custom Rule 100002, left the absence of Rule 100002 from the reviewed creation/deletion records unresolved, recorded observations of custom Rules 100003 and 100004 on 31 October without establishing their trigger or repeatability, and identified the "/home/" path-matching scope (present in the on-disk Rule 100002 definition checked on 3 November) as an area for further evaluation. The 2 November controlled lifecycle session adds a further validation milestone: Rules 100003, 100002 and 100004 were each observed for creation, modification and deletion of one dedicated test file. It is a single session and does not close the open detection-engineering work. Proposed tuning must be tested before its effectiveness is claimed.

Open detection-engineering work includes:

- Investigating the 16 October observations (cause unresolved).
- Investigating the differences between the 16 and 31 October observations (no explanation established).
- Verifying the loaded (in-memory) rule definitions and the configuration loaded on 16 October.
- Broader false-positive and false-negative testing.
- Building repeatable regression tests.
- Tuning detections and validating the effectiveness of any change.

No complete detection coverage or finished SOC workflow is claimed.

> Attack DNA and Attack Mutation are not currently implemented in SENTINEL. A future use of this directory may be to record how attacker behavior and detection performance change under mutation.

---

## Current Status

- ✅ Investigation methodology and directory structure are documented.
- ✅ SENTINEL-WAZUH and SENTINEL-LINUX01 provide the telemetry foundation for the current investigation workflow.
- ✅ CASE-001 is documented in [`investigations/CASE-001.md`](CASE-001.md) and [`investigations/fim-rule-100002-investigation.md`](fim-rule-100002-investigation.md); supporting evidence is under [`evidence/v0.3/`](../evidence/v0.3/) and [`evidence/v0.2/`](../evidence/v0.2/) (26 October screenshot, linked above).
- ✅ SENTINEL v0.3 documentation and evidence phase milestone: complete. This does not mean CASE-001 is resolved: CASE-001 remains open overall (evidence reconciliation for the reviewed scope is closed), and the broader investigation and detection-engineering work remain outstanding.
- ✅ Historical modification observations (11 and 26 October 2026): custom Rule 100002 detected the controlled file modifications tested (tested scenarios only; the 26 October result is two consecutive modifications of one file).
- ✅ Historical built-in creation/deletion observations (16 October): the creation and deletion records were reviewed; built-in Rules 554 (Level 5) and 553 (Level 7) were observed, and Rule 100002 was absent from both records. The cause is unresolved and this is not a confirmed detection failure.
- ✅ Custom creation/deletion observations (31 October 2026): custom Rules 100003 (creation) and 100004 (deletion) were observed and documented at Level 8 in a single terminal screenshot, under an application configuration path. Their behavior is not fully validated or shown to be repeatable, and the events are not established as deliberate or controlled tests.
- ✅ Controlled lifecycle validation (2 November 2026): Rules 100003 (creation), 100002 (modification) and 100004 (deletion) were each observed at Level 8 for one dedicated test file in one controlled session. This is not a regression suite or repeatability test, does not establish comprehensive FIM coverage, and does not explain the 16 October observations or validate the 31 October events retroactively. Evidence is a terminal screenshot; raw alert records are not committed.
- ✅ On-disk rule verification (3 November 2026): a read-only check confirmed the on-disk Rule 100002 definition on SENTINEL-WAZUH and that `wazuh-analysisd` was running. It does not prove the in-memory rule or the configuration loaded on 16 October.
- ✅ Configuration evidence is committed: E14 (endpoint SENTINEL-LINUX01, including real-time monitoring of `/home`) and E15 (manager SENTINEL-WAZUH, manager-side only) are linked above. Both show local configuration only.
- ✅ Additional home-directory FIM events within the 11 October reviewed dataset were reviewed, and potential noise from routine desktop activity was documented with appropriate attribution limitations.
- 🟡 Open: why Rule 100002 was absent from the reviewed creation/deletion records, and the differences between the 16 and 31 October observations. The on-disk Rule 100002 definition was confirmed on 3 November, but the in-memory rule, the historical loaded rule and Syscheck configurations, and matching behavior have not been verified, and no root cause is asserted.
- ⬜ Broader false-positive/false-negative testing, repeatable regression testing, detection tuning, and validation of tuning effectiveness remain outstanding. No detection rates or comprehensive FIM coverage have been established.
- ⬜ Process attribution and trigger for the 31 October events remain unestablished.
- ⬜ Threat hunting and additional investigation cases remain planned; future investigations should receive unique case IDs and follow the evidence-first principles described in this guide.
- ⬜ Attack Mutation is not implemented.
- ⬜ No containment, eradication, or recovery exercise has been completed.
