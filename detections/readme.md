# SENTINEL Detection Library

Custom Wazuh detections built and tested in the SENTINEL lab, a Linux-first environment on an isolated VirtualBox network. There is no live Windows endpoint and no Active Directory; Windows Sysmon events are replayed telemetry.

Detections are designed to be observable (grounded in real telemetry), testable (checked against a controlled scenario) and explainable (an analyst can say why one fired). A rule that exists is not a rule that works. Each detection below is labeled with its actual validation status, scoped to the scenarios that were tested. Methodology is in [`../docs/05-detection-engineering.md`](../docs/05-detection-engineering.md) and metrics in [`../docs/07-testing-and-metrics.md`](../docs/07-testing-and-metrics.md); this README is the index between them.

---

## 1. Detection Inventory

| Family | Rules | Data source | Validation status and key evidence |
|---|---|---|---|
| **Linux FIM** ([`local_rules.xml`](local_rules.xml)) | `100002` modification (parent `550`), `100003` creation (parent `554`), `100004` deletion (parent `553`); all Level 8 | Wazuh Syscheck, real-time, `/home` scope on `SENTINEL-LINUX01` (Agent `002`) | Three separate controlled single-file lifecycle sessions (2 Nov, 20 Nov v0.6, 21 Nov v0.8). v0.8 tuning implemented and probe-verified; broader noise retest pending |
| **SSH authentication** ([`sentinel_ssh_bruteforce_rules.xml`](sentinel_ssh_bruteforce_rules.xml)) | `100200` failure (Level 5); `100201` escalation (Level 10) after six matching failures in 60 s from the same source IP | `sshd` logs on `SENTINEL-LINUX01`, collected by Agent `002` | CASE-003 (21 failed attempts), v0.6 C1/C2 measurement, v0.8 `wazuh-logtest` threshold check. One controlled source |
| **Windows Sysmon** ([`sentinel_sysmon_replay_rules.xml`](sentinel_sysmon_replay_rules.xml)) | `100100`–`100104` base/suppression (Level 0); `100110`, `100111`, `100112`, `100120`, `100130`, `100131`, `100140` behavioral (Levels 8–14) | Replayed Sysmon EVTX (v0.4) and JSON (v0.9) telemetry | Selected detections fired on replay samples (v0.6: 7/7). v0.9 JSON replay alerted for `100110`, `100130`, `100140` only. Not a live endpoint |

---

## 2. Key Validation Highlights

### FIM

Three separate controlled sessions each created, modified and deleted one dedicated file. They are not a regression suite and validate those scenarios only.

| Date | Session | Result |
|---|---|---|
| 2 Nov 2026 | Single-file lifecycle | `100003`, `100002`, `100004` each matched at Level 8 (terminal screenshot evidence) |
| 20 Nov 2026 | v0.6 measurement | Same three rules matched at Level 8: 3/3 selected lifecycle events detected; 0/3 alerts for `/tmp` negative-control operations (outside the monitored scope) |
| 21 Nov 2026 | v0.8 live probe, Agent `002` | Same three rules matched at Level 8, carrying `sentinel_fim` without `sshd`; hidden dot-directory monitoring still active |

- **Modification rule:** `100002` was also confirmed in two earlier controlled modification tests (11 and 26 October).
- **v0.8 tuning (implemented, probe-verified):** FIM rules moved into a `sentinel_fim` group (no longer inheriting `sshd`); anchored `^/home/` matching retained; selected Tracker3 and Nautilus database activity excluded; hidden dot-directory monitoring preserved.
- **Still open:** residual desktop noise under `/home/sentinel-admin/.config/dconf/user` still triggers `100002`; the broader noise-suppression retest is pending, and the exclusions have not been validated by dedicated tests.
- **31 October observation:** `100003` and `100004` were seen firing under an application config path. This was a single screenshot with an unestablished trigger, not a controlled test, and it is not counted as validation.
- **16 October question (unresolved):** the reviewed records of a controlled create/delete show only built-in Rules `554` and `553`, not custom `100003`/`100004`. Whether the custom rules were deployed and loaded then is unknown; [CASE-001](../investigations/CASE-001.md) leaves the historical loaded configuration unresolved. `100002` is the modification rule and is not expected to cover those events.

### SSH

- CASE-003 documented 21 failed attempts from `SENTINEL-KALI`, baseline `100200` alerts, `100201` escalation, and manual confirmation of zero successful logins.
- v0.6: C1 produced four `100200` alerts and no `100201`; C2 produced eight `100200` alerts and two `100201`. The first C2 escalation fired early because four C1 failures were still inside the 60-second sliding window.
- v0.8: a stateful `wazuh-logtest` session confirmed that six failures in 60 s trigger `100201`.

