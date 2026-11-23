# SENTINEL Lessons & Failures

> Does your detection still work when the attacker changes tactics?

This document preserves the real engineering history of SENTINEL: what failed, why it failed, how it was investigated, what changed, whether the fix worked, what was learned, and what should be retested. It is not a generic "lessons learned" article — it is a living engineering record, and it only contains failures, detection gaps and findings that actually occurred. Hypothetical scenarios are included only when explicitly labeled **Example** or **Hypothetical**.

---

## 1. Purpose

SENTINEL follows this working cycle:

```
BUILD → UNDERSTAND → TEST → BREAK → FIX → MEASURE → DOCUMENT → EXPLAIN
```

Failures are expected during security engineering, not a sign something went wrong with the project itself:

- A failed detection is useful information.
- A broken VM is useful information.
- A telemetry gap is useful information.
- A false positive is useful information.
- A failed response action is useful information.

The goal of this document is not to eliminate evidence of failure — it's to understand failure and convert it into engineering improvement.

---

## 2. Failure-Driven Engineering Principle

**Failure is data.** For every failure, SENTINEL asks:

- What assumption was wrong?
- What failed?
- Why did it fail?
- What evidence proves the failure?
- What was changed?
- Did the change solve the actual problem?
- Did the fix introduce a new problem?
- How should the result affect future testing?

```
FAIL → CAPTURE → ANALYZE → FIX → RETEST → MEASURE → DOCUMENT → IMPROVE
```

---

## 3. Current Environment and Project State

SENTINEL is a **Linux-first lab**. There is no live Windows or Active Directory endpoint. Windows Sysmon telemetry is **replayed** (CASE-002), not collected from a live Windows host. The Linux-first design originated as a v0.1 architecture decision after the Windows VM failure recorded in FAIL-001 (Section 4); the project has since progressed through v0.10 (Section 16).

### SENTINEL-WAZUH
| Field | Value |
|---|---|
| OS | Ubuntu 24.04 |
| Wazuh | 4.14.8 |
| IP | 10.10.10.10 |
| Role | SOC / monitoring platform |

### SENTINEL-KALI
| Field | Value |
|---|---|
| Role | Controlled attacker VM |
| IP | 10.10.10.20 |

### SENTINEL-LINUX01
| Field | Value |
|---|---|
| OS | Ubuntu 24.04.5 LTS |
| IP | 10.10.10.40 |
| Wazuh Agent | 4.14.8, Agent ID `002`, agent name `sentinel-linux01` |

**Network:** `SENTINEL-LAB` — `10.10.10.0/24`.

**Historical v0.1 context:** v0.1 established the core infrastructure — Wazuh operational, Kali operational, Linux01 operational, Wazuh Agent connected — with SENTINEL-LINUX01 as the initial monitored endpoint.

**Current state:** testing has since covered Sysmon replay (CASE-002), controlled SSH authentication testing (CASE-003), mutation and noise findings (CASE-004), FIM tuning (v0.8), and a live Linux FIM probe with file-based Python triage (v0.10). Failures, detection gaps, benign noise, scope limitations and unresolved questions are kept separate in Section 11.

---

## 4. Documented Infrastructure Lessons

### Verified lesson: Windows 11 endpoint deployment

The project initially attempted to include a Windows 11 endpoint as part of the core v0.1 architecture. That VM repeatedly failed to boot/render correctly in the VirtualBox environment.

**Troubleshooting attempted:**
- Fresh VM creation
- NAT-only boot testing
- VirtualBox graphics configuration changes
- UEFI / Secure Boot / TPM configuration adjustments
- VirtualBox version upgrade
- Boot-menu testing

**Result of troubleshooting:** the issue persisted. No definitive technical root cause was conclusively determined — the exact underlying cause (hypervisor interaction, graphics configuration, firmware settings, or something else) was not confirmed, and this document does not speculate beyond what was actually verified.

**Engineering decision:** do not allow the unresolved Windows VM problem to block SENTINEL's overall development.

**Result:** the architecture was revised so that SENTINEL-LINUX01 became the initial monitored endpoint for v0.1. Windows/Active Directory was moved to future expansion (see `docs/03-architecture.md`, Section 3.4) rather than being treated as a blocker. That deferral remains in effect: there is still no live Windows or Active Directory endpoint.

This is the only infrastructure lesson formally recorded in this document. It is documented factually, without an invented root cause.

---

## 5. Failure Record Format

Every failure should be recorded using this template:

