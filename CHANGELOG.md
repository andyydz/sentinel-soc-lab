## ChangeLog

All notable changes to SENTINEL are documented here: project-level changes, architecture decisions, validated milestones, and lessons learned.

This file is a summary, not a Git commit history, a technical tutorial, or a replacement for the detailed project documentation. Architecture, threat model, detection engineering, incident response, testing/metrics, and lessons/failure records are maintained separately, and the investigation record is in "investigations/CASE-001.md". Where this file and those documents differ in detail, the detailed documents govern.

SENTINEL is a virtual cybersecurity SOC lab built around the lifecycle:

SIMULATE → DETECT → INVESTIGATE → RESPOND → MEASURE → IMPROVE → RETEST

The project's guiding question is: does your detection still work when the attacker changes tactics?

## Status at a glance

- **Built:** a Linux-first lab (Wazuh 4.14.8 on SENTINEL-WAZUH, SENTINEL-LINUX01 monitored endpoint with an active agent, SENTINEL-KALI attacker system) with File Integrity Monitoring (FIM) scoped to "/home".
- **Validated:** custom Rule "100002" (Level 8) on controlled file modification (11 and 26 October 2026). Modification scenario only.
- **Observed, not validated:** custom Rules "100003" (creation, Level 8) and "100004" (deletion, Level 8) appeared in one terminal screenshot dated 31 October 2026. This is not a validated controlled test.
- **Documented:** CASE-001, an evidence-backed investigation. Evidence reconciliation for the reviewed scope is closed; the overall case remains open.
- **Unresolved:** Rule "100002" was absent from the reviewed 16 October creation and deletion records, which showed built-in Rules "554" and "553". The reason is unknown; this is not a confirmed detection miss.
- **Not done:** detection rate, false-positive/false-negative measurement, complete FIM coverage, and any containment, eradication, or recovery exercise. v0.4–v0.6 are planned.

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

Four separate sets of observations. They are different tests on different dates and are not one lifecycle test. Full detail (timestamps, file-size transitions, rule definitions) is in CASE-001 and the detection-engineering and testing/metrics documentation.

| Date (2026) | Scenario | Result | Status |
|---|---|---|---|
| 11 Oct | Controlled modification of "sentinel-fim-validation.txt" | Custom Rule "100002" Level 8 alert (built-in Rule "550" also observed) | Modification only. Supported by screenshots; original source alert log not recovered. |
| 16 Oct | Creation and deletion of "sentinel-audit-test.txt" | Built-in Rules "554" (creation) and "553" (deletion); Rule "100002" absent from both | Reviewed source records. Not a custom-rule validation; not counted toward any metric. |
| 26 Oct | Two consecutive modifications of one file ("sentinel-v02-mod-test.txt") | Two Rule "100002" Level 8 alerts | Modification only. Not two independent test cases or a regression suite. |
| 31 Oct | Observation of custom Rules "100003" (creation, Level 8) and "100004" (deletion, Level 8) | Seen in one terminal screenshot | **Observed, not validated.** Not a controlled test. |

**Rule "100002":** validated for the controlled modification scenario only. It is not validated for creation or deletion, other paths or event types, or as a regression suite, and no detection rate is claimed.

**Rules "100003" and "100004" (31 October):** raw alert records, process attribution, and root cause are not established. Their on-disk definitions and loaded configuration were not inspected for this entry, so no matching behavior is asserted. These observations are kept separate from the 16 October built-in records and the Rule "100002" modification validation, and they do not explain or resolve the open question below.

**Open question:** why Rule "100002" was absent from the reviewed 16 October creation and deletion records, and whether it is intended to cover those events, is unresolved. A read-only inspection showed its parent condition is "<if_sid>550</if_sid>" with a "/home/" file condition, but that is an unexamined dependency, not an established cause. The rule version loaded during the historical tests has not been reverified. No Wazuh rule changes, tuning, or metric measurements are claimed.

**Superseded wording:** earlier revisions of this file stated that Rules "554" and "100002" fired together on creation, recorded a different creation timestamp, and carried inconsistent creation-screenshot filenames. The source-record review supersedes these.

## Evidence

