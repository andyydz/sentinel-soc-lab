# CASE-003 — SSH Brute-Force Incident Response and Triage Automation

| Field | Value |
|---|---|
| Case ID | CASE-003 |
| Project | SENTINEL — SOC Lab |
| Milestone | v0.5 — Incident Response & SSH Brute-Force Triage |
| Status | **Complete / Verified** (Controlled attack, automated triage, manual IR) |
| Case severity | High |
| Detection source | Linux Syslog / `sshd` authentication telemetry |
| Ingest Endpoint | `SENTINEL-LINUX01` (`10.10.10.40`, Agent ID `002`) |
| Attacker Origin | `SENTINEL-KALI` (`10.10.10.20`, source port 55582) |
| Rules Triggered | `100200` (Level 5, 21 hits), `100201` (Level 10, 1 hit escalation) |
| MITRE ATT&CK | `T1110` (Brute Force), `T1110.001` (Password Guessing) |
| Evidence File | `evidence/v0.5/raw-alerts/ssh_bruteforce_alerts_raw.json` |
| Evidence SHA-256 | `16d3ce3be500c6e3537ff13703240424bd24fbdf55ba523a8e32e1b1eb7a47df` |

---

## 1. Executive Summary

On 20 November 2026, a controlled Hydra password-guessing simulation was executed from `SENTINEL-KALI` (`10.10.10.20`) against `SENTINEL-LINUX01` (`10.10.10.40`). Over 2m 46s (`13:52:38` to `13:55:25 IST`), 21 failed attempts were recorded.

Wazuh evaluated telemetry against `sentinel_ssh_bruteforce_rules.xml`, triggering baseline Rule `100200` (Level 5) and frequency escalation Rule `100201` (Level 10) once its frequency condition was met: six matching Rule `100200` events from the same source IP within the configured 60-second window. These matching events are not necessarily six unique failed-password attempts. Automated triage via `python-soc-automation` successfully isolated the Level 10 escalation while preserving raw alert hash integrity. Manual analyst verification confirmed zero successful logins and targeting of non-existent account `sentinel-probe`.

---

## 2. Attack Telemetry Profile

- **Attacker Host:** `SENTINEL-KALI` (`10.10.10.20`, source port 55582)
- **Target Host:** `SENTINEL-LINUX01` (`10.10.10.40:22`, Agent `002`)
- **Targeted Account:** `sentinel-probe` (invalid user)
- **Syslog Event:** `sshd[7293]: Invalid user sentinel-probe from 10.10.10.20 port 55582`

---

### Detection & Noise-Control Rationale
- **Trigger:** `100200` (Lvl 5) matches `sshd` auth failures (`5710`/`5716`); `100201` (Lvl 10) is a frequency-based escalation when `6+` matching Rule `100200` events from the same source IP occur within `60s` (`frequency=6`, `same_srcip`). The rule counts matching `100200` events, not a number of unique failed-password attempts.
- **Noise control:** `frequency=6` + `same_srcip` is intended to keep Lvl 10 escalation from firing on low-count activity such as 1-2 admin typos. Matching events are not assumed to map one-to-one to authentication attempts.

## 3. Automation vs. Manual SOC Analysis Boundary

| Investigation Activity | Execution Layer | Mechanism / Responsibility |
|---|---|---|
| **Severity Triage & Filtering** | **Automated (Python CLI)** | `python-soc-automation` applied `--min-level 8`, suppressing 21 Level 5 events to surface Rule `100201`. |
| **Evidence Integrity Check** | **Automated (Hashing)** | Verified raw JSON alert bytes match recorded SHA-256 (`16d3ce...`). |
| **Log Forensic Unmasking** | **Manual (SOC Analyst)** | Extracted target username `sentinel-probe` from syslog `full_log`. |
| **Blast Radius & Persistence** | **Manual (SOC Analyst)** | Reviewed raw alerts (0 accepted sessions) and documented endpoint verify commands. |
| **Containment Action** | **Manual (Human Decision)** | Documented source-scoped IP drop procedure. Procedure documented only; not executed, and no firewall block was applied. |

---

## 4. Incident Response Lifecycle (NIST SP 800-61r2)

Only Detection & Analysis was exercised in this case. Containment is a documented procedure that was not executed, and Eradication and Recovery were not exercised.

- **Preparation:** Active rules `100200` & `100201` on manager; agent `002` shipping `/var/log/auth.log`.
- **Detection & Analysis (exercised):** Rule `100201` escalation at `13:55:11 IST`. Python triage CLI filtered noise; manual log audit confirmed 0 successful sessions.
- **Containment (procedure documented; not executed):** Documented source-scoped containment procedure for `SENTINEL-LINUX01` (keeps `sshd` up for admins): (`sudo iptables -I INPUT 1 -s 10.10.10.20 -p tcp --dport 22 -j DROP` or `sudo ufw deny from 10.10.10.20 to any port 22`). These commands are documented only; they were not executed in this case, and no firewall block was applied. Containment is a manual, human-decision step; no automated containment or SOAR is implemented.
- **Eradication (not exercised):** 0 accepted-login alerts observed; post-incident verification commands are documented (`grep Accepted /var/log/auth.log`, `grep sentinel-probe /etc/passwd`, and `iptables -L INPUT -n`).
- **Recovery (not exercised):** Confirmed SSH service is responsive and healthy for authorized users. This is a service-health verification; it does not establish that a recovery exercise was performed.
- **Lessons Learned (findings documented; no complete post-incident lifecycle exercise):** Hardening recommendations: disable password authentication (`PasswordAuthentication no`), transition to SSH keys, and evaluate Wazuh active response (not implemented; any such automation would require human approval).

---

## 5. Evidence & Integrity Verification

- **Raw Alerts:** `evidence/v0.5/raw-alerts/ssh_bruteforce_alerts_raw.json` (22 records)
- **SHA-256 Checksum:** `16d3ce3be500c6e3537ff13703240424bd24fbdf55ba523a8e32e1b1eb7a47df`
- **Dashboard Proof:** `evidence/v0.5/screenshots/v0.5-nov20-ssh-bruteforce-rule-100201.png`
