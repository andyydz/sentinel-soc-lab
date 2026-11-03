## ChangeLog

All notable changes to SENTINEL are documented here: project-level changes, architecture decisions, validated milestones, and lessons learned.

This file is a summary, not a Git commit history, a technical tutorial, or a replacement for the detailed project documentation. Architecture, threat model, detection engineering, incident response, testing/metrics, and lessons/failure records are maintained separately, and the investigation record is in "investigations/CASE-001.md". Where this file and those documents differ in detail, the detailed documents govern.

SENTINEL is a virtual cybersecurity SOC lab built around the lifecycle:

SIMULATE → DETECT → INVESTIGATE → RESPOND → MEASURE → IMPROVE → RETEST

The project's guiding question is: does your detection still work when the attacker changes tactics?

## Status at a glance

- **Built:** a Linux-first lab (Wazuh 4.14.8 on SENTINEL-WAZUH, SENTINEL-LINUX01 monitored endpoint with an active agent, SENTINEL-KALI attacker system) with File Integrity Monitoring (FIM) scoped to "/home".
- **Validated:** custom Rule "100002" (Level 8) on controlled file modification (11 and 26 October 2026), plus one controlled FIM lifecycle session on 2 November 2026.
- **2 November lifecycle:** one controlled session on "/home/sentinel-admin/sentinel-v03-final-test.txt": creation — Rule "100003", Level 8; modification — Rule "100002", Level 8; deletion — Rule "100004", Level 8. This is one controlled lifecycle session on one dedicated file, not a repeatable regression suite or proof of comprehensive FIM coverage.
- **Observed, not validated:** custom Rules "100003" (creation, Level 8) and "100004" (deletion, Level 8) appeared in one terminal screenshot dated 31 October 2026. This is separate from the 2 November session and is not a validated controlled test.
- **Verified on disk only:** a read-only check on 3 November 2026 confirmed the on-disk Rule "100002" definition and that "wazuh-analysisd" was running. The in-memory rule version is not verified.
- **Documented:** CASE-001, an evidence-backed investigation. Evidence reconciliation for the reviewed scope is closed; the overall case remains open.
- **Unresolved:** Rule "100002" was absent from the reviewed 16 October creation and deletion records, which showed built-in Rules "554" and "553". The reason is unknown; this is not a confirmed detection miss.
- **Not done:** detection rate, false-positive/false-negative measurement, repeatable regression testing, broader creation/deletion coverage, complete FIM coverage, and any containment, eradication, or recovery exercise. v0.4–v0.6 are planned.
- **Project status:** v0.1 complete; v0.3 phase milestone complete (documentation and evidence deliverables), with CASE-001 and broader detection-engineering work still open.

---

[Unreleased]

## Architecture and infrastructure

- **Decision:** replaced the original Windows-first architecture with a Linux-first initial endpoint. The Windows VM (SENTINEL-WIN01) hit repeated deployment/boot issues that made it unsuitable as a dependency for v0.1. This is recorded as an infrastructure/deployment issue, not an attributed technical root cause. Windows and Active Directory are deferred to future expansion.
- Deployed SENTINEL-WAZUH (Ubuntu 24.04), SENTINEL-KALI (controlled attacker/adversary-emulation), and SENTINEL-LINUX01 (Ubuntu 24.04, monitored endpoint) on the isolated SENTINEL-LAB network (10.10.10.0/24). Connectivity verified between Wazuh and Linux01 and between Kali and Wazuh.
- Completed Wazuh all-in-one deployment (4.14.8); Dashboard operational; agent on SENTINEL-LINUX01 enrolled and active.
- Disabled the Wazuh package repository after installation to reduce the risk of accidental upgrades. Upgraded VirtualBox from 7.2.8 to 7.2.20 during troubleshooting.

Current topology:

```text
INTERNET
   |
  NAT
   |
SENTINEL-WAZUH (10.10.10.10) — SOC / Wazuh
   |
SENTINEL-LAB (10.10.10.0/24)
   |
   +----------------------+
   |                      |
SENTINEL-KALI          SENTINEL-LINUX01
10.10.10.20            10.10.10.40
Attacker               Monitored Endpoint
```

