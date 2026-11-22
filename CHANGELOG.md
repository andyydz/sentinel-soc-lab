## ChangeLog

All notable changes to SENTINEL are documented here: project-level changes, architecture decisions, validated milestones, and lessons learned.

This file is a summary, not a Git commit history, a technical tutorial, or a replacement for the detailed project documentation. Architecture, threat model, detection engineering, incident response, testing/metrics, and lessons/failure records are maintained separately, and investigation records are in "investigations/CASE-001.md" through "investigations/CASE-004.md" (indexed in "investigations/readme.md"). Where this file and those documents differ in detail, the detailed documents govern.

SENTINEL is a virtual cybersecurity SOC lab built around the lifecycle:

SIMULATE → DETECT → INVESTIGATE → RESPOND → MEASURE → IMPROVE → RETEST

The project's guiding question is: does your detection still work when the attacker changes tactics?

## Status at a glance

- **Built:** a Linux-first lab (Wazuh 4.14.8 on SENTINEL-WAZUH, SENTINEL-LINUX01 monitored endpoint with an active agent, SENTINEL-KALI attacker system) with File Integrity Monitoring (FIM) scoped to "/home".
- **Validated:** custom Rule "100002" (Level 8) on controlled file modification (11 and 26 October 2026), plus two separate controlled FIM lifecycle sessions (2 November and 18 November 2026).
- **2 November lifecycle:** one controlled session on "/home/sentinel-admin/sentinel-v03-final-test.txt": creation — Rule "100003", Level 8; modification — Rule "100002", Level 8; deletion — Rule "100004", Level 8. Terminal screenshot evidence. One controlled lifecycle session on one dedicated file, not a repeatable regression suite or proof of comprehensive FIM coverage.
- **18 November lifecycle:** a separate controlled session on "/home/sentinel-admin/fim-sprint-test.txt", with the same three rules at Level 8 (creation "100003", modification "100002", deletion "100004"), evidenced by raw alert JSON. One session on one file; not a regression suite or a detection rate. It is not merged with the 2 November session.
- **Observed, not validated:** custom Rules "100003" (creation, Level 8) and "100004" (deletion, Level 8) appeared in one terminal screenshot dated 31 October 2026 (application configuration path, trigger not established). Two separate 31 October raw alert JSON records for "sentinel-v03-controlled-test.txt" (creation and deletion only) are also committed; their relationship to the screenshot observation is not established.
- **Verified on disk only:** a read-only check on 3 November 2026 confirmed the on-disk Rule "100002" definition and that "wazuh-analysisd" was running. The in-memory rule version is not verified.
- **Documented:** CASE-001, an evidence-backed investigation, **closed on 18 November 2026 for its reviewed scope**; evidence reconciliation for that scope is closed. Closure does not mean the whole project or all detection engineering is complete.
- **Unresolved (historical):** Rule "100002" was absent from the reviewed 16 October creation and deletion records, which showed built-in Rules "554" and "553". The reason is unknown, including whether the custom rules were deployed and loaded on that date; this is not a confirmed detection miss.
- **Not done:** live Windows/Active Directory telemetry, full automated regression suite, and exhaustive false-positive/false-negative benchmarks across all paths.
- **Project status:** v0.1–v0.7 complete (CASE-001–004 + v0.6 purple-team metrics; v0.7 logtest transcripts restored and checksum-verified); v0.8 (FIM group isolation/Agent 002 probe) and v0.9 (Sysmon JSON replay ingestion & evidence) merged on main. Post-closeout engineering, validation and noise-tuning work remains open, including the post-tuning noise-suppression retest (residual `dconf` noise remains) and live Windows agent telemetry (out of scope for now). These are not prerequisites for CASE-001 closure.

---

[Unreleased]

### Windows Sysmon Telemetry Replay & Attack Detection (v0.4 milestone)

- **Telemetry replay:** replayed Windows Sysmon `.evtx` captures (Event IDs 1, 3, 10, 11) via `SENTINEL-LINUX01` using `python-evtx` NDJSON conversion and `wazuh-logcollector` ingestion (`json` format).
- **Detections validated:** custom ruleset `sentinel_sysmon_replay_rules.xml` (`100100+`). Validated 7 distinct attack alerts: Rule `100110` (Level 12, `T1059.003`), Rule `100111` (Level 10, `T1059.005`), Rule `100112` (Level 13, `T1003.001`/`T1218.011`), Rule `100140` (Level 10, `T1003.001`), Rule `100131` (Level 12, `T1003.001`/`T1218.011`), Rule `100120` (Level 8, `T1059.001`; candidate `T1105`), and Rule `100130` (Level 14, `T1003.001`).
- **Noise filtering:** base structural rules (`100100`-`100104`, Level 0) suppressed alert noise for 3 benign `services.exe -> svchost.exe` process creates.
- **Evidence preserved:** raw alert events committed to `evidence/sysmon-replay/sysmon_alerts_raw.json` with SHA-256 `b53473fd6340ec17365fec9cbbc1403e445523322c4c84ae28e40882995d7a59`. Full investigation write-up in `investigations/CASE-002.md`.
- **Scope & limitations:** validates parser, decoder, and rule logic against replayed EVTX logs; does not validate live kernel driver (`SysmonDrv.sys`) telemetry on bare-metal Windows.

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

