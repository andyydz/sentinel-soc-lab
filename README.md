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
| SENTINEL-KALI (`10.10.10.20`) | Kali Linux 2026.2 — intended for controlled adversary emulation. No Kali-driven attack is documented as executed yet. |
| SENTINEL-LINUX01 (`10.10.10.40`, Agent ID `002`) | Ubuntu 24.04.5 LTS, Wazuh Agent 4.14.8 — monitored endpoint with real-time File Integrity Monitoring (FIM) on `/home`. |
| SENTINEL-LAB (`10.10.10.0/24`) | Isolated internal network; NAT provides outbound access. |

> An earlier Windows endpoint (SENTINEL-WIN01) was dropped after repeated boot/deployment failures. There is no Windows, Sysmon, or Active Directory endpoint in the current lab; that is future work.

---

## Current Status

**v0.1 — Foundation: complete.** Wazuh deployed, Kali and Linux01 deployed, isolated network established, agent enrolled and communicating.

**v0.2 — Telemetry & Initial Detection Engineering: in progress.** v0.2 remains in progress. The original infrastructure and initial FIM setup are documented, and custom Rule `100002` has fired in the controlled modification scenarios tested. Creation/deletion coverage and repeatable regression testing remain unresolved.

Key findings (October 2026):
- **Modification:** Rule `100002` (Level 8) fired on controlled modifications on 11 Oct (supported by screenshots; the original source log was not recovered) and 26 Oct (two alerts from consecutive modifications of one file, not two independent test cases).
- **Creation and deletion (16 Oct):** the reviewed records showed built-in Rules `554` and `553`, and Rule `100002` was absent. The reason is unresolved. No root cause is claimed, and this is not labeled a confirmed detection failure.
- **Custom creation/deletion rules (31 Oct, observation only):** custom Rule `100003` (creation, Level 8) and custom Rule `100004` (deletion, Level 8) appeared in one terminal screenshot: [`evidence/v0.3/screenshots/v0.3-fim-lifecycle-custom-detections.png`](evidence/v0.3/screenshots/v0.3-fim-lifecycle-custom-detections.png). These are observations, not validated controlled tests. Raw alert records, process attribution, and root cause are not established. This is separate from the 16 Oct built-in Rule `554`/`553` records and from the 11/26 Oct Rule `100002` modification results, and it does not explain the Rule `100002` absence above.

These results do not establish complete FIM coverage, measured detection rates, or malicious activity. Details: [Rule 100002 investigation](investigations/fim-rule-100002-investigation.md).

**SCA observation (29 Oct 2026).** The [SCA baseline report](evidence/v0.2/sca-baseline.md) records a single Wazuh dashboard observation using built-in Wazuh functionality. It is not a custom SENTINEL detection, a remediation exercise, proof of compliance or improved posture, or a detection-engineering milestone.

**v0.3 — SOC Investigation: in progress.** CASE-001 evidence reconciliation for the reviewed scope is closed. The case itself and the broader investigation remain open, with no root cause, attribution, or malicious activity established and no containment, eradication, or recovery exercised. See [CASE-001](investigations/CASE-001.md).

---

## Roadmap

| Version | Focus | Status |
|---|---|---|
| v0.1 | Foundation — infrastructure, network, Wazuh deployment | Complete |
| v0.2 | Telemetry and detection engineering — FIM and custom Rule `100002` | In progress |
| v0.3 | SOC investigation — CASE-001 and FIM investigation | In progress |
| v0.4 | Incident response | Planned |
| v0.5 | Purple-team measurement | Planned |
| v0.6 | Attack DNA and mutation testing | Planned |
| Future | Custom SENTINEL console over Wazuh; Windows/AD endpoint | Planned |

Not yet in place: a repeatable regression suite, false-positive/false-negative analysis, measured detection rates, broader telemetry (auth, process execution), project-level MITRE ATT&CK mapping, and everything in v0.4 and later.

---

## Documentation & Evidence

| Area | Links |
|---|---|
| **Methodology** | [Detection engineering](docs/05-detection-engineering.md) · [Incident response](docs/06-incident-response.md) · [Testing and metrics](docs/07-testing-and-metrics.md) |
| **Investigations** | [CASE-001](investigations/CASE-001.md) · [Rule 100002 investigation](investigations/fim-rule-100002-investigation.md) · [Investigations guide](investigations/readme.md) |
| **Detections** | [Detections guide](detections/readme.md) |
| **Evidence** | [Evidence guide](evidence/readme.md) · [v0.1](evidence/v0.1/) · [v0.2 index](evidence/v0.2/readme.md) · [v0.3 index](evidence/v0.3/readme.md) |
| **v0.2 reports** | [Infrastructure and telemetry foundation](evidence/v0.2/infrastructure-and-telemetry-foundation.md) · [Wazuh–Linux01 integration](evidence/v0.2/wazuh-linux01-integration.md) · [SCA baseline](evidence/v0.2/sca-baseline.md) |
| **Project** | [Security policy](SECURITY.md) · [Changelog](CHANGELOG.md) |

Not every source record is committed. The reviewed 16 October alert records came from the Wazuh runtime log, and the repository does not claim to contain an exported copy.

---

## Security & Safety

SENTINEL is an authorized, isolated lab. All testing stays inside SENTINEL-LAB: no real credentials, no production targets, no external attacks, and no VM disks or secrets committed. Full policy in [`SECURITY.md`](SECURITY.md).
