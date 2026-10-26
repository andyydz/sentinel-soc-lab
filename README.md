# SENTINEL — SOC Lab

> Does your detection still work when the attacker changes tactics?

SENTINEL is a controlled virtual SOC lab (VirtualBox + Wazuh + Kali + an Ubuntu endpoint) built to practice and evidence a full defensive engineering workflow, not just install security tools.

## Objective

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
| SENTINEL-WAZUH (`10.10.10.10`) | Ubuntu 24.04, Wazuh 4.14.8 — SOC/monitoring platform, dashboard operational. |
| SENTINEL-KALI (`10.10.10.20`) | Kali Linux — controlled attacker/adversary-emulation VM. |
| SENTINEL-LINUX01 (`10.10.10.40`, Agent ID `002`) | Ubuntu 24.04, Wazuh Agent 4.14.8 — monitored endpoint; real-time File Integrity Monitoring (FIM) configured on `/home`. |
| SENTINEL-LAB (`10.10.10.0/24`) | Isolated internal network; NAT used only for legitimate package/update traffic. |

> An earlier Windows endpoint (SENTINEL-WIN01) was dropped after repeated boot/deployment failures. Windows/AD is now future work, not a blocking dependency.

---

## Current Status

**v0.1 — Foundation (complete).** Wazuh deployed and operational, Kali and Linux01 deployed, isolated lab network established, Wazuh agent enrolled and communicating with the manager.

**v0.2 — Telemetry & Initial Detection Engineering (in progress).** Real-time FIM is configured on `/home`. Custom Rule `100002` (Level 8) has been observed firing on controlled **modification** tests. Creation and deletion are tracked separately and are **not** validated for the custom rule. Each result applies only to its own test:

| Scenario | Test file | Result |
|---|---|---|
| Modification (11 Oct 2026) | `/home/sentinel-admin/sentinel-fim-validation.txt` | Existing screenshots support a controlled modification that triggered custom Rule `100002` at Level 8. The original source alert log was not recovered during the 26 October review. |
| Modification (26 Oct 2026) | `/home/sentinel-admin/sentinel-v02-mod-test.txt` | Two controlled modifications each generated a Rule `100002` Level 8 alert: `2026-10-26T21:38:27.910+0530` (size 0 → 23 bytes) and `2026-10-26T21:38:48.473+0530` (size 23 → 61 bytes). |
| Creation (16 Oct 2026) | `/home/sentinel-admin/sentinel-audit-test.txt` | Reviewed source record showed built-in Rule `554` at `2026-10-16T11:40:06.007+0530`. Rule `100002` was absent. |
| Deletion (16 Oct 2026) | `/home/sentinel-admin/sentinel-audit-test.txt` | Reviewed source record showed built-in Rule `553` at `2026-10-16T12:31:32.819+0530`. Rule `100002` was absent. |

**Why `100002` was absent from the creation and deletion records is unresolved.** No root cause is claimed. The on-disk rule configuration was inspected earlier, but the configuration the manager had loaded during the historical tests and the exact `/home/` matching behavior have not been reverified. The creation and deletion records are not custom-rule validations.

Still open in v0.2:
- Inspect the current loaded rule configuration and verify `/home/` matching behavior; historical runtime configuration remains unconfirmed.
- Investigate custom-rule coverage for creation and deletion.
- Build a repeatable creation/modification/deletion regression test (not yet done).
- Complete false-positive/false-negative analysis (not yet done).
- Review background FIM activity and tune rules (not yet done).

The modification results show that Rule `100002` fires in the controlled modification tests performed. They do not establish complete FIM coverage, measured detection rates, or malicious activity. ATT&CK mappings on built-in events are telemetry metadata, not evidence of intent.

**v0.3 — SOC Investigation (in progress).** CASE-001 evidence reconciliation for the reviewed scope is **closed**. Broader investigation and detection-engineering work remain **open**. No attribution, malicious intent, or comprehensive root cause has been established. Full findings:
- [`investigations/CASE-001.md`](investigations/CASE-001.md)
- [`investigations/fim-rule-100002-investigation.md`](investigations/fim-rule-100002-investigation.md)

> **Not yet in place:** custom-rule validation for creation and deletion, complete FIM coverage, a repeatable regression suite, false-positive/false-negative analysis, measured detection rates, broader telemetry (auth, process execution), project-level MITRE ATT&CK mapping, incident response, purple-team validation, attack mutation, or a custom console.

---

## Roadmap

| Version | Focus | Status |
|---|---|---|
| v0.1 | Foundation — infrastructure, network, Wazuh deployment | Complete |
| v0.2 | Telemetry and detection engineering — FIM and custom Rule `100002` | In progress — modification validated in controlled tests (11 and 26 Oct); creation/deletion not validated for the custom rule |
| v0.3 | SOC investigation — CASE-001 and FIM investigation | In progress — reviewed-scope evidence reconciliation closed; broader investigation open |
| v0.4 | Incident response | Planned — not started until v0.3 is properly closed |
| v0.5 | Purple-team measurement | Planned |
| v0.6 | Attack DNA and mutation testing | Planned |
| Future | Custom SENTINEL console — visualization layer over Wazuh | Planned |

---

## What Makes It Valuable

SENTINEL isn't judged by tool count. It's judged by whether each claim is backed by evidence. Rule `100002` is presented as working for controlled modification tests only. Creation and deletion results are not presented as custom-rule validations, and open questions are tracked rather than hidden.

The project's differentiator is the full loop (simulate, detect, investigate, measure, improve, retest), not any single component in it.

---

## Documentation & Evidence

| Resource | Covers |
|---|---|
| [`docs/05-detection-engineering.md`](docs/05-detection-engineering.md) | Detection methodology and Rule `100002` validation status |
| [`docs/06-incident-response.md`](docs/06-incident-response.md) | Incident response methodology and CASE-001 status |
| [`docs/07-testing-and-metrics.md`](docs/07-testing-and-metrics.md) | Testing/validation methodology and metrics framework |
| [`evidence/v0.1/`](evidence/v0.1/) • [`v0.2/`](evidence/v0.2/) • [`v0.3/`](evidence/v0.3/) | Screenshots and artifacts for each milestone. Not every source record cited in the status table is committed as a repository artifact; see the investigation documents for evidence handling. |
| [`detections/readme.md`](detections/readme.md) • [`investigations/readme.md`](investigations/readme.md) | How detections and investigations are organized |
| [`investigations/CASE-001.md`](investigations/CASE-001.md) | Current SOC investigation case record |
| [`investigations/fim-rule-100002-investigation.md`](investigations/fim-rule-100002-investigation.md) | Investigation notes on Rule `100002` |
| [`SECURITY.md`](SECURITY.md) | Safe-testing boundaries |
| [`CHANGELOG.md`](CHANGELOG.md) | Version history |

---

## Security & Safety

SENTINEL is an authorized, isolated lab. All testing stays inside SENTINEL-LAB: no real credentials, no production targets, no external attacks, and no VM disks or secrets committed. Full policy in [`SECURITY.md`](SECURITY.md).

---

SENTINEL — a detection is only "working" once it's been tested and the result holds up.
