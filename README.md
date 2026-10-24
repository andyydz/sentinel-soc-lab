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
Real-time File Integrity Monitoring (FIM) is configured on `/home`, and initial detection engineering is established. Controlled modification detection is confirmed. The 16 October creation and deletion screenshots have been reviewed; the source alert JSON for them has not been confirmed as located or reviewed. Each result is limited to its own test or record:

| Scenario | Test file | Result | Status |
|---|---|---|---|
| Modification | `/home/sentinel-admin/sentinel-fim-validation.txt` | Custom Rule `100002` fired at Level 8 (`2026-10-11T20:25:14.746+0530`); built-in Rule 550 (Level 7, "Integrity checksum changed") also observed. | **Confirmed** — controlled test, 11 October 2026 |
| Creation | `/home/sentinel-admin/sentinel-audit-test.txt` | Built-in Rule `554` ("File added to the system") observed; custom Rule `100002` absent from the reviewed screenshot. Timestamp unresolved: `2026-10-16T11:40:06.007+0530` (screenshot) vs `2026-10-16T11:40:06.087+0530` (evidence README). | **Reviewed screenshot** — built-in Rule 554 observed; custom Rule 100002 absent |
| Deletion | `/home/sentinel-admin/sentinel-audit-test.txt` | Built-in Rule `553` ("File deleted") observed at `2026-10-16T12:31:32.819+0530`; custom Rule `100002` absent from the reviewed screenshot. | **Reviewed screenshot** — built-in Rule 553 observed; custom Rule 100002 absent |

The creation and deletion records are **not** custom-rule validations. An earlier claim that Rules 554 and 100002 fired together on creation is unsupported by the reviewed screenshot and remains unexplained. For deletion, the absence of `100002` is an unresolved coverage question, not a confirmed detection miss or a root cause. The creation screenshot's filename contains `creation-rule-553` although its content shows Rule 554, and the evidence README references `creation-rule-664`; both discrepancies remain unresolved.

**Rule `100002` and its parent dependency.** A read-only check of the on-disk `/var/ossec/etc/rules/local_rules.xml` on SENTINEL-WAZUH showed Rule `100002` at Level 8, group `sentinel_fim`, with parent `<if_sid>550</if_sid>` and a `file` field condition of `/home/`. This shows the on-disk definition at inspection time, not which version the manager had loaded during the earlier tests. The reviewed creation and deletion records show built-in Rules 554 and 553 and do not show Rule 550 as the matching parent rule; this is consistent with `100002` being absent but does not explain the earlier creation claim. The matching semantics of `/home/` remain unverified, and the rule has not been changed. Details: [`investigations/CASE-001.md`](investigations/CASE-001.md) and [`docs/05-detection-engineering.md`](docs/05-detection-engineering.md).

Still outstanding, as separate items:
- Locating and reviewing the source alert JSON for the 16 October records, and settling the creation timestamp.
- Reconciling the creation screenshot filename and evidence README references (separately approved documentation pass).
- Confirming which rule version the running manager had loaded, if historical evidence permits, and verifying the `/home/` matching behavior.
- Running a repeatable creation/modification/deletion regression test (not yet done).
- Broader false-positive/false-negative analysis (not yet done).
- Review of background FIM activity and detection-rule tuning (not yet done).

The confirmed modification result is scoped to a single controlled test; it does not establish complete FIM coverage, measured detection rates, or malicious activity. Any ATT&CK mappings shown on built-in events are telemetry metadata, not evidence of intent.

**v0.3 — SOC Investigation (in progress)**
Investigation `CASE-001` (`investigations/CASE-001.md`) is underway, with a related write-up in `investigations/fim-rule-100002-investigation.md`. FIM events have been filtered and reviewed, including the Rule 550 and Rule 100002 event details and the 16 October creation (Rule 554) and deletion (Rule 553) screenshots. **CASE-001's controlled modification-validation objective is closed; the overall investigation remains open.** Final v0.3 closeout is still pending (evidence reconciliation, link checks, document reconciliation, repository review, and the broader investigation). No attribution, malicious intent, or comprehensive root cause has been established.

> Not yet in place: custom-rule validation for creation and deletion, complete FIM coverage, broader telemetry (auth, process execution), project-level MITRE ATT&CK mapping, a completed investigation, incident response, performance metrics, purple-team validation, attack mutation, or a custom console.

---

## Roadmap

| Version | Focus | Status |
|---|---|---|
| v0.1 | Foundation — infrastructure, network, and Wazuh deployment | Complete |
| v0.2 | Telemetry and detection engineering — FIM and custom Rule `100002` | In progress — controlled modification detection confirmed; reviewed creation/deletion screenshots show built-in Rules 554/553 with `100002` absent (not custom-rule validations); open items listed under Current Status |
| v0.3 | SOC investigation — CASE-001 and evidence-backed FIM investigation | In progress — CASE-001's controlled modification-validation objective is closed; the overall investigation remains open and v0.3 closeout is pending |
| v0.4 | Incident response | Planned — not started until v0.3 is properly closed |
| v0.5 | Purple-team measurement | Planned |
| v0.6 | Attack DNA and mutation testing | Planned |
| Future | Custom SENTINEL console — visualization layer over Wazuh | Planned |

---

## What Makes It Valuable

SENTINEL isn't judged by tool count — it's judged by whether each claim is backed by evidence. A detection is "working" only once it's been tested and the result documented. Rule `100002`'s Level 8 alert is confirmed for one controlled modification test and is not presented as complete FIM coverage; the creation and deletion results are not presented as custom-rule validations. Open questions are tracked rather than hidden — see Current Status and [`investigations/CASE-001.md`](investigations/CASE-001.md).

The project's differentiator is the full loop — simulate, detect, investigate, measure, improve, retest — not any single component in it.

---

## Documentation & Evidence

| Resource | Covers |
|---|---|
| [`docs/05-detection-engineering.md`](docs/05-detection-engineering.md) | Detection methodology and Rule `100002`'s current validation status |
| [`docs/06-incident-response.md`](docs/06-incident-response.md) | Incident response methodology and CASE-001 status |
| [`docs/07-testing-and-metrics.md`](docs/07-testing-and-metrics.md) | Testing/validation methodology and metrics framework |
| [`evidence/v0.1/`](evidence/v0.1/) • [`v0.2/`](evidence/v0.2/) • [`v0.3/`](evidence/v0.3/) | Screenshots and artifacts for each milestone above. The 16 October screenshots are referenced in `evidence/v0.3/readme.md`; source alert JSON and filename/timestamp discrepancies are outstanding (see Current Status) |
| [`detections/readme.md`](detections/readme.md) • [`investigations/readme.md`](investigations/readme.md) | How detections and investigations are organized |
| [`investigations/CASE-001.md`](investigations/CASE-001.md) | The current SOC investigation case record |
| [`investigations/fim-rule-100002-investigation.md`](investigations/fim-rule-100002-investigation.md) | Investigation notes on Rule `100002` |
| [`SECURITY.md`](SECURITY.md) | Safe-testing boundaries |
| [`CHANGELOG.md`](CHANGELOG.md) | Version history |

---

## Security & Safety

SENTINEL is an authorized, isolated lab. All testing stays inside SENTINEL-LAB; no real credentials, no production targets, no external attacks, no VM disks or secrets committed. Full policy in [`SECURITY.md`](SECURITY.md).

---

SENTINEL — a detection is only "working" once it's been tested and the result holds up.
