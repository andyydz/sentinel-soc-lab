
# SENTINEL — SOC Lab

> Does your detection still work when the attacker changes tactics?


SENTINEL is a controlled virtual SOC lab (VirtualBox + Wazuh + Kali + an Ubuntu endpoint) built to practice and evidence a full defensive engineering workflow, not just install security tools.

```
SIMULATE → DETECT → INVESTIGATE → RESPOND → MEASURE → IMPROVE → RETEST
```

Each stage is meant to be demonstrated with real evidence before the next is trusted. A detection isn't "done" because a rule exists. It's done once it's been tested, the result recorded, and the result holds up.

---



## Architecture

```text
                        INTERNET
                            |
                           NAT
                            |
                   +----------------+
                   | SENTINEL-WAZUH |
                   |  10.10.10.10   |
                   +----------------+
                            |
                     SENTINEL-LAB
                     10.10.10.0/24
                            |
                 +----------+----------+
                 |                     |
        +---------------+     +------------------+
        | SENTINEL-KALI |     | SENTINEL-LINUX01 |
        |  10.10.10.20  |     |  10.10.10.40     |
        +---------------+     +------------------+
```

| Host | Role |
|---|---|
| SENTINEL-WAZUH (`10.10.10.10`) | Ubuntu 24.04, Wazuh 4.14.8 — manager and dashboard. |
| SENTINEL-KALI (`10.10.10.20`) | Kali Linux 2026.2 — controlled adversary-emulation VM used for simulated SSH authentication testing ([CASE-003](investigations/CASE-003.md)). |
| SENTINEL-LINUX01 (`10.10.10.40`, Agent ID `002`) | Ubuntu 24.04.5 LTS, Wazuh Agent 4.14.8 — monitored endpoint with real-time File Integrity Monitoring (FIM) on `/home`. Also the replay endpoint for the v0.4 Windows Sysmon telemetry. |
| SENTINEL-LAB (`10.10.10.0/24`) | Isolated internal network; NAT provides outbound access. |

> An earlier Windows endpoint (SENTINEL-WIN01) was dropped after repeated boot/deployment failures. There is still no live Windows, Sysmon, or Active Directory endpoint in the lab; that is future work. Windows detection coverage in v0.4 comes from replayed Sysmon `.evtx` telemetry processed on SENTINEL-LINUX01 (see [CASE-002](investigations/CASE-002.md)).

---

## Current Status

**v0.1 — Foundation: complete.** Wazuh deployed, Kali and Linux01 deployed, isolated network established, agent enrolled and communicating.

**v0.2 — Telemetry & Initial Detection Engineering: complete.** Completed on 18 Nov 2026. Coverage gap resolved: identified parent SID chaining constraint (Rule 100002 chained strictly to SID 550 modification). Standardized custom rules 100002, 100003, and 100004 with anchored regex `^/home/` and enriched with MITRE ATT&CK taxonomy tags (T1105, T1565.001, T1070.004).

Key findings (October 2026):
- **Modification:** Rule `100002` (Level 8) fired on controlled modifications on 11 Oct (supported by screenshots; the original source log was not recovered) and 26 Oct (two alerts from consecutive modifications of one file, not two independent test cases).
- **Creation and deletion (16 Oct):** the reviewed records showed built-in Rules `554` and `553`, and Rule `100002` was absent. The reason is unresolved. No root cause is claimed, and this is not labeled a confirmed detection failure.
- **Custom creation/deletion rules (31 Oct, observation only):** custom Rule `100003` (creation, Level 8) and custom Rule `100004` (deletion, Level 8) appeared in one terminal screenshot: [`evidence/v0.3/screenshots/v0.3-fim-lifecycle-custom-detections.png`](evidence/v0.3/screenshots/v0.3-fim-lifecycle-custom-detections.png). These are observations, not validated controlled tests. Raw alert records, process attribution, and root cause are not established. This is separate from the 16 Oct built-in Rule `554`/`553` records and from the 11/26 Oct Rule `100002` modification results, and it does not explain the Rule `100002` absence above.

These results do not establish complete FIM coverage, measured detection rates, or malicious activity. Details: [Rule 100002 investigation](investigations/fim-rule-100002-investigation.md).

**SCA observation (29 Oct 2026).** The [SCA baseline report](evidence/v0.2/sca-baseline.md) records a single Wazuh dashboard observation using built-in Wazuh functionality. It is not a custom SENTINEL detection, a remediation exercise, proof of compliance or improved posture, or a detection-engineering milestone.