```markdown
# Failure ID

## Date
## Version
## Category
## Component
## Expected Behavior
## Actual Behavior
## Impact
## Evidence
## Initial Hypothesis
## Investigation
## Root Cause
## Corrective Action
## Retest
## Final Result
## Lesson Learned
## Preventive Action
## Related Test
## Related Documentation
```

Unknown fields are recorded as `Unknown`, `Not yet determined`, or `Not tested` — never filled with invented information.

---

## 6. Failure Categories

### Infrastructure Failure
VM, OS, networking, storage, VirtualBox, or configuration issues.

### Telemetry Failure
Expected telemetry not generated, collected, or received.

### Detection Failure
Expected malicious/suspicious behavior not detected.

### False Positive
Benign activity incorrectly detected.

### Investigation Failure
Available evidence insufficient to answer the required investigation questions.

### Response Failure
A response action failed or produced an unexpected result.

### Mutation Failure
A detection failed after a controlled attack variation.

### Documentation Failure
Important information was not recorded correctly at the time.

### Process Failure
The methodology itself caused an avoidable problem.

---

## 7. Failure Severity / Impact

These are **project engineering impact** categories, not formal incident-severity ratings:

| Level | Meaning |
|---|---|
| LOW | Minor inconvenience; no meaningful project blockage |
| MEDIUM | Delays a development task; requires troubleshooting |
| HIGH | Blocks an important project capability; requires an architectural or implementation change |
| CRITICAL | Threatens lab safety or host/environment integrity |

The Windows 11 boot failure documented in Section 4 is classified as **HIGH** under this scale: it blocked the originally planned architecture and required an architecture change, but did not threaten lab safety or host integrity.

---

## 8. Failure Triage

1. Identify the failure.
2. Stop unsafe activity if necessary.
3. Capture evidence.
4. Record exact symptoms.
5. Identify the affected component.
6. Form hypotheses.
7. Test hypotheses.
8. Identify root cause where possible.
9. Apply corrective action.
10. Retest.
11. Record the final result.
12. Update related documentation.

Guiding principle:

```
STOP → CAPTURE → DOCUMENT → CONTINUE
```

---

## 9. Root Cause Analysis

The first symptom observed is not necessarily the root cause. Useful methods include:

- 5 Whys
- Timeline analysis
- Configuration comparison
- Controlled reproduction
- Dependency analysis
- Before/after comparison

A root cause is never forced when the evidence doesn't support one. A valid, honest result is:

> "Root cause not conclusively determined."

— as is the case for the Windows 11 boot failure in Section 4.

---

## 10. Corrective Action

Corrective actions may include:

- Configuration change
- Code change
- Detection-rule change
- Telemetry change
- Network change
- VM configuration change
- Documentation change
- Test improvement
- Process improvement
- Architecture change

Every significant corrective action should be recorded against the failure it addresses, including whether it was retested and whether the retest confirmed the fix. A corrective action is not considered complete until its retest result has been documented — "we made a change" is not the same as "we confirmed the change worked."

For the Windows 11 case (Section 4), the corrective action was architectural: removing the Windows endpoint from the current scope and substituting SENTINEL-LINUX01 as the v0.1 monitored endpoint. This action has been confirmed effective in the sense that v0.1 was completed successfully with Linux01 in that role; it does not resolve the original Windows boot issue itself, which remains unresolved and out of current scope.

---

## 11. Verified Failure Log

This is the authoritative log of what has actually occurred in SENTINEL. Entries are added only as real events happen — nothing here is invented in advance.

Five different kinds of record are kept deliberately separate. They are not interchangeable, and testing an area does not mean that area "failed":

| Kind | Meaning | Where |
|---|---|---|
| Formally recorded failure entry | A failure with an ID and the full template | 11.1 |
| Documented detection gap | A demonstrated miss for a specific tested scenario | 11.2 |
| Observed benign noise | Benign activity that generated alerts and needs tuning | 11.3 |
| Known scope limitation | Activity outside what a control is configured to monitor | 11.4 |
| Unresolved historical question | An observation whose cause is not established | 11.5 |

Section 11.6 records phase results that were not failures, for context.

### 11.1 Formally recorded failure entries

#### FAIL-001