Seven distinct evidence sets across six dates (11, 16, 26 and 31 October; 2 and 18 November). The 31 October date has two separate evidence sets, a screenshot observation and a raw alert JSON set, and their relationship is not established. The sets represent distinct observations or controlled tests, not one lifecycle test. Full detail (timestamps, file-size transitions, rule definitions) is in CASE-001 and the detection-engineering and testing/metrics documentation.

| Date (2026) | Scenario | Result | Status |
|---|---|---|---|
| 11 Oct | Controlled modification of "sentinel-fim-validation.txt" | Custom Rule "100002" Level 8 alert (built-in Rule "550" also observed) | Modification only. Supported by screenshots; original source alert log not recovered. |
| 16 Oct | Creation and deletion of "sentinel-audit-test.txt" | Built-in Rules "554" (creation) and "553" (deletion); Rule "100002" absent from both | Reviewed source records. Not a custom-rule validation; not counted toward any metric. |
| 26 Oct | Two consecutive modifications of one file ("sentinel-v02-mod-test.txt") | Two Rule "100002" Level 8 alerts | Modification only. Not two independent test cases or a regression suite. |
| 31 Oct (screenshot) | Observation of custom Rules "100003" (creation, Level 8) and "100004" (deletion, Level 8) under an application configuration path | Seen in one terminal screenshot | **Observed, not validated.** Not a controlled test; trigger not established. |
| 31 Oct (raw JSON) | Creation and deletion records for "sentinel-v03-controlled-test.txt" | Rule "100003" (creation) and "100004" (deletion), each Level 8, in two committed raw alert JSON records | Creation and deletion only; not a lifecycle test. Relationship to the 31 Oct screenshot observation not established. |
| 2 Nov | One controlled creation, modification and deletion of one dedicated file ("sentinel-v03-final-test.txt") | Rule "100003" (creation), "100002" (modification), "100004" (deletion), each Level 8 | **Controlled lifecycle session.** One session on one file; not a regression suite, repeatability test or comprehensive coverage. Terminal screenshot; raw alert JSON not committed. |
| 18 Nov | One controlled creation, modification and deletion of one dedicated file ("fim-sprint-test.txt") | Rule "100003" (creation), "100002" (modification), "100004" (deletion), each Level 8 | **Separate controlled lifecycle session** with raw alert JSON ("evidence/v0.3/raw-alerts/fim-lifecycle-evidence.json"). One session on one file; not a regression suite, detection rate or comprehensive coverage. Not merged with 2 Nov. |

**Rule "100002":** validated for controlled modification (11 and 26 October, and within the 2 and 18 November sessions on one dedicated file each). It is not validated for other paths or event types or as a regression suite, and no detection rate is claimed.

**Rules "100003" and "100004":**
- **31 October (screenshot):** observation only. Raw alert records for it, process attribution, trigger and root cause are not established, and their definitions and loaded configuration were not inspected for that entry, so no matching behavior is asserted.
- **31 October (raw JSON):** two committed alert records for "sentinel-v03-controlled-test.txt", creation and deletion only. Separate from the screenshot observation and from the 2 November session.
- **2 and 18 November:** both rules were observed at Level 8 in two separate controlled lifecycle sessions, each on one dedicated file. Controlled-session evidence only. It does not retroactively validate the 31 October observations, does not explain the 16 October observations, and does not establish repeatability or comprehensive coverage.

**3 November on-disk verification of Rule "100002" (read-only):** the rule was present in "/var/ossec/etc/rules/local_rules.xml" with Level 8, parent condition "<if_sid>550</if_sid>" and file condition "^/home/", and "wazuh-analysisd" was running. The rule file's modification time preceded the analysis engine's start time, which is consistent with the engine starting after the file was modified. This does not conclusively establish the exact in-memory rule version loaded by the running engine, or the configuration loaded during the 16 October tests. No rule changes or manager restart were performed.

