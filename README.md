# SENTINEL — Evidence-Driven SOC Detection, Investigation and Response Lab

> Does your detection still work when the attacker changes tactics?

SENTINEL is a personal SOC engineering lab built with Wazuh, VirtualBox, Linux, Kali Linux and Python. It focuses on developing custom detections, investigating security alerts, analysing replayed Windows Sysmon telemetry and validating detection behaviour through controlled testing.

The project is organised around this evidence-driven workflow:

```
SIMULATE → DETECT → INVESTIGATE → RESPOND → MEASURE → IMPROVE → RETEST
```

Not every stage has been fully exercised. Simulation, detection, investigation and measurement are evidenced for selected, controlled cases. Response is documented and planned, but a fully evidenced containment, eradication and recovery exercise remains outstanding. The intent is that each stage is demonstrated with real evidence before it is relied on. A detection is not "done" because a rule exists. It is done once it has been tested, the result recorded, and the result holds up. See [Scope and Limitations](#scope-and-limitations).

It is a Linux-first learning and engineering environment, not a production SOC. Windows telemetry is tested through pre-recorded Sysmon `.evtx` event replay, converted and replayed through the Linux endpoint. There is currently no live Windows endpoint or Active Directory environment.

**Primary focus:** Wazuh detection engineering, SOC alert investigation, Linux security monitoring, Python-assisted triage and evidence-based testing.

---

## What makes this project different?

SENTINEL is not a replacement for Wazuh, Microsoft Sentinel or an enterprise SIEM. It uses Wazuh as its monitoring and detection platform and focuses on the engineering work around it.

The project goes beyond deploying an agent and viewing alerts:

- **Detection engineering:** custom Wazuh rules for FIM, SSH authentication and replayed Sysmon telemetry.
- **Investigation:** case-based analysis that distinguishes observed events from confirmed conclusions.
- **Telemetry engineering:** Python-assisted conversion and ingestion of Windows Sysmon event data into the Linux-based lab.
- **Testing and reliability:** controlled simulations, rule validation, noise suppression and documented limitations.
- **Evidence and measurement:** investigation reports, screenshots, raw alert records and controlled test results.

The objective is to understand how detections behave, investigate their results and identify where they need improvement, not simply to show that a SIEM is running. The emphasis is on understanding why an alert fired, validating the underlying detection logic, examining false-positive behaviour and documenting investigation conclusions—not simply collecting alerts from a monitoring platform.

---

## Contents

- [What makes this project different?](#what-makes-this-project-different)
- [Start here](#start-here)
- [Technology stack](#technology-stack)
- [What this demonstrates](#what-this-demonstrates)
- [Architecture](#architecture)
- [Detections](#detections)
- [Milestone history](#milestone-history)
- [Testing and Metrics](#testing-and-metrics)
- [Python tooling](#python-tooling)
- [Scope and Limitations](#scope-and-limitations)
- [Documentation and Evidence](#documentation-and-evidence)
- [Security & Safety](#security--safety)

---

## Start here

If you have a few minutes, these show the most:

| What | Where |
|---|---|
| Windows Sysmon replay investigation (7 selected replay detections, 3 benign events suppressed) | [CASE-002](investigations/CASE-002.md) |
| SSH brute-force investigation and response planning | [CASE-003](investigations/CASE-003.md) |
| FIM investigation with an unresolved discrepancy documented openly | [Rule 100002 investigation](investigations/fim-rule-100002-investigation.md) |
| Detection rules and how they are organised | [Detections guide](detections/readme.md) |
| Controlled measurement results and their caveats | [v0.6 purple-team measurement](metrics/v0.6-purple-team-measurement.md) |
| Where the evidence lives | [Evidence guide](evidence/readme.md) |

---

## Technology stack

| Area | Used |
|---|---|
| Virtualisation | Oracle VirtualBox (isolated lab network, NAT on the Wazuh VM) |
| Security monitoring platform | Wazuh 4.14.8 — manager, dashboard, agent, custom rules, File Integrity Monitoring and SCA (built-in, observation only) |
| Operating systems | Ubuntu 24.04 (manager), Ubuntu 24.04.5 LTS (endpoint), Kali Linux 2026.2 (adversary emulation) |
| Windows telemetry | Pre-recorded Sysmon `.evtx` captures, replayed as JSON through a Wazuh `<localfile>` |
| Scripting | Python ([`scripts/evtx_to_wazuh.py`](scripts/evtx_to_wazuh.py)) |
| Project hygiene | Git/GitHub, SHA-256 checksums on committed alert records, written investigation reports |

---

## What this demonstrates

- Deploying and connecting a Wazuh manager, dashboard and Linux agent in an isolated lab network.
- Writing and tuning custom Wazuh rules (FIM, SSH authentication, Sysmon replay) and understanding rule parent/child chaining.
- Investigating alerts and documenting what is and is not established, including an unresolved discrepancy that is left open rather than explained away.
- Ingesting and normalising Windows Sysmon telemetry through a Python converter and a dedicated ruleset.
- Running small controlled tests, recording results, and being explicit about their limits.
- Keeping evidence traceable: screenshots, raw alert records, checksums, and a note on what is *not* committed.

---

## Architecture

The lab uses an isolated VirtualBox network (`10.10.10.0/24`) for communication between the lab systems. The Wazuh VM additionally uses NAT connectivity for outbound access.

```text
                        INTERNET
                            |
                           NAT   (Wazuh VM only)
                            |
                   +----------------+
                   | SENTINEL-WAZUH |
                   |  10.10.10.10   |
                   +----------------+
                            |
                     SENTINEL-LAB
                     10.10.10.0/24
                     (isolated network)
                            |
                 +----------+----------+
                 |                     |
        +---------------+     +------------------+
        | SENTINEL-KALI |     | SENTINEL-LINUX01 |
        |  10.10.10.20  |     |  10.10.10.40     |
        +---------------+     +------------------+
```

`10.10.10.30` is not in use. It was allocated to an earlier Windows endpoint (SENTINEL-WIN01) that was dropped after repeated boot/deployment failures. No live Windows, Sysmon or Active Directory endpoint exists in the lab; that is future work.

| Host | Role |
|---|---|
| SENTINEL-WAZUH (`10.10.10.10`) | Ubuntu 24.04, Wazuh 4.14.8 — manager and dashboard. |
| SENTINEL-KALI (`10.10.10.20`) | Kali Linux 2026.2 — controlled adversary-emulation VM used for simulated SSH authentication testing ([CASE-003](investigations/CASE-003.md)). |
| SENTINEL-LINUX01 (`10.10.10.40`, Agent ID `002`) | Ubuntu 24.04.5 LTS, Wazuh Agent 4.14.8 — monitored endpoint with real-time File Integrity Monitoring (FIM) on `/home`. Also the replay endpoint for the Windows Sysmon telemetry ([CASE-002](investigations/CASE-002.md)). |

Windows detection coverage comes from replayed Sysmon `.evtx` telemetry processed on SENTINEL-LINUX01, not from a monitored Windows host.

---

## Detections

| Family | Rule IDs | Detection intent | Rule file |
|---|---|---|---|
| File Integrity Monitoring | `100002` (modification), `100003` (creation), `100004` (deletion) | Alert on file changes under `/home` (anchored regex `^/home/`). `100002` is chained to built-in parent Rule `550`. | [`detections/local_rules.xml`](detections/local_rules.xml) |
| SSH authentication | `100200` (authentication failure), `100201` (repeated-failure escalation) | Detect failed SSH logins and escalate repeated failures. | [`detections/sentinel_ssh_bruteforce_rules.xml`](detections/sentinel_ssh_bruteforce_rules.xml) |
| Sysmon replay | Base rules `100100–100104`; attack rules `100110`, `100111`, `100112`, `100120`, `100130`, `100131`, `100140` | Evaluate replayed Sysmon events: process creation, script execution, `comsvcs.dll` MiniDump-related activity, PowerShell network egress, and `lsass.exe` / `rundll32.exe` process access. Level 0 Rule `100101` suppresses benign `services.exe → svchost.exe` events. | [`detections/sentinel_sysmon_replay_rules.xml`](detections/sentinel_sysmon_replay_rules.xml) |

More detail: [Detections guide](detections/readme.md) · [Detection engineering](docs/05-detection-engineering.md).

**How to read these alerts.** A rule firing is detection intent meeting observed telemetry. It is not a confirmed finding. A file modification, creation or deletion does not by itself show tampering, payload delivery or defence evasion. A PowerShell network connection does not show a file transfer. `lsass.exe` access does not show successful credential dumping, and a dump-like file does not show a successful LSASS dump. Investigation findings are recorded separately in the case files.

**MITRE ATT&CK.** Where ATT&CK references appear in the detection documentation, they describe detection intent or observed indicators. Generic file events do not independently establish any ATT&CK technique, and no tag in this repository should be read as a confirmed attack technique. Project-level ATT&CK mapping is future work.

---

## Milestone history

Status wording used in this README:

- **Complete** — the documented scope of the milestone was finished.
- **Implemented and merged on `main`** — the work is in the main branch; additional validation or retesting may still be outstanding.

| Version | Focus | Status |
|---|---|---|
| v0.1 | Foundation — infrastructure, network, Wazuh deployment | Complete |
| v0.2 | Telemetry and detection engineering — FIM Rules `100002`–`100004` | Complete — 18 Nov 2026; documentation and evidence reconciled retroactively (see below) |
| v0.3 | SOC investigation — CASE-001 and FIM lifecycle validation | Complete (CASE-001 evidence reconciliation closed; investigation remains open) |
| v0.4 | Windows Sysmon replay and cross-platform detection — CASE-002 | Complete — 19 Nov 2026 |
| v0.5 | SSH brute-force detection and triage — CASE-003 | Complete |
| v0.6 | Controlled purple-team measurement and testing | Complete |
| v0.7 | Mutation testing, logtest validation and reliability investigation — CASE-004 | Complete |
| v0.8 | FIM group isolation, noise reduction and tuning (including an Agent 002 probe) | Implemented and merged on `main`; noise-suppression retest pending |
| v0.9 | Sysmon JSON replay ingestion and Python-assisted triage integration | Implemented and merged on `main`; replay-based, live Windows agent out of scope |
| v0.9.1 | Subsequent documentation, detection-inventory and metrics/status alignment | Documentation and alignment milestone |
| Future | Custom SENTINEL console over Wazuh; live Windows/AD endpoint | Planned |

Dates for v0.5–v0.9.1 are not restated here; see the [Changelog](CHANGELOG.md) and each evidence index.

### v0.1–v0.3 — Foundation and FIM investigation (summary)

- **v0.1:** Wazuh infrastructure, isolated network and Linux agent deployment ([evidence](evidence/v0.1/)).
- **v0.2:** custom FIM Rules `100002`–`100004`, completed 18 Nov 2026. Its documentation and evidence reconciliation were completed retroactively, after some v0.3 work; dates are kept as recorded.
- **v0.3:** CASE-001 evidence reconciliation is closed for the reviewed scope. The broader FIM investigation remains open.
- **Unresolved discrepancy (16 Oct):** the reviewed creation and deletion records showed built-in Rules `554` and `553`, and Rule `100002` was absent. The reason is unresolved. No root cause is claimed, and this is not labelled a confirmed detection failure.
- **Controlled lifecycle test (2 Nov):** the creation, modification and deletion of one dedicated file matched custom Rules `100003`, `100002` and `100004`. This was one session on one file, not a repeatability test.
- **Configuration evidence:** [E14](evidence/v0.3/screenshots/v0.3-e14-endpoint-syscheck-configuration.png) is the endpoint's Syscheck configuration. [E15](evidence/v0.3/screenshots/v0.3-e15-manager-syscheck-configuration.png) is the manager's configuration only.

The full chronology, evidence and limitations are in [CASE-001](investigations/CASE-001.md), the [Rule 100002 investigation](investigations/fim-rule-100002-investigation.md) and the [v0.2 evidence index](evidence/v0.2/readme.md).

### v0.4 — Windows Sysmon replay and cross-platform detection (19 Nov 2026)

On SENTINEL-LINUX01 (Agent ID `002`), `evtx_to_wazuh.py` converted 3 pre-recorded Windows Sysmon `.evtx` captures into 12 NDJSON records (24 lines replayed), which were ingested through a `json` `<localfile>`. SENTINEL-WAZUH evaluated them against a dedicated ruleset, `/var/ossec/etc/rules/sentinel_sysmon_replay_rules.xml` (`100100–100140`). See [CASE-002](investigations/CASE-002.md).

- **Noise suppression:** 3 benign `services.exe → svchost.exe` events were classified under Level 0 Rule `100101` (base rules `100100–100104`), and no alerts were emitted for them.
- **Detections:** all 7 selected replay detections fired (`100110`, `100111`, `100112`, `100120`, `100130`, `100131`, `100140`) at Levels 8–14, covering process creation, script execution, `comsvcs.dll` MiniDump-related activity, PowerShell network egress, and `lsass.exe` / `rundll32.exe` process access. These are replayed samples evaluated against rules. They are not seven confirmed attacks.
- **Evidence:** 7 raw alert records in [`evidence/sysmon-replay/sysmon_alerts_raw.json`](evidence/sysmon-replay/sysmon_alerts_raw.json), SHA-256 `b53473fd6340ec17365fec9cbbc1403e445523322c4c84ae28e40882995d7a59` (also in [`sysmon_alerts_raw.sha256`](evidence/sysmon-replay/sysmon_alerts_raw.sha256); replay notes in the [Sysmon replay readme](evidence/sysmon-replay/readme.md)).
- **Baseline integrity:** `local_rules.xml` (`100001–100004`, including FIM Rule `100002`) was not modified.
- **Scope boundary:** this validated replayed `.evtx` telemetry on Linux, not a live Windows host or the Sysmon kernel driver (`SysmonDrv.sys`). The replay approach was used because of VM storage constraints. The original `.evtx` captures are referenced in the documentation but are not committed to this repository.

### v0.5 — SSH brute-force detection and triage

Kali was used to generate controlled, simulated SSH authentication failures against the lab. Custom rules `100200` (authentication failure) and `100201` (repeated-failure escalation) were written and investigated. [CASE-003](investigations/CASE-003.md) documents the SSH brute-force investigation and response planning. It does not document an executed containment, eradication and recovery lifecycle. Evidence: [v0.5 index](evidence/v0.5/readme.md) · [Incident response](docs/06-incident-response.md).

### v0.6 — Controlled purple-team measurement and testing

Controlled FIM, Sysmon replay and SSH test suites with recorded results. Summary and caveats are in [Testing and Metrics](#testing-and-metrics). Evidence: [v0.6 index](evidence/v0.6/readme.md) · [measurement report](metrics/v0.6-purple-team-measurement.md).

### v0.7 — Mutation testing, logtest validation and reliability investigation

[CASE-004](investigations/CASE-004.md) covers variations of earlier test activity ("mutations"), checked against rules with Wazuh logtest, and a reliability investigation. Earlier roadmap notes called this work "Attack DNA". Terminal transcripts for this work were restored; checksum handling for them is documented with the evidence. Evidence: [v0.7 evidence folder](evidence/v0.7/).

### v0.8 — FIM group isolation, noise reduction and tuning

Changes to isolate FIM monitoring by agent group, reduce FIM noise and tune the configuration, including a probe of Agent `002`. Implemented and merged on `main`. The retest that would show whether noise suppression works after tuning is still pending.

### v0.9 — Sysmon JSON replay ingestion and Python-assisted triage integration

Extends the v0.4 replay approach with JSON ingestion and Python-assisted triage of the resulting alerts. Implemented and merged on `main`. Still replay-based; a live Windows agent is out of scope. Evidence: [v0.9 index](evidence/v0.9/readme.md) · [Python tooling](#python-tooling).

### v0.9.1 — Documentation, detection inventory and metrics/status alignment

A subsequent milestone that aligned documentation, the detection inventory and metrics/status wording across the repository. It adds no new detection or telemetry capability.

---

## Testing and Metrics

The v0.6 controlled measurement ([report](metrics/v0.6-purple-team-measurement.md), [evidence](evidence/v0.6/readme.md)) produced these results:

| Test | Result |
|---|---|
| FIM lifecycle (create / modify / delete) | 3/3 selected events detected |
| Sysmon replay | 7/7 selected replay detections fired |
| Benign Sysmon events | 3 suppressed (no alerts) |
| `/tmp` negative controls (outside the monitored path) | 0/3 FIM alerts, as expected |
| SSH threshold / sliding-window behaviour | Investigated; see the report for what was observed |

**These are small, controlled samples.** They are not enterprise detection rates, not general detection accuracy, not production false-positive rates, and not proof of complete coverage. They show that selected, pre-planned test cases behaved as intended in this lab.

These measurements describe the v0.6 test baseline. They should not be interpreted as post-v0.8 tuning results; the dedicated post-tuning noise-suppression retest remains pending.

**Clock skew.** The endpoint and manager clocks were not synchronised, which affected some timing measurements. Negative time deltas appear in that data. A negative delta is a clock artefact and must not be read as detection latency. Only positive deltas from correctly synchronised clocks would be valid latency figures, and the report should be read with that in mind.

Methodology: [Testing and metrics](docs/07-testing-and-metrics.md).

---

## Python tooling

- **[`scripts/evtx_to_wazuh.py`](scripts/evtx_to_wazuh.py)** — in this repository. Converts pre-recorded Windows Sysmon `.evtx` captures into NDJSON records that Wazuh ingests through a `json` `<localfile>` on SENTINEL-LINUX01 (used in v0.4 and extended in v0.9).
- **[Python SOC Automation Engine](https://github.com/andyydz/python-soc-automation)** — a separate repository, maintained independently (Wazuh alert parsing and triage logic). The v0.9 triage work connects replay output to Python-assisted triage; see the [v0.9 index](evidence/v0.9/readme.md) for what was actually run. It is not a production Wazuh integration.

---

## Scope and Limitations

What this lab is: a small, isolated, Linux-first environment used for controlled experiments and documented investigations.

What is not in place:

- **No live Windows endpoint** is monitored by the lab, and **no Active Directory** environment exists. Windows Sysmon telemetry is replayed from pre-recorded captures. The real Sysmon driver and a Wazuh Windows agent are future work, as is live Windows telemetry validation.
- **No production SOC claims.** Results come from small controlled samples (see [Testing and Metrics](#testing-and-metrics)). They do not establish detection rates, false-negative rates, or comprehensive FIM, SSH or Sysmon coverage.
- **Broader FP/FN testing and a repeatable regression suite** are not in place. Detection tuning exists (v0.8), but the post-tuning noise-suppression retest is still pending.
- **Open FIM questions:** the 16 Oct discrepancy (built-in Rules `554`/`553` seen, Rule `100002` absent) and the differences between the 16 and 31 Oct observations are not resolved. Historical loaded configuration and in-memory rule behaviour are not verified.
- **Response is documented, not fully exercised.** Three levels are kept apart in this repository:
  1. a *documented procedure* (for example, in [Incident response](docs/06-incident-response.md));
  2. a *manually investigated alert* (for example, [CASE-003](investigations/CASE-003.md));
  3. an *action actually executed and supported by evidence*.

  A fully evidenced containment, eradication and recovery exercise has not been carried out.
- **Detections do not prove malicious activity.** Alerts and any ATT&CK references describe detection intent and observed indicators (see [Detections](#detections)).
- **Not every source record is committed.** The reviewed 16 October alert records came from the Wazuh runtime log, and the repository does not claim to contain an exported copy. Raw alert records for 31 October and 2 November are likewise not committed; those results rest on terminal screenshots. The original `.evtx` captures are not committed. The v0.4 raw alerts are committed with a recorded SHA-256.
- **Other future work:** auth telemetry beyond the SSH work, threat hunting, additional cases, project-level MITRE ATT&CK mapping, and a custom SENTINEL console over Wazuh.

---

## Documentation and Evidence

| Area | Links |
|---|---|
| **Methodology** | [Detection engineering](docs/05-detection-engineering.md) · [Incident response](docs/06-incident-response.md) · [Testing and metrics](docs/07-testing-and-metrics.md) · [`docs/` folder (files 01–08)](docs/) |
| **Investigations** | [CASE-001](investigations/CASE-001.md) · [CASE-002](investigations/CASE-002.md) · [CASE-003](investigations/CASE-003.md) · [CASE-004](investigations/CASE-004.md) · [Rule 100002 investigation](investigations/fim-rule-100002-investigation.md) · [Investigations guide](investigations/readme.md) |
| **Detections** | [Detections guide](detections/readme.md) · [FIM rules](detections/local_rules.xml) · [SSH rules](detections/sentinel_ssh_bruteforce_rules.xml) · [Sysmon replay ruleset](detections/sentinel_sysmon_replay_rules.xml) |
| **Scripts** | [`evtx_to_wazuh.py`](scripts/evtx_to_wazuh.py) |
| **Evidence** | [Evidence guide](evidence/readme.md) · [v0.1](evidence/v0.1/) · [v0.2 index](evidence/v0.2/readme.md) · [v0.3 index](evidence/v0.3/readme.md) · [Sysmon replay (v0.4)](evidence/sysmon-replay/) · [v0.5 index](evidence/v0.5/readme.md) · [v0.6 index](evidence/v0.6/readme.md) · [v0.7 evidence](evidence/v0.7/) · [v0.9 index](evidence/v0.9/readme.md) |
| **Metrics** | [v0.6 purple-team measurement](metrics/v0.6-purple-team-measurement.md) |
| **v0.2 reports** | [Infrastructure and telemetry foundation](evidence/v0.2/infrastructure-and-telemetry-foundation.md) · [Wazuh–Linux01 integration](evidence/v0.2/wazuh-linux01-integration.md) · [SCA baseline](evidence/v0.2/sca-baseline.md) |
| **Project** | [Security policy](SECURITY.md) · [Changelog](CHANGELOG.md) |

---

## Security & Safety

SENTINEL is an authorized, isolated lab. All testing stays inside SENTINEL-LAB: no real credentials, no production targets, no external attacks, and no VM disks or secrets committed. Full policy in [`SECURITY.md`](SECURITY.md).