## Documentation

- Established repository documentation (overview, requirements, architecture, threat model, detection engineering, incident response, testing/matrices, lessons/failures) and directories for future work: "detections/", "investigations/", "metrics/", "scenarios/", "evidence/", "failure-log/".
- Documented CASE-001 and indexed it in the investigation directory guide.
- Updated detection-engineering documentation to separate confirmed modification detection from outstanding testing and tuning work.

## Detection findings

Five separate dated evidence sets. They represent distinct observations or controlled tests, not one lifecycle test. Full detail (timestamps, file-size transitions, rule definitions) is in CASE-001 and the detection-engineering and testing/metrics documentation.

| Date (2026) | Scenario | Result | Status |
|---|---|---|---|
| 11 Oct | Controlled modification of "sentinel-fim-validation.txt" | Custom Rule "100002" Level 8 alert (built-in Rule "550" also observed) | Modification only. Supported by screenshots; original source alert log not recovered. |
| 16 Oct | Creation and deletion of "sentinel-audit-test.txt" | Built-in Rules "554" (creation) and "553" (deletion); Rule "100002" absent from both | Reviewed source records. Not a custom-rule validation; not counted toward any metric. |
| 26 Oct | Two consecutive modifications of one file ("sentinel-v02-mod-test.txt") | Two Rule "100002" Level 8 alerts | Modification only. Not two independent test cases or a regression suite. |
| 31 Oct | Observation of custom Rules "100003" (creation, Level 8) and "100004" (deletion, Level 8) | Seen in one terminal screenshot | **Observed, not validated.** Not a controlled test. |
| 2 Nov | One controlled creation, modification and deletion of one dedicated file ("sentinel-v03-final-test.txt") | Rule "100003" (creation), "100002" (modification), "100004" (deletion), each Level 8 | **Controlled lifecycle session.** One session on one file; not a regression suite, repeatability test or comprehensive coverage. Terminal screenshot; raw alert JSON not committed. |

**Rule "100002":** validated for controlled modification (11 and 26 October, and within the 2 November session on one dedicated file). It is not validated for other paths or event types or as a regression suite, and no detection rate is claimed.

**Rules "100003" and "100004":**
- **31 October:** screenshot-only observation. Raw alert records, process attribution, trigger and root cause are not established, and their definitions and loaded configuration were not inspected for that entry, so no matching behavior is asserted.
- **2 November:** both rules were observed at Level 8 in one controlled lifecycle session on one dedicated file. This is controlled-session evidence only. It does not retroactively validate the 31 October observations, does not explain the 16 October observations, and does not establish repeatability or comprehensive coverage.

**3 November on-disk verification of Rule "100002" (read-only):** the rule was present in "/var/ossec/etc/rules/local_rules.xml" with Level 8, parent condition "<if_sid>550</if_sid>" and file condition "^/home/", and "wazuh-analysisd" was running. The rule file's modification time preceded the analysis engine's start time, which is consistent with the engine starting after the file was modified. This does not conclusively establish the exact in-memory rule version loaded by the running engine, or the configuration loaded during the 16 October tests. No rule changes or manager restart were performed.

**Open question:** why Rule "100002" was absent from the reviewed 16 October creation and deletion records, and whether it is intended to cover those events, is unresolved. The on-disk definition confirmed on 3 November shows the "<if_sid>550</if_sid>" parent condition, but that is an unexamined dependency, not an established cause, and the in-memory and historically loaded rule versions have not been verified. No Wazuh rule changes, tuning, or metric measurements are claimed.

**Superseded wording:** earlier revisions of this file stated that Rules "554" and "100002" fired together on creation, recorded a different creation timestamp, and carried inconsistent creation-screenshot filenames. The source-record review supersedes these.

## Evidence