**Open question:** why Rule "100002" was absent from the reviewed 16 October creation and deletion records, and whether it is intended to cover those events, is unresolved. The on-disk definition confirmed on 3 November shows the "<if_sid>550</if_sid>" parent condition, but that is an unexamined dependency, not an established cause, and the in-memory and historically loaded rule versions have not been verified. No rule changes, tuning, or metric measurements are claimed for this question; the 18 November rule standardization and the v0.8 tuning are separate, later changes.

**Superseded wording:** earlier revisions of this file stated that Rules "554" and "100002" fired together on creation, recorded a different creation timestamp, and carried inconsistent creation-screenshot filenames. The source-record review supersedes these.

## Evidence

- v0.1: Dashboard showing the active SENTINEL-LINUX01 endpoint and the running Wazuh agent.
- v0.2 / v0.3 (11 October modification and CASE-001): custom Rule "100002" alert details, dashboard JSON, filtered FIM events, Rule "550" event details, and endpoint file metadata, under "evidence/v0.2/" and "evidence/v0.3/" and linked from "investigations/CASE-001.md".
- 16 October creation and deletion screenshots, referenced from "evidence/v0.3/readme.md". The source records were reviewed from "/var/ossec/logs/alerts/2026/Oct/ossec-alerts-16.json"; this runtime log is not claimed to be committed to the repository, and no raw-alert files are claimed as repository artifacts for 16 October.
- 26 October modification screenshot: "evidence/v0.2/screenschots/v0.2-oct26-controlled-modification-source-alerts-new.png", referenced from "evidence/v0.3/readme.md" as "../v0.2/screenschots/v0.2-oct26-controlled-modification-source-alerts-new.png".
- 31 October observation: "evidence/v0.3/screenshots/v0.3-fim-lifecycle-custom-detections.png". Screenshot evidence only; no raw alert records are committed for this observation.
- 31 October raw alert JSON (separate set): "evidence/v0.3/raw-alerts/sentinel-v03-creation-alert.json" and "evidence/v0.3/raw-alerts/sentinel-v03-deletion-alert.json" (file "sentinel-v03-controlled-test.txt"). These are Wazuh alert records, not original Syscheck input logs.
- 18 November lifecycle raw alert JSON: "evidence/v0.3/raw-alerts/fim-lifecycle-evidence.json" (three Wazuh alert records for "fim-sprint-test.txt"). The manifest "evidence/v0.3/raw-alerts/SHA256SUMS" covers the three raw JSON files; the checksums were not independently recomputed for this documentation.
- E14 (endpoint configuration): "evidence/v0.3/screenshots/v0.3-e14-endpoint-syscheck-configuration.png". SENTINEL-LINUX01 local Syscheck configuration: "/home" monitored in real time, startup scan enabled, 43,200-second scan frequency.
- E15 (manager configuration): "evidence/v0.3/screenshots/v0.3-e15-manager-syscheck-configuration.png". SENTINEL-WAZUH manager-side Syscheck configuration only. It is not evidence of endpoint "/home" monitoring; E14 documents that.
- E16 (2 November lifecycle): "evidence/v0.3/screenshots/v0.3-fim-full-lifecycle-custom-rules.png". Controlled creation/modification/deletion session on one dedicated file.
- E14 and E15 are screenshots of local configuration files as captured; neither establishes which configuration was loaded during the 16 October tests. E16 is controlled-test evidence in a terminal screenshot. None of E14–E16 is a raw alert JSON record, and no raw alert JSON is committed for the 2 November session or the 31 October screenshot observation.
- The 3 November on-disk verification is a maintainer-run read-only check; no screenshot or capture of it is claimed to be committed.
- The original source alert log for the 11 October test was not recovered; that result rests on the existing screenshots.
- Operational artifacts from the reported Wazuh Manager startup observation have not been confirmed saved in the repository.

## Engineering principles

- Development philosophy: BUILD → UNDERSTAND → TEST → BREAK → FIX → MEASURE → DOCUMENT → EXPLAIN. A control is not successful simply because it exists; detections must be tested, evidenced, measured, improved, and retested.
- Failure handling: STOP → CAPTURE → DOCUMENT → CONTINUE. Significant failures and architecture changes are recorded rather than hidden.
- Continue development when an optional environment component is unreliable rather than letting it block progress (lesson from the Windows VM issue).
- Configuration syntax validation, telemetry observation, custom-rule validation, and broader detection coverage are distinct claims and are documented separately.
- Broad home-directory FIM matching is flagged for noise evaluation; tuning must be tested before its effectiveness is claimed. v0.8 tuning is implemented; residual `dconf` noise remains and the broader retest is pending.