- **Date:** Not precisely recorded at the time; occurred during v0.1 infrastructure buildout
- **Version:** v0.1
- **Category:** Infrastructure Failure
- **Component:** Planned Windows 11 endpoint (SENTINEL-WIN01, VirtualBox)
- **Expected Behavior:** Windows 11 VM boots normally and renders a usable guest display
- **Actual Behavior:** VirtualBox displayed a gray window with a small, non-functional guest display area; the VM did not reach a usable boot state
- **Impact:** HIGH — blocked the originally planned three-OS architecture (Wazuh, Kali, Windows)
- **Evidence:** Observed VirtualBox display behavior (not preserved as a stored artifact at the time)
- **Initial Hypothesis:** Graphics/display configuration or firmware (UEFI/Secure Boot/TPM) interaction issue
- **Investigation:** Fresh VM creation, NAT-only boot testing, graphics configuration changes, UEFI/Secure Boot/TPM configuration adjustments, VirtualBox version upgrade, boot-menu testing
- **Root Cause:** Not yet determined
- **Corrective Action:** Removed Windows from the current v0.1 architecture; substituted SENTINEL-LINUX01 as the initial monitored endpoint; moved Windows/AD to future expansion
- **Retest:** Not applicable to the original issue — the Windows VM itself was not retested after the architecture change
- **Final Result:** v0.1 completed successfully using the revised (Linux-based) architecture
- **Lesson Learned:** An unresolved infrastructure blocker should not stall the whole project — the architecture can be adapted around it while the original problem is deferred rather than ignored
- **Preventive Action:** Windows/AD reintroduction is documented as future work with no fixed timeline, so it isn't silently reattempted without accounting for this history
- **Related Test:** None (pre-dates the formal test framework in `docs/07-testing-and-metrics.md`)
- **Related Documentation:** `docs/03-architecture.md` (Section 3.4, Future Windows / Active Directory Expansion), `docs/02-requirements.md`

FAIL-001 is the only formally recorded failure entry. The entries in Sections 11.2–11.5 have no formal failure IDs or severity ratings. Known dates are recorded rather than omitted, and details that are not recorded here are not invented.

### 11.2 Documented detection gap: Sysmon `comsvcs.dll, #24` variation (CASE-004 / v0.7)

This is a real, evidence-backed detection weakness for the tested variation. It has no formal failure ID or severity rating, but its observed date is recorded below.

- **Identifier:** None assigned (not a formal failure entry)
- **Date:** 20 November 2026
- **Version / case:** v0.7, CASE-004
- **Category:** Mutation — documented detection gap
- **Component:** Keyword-specific Rule `100112`; base Event ID 1 Rule `100101` (Level 0)
- **Expected Behavior:** The tested Sysmon command-line variation using `comsvcs.dll, #24` produces the intended behavioral alert from Rule `100112`
- **Actual Behavior:** The event matched base Event ID 1 Rule `100101` at Level 0 instead of generating the intended behavioral alert
- **Impact:** Not formally rated
- **Evidence:** Documented in CASE-004; artifact references are not restated here
- **Root Cause:** Not yet determined beyond the observation that this variation did not produce the Rule `100112` alert
- **Corrective Action:** Not completed. Correlation with Sysmon Event ID 10 and Event ID 11 was identified as a possible improvement; it has not been implemented
- **Retest:** Not tested
- **Final Result:** Open. This is a demonstrated gap for the tested variation only. It does not show that all variants evade Rule `100112`, and it does not show that other rules fail

### 11.3 Observed benign noise: FIM alerts (CASE-004 / v0.7, v0.8)

- Benign cache and desktop activity generated Level 8 FIM alerts. This is recorded as observed benign noise requiring tuning. It is not proof that all such activity is incorrectly detected.
- v0.8 implemented selected exclusions and FIM group isolation. One controlled probe confirmed that the selected rules still detected the tested hidden-file lifecycle.
- Residual `dconf` noise remains, and broader retesting is pending. The noise problem is **not** fully resolved, and no complete FIM regression suite exists.

### 11.4 Known scope limitation: FIM monitoring scope (CASE-004 / v0.7)

- Hidden files inside `/home` triggered FIM rules.
- A test file staged under `/var/tmp`, outside the configured `/home` scope, produced no FIM alerts. This is recorded as a known monitoring-scope limitation. It is not automatically a broken control, because the path was not within the configured scope.

### 11.5 Unresolved historical questions

These are deliberately not recorded as confirmed failures:

- **16 October FIM records:** custom FIM rule alerts (Rule `100002` specifically) were absent from the reviewed creation and deletion records, where built-in Rules `554` and `553` were the alerting rules. The reason is unresolved. No root cause is claimed, and this is not a confirmed detection failure.
- **31 October Set A:** the screenshot observations of Rules `100003` and `100004` under an application configuration path remain observations with unestablished trigger origin. The separate 31 October Set B raw JSON records (creation and deletion of a dedicated test file) are a different evidence set and are not merged with Set A.
- **Later controlled FIM lifecycle sessions** demonstrate only the scenarios and files tested. They do not explain the 16 October observations and do not establish complete coverage.

See `docs/07-testing-and-metrics.md` for the evidence-level detail.

### 11.6 Phase results that were not failures (context)

| Phase | Result | Boundaries |
|---|---|---|
| CASE-002 / v0.4 — Sysmon replay | Seven selected behavioral rules fired on replayed Sysmon telemetry. Three benign process-creation events matched general Level 0 Rule `100101` and generated no alerts. | Sample-bound. Not a live Windows endpoint test. Does not establish broad coverage or statistically meaningful rates. |
| CASE-003 / v0.5 — SSH | 21 controlled failed SSH authentication attempts from Kali against Linux01. Rule `100200` generated baseline alerts and Rule `100201` generated a threshold escalation. Manual investigation confirmed zero successful logins. | Python triage assisted prioritisation. Containment was a documented manual procedure, not automated. No failure entry is recorded from this case. |
| v0.6 — Controlled purple-team measurement (20 November 2026) | FIM: 3/3 selected lifecycle events detected; negative control: 0/3 alerts for `/tmp` operations outside the configured `/home` scope. Sysmon replay: 7/7 selected detections fired and 0/3 benign events generated alerts at Level 0; two Sysmon Event ID 7 ImageLoad events remained uncovered. SSH: Rule `100200` baseline alerts and Rule `100201` threshold escalations were recorded. The first C2 escalation occurred early because the 60-second sliding window carried over four failures from C1 and combined them with two C2 failures. | Small controlled samples, not statistically meaningful detection or false-positive rates. Cross-VM clock skew prevents claiming reliable detection-latency measurements. The two uncovered Event ID 7 events and the early escalation are recorded as measurement findings, not formal failures. |
| v0.8 — FIM tuning and verification | Selected FIM path exclusions and FIM group isolation using `sentinel_fim` were implemented and manager-validated. A controlled Agent 002 probe on 21 November 2026 created, modified and deleted a hidden file under `/home/sentinel-admin/.v08-check/`; Rules `100003`, `100002` and `100004` fired at Level 8 for the respective events. The alerts carried the `sentinel_fim` group without the `sshd` group. Residual desktop `dconf` noise remained. | One controlled lifecycle probe, not a regression suite or broad noise-reduction assessment. Does not establish complete FIM coverage. Broader retesting remained pending. |
| v0.10 — Live Linux FIM and Python triage | A live Linux FIM probe generated creation, modification and deletion alerts for Rules `100003`, `100002` and `100004`. Exported Wazuh alert JSON was then processed separately with the Python SOC Automation CLI. | File-based workflow. Not a live API integration, continuous pipeline, SOAR workflow, or automated response. The evidence archive is stored outside the SENTINEL repository (`~/soc-evidence/v0.10-fim-probe/`) and is not committed repository evidence. |

---

## 12. Lessons Learned Summary

| Lesson | Source | Applies To |
|---|---|---|
| Don't let one blocked component stall the whole project — adapt the architecture and defer the blocker explicitly | FAIL-001 | Future infrastructure changes, especially Windows/AD reintroduction |
| Root cause is sometimes genuinely "not determined" — document that honestly rather than guessing | FAIL-001; Section 11.2 | All future failure records |
| A keyword-specific rule can miss a tested command-line variation; the gap holds for the tested variation only, and correlation (Event ID 10 and 11) is a possible improvement that is not implemented | Section 11.2 (CASE-004 / v0.7) | Sysmon-based detection design and mutation testing |
| A control only sees what it is configured to monitor; activity outside the configured FIM scope (such as `/var/tmp`) produces no alert | Section 11.4 (CASE-004 / v0.7) | FIM scope decisions and test design |
| Tuning must be retested: one probe showed selected rules still detected the tested hidden-file lifecycle, but residual `dconf` noise remains and broader retesting is pending | Section 11.3 (v0.8) | FIM tuning |
| Keep unresolved observations labeled unresolved rather than converting them into confirmed failures or confirmed validations | Section 11.5 | Evidence handling across all phases |
| Describe workflows at the level actually implemented: sample-bound replay is not live Windows coverage, and file-based triage is not live API integration, SOAR, or automated response | Section 11.6 (CASE-002, CASE-003, v0.10) | Claims about capability |