- v0.1: Dashboard showing the active SENTINEL-LINUX01 endpoint and the running Wazuh agent.
- v0.2 / v0.3 (11 October modification and CASE-001): custom Rule "100002" alert details, dashboard JSON, filtered FIM events, Rule "550" event details, and endpoint file metadata, under "evidence/v0.2/" and "evidence/v0.3/" and linked from "investigations/CASE-001.md".
- 16 October creation and deletion screenshots, referenced from "evidence/v0.3/readme.md". The source records were reviewed from "/var/ossec/logs/alerts/2026/Oct/ossec-alerts-16.json"; this runtime log is not claimed to be committed to the repository, and no raw-alert files are claimed as repository artifacts.
- 26 October modification screenshot: "evidence/v0.2/screenschots/v0.2-oct26-controlled-modification-source-alerts-new.png", referenced from "evidence/v0.3/readme.md" as "../v0.2/screenschots/v0.2-oct26-controlled-modification-source-alerts-new.png".
- 31 October observation: "evidence/v0.3/screenshots/v0.3-fim-lifecycle-custom-detections.png". Screenshot evidence only; no raw alert records are claimed as repository artifacts.
- E14 (endpoint configuration): "evidence/v0.3/screenshots/v0.3-e14-endpoint-syscheck-configuration.png". SENTINEL-LINUX01 local Syscheck configuration: "/home" monitored in real time, startup scan enabled, 43,200-second scan frequency.
- E15 (manager configuration): "evidence/v0.3/screenshots/v0.3-e15-manager-syscheck-configuration.png". SENTINEL-WAZUH manager-side Syscheck configuration only. It is not evidence of endpoint "/home" monitoring; E14 documents that.
- E16 (2 November lifecycle): "evidence/v0.3/screenshots/v0.3-fim-full-lifecycle-custom-rules.png". Controlled creation/modification/deletion session on one dedicated file.
- E14 and E15 are screenshots of local configuration files as captured; neither establishes which configuration was loaded during the 16 October tests. E16 is controlled-test evidence in a terminal screenshot. None of E14–E16 is a raw alert JSON record, and raw alert records for 31 October and 2 November are not committed.
- The 3 November on-disk verification is a maintainer-run read-only check; no screenshot or capture of it is claimed to be committed.
- The original source alert log for the 11 October test was not recovered; that result rests on the existing screenshots.
- Operational artifacts from the reported Wazuh Manager startup observation have not been confirmed saved in the repository.

## Engineering principles

- Development philosophy: BUILD → UNDERSTAND → TEST → BREAK → FIX → MEASURE → DOCUMENT → EXPLAIN. A control is not successful simply because it exists; detections must be tested, evidenced, measured, improved, and retested.
- Failure handling: STOP → CAPTURE → DOCUMENT → CONTINUE. Significant failures and architecture changes are recorded rather than hidden.
- Continue development when an optional environment component is unreliable rather than letting it block progress (lesson from the Windows VM issue).
- Configuration syntax validation, telemetry observation, custom-rule validation, and broader detection coverage are distinct claims and are documented separately.
- Broad home-directory FIM matching is flagged for noise evaluation; proposed tuning must be tested before its effectiveness is claimed.

## Roadmap

- v0.1 — Foundation: Complete.
- v0.2 — Detection Engineering: Controlled file-modification scenario validated; one controlled creation/modification/deletion lifecycle session recorded on 2 November (documented under v0.3). Broader coverage, additional telemetry sources, repeatable regression testing, and false-positive/missed-detection analysis remain open.
- v0.3 — SOC Investigation: **Complete — phase milestone.** The v0.3 documentation and evidence milestone is complete. CASE-001 remains open overall, and broader detection-engineering work and unresolved investigation questions remain open.
- v0.4 — Incident Response (Planned): controlled response actions, containment and eradication/recovery workflow, human-in-the-loop response, response performance measurement.
- v0.5 — Purple-Team Validation (Planned): detection coverage, detection rate and time, response time, false-positive/false-negative analysis, regression testing, before/after comparison.
- v0.6 — Attack DNA & Mutation (Planned): attack-chain representation, controlled attack variation, detection resilience testing, failure analysis, retesting against modified attacker behavior.

