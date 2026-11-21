# CASE-004 — Attack Mutation, Evasion Testing, and Benign Noise Filtering

| Field | Value |
|---|---|
| Case ID | CASE-004 |
| Project | SENTINEL — SOC Lab |
| Milestone | v0.7 — Attack Mutation & Noise Filtering |
| Status | **Complete / Verified** (FIM live capture + Sysmon/SSH `wazuh-logtest` validation) |
| Case severity | Medium |
| Detection sources | Wazuh Syscheck FIM (`100002–100004`), Sysmon Replay Rules (`100101`, `100110–100140`), SSHD Rules (`100200–100201`, `5715`) |
| Monitored Host | `SENTINEL-LINUX01` (`10.10.10.40`, Agent ID `002`) & Wazuh Manager (`10.10.10.10`) |
| Test Origin / Source | `10.10.10.20` (SSH test) / Local endpoint & `wazuh-logtest` v4.14.8 |
| Rules Observed | FIM `100002`–`100004` (Level 8); Sysmon `100101` (Level 0, `100112` bypassed via `#24`); SSH `100200` (Level 5, 3 hits, `100201` not triggered) & `5715` (Level 3 benign login) |
| MITRE ATT&CK | `T1003.001` (LSASS Memory / Credential Dumping), `T1059.003` (Windows Command Shell), `T1110` (Brute Force) |
| Evidence Files | `evidence/v0.7/fim_mutation_alerts_raw.json`, `evidence/v0.7/sysmon_mutation_logtest.txt`, `evidence/v0.7/ssh_mutation_logtest.txt` |
| Checksum Manifest | `evidence/v0.7/SHA256SUMS` |

---

## 1. Executive Summary

On 20 November 2026, Milestone `v0.7` evaluated detection resilience, scope blind spots, and noise trade-offs across three suites:
- **Suite A (Linux FIM):** Executed controlled hidden-file, out-of-scope staging, and cache churn tests on `SENTINEL-LINUX01` (`21:44:12.642+0530` to `21:44:27.723+0530`). Hidden `/home/` activity was caught at Level 8 (`100002`–`100004`), `/var/tmp/` was out of scope, and desktop/cache churn produced Level 8 noise.
- **Suite B (Sysmon Rule Logic via `wazuh-logtest`):** Tested `rundll32.exe` invoking `comsvcs.dll` with ordinal `#24` instead of literal `minidump` (bypassing `100112`, Level 13, landing on `100101`, Level 0) alongside `svchost.exe` spawning `conhost.exe` (suppressed from shell rule `100110`).
- **Suite C (SSH Timing & Benign Baseline via `wazuh-logtest`):** Tested 3 failed SSH attempts (below `frequency="6"` in `60s` for `100201`) plus 1 accepted publickey login (`5715`, Level 3).

---

## 2. Test Suite Findings & Detection Trade-Offs

### Suite A — Linux File Integrity Monitoring (`100002–100004`)
- **Mutation 1A (Hidden dot-dir + hidden payload):** `/home/sentinel-admin/.v07-hidden-dir/.v07-payload.sh` triggered `100003` (create), `100002` (modify), and `100004` (delete) at Level 8. Hiding behind leading dots inside `/home/` does not evade FIM.
- **Mutation 1B (Out-of-scope staging):** `/var/tmp/.v07-staging.sh` produced zero `100002`–`100004` alerts because FIM monitoring is scoped to `/home/`. Staging outside `/home/` is a real blind spot if unmonitored by process or broader path rules.
- **Benign Noise 1C (Cache & desktop churn):** `/home/sentinel-admin/.cache/v07-benign-cache-test.tmp` plus background `nautilus` and `tracker3` file updates triggered Level 8 FIM alerts, showing that unrefined `/home/` FIM generates background noise requiring downstream triage filtering.

### Suite B — Sysmon Replay Rules (`100100–100140`)
- **Evasion / Mutation:** `rundll32.exe C:\Windows\System32\comsvcs.dll, #24 4868 C:\Users\Public\out.bin` avoided the `minidump` substring required by Rule `100112` (`comsvcs\.dll.*minidump`) and stopped at base EID1 Rule `100101` (Level 0). Relying on a single command-line keyword creates an evasion gap unless correlated with EID10 (`100131`) or EID11 (`100140`).
- **Benign Noise Suppression:** `svchost.exe` launching `conhost.exe` matched `100101` (Level 0) and did not trigger `100110` (`cmd|powershell|pwsh`).

### Suite C — SSH Brute-Force Threshold (`100200–100201`) & Benign Login
- **Slow-and-Low / Sub-Threshold Activity:** Three failed SSH attempts (`admin`, `root`, `ops` from `10.10.10.20`) each triggered `100200` (Level 5, `T1110`) but did not escalate to `100201` (Level 10), because `100201` requires `frequency="6"` within `timeframe="60"` seconds from `same_srcip`.
- **Benign Baseline:** An accepted publickey login (`sentinal-admin` from `10.10.10.20`) triggered built-in Rule `5715` (Level 3) without firing `100200` or `100201`.

---

## 3. Evidence Integrity (SHA-256)

Recorded in `evidence/v0.7/SHA256SUMS`:
- `e757820e27b9c24b7bebdb6d6cfc9d64bbb7ebebd82ae2a6a3dfe714a9c4d0ba` — `evidence/v0.7/fim_mutation_alerts_raw.json`
- `736634982f8f35d1cd4452aaa4bc001350c92df56949b2c4e499f0edb4bded68` — `evidence/v0.7/sysmon_mutation_logtest.txt`
- `07470216acc31a40e57dbfe105d5c4d08ab203d008283aa429a6fee8c0556c85` — `evidence/v0.7/ssh_mutation_logtest.txt`

---

## 4. Analyst Takeaways & Follow-Up Improvements
1. **Defense in Depth Beyond Single Indicators:** Never depend on a single command-line string like `minidump` when `#24` ordinal invocation is possible; combine process creation, process access (`EID10`), and file write (`EID11`) signals.
2. **Explicit Scope Documentation:** Document `/var/tmp/` exclusion honestly—either expand scope deliberately or pair FIM with process/audit monitoring rather than pretending `/home/` FIM covers the whole OS.
3. **Triage Automation (`python-soc-automation`):** Filter out low-value Level 0/3 noise and separate Level 5 single/low-count events from high-confidence escalations during alert triage.