This table will grow as new verified findings are added to Section 11.

---

## 13. Preventive Actions Registry

| Preventive Action | Originating Failure | Status |
|---|---|---|
| Do not reintroduce Windows/AD without accounting for the unresolved VirtualBox boot issue from FAIL-001 | FAIL-001 | Active — applies whenever Windows expansion is revisited |
| Correlate Sysmon Event ID 10 and Event ID 11 with process-creation detections for the `comsvcs.dll, #24` variation | Documented detection gap (Section 11.2) | Identified as a possible improvement; not implemented; not retested |
| Broader FIM retesting after v0.8 tuning, including residual `dconf` noise | Observed benign noise (Section 11.3) | Pending; not completed |

---

## 14. Relationship to Other SENTINEL Documents

| Document | Relationship |
|---|---|
| `docs/03-architecture.md` | Documents the current implementation that failures may have shaped (e.g., the Linux-first architecture) |
| `docs/02-requirements.md` | Reflects infrastructure decisions informed by past failures |
| `docs/07-testing-and-metrics.md` | Defines how tests are executed and records their evidence levels; failed or inconclusive tests from that framework feed into this document |
| `docs/05-detection-engineering.md` | Detection-specific gaps, false positives and noise findings are recorded here (see Section 11) |
| `docs/06-incident-response.md` | Response failures from incident-response exercises will be logged here; none are currently recorded (the CASE-003 containment was a documented manual procedure) |
| `docs/04-threat-model.md` | Threat-model assumptions that prove wrong in practice should be captured as lessons here |
| `failure-log/readme.md` | Readme for the `failure-log/` directory; its contents are not summarized here |

This document is the shared destination for failure evidence surfaced by all of the above — it does not duplicate their methodology, only records what actually happened when that methodology was applied.

---

## 15. Maintenance

This document should be updated when:

- A real failure occurs anywhere in the project (infrastructure, telemetry, detection, investigation, response, or process).
- A corrective action is applied and its retest result becomes known.
- A previously "not determined" root cause is later confirmed.
- A lesson changes a standing assumption recorded elsewhere (e.g., in `docs/04-threat-model.md`).
- A preventive action needs to be added, updated, or retired.

This document is **not** rewritten for cosmetic reasons or minor day-to-day activity — only for genuine, verified engineering failures, gaps and findings, and their resolution.

---

## 16. Current Status

**Project state:** through v0.10. SENTINEL is a Linux-first lab with no live Windows or Active Directory endpoint; Windows Sysmon telemetry is replayed. The Windows/AD deferral from FAIL-001 remains in effect.

**Formally recorded failures:** 1 (FAIL-001 — Windows 11 endpoint boot failure, v0.1)

**Documented detection gaps:** 1 — the Sysmon `comsvcs.dll, #24` variation that matched Level 0 Rule `100101` instead of Rule `100112` (CASE-004 / v0.7). Open: correlation with Event ID 10 and 11 is a possible improvement that is not implemented, and the variation has not been retested. No formal failure ID or severity rating has been assigned; the known date, 20 November 2026, is retained.

**Observed benign noise:** Level 8 FIM alerts from benign cache and desktop activity. v0.8 exclusions and FIM group isolation were implemented, and one controlled probe confirmed the tested hidden-file lifecycle was still detected. Residual `dconf` noise remains and broader retesting is pending; the noise problem is not fully resolved.

**Known scope limitation:** FIM is configured for `/home`; a file staged under `/var/tmp` produced no alerts.

**Unresolved historical questions:** the 16 October absence of custom FIM rule alerts from the reviewed records, and the trigger origin of the 31 October Set A screenshot observations.

**Categories with no formally recorded failure entry:** Telemetry, Detection, False Positive, Investigation, Response, Mutation, Documentation, Process. For Detection/Mutation and False Positive, the related gap and noise findings are recorded in Sections 11.2 and 11.3 without formal failure IDs. This does not mean those areas are failure-free.

**Not established:** a complete FIM regression suite, broad detection coverage or statistically meaningful detection rates, live Windows/AD coverage, and automated response. The CASE-003 containment was a documented manual procedure.

**Next expected sources of new entries:** broader FIM retesting after v0.8 tuning, any retest of the Sysmon `#24` variation after a rule or correlation change, and further controlled testing.