**v0.3 — SOC Investigation: phase milestone complete.** The v0.3 project phase and its planned documentation and evidence milestone are complete. For CASE-001, evidence reconciliation for the reviewed scope is closed (endpoint FIM configuration verified with realtime="yes" in E14, single-file lifecycle behavior observed on 2 Nov, committed JSON alerts with SHA-256 checksums, and background/cache noise noted), while broader investigation and detection-engineering work remain open. No root cause, attribution, or malicious activity is established, and no containment, eradication, or recovery has been exercised. See [CASE-001](investigations/CASE-001.md) and the [v0.3 evidence index](evidence/v0.3/readme.md).

v0.3 additions (2–3 November 2026):
- **Controlled lifecycle validation (2 Nov):** in one controlled session on SENTINEL-LINUX01, a single dedicated file, `/home/sentinel-admin/sentinel-v03-final-test.txt`, was created, modified, and deleted. Creation matched custom Rule `100003`, modification matched `100002`, and deletion matched `100004`, each at Level 8 ([screenshot](evidence/v0.3/screenshots/v0.3-fim-full-lifecycle-custom-rules.png)). This was one controlled lifecycle session on one dedicated file. It is not a regression suite or repeatability test, and it does not establish comprehensive FIM coverage. Raw 2 November alert JSON records are not committed. The session does not explain the 16 Oct observations or retroactively validate the 31 Oct observations.
- **Configuration evidence (committed):** [E14](evidence/v0.3/screenshots/v0.3-e14-endpoint-syscheck-configuration.png) shows the SENTINEL-LINUX01 endpoint's local Syscheck configuration: real-time monitoring of `/home`, startup scanning enabled, and a 43,200-second scheduled scan frequency. [E15](evidence/v0.3/screenshots/v0.3-e15-manager-syscheck-configuration.png) shows only the SENTINEL-WAZUH manager's Syscheck configuration; it is not evidence of endpoint `/home` monitoring, which E14 supports. Both show local configuration files as captured, and neither independently proves which configuration was loaded during the 16 Oct tests.
- **Rule `100002` on-disk verification (3 Nov):** a read-only check on SENTINEL-WAZUH confirmed the on-disk definition in `/var/ossec/etc/rules/local_rules.xml` (Level 8, parent Rule `550`, file condition `^/home/`) and that `wazuh-analysisd` was running. The rule file's modification time preceded the analysis engine's start time, which is consistent with the engine starting after the file was modified. It does not prove the exact in-memory rule definition or the configuration loaded on 16 Oct. No configuration changes or restart were performed.

**v0.4 — Windows Sysmon Replay & Cross-Platform Detection: complete.** Completed on 19 Nov 2026. On SENTINEL-LINUX01 (Agent ID `002`), `evtx_to_wazuh.py` converted 3 pre-recorded Windows Sysmon `.evtx` captures into 12 NDJSON records (24 lines replayed), which were ingested through a `json` `<localfile>`. SENTINEL-WAZUH evaluated them against a dedicated ruleset, `/var/ossec/etc/rules/sentinel_sysmon_replay_rules.xml` (`100100–100140`). See [CASE-002](investigations/CASE-002.md).
- **Noise suppression:** 3 benign `services.exe → svchost.exe` events were classified under Level 0 Rule `100101` (base rules `100100–100104`), and no alerts were emitted for them.
- **Detections:** all 7 attack rules fired (`100110`, `100111`, `100112`, `100120`, `100130`, `100131`, `100140`) at Levels 8–14, covering process creation, script execution, `comsvcs.dll` MiniDump credential dumping, PowerShell network egress, and `lsass.exe` / `rundll32.exe` process access.
- **Evidence:** 7 raw alert records in [`evidence/sysmon-replay/sysmon_alerts_raw.json`](evidence/sysmon-replay/sysmon_alerts_raw.json), SHA-256 `b53473fd6340ec17365fec9cbbc1403e445523322c4c84ae28e40882995d7a59`.
- **Baseline integrity:** `local_rules.xml` (`100001–100004`, including FIM Rule `100002`) was not modified.
- **Scope boundary:** this validated replayed `.evtx` telemetry on Linux, not a live Windows host or the Sysmon kernel driver (`SysmonDrv.sys`). The replay approach was used because of VM storage constraints. It does not establish detection rates, false-negative rates, or broad technique coverage.

