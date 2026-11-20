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

Wazuh evaluated telemetry against `sentinel_ssh_bruteforce_rules.xml`, triggering baseline Rule `100200` (Level 5) and frequency escalation Rule `100201` (Level 10) once 6 failures in 60s occurred from a single IP. Automated triage via `python-soc-automation` successfully isolated the Level 10 escalation while preserving raw alert hash integrity. Manual analyst verification confirmed zero successful logins and targeting of non-existent account `sentinel-probe`.

---

## 2. Attack Telemetry Profile

- **Attacker Host:** `SENTINEL-KALI` (`10.10.10.20`, source port 55582)
- **Target Host:** `SENTINEL-LINUX01` (`10.10.10.40:22`, Agent `002`)
- **Targeted Account:** `sentinel-probe` (invalid user)
- **Syslog Event:** `sshd[7293]: Invalid user sentinel-probe from 10.10.10.20 port 55582`

---

### Detection & Noise-Control Rationale
- **Trigger:** `100200` (Lvl 5) matches `sshd` auth failures (`5710`/`5716`); `100201` (Lvl 10) escalates on `6+` failures in `60s` (`same_srcip`).
- **Noise control:** `frequency=6` + `same_srcip` suppresses Lvl 10 alerts on 1-2 admin typos.

## 3. Automation vs. Manual SOC Analysis Boundary

| Investigation Activity | Execution Layer | Mechanism / Responsibility |
|---|---|---|
| **Severity Triage & Filtering** | **Automated (Python CLI)** | `python-soc-automation` applied `--min-level 8`, suppressing 21 Level 5 events to surface Rule `100201`. |
| **Evidence Integrity Check** | **Automated (Hashing)** | Verified raw JSON alert bytes match recorded SHA-256 (`16d3ce...`). |
| **Log Forensic Unmasking** | **Manual (SOC Analyst)** | Extracted target username `sentinel-probe` from syslog `full_log`. |
| **Blast Radius & Persistence** | **Manual (SOC Analyst)** | Reviewed raw alerts (0 accepted sessions) and documented endpoint verify commands. |
| **Containment Action** | **Manual (Human Decision)** | Documented IP drop procedure (no persistent block left active). |

---

## 4. Incident Response Lifecycle (NIST SP 800-61r2)

- **Preparation:** Active rules `100200` & `100201` on manager; agent `002` shipping `/var/log/auth.log`.
- **Detection & Analysis:** Rule `100201` escalation at `13:55:11 IST`. Python triage CLI filtered noise; manual log audit confirmed 0 successful sessions.
- **Containment:** Documented source-scoped containment on `SENTINEL-LINUX01` (keeps `sshd` up for admins; not left active): (`sudo iptables -I INPUT 1 -s 10.10.10.20 -p tcp --dport 22 -j DROP` or `sudo ufw deny from 10.10.10.20 to any port 22`).
- **Eradication:** 0 accepted-login alerts observed; post-incident verify via `grep Accepted /var/log/auth.log`, `grep sentinel-probe /etc/passwd`, and `iptables -L INPUT -n`.
- **Recovery:** Confirmed SSH service is responsive and healthy for authorized users.
- **Lessons Learned:** Hardening: disable password authentication (`PasswordAuthentication no`), transition to SSH keys, and evaluate automated Wazuh active response.

---

## 5. Evidence & Integrity Verification

- **Raw Alerts:** `evidence/v0.5/raw-alerts/ssh_bruteforce_alerts_raw.json` (22 records)
- **SHA-256 Checksum:** `16d3ce3be500c6e3537ff13703240424bd24fbdf55ba523a8e32e1b1eb7a47df`
- **Dashboard Proof:** `evidence/v0.5/screenshots/v0.5-nov20-ssh-bruteforce-rule-100201.png`
