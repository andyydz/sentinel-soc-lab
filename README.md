# SENTINEL — Evidence-Driven SOC Detection and Investigation Lab

> Does your detection still work when the attacker changes tactics?

SENTINEL is a personal SOC engineering lab built with Wazuh 4.14.8, VirtualBox, Linux, Kali Linux and Python. I use it to write custom detections, investigate the alerts they produce, analyse replayed Windows Sysmon telemetry, and test whether detections behave as intended.

```
SIMULATE → DETECT → INVESTIGATE → RESPOND → MEASURE → IMPROVE → RETEST
```

A detection is not "done" because a rule exists; it is done once it has been tested and the result recorded. Simulation, detection, investigation and measurement are evidenced for selected controlled cases. Response is documented and planned, but a fully evidenced containment, eradication and recovery exercise has not been carried out.

**This is a Linux-first learning and engineering lab, not a production SOC.** Windows telemetry comes from pre-recorded Sysmon `.evtx` captures that are replayed; there is no live Windows endpoint and no Active Directory.

---

## Start here

| What | Where |
|---|---|
| Windows Sysmon replay investigation (7 selected replay detections, 3 benign events suppressed) | [CASE-002](investigations/CASE-002.md) |
| SSH brute-force investigation and response planning | [CASE-003](investigations/CASE-003.md) |
| FIM investigation, with an unresolved question documented openly | [Rule 100002 investigation](investigations/fim-rule-100002-investigation.md) |
| Detection rules and validation status | [Detections guide](detections/readme.md) |
| Controlled measurement results and caveats | [v0.6 purple-team measurement](metrics/v0.6-purple-team-measurement.md) |
| Where the evidence lives | [Evidence guide](evidence/readme.md) |

---

## What this demonstrates

- Building a Wazuh manager, dashboard and Linux agent in an isolated lab network.
- Writing custom Wazuh rules (FIM, SSH authentication, Sysmon replay) and working with rule parent/child chaining.
- Investigating alerts and recording what is and is not established, including questions left open rather than explained away.
- Converting and ingesting Windows Sysmon telemetry with a Python script and a dedicated ruleset.
- Running small controlled tests, recording results, and stating their limits.
- Keeping evidence traceable: screenshots, raw alert records, SHA-256 checksums where committed, and notes on what is *not* committed.

---

## Lab and architecture

| Host | Role |
|---|---|
| SENTINEL-WAZUH (`10.10.10.10`) | Ubuntu 24.04, Wazuh 4.14.8 manager and dashboard; NAT for outbound access |
| SENTINEL-KALI (`10.10.10.20`) | Kali Linux 2026.2, controlled adversary-emulation VM (simulated SSH failures, [CASE-003](investigations/CASE-003.md)) |
| SENTINEL-LINUX01 (`10.10.10.40`, Agent `002`) | Ubuntu 24.04.5 LTS, Wazuh Agent 4.14.8; real-time FIM on `/home`; also the replay endpoint for Sysmon telemetry ([CASE-002](investigations/CASE-002.md)) |

The lab uses an isolated VirtualBox network (`10.10.10.0/24`). `10.10.10.30` is unused: it was allocated to an earlier Windows endpoint that was dropped after repeated deployment failures. A live Windows/Sysmon/AD endpoint is future work.

**Tooling:** VirtualBox, Wazuh (custom rules, FIM, SCA in observation-only mode), Python ([`scripts/evtx_to_wazuh.py`](scripts/evtx_to_wazuh.py)), Git/GitHub, and written investigation reports.

---

## Detections

