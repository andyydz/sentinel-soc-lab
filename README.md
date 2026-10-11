## SENTINEL — SOC Lab

> Does your detection still work when the attacker changes tactics?

SENTINEL is a controlled virtual SOC lab (VirtualBox + Wazuh + Kali + an Ubuntu endpoint) built to practice and evidence a full defensive engineering workflow — not just install security tools.

## Objective

SIMULATE → DETECT → INVESTIGATE → RESPOND → MEASURE → IMPROVE → RETEST

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

Host	Role	
SENTINEL-WAZUH (`10.10.10.10`)	Ubuntu 24.04, Wazuh 4.14.8 — SOC/monitoring platform, dashboard operational.	
SENTINEL-KALI (`10.10.10.20`)	Kali Linux — controlled attacker/adversary-emulation VM.	
SENTINEL-LINUX01 (`10.10.10.40`)	Ubuntu 24.04, Wazuh Agent 4.14.8 — monitored endpoint; real-time File Integrity Monitoring (FIM) configured on `/home`.	
SENTINEL-LAB (`10.10.10.0/24`)	Isolated internal network; NAT used only for legitimate package/update traffic.	

>  An earlier Windows endpoint (SENTINEL-WIN01) was dropped after repeated boot/deployment failures. Windows/AD is now future work, not a blocking dependency.

---

## Current Status

## v0.1 — Foundation (complete)
Wazuh deployed and operational, Kali and Linux01 deployed, isolated lab network established, Wazuh agent enrolled and communicating with the manager.

## v0.2 — Telemetry & Initial Detection Engineering (in progress)
Real-time FIM configured on `/home`; controlled file creation/modification tests performed; real FIM telemetry observed, including built-in Wazuh Rule 550 (Level 7, "Integrity checksum changed"). A custom rule, Rule 100002, was written and passed Wazuh's configuration syntax check — its end-to-end validation (a confirmed Level 8 alert) is not yet established. Rule 550 firing confirms the telemetry pipeline works; it does not confirm the custom rule does.

## v0.3 — SOC Investigation (started)
Investigation CASE-001 is underway. FIM events have been filtered and reviewed, including the Rule 550 event details, as a first investigation exercise. Timeline, root cause, attribution, and final conclusions are not yet complete.

>  Not yet in place: a validated custom detection, broader telemetry (auth, process execution), MITRE ATT&CK mapping, a completed investigation, incident response, performance metrics, purple-team validation, attack mutation, or a custom console.

---

## Roadmap

Version	Focus	Status	
v0.1	Foundation — infrastructure, network, Wazuh	 Complete	
v0.2	Telemetry & detection engineering (FIM, Rule 100002)	 In progress	
v0.3	SOC investigation (CASE-001)	 In progress	
v0.4	Incident response	 Planned	
v0.5	Purple-team measurement	 Planned	
v0.6	Attack DNA & mutation testing	 Planned	
Future	Custom SENTINEL console (visualization layer over Wazuh)	 Not started	

---

## What Makes It Valuable

SENTINEL isn't judged by tool count — it's judged by whether each claim is backed by evidence. A detection is "working" only once it's been tested and the result documented, including when it fails: Rule 100002's unresolved status is treated as useful data, not something to hide.

The project's differentiator is the full loop — simulate, detect, investigate, measure, improve, retest — not any single component in it.

---

## Documentation & Evidence

Resource	Covers	
[`docs/05-detection-engineering.md`](docs/05-detection-engineering.md)	Detection methodology and Rule 100002's current status	

[`docs/06-incident-response.md`](docs/06-incident-response.md)	Incident response methodology (not yet executed)	

[`docs/07-testing-and-matrices.md`](docs/07-testing-and-matrices.md)	Testing/validation methodology	

[`evidence/v0.1/`](evidence/v0.1/) • [`v0.2/`](evidence/v0.2/) • [`v0.3/`](evidence/v0.3/)	Screenshots and artifacts backing each milestone above	

[`detections/README.md`](detections/README.md) • [`investigations/README.md`](investigations/README.md)	How detections and investigations are organized	

[`SECURITY.md`](SECURITY.md)	Safe-testing boundaries	

[`CHANGELOG.md`](CHANGELOG.md)	Version history	

---

## Security & Safety

SENTINEL is an authorized, isolated lab. All testing stays inside SENTINEL-LAB; no real credentials, no production targets, no external attacks, no VM disks or secrets committed. Full policy in [`SECURITY.md`](SECURITY.md).

---

SENTINEL — a detection is only "working" once it's been tested and the result holds up.
