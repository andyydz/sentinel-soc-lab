# CASE-002 — Windows Sysmon Telemetry Replay and Attack Detection Validation

| Field | Value |
|---|---|
| Case ID | CASE-002 |
| Project | SENTINEL — SOC Lab |
| Version | v0.4 — Windows Telemetry & Detection Engineering |
| Status | Controlled telemetry replay and detection rule validation: Complete / Verified |
| Severity | Medium |
| Detection Source | Replayed Windows Sysmon Event Logs (Event IDs 1, 3, 10, 11) |
| Ingestion Method | python-evtx conversion -> NDJSON -> Wazuh logcollector (json format) |
| Custom Rules | Base structural: 100100-100104 (Level 0) \| Detections: 100110, 100111, 100112, 100120, 100130, 100131, 100140 |
| Ingest Endpoint | SENTINEL-LINUX01 (10.10.10.40), Agent ID 002 |
| Telemetry Origin | Microsoft-Windows-Sysmon/Operational (MSEDGEWIN10 / IEWIN7) |
| Evidence File | evidence/sysmon-replay/sysmon_alerts_raw.json |
| Evidence SHA-256 | b53473fd6340ec17365fec9cbbc1403e445523322c4c84ae28e40882995d7a59 |

> Severity note: Case severity Medium is an administrative investigation classification for this detection validation milestone. Fired alert severity levels range from Level 8 to Level 14.

---

## Executive Summary

On 19 November 2026, a controlled telemetry replay and detection validation exercise was executed in the SENTINEL SOC Lab to establish Windows endpoint threat detection capabilities without requiring a persistent high-overhead Windows VM on the host.

Pre-recorded Windows Sysmon `.evtx` attack captures were transferred to `SENTINEL-LINUX01`, converted into Wazuh-standard JSON via `python-evtx`, and ingested in real time via `wazuh-logcollector`. On `SENTINEL-WAZUH`, custom ruleset `sentinel_sysmon_replay_rules.xml` (`100100+`) was loaded alongside existing Linux FIM rules (`100001-100004`), which remained untouched.

### Validation Results

1. **Noise Filtering (Level 0 Base Rules)**:
   - 3 benign process creation events (`services.exe` -> `svchost.exe`) were ingested and classified under Rule `100101` (Level 0).
   - Zero false-positive alerts were emitted to `alerts.json`.
2. **Attack Scenario Detections (7 of 7 Validated)**:
   - All 7 distinct malicious actions across process creation, scripting, LOLBin credential dumping, network egress, and process injection fired high-severity alerts.
3. **Evidence Integrity**:
   - 7 raw JSON alert records were extracted to `evidence/sysmon-replay/sysmon_alerts_raw.json` with SHA-256 hash `b53473fd6340ec17365fec9cbbc1403e445523322c4c84ae28e40882995d7a59`.

---

## Detection-Validation Summary

| Rule ID | Level | Event Type | Technique / Trigger | MITRE ATT&CK |
|---|---|---|---|---|
| 100110 | 12 | Sysmon EID 1 (Process Create) | `svchost.exe` spawning `cmd.exe` shell | T1059.003 |
| 100111 | 10 | Sysmon EID 1 (Process Create) | `cscript.exe` executing `memdump.vbs` from ProgramData | T1059.005 |
| 100112 | 13 | Sysmon EID 1 (Process Create) | `rundll32.exe` invoking `comsvcs.dll, MiniDump` | T1003.001, T1218.011 |
| 100140 | 10 | Sysmon EID 11 (File Create) | `rundll32.exe` creating `.bin` dump file in System32 | T1003.001 |
| 100131 | 12 | Sysmon EID 10 (Process Access) | `rundll32.exe` access with `comsvcs/dbgcore` call trace | T1003.001, T1218.011 |
| 100120 | 8 | Sysmon EID 3 (Network Connect) | `powershell.exe` outbound connection to 151.101.36.133:443 | T1059.001, T1105 |
| 100130 | 14 | Sysmon EID 10 (Process Access) | `powershell.exe` opening handle to `lsass.exe` | T1003.001 |

---

## Technical Scope and Limitations

- **Replay Telemetry**: Events originated from historical EVTX captures replayed through `SENTINEL-LINUX01`. This validates logcollector parsing, decoder mapping, `analysisd` regex evaluation, and alert generation, but does not test real-time kernel driver interception (`SysmonDrv.sys`) on a live Windows machine.
- **Rule Isolation**: Custom rules `100100-100140` are isolated in `detections/sentinel_sysmon_replay_rules.xml`. Existing Linux FIM rule `100002` and local rules `100001-100004` were preserved without modification.
- **Repeatability**: The replay script (`evtx_to_wazuh.py`) provides repeatable, deterministic log injection for future automated regression testing.