## Roadmap

- v0.1 — Foundation: Complete.
- v0.2 — Detection Engineering: Controlled file-modification scenario validated; controlled creation/modification/deletion lifecycle sessions recorded on 2 November and 18 November (documented under v0.3). Broader coverage, additional telemetry sources, repeatable regression testing, and false-positive/missed-detection analysis remain open.
- v0.3 — SOC Investigation: **Complete — phase milestone.** The v0.3 documentation and evidence milestone is complete, and CASE-001 was closed on 18 November 2026 for its reviewed scope. Post-closeout engineering, validation, noise-tuning and historical evidence-recovery work remains open and is not a prerequisite for CASE-001 closure.
- v0.4 — Windows Sysmon Replay Detection (Complete — CASE-002): validated Rules 100110-100140 on replayed EVTX telemetry.
- v0.5 — Incident Response & SSH Brute-Force Triage (Complete — CASE-003): validated SSH rules 100200/100201 against Hydra simulation from SENTINEL-KALI. Triage used an automated Python CLI; containment was a documented manual procedure referencing NIST SP 800-61r2. No automated containment or persistent IP block is claimed.

- v0.6 — Purple-Team Measurement (Complete — metrics/v0.6-purple-team-measurement.md): measurement of detection results across controlled FIM, Sysmon replay and SSH tests, with false-positive/false-negative observations and before/after comparison; the outcomes are in the measurement report. Response time was not measured, and cross-VM timing is limited by clock skew. Results are small controlled samples, not statistically meaningful detection or false-positive/false-negative rates, and not a completed automated regression suite.
- v0.7 — Attack DNA & Mutation (Complete — CASE-004): hidden-path FIM testing, benign cache/desktop noise observation, Sysmon `#24` mutation testing, SSH sub-threshold/publickey checks, and `wazuh-logtest` transcript restoration.
- v0.8 & v0.9 — FIM Group Isolation, Noise/Hidden-Path Tuning, SSH Checks & Sysmon Replay: Complete and merged on `main`. For v0.8, FIM group isolation and selected noise exclusions are implemented tuning, not complete noise resolution. v0.9 is Sysmon JSON replay ingestion and evidence; v0.9.1 is a separate, later follow-up on field/timestamp separation in the Python triage integration. These are post-closeout developments, not CASE-001 evidence. The post-tuning noise-suppression retest (residual `dconf` noise remains) and live Windows endpoint telemetry remain pending/out-of-scope.

**Future expansion:** Windows and Active Directory endpoints (deferred from the core path), and a custom SENTINEL console on top of Wazuh (incident visualization, detection timelines, MITRE ATT&CK mapping, metrics, Attack DNA visualization, case reporting). Not currently implemented.

---

[0.3.0] - Unreleased

## v0.3 — SOC Investigation phase.

Purpose: investigate relevant security telemetry, validate detection results, document evidence, and produce a traceable investigation record. It builds on the v0.2 FIM detection and does not represent a complete threat-hunting, incident-response, or purple-team capability.

### Investigation

- Created CASE-001 for a controlled file-integrity modification test on SENTINEL-LINUX01 (test file "/home/sentinel-admin/sentinel-fim-validation.txt") and review of related FIM events.
- Reviewed additional home-directory events (desktop configuration, application state, cache files) and distinguished them from the controlled test result. Process attribution for those events was not established.
- Recorded a controlled creation/modification/deletion lifecycle session on one dedicated file (2 November), committed the endpoint and manager Syscheck configuration screenshots (E14, E15), and performed a read-only on-disk verification of Rule "100002" (3 November).
- 18 November closeout: verified the endpoint's real-time "/home" Syscheck configuration; standardized the three custom FIM rules to the anchored "^/home/" prefix and added MITRE ATT&CK tags (Rule "100003" T1105, Rule "100002" T1565.001, Rule "100004" T1070.004), which describe each rule's detection purpose and are not evidence that a technique occurred; recorded a separate controlled lifecycle session on "fim-sprint-test.txt" with raw alert JSON; and observed benign GNOME Tracker3 cache activity triggering Rule "100002" at Level 8.
- Scope, findings, limitations, disposition, and follow-up actions are in "investigations/CASE-001.md".
- Status: CASE-001 was closed on 18 November 2026 for its reviewed scope, and the v0.3 phase milestone and its documentation/evidence deliverables are complete. Closure does not mean all detection engineering is complete. Post-closeout engineering, validation, noise-tuning and historical evidence-recovery work remains open and is not a prerequisite for closure. The later milestones v0.6, v0.8, v0.9 and v0.9.1 are separate developments, not CASE-001 evidence.