- v0.1: Dashboard showing the active SENTINEL-LINUX01 endpoint and the running Wazuh agent.
- v0.2 / v0.3 (11 October modification and CASE-001): custom Rule "100002" alert details, dashboard JSON, filtered FIM events, Rule "550" event details, and endpoint file metadata, under "evidence/v0.2/" and "evidence/v0.3/" and linked from "investigations/CASE-001.md".
- 16 October creation and deletion screenshots, referenced from "evidence/v0.3/readme.md". The source records were reviewed from "/var/ossec/logs/alerts/2026/Oct/ossec-alerts-16.json"; this runtime log is not claimed to be committed to the repository, and no raw-alert files are claimed as repository artifacts.
- 26 October modification screenshot: "evidence/v0.2/screenshots/v0.2-oct26-controlled-modification-source-alerts-new.png", referenced from "evidence/v0.3/readme.md" as "../v0.2/screenshots/v0.2-oct26-controlled-modification-source-alerts-new.png".
- 31 October observation: "evidence/v0.3/screenshots/v0.3-fim-lifecycle-custom-detections.png". Screenshot evidence only; no raw alert records are claimed as repository artifacts.
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
- v0.2 — Detection Engineering: Controlled file-modification scenario validated. Broader coverage, additional telemetry sources, and false-positive/missed-detection analysis remain open.
- v0.3 — SOC Investigation (In progress): CASE-001 documented; reviewed-scope evidence reconciliation closed; overall case and broader detection-engineering work open.
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
- Scope, findings, limitations, disposition, and follow-up actions are in "investigations/CASE-001.md".
- Status: the controlled modification-validation objective and reviewed-scope evidence reconciliation are closed. The overall CASE-001 investigation and broader detection-engineering work remain open.

### Detection findings

See the "Detection findings" table and open question under "[Unreleased]". In brief: Rule "100002" is validated for controlled modification only; the 16 October records show built-in Rules "554"/"553" with Rule "100002" absent (unresolved, not a confirmed miss); Rules "100003"/"100004" were observed in one 31 October screenshot and are not validated.

### Operational incident (reported; root cause unconfirmed)

- A Wazuh Manager startup reportedly timed out at about 45 seconds. A lock directory was removed after a check reportedly found no active Manager processes, and the Manager then started. The root cause is unconfirmed and the lock is not claimed to be the cause.
- One graceful Manager/endpoint VM restart cycle was reported successful, with Agent "002" reconnecting to Active. This is a single observation, not proof of resilience.

### Evidence

- CASE-001: "evidence/v0.3/v0.3-custom-rule-100002.png", "evidence/v0.3/v0.3-custom-rule-100002-dashboard-json.png", "evidence/v0.3/v0.3-case001-fim-filtered-events.png", "evidence/v0.3/v0.3-case001-rule-550-event-details.png", "evidence/v0.3/v0.3-case001-endpoint-file-metadata.png".
- 16 October (referenced from "evidence/v0.3/readme.md"): "evidence/v0.3/v0.3-oct16-creation-rule-554.png", "evidence/v0.3/v0.3-oct16-creation-file-path.png", "evidence/v0.3/v0.3-oct16-detection-rule-553.png", "evidence/v0.3/v0.3-oct16-detection-file-path.png".
- 26 October: "evidence/v0.2/screenschots/v0.2-oct26-controlled-modification-source-alerts-new.png" (stored under "evidence/v0.2/screenshots/", not copied into "evidence/v0.3/"; referenced as "../v0.2/screenschots/v0.2-oct26-controlled-modification-source-alerts-new.png").
- 31 October: "evidence/v0.3/screenshots/v0.3-fim-lifecycle-custom-detections.png". Screenshot evidence only.

### Lessons learned

- A controlled test confirms only the behavior it exercised.
- A FIM alert shows a monitored file changed; it does not establish malicious intent or identify the responsible process.
- A built-in rule alert (Rule 554 or 553) is not a custom Rule 100002 alert and does not show whether the custom rule covers the same event.
- A single terminal screenshot is an observation, not a validated test.
- Screenshots and source records are different levels of evidence, and reviewing a source record is not the same as committing it to the repository.
- Broad path matching can capture routine desktop activity; tuning must be followed by testing.
- Investigation conclusions must distinguish observed facts, interpretations, and unresolved questions.

### Not yet included in v0.3

- Resolution of why Rule "100002" was absent from the 16 October creation and deletion records
- Validated controlled tests of Rules "100003" and "100004", with raw alert records and review of their definitions and loaded configuration
- Verification of current loaded rule configuration and "/home/" matching behavior
- Repeatable regression tests for creation, modification, and deletion
- Systematic false-positive/false-negative testing and tested noise-reduction tuning
- Additional investigation cases and comprehensive multi-source threat hunting
- Incident-response workflow, detection coverage metrics, purple-team validation, MITRE ATT&CK mapping, Attack DNA / mutation testing

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
