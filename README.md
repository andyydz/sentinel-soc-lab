# SENTINEL — SOC Lab

> Does your detection still work when the attacker changes tactics?

SENTINEL is a controlled virtual SOC lab (VirtualBox + Wazuh + Kali + an Ubuntu endpoint) built to practice and evidence a full defensive engineering workflow — not just install security tools.

## Objective

```
SIMULATE → DETECT → INVESTIGATE → RESPOND → MEASURE → IMPROVE → RETEST
```

Each stage is meant to be demonstrated with real evidence before the next is trusted. A detection isn't "done" because a rule exists — it's done once it's been tested, the result recorded, and the result holds up.

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

**v0.1 — Foundation (complete)**
Wazuh deployed and operational, Kali and Linux01 deployed, isolated lab network established, Wazuh agent enrolled and communicating with the manager.

**v0.2 — Telemetry & Initial Detection Engineering (in progress)**
Real-time File Integrity Monitoring (FIM) is configured on `/home`. Controlled file-integrity testing has produced the following results. All three results below are reported lab observations (the creation and deletion tests were run on 16 October 2026); the supporting raw alerts and screenshots have not yet been reviewed for this README, and each result is limited to its specific test:

| Scenario | Test file | Reported result |
|---|---|---|
| Modification | `/home/sentinel-admin/sentinel-fim-validation.txt` | Custom Rule `100002` fired at Level 8; built-in Rule 550 (Level 7, "Integrity checksum changed") also observed. |
| Creation | `/home/sentinel-admin/sentinel-audit-test.txt` | Custom Rule `100002` fired at Level 8, alongside built-in Rule 554 ("File added to the system"), as real-time FIM activity. |
| Deletion | `/home/sentinel-admin/sentinel-audit-test.txt` | Built-in Rule 553 (Level 7, "File deleted") generated an alert; custom Rule `100002` **did not** fire. |

Rule `100002` is currently anchored to built-in Rule 550 and matches the `file` field against `/home/`. The deletion result is an **observed coverage gap and an open engineering finding** — the deletion was still alerted on by the built-in rule. **Unresolved discrepancy:** `100002` reportedly fired on the creation event even though it is anchored to Rule 550. This has not been explained and must be verified against the raw alert and the active rule definition before any coverage claim is relied on. The rule has not been modified in response to these findings.

Still outstanding: investigation and resolution of the deletion gap, a repeatable creation/modification/deletion regression test, broader false-positive/false-negative analysis (including review of background FIM activity), and detection-rule tuning. These results are reported lab observations scoped to single controlled tests; they do not establish complete FIM coverage, measured detection rates, or malicious activity. Any ATT&CK mappings shown on built-in events are telemetry metadata, not evidence of intent.

**v0.3 — SOC Investigation (started)**
Investigation `CASE-001` (`investigations/CASE-001.md`) is underway. FIM events have been filtered and reviewed, including the Rule 550 and Rule 100002 event details. **CASE-001's controlled-validation objective is closed** — it confirms the tested modification-detection scenario only. Timeline reconstruction, root-cause analysis, attribution, and broader event review remain ongoing and are not yet complete. Recording the creation and deletion results in the case record is pending review.

> Not yet in place: complete FIM coverage (deletion not covered by the custom rule; creation and modification validated only for single controlled tests), broader telemetry (auth, process execution), project-level MITRE ATT&CK mapping, a completed investigation, incident response, performance metrics, purple-team validation, attack mutation, or a custom console.

---

## Roadmap

| Version | Focus | Status |
|---|---|---|
| v0.1 | Foundation — infrastructure, network, and Wazuh deployment | Complete |
| v0.2 | Telemetry and detection engineering — FIM and custom Rule `100002` | In progress — controlled modification and creation detection reported; deletion coverage gap open; broader testing and tuning remain |
| v0.3 | SOC investigation — CASE-001 and evidence-backed FIM investigation | In progress — CASE-001's controlled-validation objective is closed; broader investigation work remains |
| v0.4 | Incident response | Planned |
| v0.5 | Purple-team measurement | Planned |
| v0.6 | Attack DNA and mutation testing | Planned |
| Future | Custom SENTINEL console — visualization layer over Wazuh | Planned |

---

## What Makes It Valuable

SENTINEL isn't judged by tool count — it's judged by whether each claim is backed by evidence. A detection is "working" only once it's been tested and the result documented. Rule `100002`'s Level 8 alerts are scoped honestly to the controlled modification and creation scenarios they were tested against — they are not presented as complete FIM coverage. The deletion test, where built-in Rule 553 alerted but `100002` did not, is tracked openly as a coverage gap rather than hidden, alongside the remaining validation work (regression testing, false-positive/negative testing, tuning).

The project's differentiator is the full loop — simulate, detect, investigate, measure, improve, retest — not any single component in it.

---

## Documentation & Evidence

| Resource | Covers |
|---|---|
| [`docs/05-detection-engineering.md`](docs/05-detection-engineering.md) | Detection methodology and Rule `100002`'s current validation status |
| [`docs/06-incident-response.md`](docs/06-incident-response.md) | Incident response methodology and CASE-001 status |
| [`docs/07-testing-and-metrics.md`](docs/07-testing-and-metrics.md) | Testing/validation methodology and metrics framework |
| [`evidence/v0.1/`](evidence/v0.1/) • [`v0.2/`](evidence/v0.2/) • [`v0.3/`](evidence/v0.3/) | Screenshots and artifacts for each milestone above. Evidence for the newly reported creation and deletion results is not yet confirmed to be filed here and still needs to be reviewed and added |
| [`detections/readme.md`](detections/readme.md) • [`investigations/readme.md`](investigations/readme.md) | How detections and investigations are organized |
| [`investigations/CASE-001.md`](investigations/CASE-001.md) | The current SOC investigation case record |
| [`SECURITY.md`](SECURITY.md) | Safe-testing boundaries |
| [`CHANGELOG.md`](CHANGELOG.md) | Version history |

---

## Security & Safety

SENTINEL is an authorized, isolated lab. All testing stays inside SENTINEL-LAB; no real credentials, no production targets, no external attacks, no VM disks or secrets committed. Full policy in [`SECURITY.md`](SECURITY.md).

---

SENTINEL — a detection is only "working" once it's been tested and the result holds up.