---

## Roadmap

| Version | Focus | Status |
|---|---|---|
| v0.1 | Foundation — infrastructure, network, Wazuh deployment | Complete |
| v0.2 | Telemetry and detection engineering — FIM Rules `100002`–`100004` (MITRE mapped) | Complete |
| v0.3 | SOC investigation — CASE-001 and FIM lifecycle validation | Complete (CASE-001 evidence reconciliation closed; investigation open) |
| v0.4 | Windows Sysmon Replay & Cross-Platform Detection — CASE-002 | Complete |
| v0.5 | Incident Response — SSH brute-force IR & triage (`CASE-003`) | Complete |
| v0.6 | Purple-Team Measurement — controlled FIM, Sysmon & SSH suites | Complete |
| v0.7 | Attack DNA & Mutation Testing (`CASE-004`) | Complete (transcripts restored & checksums verified) |
| v0.8 | FIM group isolation, tuning & Agent 002 probe | Merged on `main` (noise-suppression retest pending) |
| v0.9 | Sysmon JSON replay ingestion & triage integration (`v0.9.1` cleanup) | Merged on `main` (replay-based; live Windows agent out-of-scope) |
| Future | Custom SENTINEL console over Wazuh; live Windows/AD endpoint | Planned |

Outstanding work (not yet in place):
- Investigation of the 16 Oct discrepancy and of the differences between the 16 and 31 Oct observations.
- Verification of historical loaded configurations and in-memory rule behavior.
- Broader false-positive/false-negative testing, a repeatable regression suite, and detection tuning with validation of its effectiveness.
- Measured detection rates and comprehensive FIM and Sysmon coverage.
- Live Windows endpoint telemetry (real Sysmon driver and Wazuh Windows agent), auth telemetry, threat hunting, additional cases, and project-level MITRE ATT&CK mapping.
- A fully evidenced containment, eradication, and recovery exercise remains outstanding (`CASE-003` documents SSH brute-force investigation and response planning rather than a complete executed IR lifecycle).

---

## Documentation & Evidence

| Area | Links |
|---|---|
| **Methodology** | [Detection engineering](docs/05-detection-engineering.md) · [Incident response](docs/06-incident-response.md) · [Testing and metrics](docs/07-testing-and-metrics.md) |
| **Investigations** | [CASE-001](investigations/CASE-001.md) · [CASE-002](investigations/CASE-002.md) · [CASE-003](investigations/CASE-003.md) · [CASE-004](investigations/CASE-004.md) · [Rule 100002 investigation](investigations/fim-rule-100002-investigation.md) · [Investigations guide](investigations/readme.md) |
| **Detections** | [Detections guide](detections/readme.md) · [Sysmon replay ruleset](detections/sentinel_sysmon_replay_rules.xml) |
| **Evidence** | [Evidence guide](evidence/readme.md) · [v0.1](evidence/v0.1/) · [v0.2 index](evidence/v0.2/readme.md) · [v0.3 index](evidence/v0.3/readme.md) · [Sysmon replay (v0.4)](evidence/sysmon-replay/) · [v0.5 index](evidence/v0.5/readme.md) · [v0.6 index](evidence/v0.6/readme.md) · [v0.7 evidence](evidence/v0.7/) · [v0.9 index](evidence/v0.9/readme.md) · [v0.6 metrics](metrics/v0.6-purple-team-measurement.md) |
| **v0.2 reports** | [Infrastructure and telemetry foundation](evidence/v0.2/infrastructure-and-telemetry-foundation.md) · [Wazuh–Linux01 integration](evidence/v0.2/wazuh-linux01-integration.md) · [SCA baseline](evidence/v0.2/sca-baseline.md) |
| **Project** | [Security policy](SECURITY.md) · [Changelog](CHANGELOG.md) |

Not every source record is committed. The reviewed 16 October alert records came from the Wazuh runtime log, and the repository does not claim to contain an exported copy. Raw alert records for 31 October and 2 November are likewise not committed; those results rest on terminal screenshots. The v0.4 raw alerts are committed with a recorded SHA-256.

---

## Security & Safety

SENTINEL is an authorized, isolated lab. All testing stays inside SENTINEL-LAB: no real credentials, no production targets, no external attacks, and no VM disks or secrets committed. Full policy in [`SECURITY.md`](SECURITY.md).
