# SENTINEL Detection Library

Custom Wazuh detections built and tested in the SENTINEL lab, a Linux-first environment on an isolated VirtualBox network. There is no live Windows endpoint and no Active Directory; Windows Sysmon events are replayed telemetry.

Detections are designed to be observable (grounded in real telemetry), testable (checked against a controlled scenario) and explainable (an analyst can say why one fired). A rule that exists is not a rule that works. Each detection below is labeled with its actual validation status, scoped to the scenarios that were tested. Methodology is in [`../docs/05-detection-engineering.md`](../docs/05-detection-engineering.md) and metrics in [`../docs/07-testing-and-metrics.md`](../docs/07-testing-and-metrics.md); this README is the index between them.

**CASE-001 boundary.** [CASE-001](../investigations/CASE-001.md) was closed on 18 November 2026 for its reviewed scope. Subsequent milestones and follow-up work, including v0.6, v0.7, v0.8, v0.9, v0.9.1, v0.10 and v0.11, are separate post-closeout developments and are not CASE-001 evidence. Closing the case does not mean detection engineering is complete.

---

## 1. Detection Inventory

| Family | Rules | Data source | Validation status and key evidence |
|---|---|---|---|
| **Linux FIM** ([`local_rules.xml`](local_rules.xml)) | `100002` modification (parent `550`), `100003` creation (parent `554`), `100004` deletion (parent `553`); all Level 8 | Wazuh Syscheck, real-time, `/home` scope on `SENTINEL-LINUX01` (Agent `002`) | Implemented. Four documented controlled single-file lifecycle sessions (2 Nov and 18 Nov in CASE-001; 20 Nov v0.6 and 21 Nov v0.8, post-closeout). Not a regression suite. v0.8 tuning implemented and probe-verified; broader noise retest pending |
| **SSH authentication** ([`sentinel_ssh_bruteforce_rules.xml`](sentinel_ssh_bruteforce_rules.xml)) | `100200` failure (Level 5); `100201` escalation (Level 10) after six matching failures in 60 s from the same source IP | `sshd` logs on `SENTINEL-LINUX01`, collected by Agent `002` | Implemented. [CASE-003](../investigations/CASE-003.md) (21 failed attempts), v0.6 C1/C2 measurement, v0.8 `wazuh-logtest` threshold check. One controlled source |
| **Windows Sysmon** ([`sentinel_sysmon_replay_rules.xml`](sentinel_sysmon_replay_rules.xml)) | `100100`–`100104` base structural (Level 0); `100110`, `100111`, `100112`, `100120`, `100130`, `100131`, `100140` behavioral (Levels 8–14) | Replayed Sysmon EVTX (v0.4) and JSON (v0.9) telemetry | Implemented. Selected detections fired on replay samples (v0.6: 7/7). v0.9 JSON replay alerted for `100110`, `100130`, `100140` only. Not a live endpoint |

---

## 2. Key Validation Highlights

### FIM

Four separate controlled single-file lifecycle sessions are recorded. Each is its own session on its own scope of testing; they are not combined into one test, are not a regression suite, and validate only those scenarios. The 2 and 18 November sessions belong to CASE-001. The 20 and 21 November sessions are post-closeout developments.

| Date | Context | Result |
|---|---|---|
| 2 Nov 2026 | CASE-001 | `100003`, `100002`, `100004` each matched at Level 8. Terminal screenshot evidence; raw JSON not committed |
| 18 Nov 2026 | CASE-001 closeout | Same three rules matched at Level 8. Raw alert JSON: [`fim-lifecycle-evidence.json`](../evidence/v0.3/raw-alerts/fim-lifecycle-evidence.json) |
| 20 Nov 2026 | Post-closeout, v0.6 measurement | 3/3 selected lifecycle events detected; 0/3 alerts for `/tmp` negative-control operations (outside the monitored scope). See the [v0.6 report](../metrics/v0.6-purple-team-measurement.md) |
| 21 Nov 2026 | Post-closeout, v0.8 live probe, Agent `002` | Creation, modification and deletion each matched the corresponding custom rule at Level 8, carrying `sentinel_fim` without `sshd`; hidden dot-directory monitoring still active |
| 22 Nov 2026 | v0.11 evidence; milestone status pending reconciliation | Committed v0.11 alert records ([`v011_fim_alerts.json`](../evidence/v0.11/v011_fim_alerts.json), 10 records, all from Agent `002` / `sentinel-linux01`) contain three Level 8 custom-rule events (creation `100003`, modification `100002` and deletion `100004`) for `/home/sentinel-admin/v011_fim_probe.txt`. The remaining seven records concern desktop/configuration paths. In the associated [triage report](../evidence/v0.11/triage_report.md), the process, target-process and event-time enrichment fields are `None`. The milestone is pending reconciliation; these records are not counted among the four previously documented controlled lifecycle sessions |

