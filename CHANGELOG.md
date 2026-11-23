# Changelog

SENTINEL is a virtual SOC lab built around one lifecycle: **SIMULATE → DETECT → INVESTIGATE → RESPOND → MEASURE → IMPROVE → RETEST**. Its guiding question is: *does your detection still work when the attacker changes tactics?*

This file is a project-level summary: milestones, architecture decisions, what the evidence supports, and what is still open. It is not a commit history or a technical report. Where it differs in detail from the project documentation, the detailed documents govern: [`docs/05-detection-engineering.md`](docs/05-detection-engineering.md), [`docs/07-testing-and-metrics.md`](docs/07-testing-and-metrics.md), [`detections/readme.md`](detections/readme.md), and the investigation records [`CASE-001`](investigations/CASE-001.md) to [`CASE-004`](investigations/CASE-004.md) (indexed in [`investigations/readme.md`](investigations/readme.md)).

---

## Status at a glance

- **Built:** a Linux-first lab on an isolated network: Wazuh 4.14.8 (`SENTINEL-WAZUH`), a monitored endpoint with an active agent (`SENTINEL-LINUX01`), and a controlled attacker VM (`SENTINEL-KALI`). Detections cover Linux file integrity monitoring (FIM) on `/home`, SSH authentication, and replayed Windows Sysmon telemetry.
- **CASE-001 is closed.** It was closed on **18 November 2026** for its reviewed scope, and the v0.3 documentation and evidence milestone is complete. Closure does not mean the whole project or all detection engineering is complete.
- **FIM evidence:** custom Rule `100002` (modification, Level 8) was confirmed in controlled modification tests on 11 October (screenshot-supported only) and 26 October. Four documented controlled single-file lifecycle sessions (creation, modification, deletion) exist. The 2 and 18 November sessions belong to CASE-001. The 20 November (v0.6) and 21 November (v0.8) sessions are separate post-closeout developments. They are not a repeatable automated regression suite and do not establish comprehensive FIM coverage. The additional 22 November v0.10 and v0.11 probe sequences each have separate evidence. They are distinct from these four sessions and from each other, and are not merged into either. They also do not establish a repeatable automated regression suite or comprehensive FIM coverage.
- **Observed, not validated:** two separate 31 October evidence sets for Rules `100003`/`100004`. Their relationship and trigger origin are not established.
- **Unresolved (historical):** the 16 October creation and deletion records show built-in Rules `554` and `553`. Whether custom Rules `100003` and `100004` were deployed and loaded then is unknown. This is not a confirmed detection failure.
- **Post-closeout work (v0.6, v0.8, v0.9, v0.9.1, v0.10, v0.11):** separate developments, not CASE-001 evidence. The v0.11 milestone status remains pending reconciliation (see the v0.11 bullet below). The broader noise-suppression retest is pending and residual `dconf` noise remains. This work is not a prerequisite for CASE-001 closure.
- **v0.11 (pending reconciliation):** evidence artifacts are committed under `evidence/v0.11/`, but the milestone description and status are not yet reconciled. See the [v0.11 evidence-status note](#v011---evidence-status-pending-reconciliation) in the version history below.
- **Not done:** live Windows or Active Directory telemetry, a repeatable automated regression suite, and false-positive/false-negative benchmarks. No detection rates are claimed.

---

## Roadmap

| Milestone | Status | Summary |
|---|---|---|
| v0.1 Foundation | Complete | Lab infrastructure, Wazuh, enrolled agent, documentation structure |
| v0.2 Detection Engineering | Complete | First custom FIM detection (Rule `100002`), validated for controlled modification only |
| v0.3 SOC Investigation | **Complete** | CASE-001 closed on 18 November 2026; documentation and evidence milestone complete |
| v0.4 Sysmon Replay Detection | Complete | CASE-002: seven selected detections on replayed EVTX telemetry |
| v0.5 Incident Response and SSH Triage | Complete | CASE-003: SSH rules `100200`/`100201`, Python-assisted triage, manual containment procedure |
| v0.6 Purple-Team Measurement | Complete | Small controlled measurement across FIM, Sysmon replay and SSH |
| v0.7 Attack DNA and Mutation | Complete | CASE-004: mutation and reliability observations |
| v0.8 FIM Tuning | Complete, merged on `main` | FIM group isolation, selected noise exclusions, Agent `002` probe; broader retest pending |
| v0.9 Sysmon JSON Replay and Triage | Complete, merged on `main` | Manager-side JSON replay ingestion; Python-assisted triage integration |
| v0.9.1 | Follow-up | Field and timestamp handling separated in the Python triage integration |
| v0.10 | Validation | Live Linux FIM probe (`100003`, `100002`, `100004`) and `python-soc-automation` triage validation |

v0.6, v0.8, v0.9, v0.9.1, and v0.10 were developed after CASE-001 closed and are not CASE-001 evidence.

v0.11 is intentionally not listed in the table above. Its evidence artifacts are committed ([`v011_fim_alerts.json`](evidence/v0.11/v011_fim_alerts.json), [`triage_report.md`](evidence/v0.11/triage_report.md), [`regression_summary.json`](evidence/v0.11/regression_summary.json)), but its milestone description and status remain pending reconciliation. It is not recorded as a completed milestone.

---

## [v0.11] - Evidence status (pending reconciliation)

v0.11 evidence artifacts are committed to the repository. The v0.11 milestone description and status remain **pending reconciliation**. This note records only what the committed artifacts establish; it does not give v0.11 a title, completion date, validation status or broader results.

### Committed artifacts
- [`evidence/v0.11/v011_fim_alerts.json`](evidence/v0.11/v011_fim_alerts.json): 10 Wazuh alert records across Rules `100002`, `100003` and `100004`.
  - Three records document creation, modification and deletion of `/home/sentinel-admin/v011_fim_probe.txt`. Those three probe events matched their corresponding custom FIM rules at Level 8.
  - The remaining seven records concern desktop/configuration paths, including `dconf` and `tiling-assistant`. The available report does not establish that these are confirmed benign noise, and it does not attribute them to a process.
- [`evidence/v0.11/triage_report.md`](evidence/v0.11/triage_report.md): reports 10 filtered alerts and three unique rules. The process, target-process and event-time enrichment fields are `None`.
- [`evidence/v0.11/regression_summary.json`](evidence/v0.11/regression_summary.json): contains pre-cutoff and post-cutoff rule counts, along with path counts. It does not independently establish test criteria, expected outcomes, pass/fail status or a completed regression suite.

### Limits
- The three-event probe is evidence of one controlled lifecycle on one file. It is not proof of a repeatable regression suite or of comprehensive FIM coverage.
- The aggregate rule counts alone do not prove that a regression suite passed.
- This evidence is repository-committed, unlike the v0.10 archive, which remains outside the repository at `~/soc-evidence/v0.10-fim-probe/`. The two are distinct.
- Residual desktop-path FIM noise and the broader noise-suppression retest remain open.

## [v0.10] - 2026-11-22

### Added
- Documented live Linux FIM (`100003`, `100002`, `100004` on `/home/sentinel-admin/.fim_probe_test.txt`) triage integration with `python-soc-automation` `v1.0` (commit `9696707`), distinct from `v0.9` Sysmon JSON replay.
- Recorded archived evidence (`fim_probe_alerts.json`, `fim_probe_report.md`, and `SHA256SUMS` in `~/soc-evidence/v0.10-fim-probe/`) and cleanup of temporary `/tmp` probe files.

### Notes
- Open FIM noise-tuning items (`dconf`, Tracker3, Nautilus) remain open and separate from `v0.10`.

## v0.9.1 and v0.9 — Sysmon JSON Replay and Python Triage

- **v0.9:** replay JSON events were ingested by a manager-side logcollector. Alerts fired for Rules `100110`, `100130` and `100140` ([evidence](evidence/v0.9/readme.md)). This does not mean every Sysmon rule was independently validated. Replayed telemetry only, not a live endpoint.
- **Python triage:** the separate companion project [`python-soc-automation`](https://github.com/andyydz/python-soc-automation) parses Wazuh alert JSON and performs severity-based triage (v0.9 used `--triage --min-level 8`). Its 195 passing pytest tests cover the Python tool, not Wazuh detection coverage. It does not perform containment, eradication or recovery and is not a SOAR platform.
- **v0.9.1:** follow-up separating field and timestamp handling in the triage integration.

## v0.8 — FIM Group Isolation and Noise Tuning

- FIM rules were given a dedicated `sentinel_fim` group, separated from SSH-related inherited grouping. Selected Tracker3 and Nautilus database activity was excluded, and hidden dot-directory monitoring was preserved.
- **21 November Agent `002` probe (post-closeout, not CASE-001 evidence):** creation, modification and deletion of one probe file each matched the corresponding custom rule at Level 8, with `sentinel_fim` present and `sshd` absent.
- A stateful `wazuh-logtest` session confirmed the six-failure threshold of SSH Rule `100201`.
- **Limits:** tuning is implemented, not noise resolved. Residual desktop noise under `/home/sentinel-admin/.config/dconf/user` remains, the broader noise-suppression retest is pending, and the exclusions have not been independently validated by targeted tests. The probe is one lifecycle on one file, not a regression suite.

## v0.7 — Attack DNA and Mutation Testing (CASE-004)

- Hidden files inside `/home` triggered FIM; staging in `/var/tmp`, outside the monitored scope, did not. Benign cache and desktop activity produced Level 8 noise.
- A Sysmon command-line mutation (`#24`) bypassed keyword-specific Rule `100112` and matched the Level 0 base rule. Correlation with other event types is a possible improvement and is not implemented.
- SSH sub-threshold and publickey checks were run, and `wazuh-logtest` transcripts were restored and checksum-verified.
- Observations from controlled testing, not complete characterisations. See [CASE-004](investigations/CASE-004.md).

## v0.6 — Purple-Team Measurement

Report: [`metrics/v0.6-purple-team-measurement.md`](metrics/v0.6-purple-team-measurement.md).

- **FIM (20 November, post-closeout):** 3/3 selected lifecycle events detected; 0/3 `/tmp` negative-control operations alerted.
- **Sysmon replay:** 7/7 selected detections fired; 0/3 benign events alerted; two Event ID 7 ImageLoad events remained uncovered.
- **SSH:** baseline and threshold escalation were measured. C1 produced four `100200` alerts and no `100201`; C2 produced eight `100200` and two `100201`. The first C2 escalation fired early because four C1 failures were still inside the 60-second window.
- **Limits:** small controlled samples, not statistically meaningful detection or false-positive/false-negative rates. Cross-VM timing was affected by clock skew, and response time was not measured. This is not a completed automated regression suite.

## v0.5 — Incident Response and SSH Triage (CASE-003)

- SENTINEL-KALI generated 21 failed SSH authentication attempts (Hydra simulation) against SENTINEL-LINUX01. Rules `100200` (Level 5) and `100201` (Level 10, six failures in 60 s from one source IP) were exercised, and manual investigation confirmed zero successful logins.
- Triage used a Python CLI. Containment was documented as a source-scoped manual procedure referencing NIST SP 800-61r2, with verification checks. No automated containment or persistent IP block is claimed.
- One controlled source only; not tested against legitimate authentication activity. See [CASE-003](investigations/CASE-003.md) and [evidence](evidence/v0.5/readme.md).

## v0.4 — Windows Sysmon Replay Detection (CASE-002)

- Replayed Windows Sysmon `.evtx` captures (Event IDs 1, 3, 10, 11) through SENTINEL-LINUX01 using `python-evtx` NDJSON conversion and Wazuh logcollector ingestion.
- Ruleset [`sentinel_sysmon_replay_rules.xml`](detections/sentinel_sysmon_replay_rules.xml): seven selected replay detections fired (Rules `100110`, `100111`, `100112`, `100120`, `100130`, `100131`, `100140`). These are seven selected detections on replayed samples, not seven confirmed attacks.
- Three benign `services.exe` → `svchost.exe` process-creation events matched the general Level 0 Event ID 1 structural rule (`100101`) and generated no alerts. No dedicated service-process rule is involved.
- Raw alerts: [`evidence/sysmon-replay/sysmon_alerts_raw.json`](evidence/sysmon-replay/sysmon_alerts_raw.json), SHA-256 `b53473fd6340ec17365fec9cbbc1403e445523322c4c84ae28e40882995d7a59`. Write-up: [CASE-002](investigations/CASE-002.md).
- **Limits:** validates parser, decoder and rule logic against replayed logs only. Sysmon is not running on a live Windows endpoint, and the kernel driver is not exercised.

---

## v0.3 — SOC Investigation (CASE-001)

**Status: complete. CASE-001 was closed on 18 November 2026 for its reviewed scope.** Closure does not mean all detection engineering is complete. Post-closeout engineering, validation, noise-tuning and historical evidence-recovery work remains open and is not a prerequisite for closure. Scope, findings, limitations, disposition and follow-up are in [`investigations/CASE-001.md`](investigations/CASE-001.md); detailed FIM findings are in [`docs/05-detection-engineering.md`](docs/05-detection-engineering.md).

**What was done**
- Investigated a controlled FIM modification test on SENTINEL-LINUX01 and reviewed related home-directory events (desktop configuration, application state, cache). Process attribution for those events was not established.
- Recorded the 16, 26 and 31 October evidence sets and the 2 November lifecycle session, committed the endpoint and manager Syscheck configuration screenshots (E14, E15), and ran a read-only on-disk check of Rule `100002` on 3 November.
- **18 November closeout:** verified the endpoint's real-time `/home` Syscheck configuration; standardized the three custom FIM rules to the anchored `^/home/` prefix and added MITRE ATT&CK tags (`100003` T1105, `100002` T1565.001, `100004` T1070.004) that describe each rule's detection purpose and are not evidence that a technique occurred; recorded a separate controlled lifecycle session with raw alert JSON; and observed benign GNOME Tracker3 cache activity triggering Rule `100002` at Level 8.

### Detection findings

Seven distinct evidence sets across six dates. The two 31 October sets are separate, and their relationship is not established. These are distinct observations or controlled tests, not one lifecycle test.

| Date (2026) | Scenario | Result | Status |
|---|---|---|---|
| 11 Oct | Controlled modification of `sentinel-fim-validation.txt` | Rule `100002` Level 8 (built-in Rule `550` also observed) | Modification only. Screenshot-supported; original source alert log not recovered |
| 16 Oct | Creation and deletion of `sentinel-audit-test.txt` | Built-in Rules `554` (creation) and `553` (deletion); custom `100003`/`100004` not present in the reviewed records | Reviewed source records. Not a custom-rule validation; historical loaded configuration unknown |
| 26 Oct | Two consecutive modifications of `sentinel-v02-mod-test.txt` | Two Rule `100002` Level 8 alerts | Modification only. Not independent test cases or a regression suite |
| 31 Oct (screenshot) | Rules `100003`/`100004` seen under an application configuration path | One terminal screenshot | **Observed, not validated.** Not a controlled test; trigger not established |
| 31 Oct (raw JSON) | Creation and deletion records for `sentinel-v03-controlled-test.txt` | Rule `100003` (creation) and `100004` (deletion), Level 8, in two committed alert records | Creation and deletion only; not a lifecycle test. Relationship to the screenshot set not established |
| 2 Nov | One controlled lifecycle on `sentinel-v03-final-test.txt` | `100003`, `100002`, `100004`, each Level 8 | **Controlled lifecycle session.** Terminal screenshot; raw JSON not committed |
| 18 Nov | One controlled lifecycle on `fim-sprint-test.txt` | `100003`, `100002`, `100004`, each Level 8 | **Separate controlled lifecycle session**, raw alert JSON committed. Not merged with 2 Nov |

**How to read these results**
- Rule `100002` is the **modification** rule (parent `550`). It is validated for the controlled modification scenarios only and is not expected to fire on creation or deletion.
- Rules `100003` (creation, parent `554`) and `100004` (deletion, parent `553`) matched in the 2 and 18 November sessions. Each is a single session on one dedicated file. This does not validate the 31 October observations, does not explain the 16 October records, and does not establish repeatability or comprehensive coverage.
- **16 October question (unresolved):** the reviewed records show built-in Rules `554` and `553` but not custom `100003`/`100004`. Whether those custom rules were deployed and loaded then is unknown. Later sessions do not answer it, and it is not a confirmed detection miss.
- **3 November check (read-only):** Rule `100002` was present on disk with Level 8, parent `<if_sid>550</if_sid>` and an `^/home/` file condition, and `wazuh-analysisd` was running. This does not establish the in-memory rule version, or the configuration loaded during the 16 October tests. No rules were changed and no restart was performed.
- **Superseded wording:** earlier revisions said Rules `554` and `100002` fired together on creation. The source-record review does not support that.

### Post-closeout FIM sessions (not CASE-001 evidence)

The 20 November v0.6 measurement and the 21 November v0.8 probe (described above) complete the four documented controlled lifecycle sessions. They are separate from the CASE-001 sessions and from each other, and the four are not combined into one test.

### Operational incident (reported; root cause unconfirmed)

A Wazuh Manager startup reportedly timed out at about 45 seconds. A lock directory was removed after a check found no active Manager processes, and the Manager then started. The lock is not claimed to be the cause. One graceful VM restart cycle was reported successful with Agent `002` reconnecting; this is a single observation, not proof of resilience.

### Lessons learned

- A controlled test confirms only the behavior it exercised; a lifecycle session confirms that session on one file.
- A FIM alert shows a monitored file changed. It does not establish malicious intent or the responsible process.
- A built-in rule alert is not a custom rule alert and does not show that a custom rule was loaded.
- Screenshots and source records are different levels of evidence, and an on-disk rule file does not by itself prove which version is loaded in memory.
- Broad path matching can capture routine desktop activity; tuning must be followed by testing.

### Post-closeout follow-up (not prerequisites for CASE-001 closure)

- Determine whether custom Rules `100003`/`100004` were deployed and loaded on 16 October, and verify the in-memory rule version, where available evidence permits.
- Establish process attribution and trigger for the 31 October events and the relationship between the two sets.
- Broader creation/deletion coverage and a repeatable regression suite; systematic false-positive/false-negative testing.
- Committed raw alert records for the 31 October screenshot observation and the 2 November session.
- The broader noise-suppression retest, including residual `dconf` noise.

---

## v0.2 — Detection Engineering

- Configured Wazuh Syscheck (FIM) on SENTINEL-LINUX01, scoped to `/home`, and authored custom Rule `100002`. Flow: Wazuh Agent → Syscheck → telemetry event → Rule `100002` → Level 8 alert.
- A controlled modification test produced a `syscheck_integrity_changed` event and a Level 8 alert. This validates the modification path for that scenario only, not creation, deletion, other paths or other scenarios. Evidence is under [`evidence/v0.2/`](evidence/v0.2/).
- Lessons: a modification alert is not automatically malicious; Rule `550` and custom Rule `100002` are distinct detections; broad path matching can add noise.
- Not included: other detection scenarios, expanded telemetry, systematic false-positive analysis, coverage metrics. Some were addressed in later milestones.

## v0.1 — Foundation

- **Architecture decision:** replaced the original Windows-first plan with a Linux-first endpoint. The Windows VM (SENTINEL-WIN01) hit repeated deployment and boot issues that made it unsuitable as a dependency. This is recorded as an infrastructure issue, not an attributed technical root cause. Windows and Active Directory are deferred.
- Deployed `SENTINEL-WAZUH` (Ubuntu 24.04, Wazuh 4.14.8 all-in-one), `SENTINEL-KALI` (controlled adversary emulation) and `SENTINEL-LINUX01` (Ubuntu 24.04, monitored endpoint, agent enrolled and active) on the isolated `SENTINEL-LAB` network (`10.10.10.0/24`). Connectivity was verified.
- Disabled the Wazuh package repository after installation to avoid accidental upgrades; upgraded VirtualBox from 7.2.8 to 7.2.20 during troubleshooting.
- Established the documentation, evidence and failure-tracking structure (`detections/`, `investigations/`, `metrics/`, `scenarios/`, `evidence/`, `failure-log/`).

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

---

## Evidence index

Detailed indexes: [`evidence/v0.3/readme.md`](evidence/v0.3/readme.md), [`evidence/v0.5/readme.md`](evidence/v0.5/readme.md), [`evidence/v0.9/readme.md`](evidence/v0.9/readme.md). Key items and their limits:

- **16 October:** screenshots referenced from `evidence/v0.3/readme.md`. The source records were reviewed from `/var/ossec/logs/alerts/2026/Oct/ossec-alerts-16.json`; that runtime log is not claimed to be committed.
- **26 October:** [`evidence/v0.2/screenschots/v0.2-oct26-controlled-modification-source-alerts-new.png`](evidence/v0.2/screenschots/v0.2-oct26-controlled-modification-source-alerts-new.png).
- **31 October screenshot:** [`evidence/v0.3/screenshots/v0.3-fim-lifecycle-custom-detections.png`](evidence/v0.3/screenshots/v0.3-fim-lifecycle-custom-detections.png). Screenshot only; no raw alert records for this set.
- **31 October raw JSON (separate set):** [`evidence/v0.3/raw-alerts/sentinel-v03-creation-alert.json`](evidence/v0.3/raw-alerts/sentinel-v03-creation-alert.json) and [`evidence/v0.3/raw-alerts/sentinel-v03-deletion-alert.json`](evidence/v0.3/raw-alerts/sentinel-v03-deletion-alert.json). Wazuh alert records, not original Syscheck input logs.
- **18 November lifecycle:** [`evidence/v0.3/raw-alerts/fim-lifecycle-evidence.json`](evidence/v0.3/raw-alerts/fim-lifecycle-evidence.json) (three alert records). The [`SHA256SUMS`](evidence/v0.3/raw-alerts/SHA256SUMS) manifest in the same directory covers the three raw JSON files; checksums were not independently recomputed for this documentation.
- **E14 / E15 (Syscheck configuration screenshots):** [`evidence/v0.3/screenshots/v0.3-e14-endpoint-syscheck-configuration.png`](evidence/v0.3/screenshots/v0.3-e14-endpoint-syscheck-configuration.png) (endpoint: `/home` real-time, startup scan, 43,200-second frequency) and [`evidence/v0.3/screenshots/v0.3-e15-manager-syscheck-configuration.png`](evidence/v0.3/screenshots/v0.3-e15-manager-syscheck-configuration.png) (manager-side only; not evidence of endpoint `/home` monitoring). Neither establishes the configuration loaded on 16 October.
- **E16 (2 November lifecycle):** [`evidence/v0.3/screenshots/v0.3-fim-full-lifecycle-custom-rules.png`](evidence/v0.3/screenshots/v0.3-fim-full-lifecycle-custom-rules.png). Terminal screenshot, not a raw alert record.
- **v0.11 (milestone status pending reconciliation):** [`evidence/v0.11/v011_fim_alerts.json`](evidence/v0.11/v011_fim_alerts.json), [`evidence/v0.11/triage_report.md`](evidence/v0.11/triage_report.md) and [`evidence/v0.11/regression_summary.json`](evidence/v0.11/regression_summary.json). Committed repository artifacts; see the v0.11 evidence-status note in the version history above for what they do and do not establish.
- Not committed or not recovered: the 11 October original source alert log, the 3 November verification capture, raw alert JSON for the 2 November session and the 31 October screenshot observation, and operational artifacts from the Manager startup observation.

---

## Engineering principles

- **BUILD → UNDERSTAND → TEST → BREAK → FIX → MEASURE → DOCUMENT → EXPLAIN.** A control is not successful because it exists; detections must be tested, evidenced, measured, improved and retested.
- **STOP → CAPTURE → DOCUMENT → CONTINUE.** Failures and architecture changes are recorded, not hidden. An unreliable optional component should not block progress.
- Configuration syntax validation, telemetry observation, custom-rule validation and broader coverage are distinct claims and are documented separately.

## Future work (not implemented)

- Windows and Active Directory endpoints (deferred), and live Sysmon telemetry from a Windows endpoint.
- The broader post-v0.8 noise-suppression retest and repeatable FIM regression tests.
- Broader telemetry sources, larger repeatable purple-team measurement, and project-level MITRE ATT&CK mapping.
- A custom SENTINEL console on top of Wazuh (incident visualization, detection timelines, metrics, case reporting).
- Automated containment and response are not implemented; any future automation would require human approval.