### Sysmon (replay)

- Rule `100101` suppresses benign `services.exe` → `svchost.exe` process creation; in v0.6, 0/3 such events alerted and 7/7 selected behavioral detections fired.
- v0.9 JSON replay (manager-side logcollector) produced alerts for `100110`, `100130` and `100140`. This does not mean every Sysmon rule was independently validated.
- **Gaps:** two EID 7 ImageLoad events remained uncovered, and a v0.7 command-line mutation ([CASE-004](../investigations/CASE-004.md)) bypassed keyword-based Rule `100112` and fell to a Level 0 base rule.
- A rule firing on replayed telemetry shows the logic matched that sample, not that an attack occurred. ATT&CK mappings in the rule files are candidate triage hypotheses.

### Python-assisted triage

[`python-soc-automation`](https://github.com/andyydz/python-soc-automation) is a separate companion project that parses Wazuh alert JSON and provides severity-based triage (v0.9 used `--triage --min-level 8`). It is not native Wazuh functionality, does not perform containment, eradication or recovery, and is not a production SOAR platform. Its 169 passing pytest tests cover the Python tool, not the Wazuh detections.

**Measurement caveat:** v0.6 results are small controlled samples, not statistically meaningful detection or false-positive rates. Endpoint and manager clocks were skewed, so negative raw cross-VM timing deltas are clock artefacts, not negative detection latency.

---

## 3. Detection Engineering Lifecycle

Design → Implement → Test (controlled scenario) → Evaluate → Tune → Retest → Document

Validation is always scoped to the scenario tested, and a rule change resets a detection's status until it is retested. Status labels:

| Label | Meaning |
|---|---|
| Implemented | Configured and loading; not yet validated by a controlled test |
| Observed | Alert seen, trigger not established; fired in that instance only |
| Validated | Fired in a controlled scenario with a known trigger; scoped to that scenario |
| Tuned | Configuration changed to address noise; not the same as noise resolved |
| Pending retest | Tuning exists; the broader retest has not been completed |

Evidence is never edited retroactively; a changed result is recorded as a new test.

---

## 4. Known Limitations

- **Coverage:** no comprehensive `/home` coverage is claimed. Three lifecycle sessions on single files are not a regression suite or a repeatability test.
- **Rates:** no statistically meaningful detection, false-positive or false-negative rates exist. The `/tmp` negative control is not comprehensive false-positive testing.
- **FIM configuration:** the current on-disk rules are not evidence of what the manager had loaded during earlier tests. Matching of `^/home/` against other outside-scope paths and case, and the Tracker3/Nautilus exclusions, have not been systematically or independently tested.
- **FIM noise:** residual desktop noise remains; broader retest pending.
- **Sysmon:** replay only; keyword-based rules can be bypassed by mutation (`100112`).
- **SSH:** one controlled source; not tested against legitimate authentication activity.
- **Built-in rules:** Wazuh rules such as `550`, `553` and `554` are not counted as SENTINEL detections; a built-in alert does not show a custom rule was loaded.
- **Alerts are not proof of malice:** an alert shows an event matched rule logic and requires investigation.
- **Packaging:** XML rule definitions are committed; packaged per-detection artifacts and per-detection subdirectories are not yet established.

---

## 5. Evidence and Related Documentation

- Design and methodology: [`../docs/05-detection-engineering.md`](../docs/05-detection-engineering.md); testing and metrics: [`../docs/07-testing-and-metrics.md`](../docs/07-testing-and-metrics.md)
- v0.6 measurement: [`../metrics/v0.6-purple-team-measurement.md`](../metrics/v0.6-purple-team-measurement.md)
- Investigations: [CASE-001](../investigations/CASE-001.md) (FIM), [CASE-002](../investigations/CASE-002.md) (Sysmon EVTX replay), [CASE-003](../investigations/CASE-003.md) (SSH), [CASE-004](../investigations/CASE-004.md) (mutation testing), [`fim-rule-100002-investigation.md`](../investigations/fim-rule-100002-investigation.md)
- Evidence: [`../evidence/v0.2/`](../evidence/v0.2/), [`../evidence/v0.3/`](../evidence/v0.3/readme.md), [`../evidence/v0.5/`](../evidence/v0.5/readme.md), [`../evidence/v0.7/`](../evidence/v0.7/), [`../evidence/sysmon-replay/`](../evidence/sysmon-replay/), [`../evidence/v0.9/`](../evidence/v0.9/readme.md)

Evidence levels differ: some results rest on reviewed source alert records, others on terminal screenshots only, and raw alert records are generally not committed. Timestamps, file paths and per-session detail are in the investigation and evidence documents above. Links are as referenced in existing project documents and have not been independently verified here.