- **Modification rule:** `100002` was also confirmed in two earlier controlled modification tests (11 and 26 October). The 11 October result is screenshot-supported only; its original source alert record was not recovered.
- **v0.8 tuning (implemented, probe-verified):** FIM rules moved into a dedicated `sentinel_fim` group, separated from the `sshd` grouping they previously inherited; anchored `^/home/` matching retained; hidden dot-directory monitoring preserved. The current on-disk [`local_rules.xml`](local_rules.xml) also configures selected exclusions for Tracker3 cache paths, Nautilus tags database files, dconf user database files, Tiling Assistant temporary/session files, and GNOME Shell temporary/application-state files. These describe the configuration, not validation: not every exclusion has been independently validated.
- **Still open:** residual desktop noise under `/home/sentinel-admin/.config/dconf/user` still triggers `100002`. The noise problem is not resolved, the broader noise-suppression retest is pending, and the exclusions have not been validated by dedicated tests.
- **31 October observations (not lifecycle sessions):** `100003` and `100004` were seen firing under an application config path (screenshot only, trigger unestablished). CASE-001 also records a separate set of two raw alert records for a different file (one creation, one deletion). The relationship between the two sets is not established. Neither is a controlled lifecycle session, neither is counted as validation, and neither explains the 16 October question.
- **16 October question (unresolved):** the reviewed records of a controlled create/delete show built-in Rule `554` (Level 5) for creation and built-in Rule `553` (Level 7) for deletion. Custom `100003` and `100004` are not present in those records. Whether the custom rules were deployed and loaded then is unknown, and [CASE-001](../investigations/CASE-001.md) leaves the historical loaded configuration unresolved. This is not a confirmed detection failure. `100002` is the modification rule (parent `550`), so its absence from creation and deletion records is consistent with its design. Later sessions in which `100003` and `100004` matched do not answer the question.

### SSH

- CASE-003 documented 21 failed attempts from `SENTINEL-KALI`, baseline `100200` alerts, `100201` escalation, and manual confirmation of zero successful logins.
- v0.6: C1 produced four `100200` alerts and no `100201`; C2 produced eight `100200` alerts and two `100201`. The first C2 escalation fired early because four C1 failures were still inside the 60-second sliding window.
- v0.8: a stateful `wazuh-logtest` session confirmed that six failures in 60 s trigger `100201`.

### Sysmon (replay)

- Rule `100101` is the general Level 0 structural rule for Sysmon Event ID 1 (process creation). It has no dedicated `services.exe` → `svchost.exe` condition. In v0.6, the three benign `services.exe` → `svchost.exe` events matched this base rule and generated no alerts (0/3), while 7/7 selected behavioral detections fired.
- v0.9 JSON replay (manager-side logcollector) produced alerts for `100110`, `100130` and `100140`. This does not mean every Sysmon rule was independently validated.
- **Gaps:** two EID 7 ImageLoad events remained uncovered, and a v0.7 command-line mutation ([CASE-004](../investigations/CASE-004.md)) bypassed keyword-based Rule `100112` and fell to a Level 0 base rule.
- A rule firing on replayed telemetry shows the logic matched that sample, not that an attack occurred. ATT&CK mappings in the rule files are candidate triage hypotheses.

### Python-assisted triage

[`python-soc-automation`](https://github.com/andyydz/python-soc-automation) is a separate companion project that parses Wazuh alert JSON and provides severity-based triage (v0.9 used `--triage --min-level 8`). It is not native Wazuh functionality, does not perform containment, eradication or recovery, and is not a production SOAR platform. Its tests validate the Python tool, not SENTINEL's Wazuh detection rules.

**Measurement caveat:** v0.6 results are small controlled samples, not statistically meaningful detection or false-positive rates. Endpoint and manager clocks were skewed, so negative raw cross-VM timing deltas are clock artefacts, not negative detection latency.

---

## 3. Detection Engineering Lifecycle

Define → Implement → Test (controlled scenario) → Validate → Tune → Retest

Validation is always scoped to the scenario tested, and a rule change resets a detection's status until it is retested. Status labels, used consistently with [`../docs/05-detection-engineering.md`](../docs/05-detection-engineering.md):

| Label | Meaning |
|---|---|
| Configured | The rule or setting exists in the configuration. Nothing is implied about behavior |
| Implemented | Built and operating in the lab and has produced alerts. Does not mean behaviorally validated |
| Observed | Alert or behavior seen, but not as a controlled, explained test; trigger not established. Fired in that instance only |
| Validated | Fired in a controlled scenario with a known trigger; scoped to that scenario only |
| Tuned | Configuration changed to address noise or gaps; not the same as noise resolved |
| Pending retest | Tuning exists; the broader retest has not been completed |

Evidence is never edited retroactively; a changed result is recorded as a new test.

---

## 4. Known Limitations

- **Coverage:** no comprehensive `/home` coverage is claimed. Four lifecycle sessions on single files are useful evidence but are not an automated regression suite, broad coverage, or a statistical repeatability test.
- **Rates:** no statistically meaningful detection, false-positive or false-negative rates exist. The `/tmp` negative control is not comprehensive false-positive testing.
- **FIM configuration:** the current on-disk rules are not evidence of what the manager had loaded during earlier tests. Matching of `^/home/` against other outside-scope paths and case, and the configured exclusions (Tracker3, Nautilus, dconf, Tiling Assistant and GNOME Shell), have not been systematically or independently tested.
- **FIM noise:** residual desktop noise remains; broader retest pending.
- **Historical evidence:** the 16 October loaded-configuration question and the 31 October trigger origin remain unresolved. Post-closeout recovery work does not reopen CASE-001.
- **Sysmon:** replay only; keyword-based rules can be bypassed by mutation (`100112`).
- **SSH:** one controlled source; not tested against legitimate authentication activity.
- **Built-in rules:** Wazuh rules such as `550`, `553` and `554` are not counted as SENTINEL detections; a built-in alert does not show a custom rule was loaded.
- **Alerts:** an alert shows an event matched rule logic. It is not proof of malicious activity.