| Family | Rules | Data source | Validation status |
|---|---|---|---|
| **File Integrity Monitoring** ([rules](detections/local_rules.xml)) | `100002` modification (parent `550`), `100003` creation (parent `554`), `100004` deletion (parent `553`); Level 8 | Wazuh Syscheck on `/home`, SENTINEL-LINUX01 | Three separate controlled lifecycle sessions; v0.8 tuning probe-verified; broader noise retest pending |
| **SSH authentication** ([rules](detections/sentinel_ssh_bruteforce_rules.xml)) | `100200` failure (Level 5); `100201` escalation (Level 10) after six matching failures within 60 s from the same source IP | `sshd` logs, Agent `002` | CASE-003, v0.6 measurement, v0.8 `wazuh-logtest` check; one controlled source |
| **Sysmon replay** ([rules](detections/sentinel_sysmon_replay_rules.xml)) | Base `100100`–`100104`; behavioral `100110`, `100111`, `100112`, `100120`, `100130`, `100131`, `100140` | Replayed `.evtx` (v0.4) and JSON (v0.9) telemetry | Selected detections fired on replay samples; not a live endpoint |

More detail: [Detections guide](detections/readme.md) · [Detection engineering](docs/05-detection-engineering.md).

**Reading alerts:** a rule firing means detection logic matched observed telemetry. It is not a confirmed finding. A file change does not show tampering, `lsass.exe` access does not show credential dumping, and a PowerShell network connection does not show a file transfer. ATT&CK references describe detection intent or observed indicators only; project-level mapping is future work.

---

## What has been tested

| Area | Result | Scope |
|---|---|---|
| **FIM** | Three separate controlled single-file lifecycle sessions (2 Nov, 20 Nov v0.6, 21 Nov v0.8 probe): Rules `100003`, `100002`, `100004` each matched at Level 8. v0.6: 3/3 selected lifecycle events detected; 0/3 alerts for `/tmp` negative controls | Specific files and sessions only; not a regression suite |
| **FIM tuning (v0.8)** | `sentinel_fim` group isolation (no longer inherits `sshd`), anchored `^/home/` matching kept, selected Tracker3/Nautilus noise excluded, hidden-directory monitoring preserved; live Agent `002` probe confirmed all three rules | Residual desktop noise remains (`.config/dconf/user`); broader retest pending |
| **Sysmon replay** | v0.6: 7/7 selected detections fired; 3 benign `services.exe → svchost.exe` events suppressed by Level 0 Rule `100101`. v0.9 JSON replay alerted for `100110`, `100130`, `100140` | Replay only; two EID 7 ImageLoad events uncovered; a v0.7 command-line mutation bypassed keyword-based Rule `100112` |
| **SSH** | [CASE-003](investigations/CASE-003.md): 21 failed attempts, zero successful logins. v0.6: C1 four `100200`/no `100201`; C2 eight `100200`/two `100201` (first C2 escalation early because four C1 failures carried over in the 60 s window). v0.8: stateful `wazuh-logtest` confirmed the six-in-60 s threshold | One controlled source; not tested against legitimate logins |

**These are small controlled samples,** not detection or false-positive rates and not proof of complete coverage. v0.6 results are a pre-tuning baseline. Endpoint and manager clocks were skewed, so negative raw timing deltas are clock artefacts, not detection latency. Methodology: [Testing and metrics](docs/07-testing-and-metrics.md).

**Open FIM findings**
- **31 Oct:** Rules `100003` and `100004` were observed firing under an application config path (one screenshot, trigger unestablished). This was not a controlled test and is not counted as validation.
- **16 Oct:** reviewed records of a controlled create/delete show built-in Rules `554` and `553`, not custom `100003`/`100004`. Whether the custom rules were loaded then is unresolved; the historical loaded configuration is unknown ([CASE-001](investigations/CASE-001.md)).

---

## Investigation and response approach

Each case file separates what was observed from what is established. Response is kept at three distinct levels: a *documented procedure* ([Incident response](docs/06-incident-response.md)), a *manually investigated alert* ([CASE-003](investigations/CASE-003.md)), and an *action executed and supported by evidence*. Only the first two exist; there is no automated containment, eradication or recovery.

## Python companion project