**Future expansion:** Windows and Active Directory endpoints (deferred from the core path), and a custom SENTINEL console on top of Wazuh (incident visualization, detection timelines, MITRE ATT&CK mapping, metrics, Attack DNA visualization, case reporting). Not currently implemented.

---

[0.3.0] - Unreleased

## v0.3 — SOC Investigation phase.

Purpose: investigate relevant security telemetry, validate detection results, document evidence, and produce a traceable investigation record. It builds on the v0.2 FIM detection and does not represent a complete threat-hunting, incident-response, or purple-team capability.

### Investigation

- Created CASE-001 for a controlled file-integrity modification test on SENTINEL-LINUX01 (test file "/home/sentinel-admin/sentinel-fim-validation.txt") and review of related FIM events.
- Reviewed additional home-directory events (desktop configuration, application state, cache files) and distinguished them from the controlled test result. Process attribution for those events was not established.
- Recorded a single controlled creation/modification/deletion lifecycle session on one dedicated file (2 November), committed the endpoint and manager Syscheck configuration screenshots (E14, E15), and performed a read-only on-disk verification of Rule "100002" (3 November).
- Scope, findings, limitations, disposition, and follow-up actions are in "investigations/CASE-001.md".
- Status: the v0.3 phase milestone and its documentation/evidence deliverables are complete. The controlled modification-validation objective and reviewed-scope evidence reconciliation are closed. The overall CASE-001 investigation and broader detection-engineering work remain open.

### Detection findings

See the "Detection findings" table, the 3 November verification and the open question under "[Unreleased]". In brief: Rule "100002" is validated for controlled modification; the 16 October records show built-in Rules "554"/"553" with Rule "100002" absent (unresolved, not a confirmed miss); Rules "100003"/"100004" were observed in one 31 October screenshot (not validated) and then in the separate 2 November controlled lifecycle session on one dedicated file (not a regression suite); the 3 November check verified the on-disk Rule "100002" definition only.

### Operational incident (reported; root cause unconfirmed)

- A Wazuh Manager startup reportedly timed out at about 45 seconds. A lock directory was removed after a check reportedly found no active Manager processes, and the Manager then started. The root cause is unconfirmed and the lock is not claimed to be the cause.
- One graceful Manager/endpoint VM restart cycle was reported successful, with Agent "002" reconnecting to Active. This is a single observation, not proof of resilience.

### Evidence

- CASE-001: "evidence/v0.3/v0.3-custom-rule-100002.png", "evidence/v0.3/v0.3-custom-rule-100002-dashboard-json.png", "evidence/v0.3/v0.3-case001-fim-filtered-events.png", "evidence/v0.3/v0.3-case001-rule-550-event-details.png", "evidence/v0.3/v0.3-case001-endpoint-file-metadata.png".
- 16 October (referenced from "evidence/v0.3/readme.md"): "evidence/v0.3/v0.3-oct16-creation-rule-554.png", "evidence/v0.3/v0.3-oct16-creation-file-path.png", "evidence/v0.3/v0.3-oct16-detection-rule-553.png", "evidence/v0.3/v0.3-oct16-detection-file-path.png".
- 26 October: "evidence/v0.2/screenschots/v0.2-oct26-controlled-modification-source-alerts-new.png" (stored under "evidence/v0.2/screenschots/", not copied into "evidence/v0.3/"; referenced as "../v0.2/screenschots/v0.2-oct26-controlled-modification-source-alerts-new.png").
- 31 October: "evidence/v0.3/screenshots/v0.3-fim-lifecycle-custom-detections.png". Screenshot evidence only.
- 2–3 November: E14, E15 and E16 are listed under "[Unreleased]" Evidence.

### Lessons learned