### Detection findings

See the "Detection findings" table, the 3 November verification and the open question under "[Unreleased]". In brief: Rule "100002" is validated for controlled modification; the 16 October records show built-in Rules "554"/"553" with Rule "100002" absent (unresolved, not a confirmed miss); Rules "100003"/"100004" were observed in one 31 October screenshot (not validated), appear in separate 31 October raw JSON records (creation and deletion only), and fired in two separate controlled lifecycle sessions on one dedicated file each (2 and 18 November; not a regression suite); the 3 November check verified the on-disk Rule "100002" definition only.

### Operational incident (reported; root cause unconfirmed)

- A Wazuh Manager startup reportedly timed out at about 45 seconds. A lock directory was removed after a check reportedly found no active Manager processes, and the Manager then started. The root cause is unconfirmed and the lock is not claimed to be the cause.
- One graceful Manager/endpoint VM restart cycle was reported successful, with Agent "002" reconnecting to Active. This is a single observation, not proof of resilience.

### Evidence

- CASE-001: "evidence/v0.3/v0.3-custom-rule-100002.png", "evidence/v0.3/v0.3-custom-rule-100002-dashboard-json.png", "evidence/v0.3/v0.3-case001-fim-filtered-events.png", "evidence/v0.3/v0.3-case001-rule-550-event-details.png", "evidence/v0.3/v0.3-case001-endpoint-file-metadata.png".
- 16 October (referenced from "evidence/v0.3/readme.md"): "evidence/v0.3/v0.3-oct16-creation-rule-554.png", "evidence/v0.3/v0.3-oct16-creation-file-path.png", "evidence/v0.3/v0.3-oct16-detection-rule-553.png", "evidence/v0.3/v0.3-oct16-detection-file-path.png".
- 26 October: "evidence/v0.2/screenschots/v0.2-oct26-controlled-modification-source-alerts-new.png" (stored under "evidence/v0.2/screenschots/", not copied into "evidence/v0.3/"; referenced as "../v0.2/screenschots/v0.2-oct26-controlled-modification-source-alerts-new.png").
- 31 October: "evidence/v0.3/screenshots/v0.3-fim-lifecycle-custom-detections.png" (screenshot evidence only) and, as a separate set, the raw alert JSON files under "evidence/v0.3/raw-alerts/".
- 2–3 November: E14, E15 and E16 are listed under "[Unreleased]" Evidence.
- 18 November: "evidence/v0.3/raw-alerts/fim-lifecycle-evidence.json", with the "SHA256SUMS" manifest in the same directory.

### Lessons learned

- A controlled test confirms only the behavior it exercised; each lifecycle session confirms that session on one file.
- A FIM alert shows a monitored file changed; it does not establish malicious intent or identify the responsible process.
- A built-in rule alert (Rule 554 or 553) is not a custom Rule 100002 alert and does not show whether the custom rule covers the same event.
- A single terminal screenshot of events with no established trigger is an observation, not a validated test.
- Screenshots and source records are different levels of evidence, and reviewing a source record is not the same as committing it to the repository.
- On-disk rule files and a running analysis engine do not by themselves prove which rule version is loaded in memory.
- Broad path matching can capture routine desktop activity; tuning must be followed by testing.
- Investigation conclusions must distinguish observed facts, interpretations, and unresolved questions.

### Not included in v0.3 (carried forward as post-closeout follow-up where applicable)

- Resolution of why Rule "100002" was absent from the 16 October creation and deletion records, and investigation of the differences between the 16 and 31 October observations
- Process attribution and trigger for the 31 October events, and the relationship between the two 31 October evidence sets
- Broader creation/deletion coverage (other paths, files, file types, sizes, repeated events) and repeatable regression tests; the 2 and 18 November results are single sessions on one dedicated file each
- Verification of the in-memory loaded rule version and the configuration loaded during the 16 October tests (only the on-disk Rule "100002" definition was verified, on 3 November)
- Committed raw alert records for the 31 October screenshot observation and the 2 November session, and documented review of the definitions and loaded configuration of Rules "100003" and "100004"
- Systematic false-positive/false-negative testing; broader noise-suppression retesting (selected tuning was implemented later, in v0.8; residual `dconf` noise remains)
- Additional investigation cases and comprehensive multi-source threat hunting
- Incident-response workflow (no containment, eradication, or recovery exercise completed for CASE-001), detection coverage metrics, purple-team validation, comprehensive MITRE ATT&CK mapping (tags were added to the three custom FIM rules at the 18 November closeout), Attack DNA / mutation testing

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