[`scripts/evtx_to_wazuh.py`](scripts/evtx_to_wazuh.py) converts Sysmon `.evtx` captures to NDJSON for Wazuh ingestion. The separate [Python SOC Automation Engine](https://github.com/andyydz/python-soc-automation) parses Wazuh alert JSON and provides severity-based triage; v0.9 connects replay alerts to it (see the [v0.9 index](evidence/v0.9/readme.md)). It is not native Wazuh functionality, a SOAR platform or automated response.

---

## Milestones

| Version | Focus | Status |
|---|---|---|
| v0.1 | Infrastructure, network, Wazuh deployment | Complete |
| v0.2 | FIM Rules `100002`–`100004` | Complete (18 Nov 2026); documentation reconciled retroactively |
| v0.3 | CASE-001 and FIM lifecycle validation | Complete; evidence reconciliation closed, investigation remains open |
| v0.4 | Sysmon `.evtx` replay, CASE-002 | Complete (19 Nov 2026) |
| v0.5 | SSH brute-force detection and triage, CASE-003 | Complete |
| v0.6 | Controlled purple-team measurement | Complete |
| v0.7 | Mutation testing, logtest validation, CASE-004 | Complete |
| v0.8 | FIM group isolation, noise tuning, Agent `002` probe | Implemented on `main`; noise retest pending |
| v0.9 | Sysmon JSON replay and Python-assisted triage | Implemented on `main`; replay-based |
| v0.9.1 | Documentation and status alignment | Documentation only |
| Future | Live Windows/AD endpoint; custom console over Wazuh | Planned |

Dates and per-milestone detail: [Changelog](CHANGELOG.md) and each evidence index.

---

## Scope and limitations

- **No live Windows endpoint or Active Directory;** Sysmon telemetry is replayed, and the Sysmon driver is not exercised.
- **No production claims.** Results are small controlled samples; no detection, false-positive or false-negative rates, and no comprehensive FIM, SSH or Sysmon coverage are established.
- **No regression suite.** v0.8 tuning is implemented and probe-verified, but the broader noise-suppression retest is pending.
- **Open FIM questions** (above): the 16 Oct loaded-configuration question and the unexplained differences between the 16 and 31 Oct observations.
- **Not every record is committed.** The 16 Oct alert records came from the Wazuh runtime log; raw records for 31 Oct and 2 Nov are not committed (those results rest on screenshots); the original `.evtx` captures are not committed. The v0.4 raw alerts are committed with a SHA-256.
- **Future work:** live Windows telemetry, broader authentication telemetry, threat hunting, additional cases, ATT&CK mapping, and a custom console over Wazuh.

---

## Documentation and evidence

| Area | Links |
|---|---|
| Methodology | [Detection engineering](docs/05-detection-engineering.md) · [Incident response](docs/06-incident-response.md) · [Testing and metrics](docs/07-testing-and-metrics.md) · [`docs/`](docs/) |
| Investigations | [CASE-001](investigations/CASE-001.md) · [CASE-002](investigations/CASE-002.md) · [CASE-003](investigations/CASE-003.md) · [CASE-004](investigations/CASE-004.md) · [Rule 100002 investigation](investigations/fim-rule-100002-investigation.md) · [Guide](investigations/readme.md) |
| Detections | [Guide](detections/readme.md) · [FIM](detections/local_rules.xml) · [SSH](detections/sentinel_ssh_bruteforce_rules.xml) · [Sysmon replay](detections/sentinel_sysmon_replay_rules.xml) |
| Evidence | [Guide](evidence/readme.md) · [v0.1](evidence/v0.1/) · [v0.2](evidence/v0.2/readme.md) · [v0.3](evidence/v0.3/readme.md) · [Sysmon replay](evidence/sysmon-replay/) · [v0.5](evidence/v0.5/readme.md) · [v0.6](evidence/v0.6/readme.md) · [v0.7](evidence/v0.7/) · [v0.9](evidence/v0.9/readme.md) |
| Metrics and project | [v0.6 measurement](metrics/v0.6-purple-team-measurement.md) · [Security policy](SECURITY.md) · [Changelog](CHANGELOG.md) |

---

## Security and safety

SENTINEL is an authorized, isolated lab: no real credentials, production targets or external attacks, and no VM disks or secrets committed. See [`SECURITY.md`](SECURITY.md).