- A controlled test confirms only the behavior it exercised; the 2 November lifecycle session confirms that session on one file.
- A FIM alert shows a monitored file changed; it does not establish malicious intent or identify the responsible process.
- A built-in rule alert (Rule 554 or 553) is not a custom Rule 100002 alert and does not show whether the custom rule covers the same event.
- A single terminal screenshot of events with no established trigger is an observation, not a validated test.
- Screenshots and source records are different levels of evidence, and reviewing a source record is not the same as committing it to the repository.
- On-disk rule files and a running analysis engine do not by themselves prove which rule version is loaded in memory.
- Broad path matching can capture routine desktop activity; tuning must be followed by testing.
- Investigation conclusions must distinguish observed facts, interpretations, and unresolved questions.

### Not yet included in v0.3

- Resolution of why Rule "100002" was absent from the 16 October creation and deletion records, and investigation of the differences between the 16 and 31 October observations
- Process attribution and trigger for the 31 October events
- Broader creation/deletion coverage (other paths, files, repeated events) and repeatable regression tests; the 2 November lifecycle result is a single session on one dedicated file
- Verification of the in-memory loaded rule version, the configuration loaded during the 16 October tests, and "/home/" matching behavior (only the on-disk Rule "100002" definition was verified, on 3 November)
- Committed raw alert records for the 31 October and 2 November observations, and documented review of the definitions and loaded configuration of Rules "100003" and "100004"
- Systematic false-positive/false-negative testing and tested noise-reduction tuning
- Additional investigation cases and comprehensive multi-source threat hunting
- Incident-response workflow (no containment, eradication, or recovery exercise completed), detection coverage metrics, purple-team validation, MITRE ATT&CK mapping, Attack DNA / mutation testing

---

[0.2.0] - Unreleased

## v0.2 — Detection Engineering phase.

Purpose: build, test, and validate a first security detection on the Wazuh/Linux01 telemetry pipeline from v0.1. It does not represent complete detection coverage, investigation workflows, or response workflows.

- Configured Wazuh Syscheck (FIM) on SENTINEL-LINUX01, scoped to "/home".
- Authored custom rule "100002" to flag file-integrity modification events. Flow: SENTINEL-LINUX01 → Wazuh Agent → Syscheck/FIM → telemetry event → Rule "100002" → Level 8 alert.
- A controlled modification test produced a "syscheck_integrity_changed" event, a Rule "100002" match, and a Level 8 alert identifying the file and including integrity metadata. This validates the modification path for the controlled scenario only. It does not establish creation, deletion, other paths, or other scenarios.
- Evidence: the configured rule, the controlled test, the event, and the alert (under "evidence/v0.2/"); this was the first confirmed custom detection validation.

Lessons learned:

- A modification alert is not automatically malicious; it must be correlated with user, process, path, timestamp, and context.
- Rule 550 and custom Rule 100002 are distinct detections; evidence for one does not substitute for the other.
- Broad path matching can add noise from normal user-session activity.

Not yet included (planned for v0.3+): detection scenarios beyond FIM; expanded telemetry (authentication, process, command execution); systematic false-positive and missed-detection analysis; MITRE ATT&CK mapping; broader case workflows; metrics, coverage measurement, and purple-team validation; Attack DNA / mutation testing.

---

[0.1.0] - Unreleased

## v0.1 — Foundation phase.

Purpose: establish the infrastructure for later security testing. It does not represent a complete detection, investigation, or response system.

Completed:

- Virtual SOC infrastructure (SENTINEL-WAZUH), isolated lab network (SENTINEL-LAB), Kali attacker environment (SENTINEL-KALI), and Linux monitored endpoint (SENTINEL-LINUX01) with an enrolled, running Wazuh agent visible in the dashboard.
- Initial telemetry pipeline (agent-to-manager connectivity verified).
- Documentation, evidence, and failure-tracking structure.
- Architecture decision to proceed Linux-first, deferring Windows/AD.

Not yet included (planned for v0.2+): detection rules and testing, controlled attack scenarios, investigation and response workflows, metrics and purple-team validation, Attack DNA / mutation testing, SENTINEL console.
