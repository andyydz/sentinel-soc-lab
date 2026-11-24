# SENTINEL Threat Model

> What can go wrong in this lab, which of it can SENTINEL see, and where is it blind?

This document is a threat model for the SENTINEL SOC Lab, an educational detection and investigation lab. It identifies the assets, trust boundaries, threat actors, and attack paths that matter to the lab, and records honestly which threats are covered by configured controls, which have been exercised in controlled tests, and which remain unvalidated.

SENTINEL is not a production security platform. Nothing here claims comprehensive protection, measured enterprise-grade detection performance, or production readiness. A threat scenario in this document is a hypothesis about what could happen, not a confirmed incident.

---

## 1. Purpose and Scope

### 1.1 Purpose

The threat model exists to keep detection engineering and investigation work grounded in specific threats. For each scenario it asks: what is being attacked, how, what telemetry would show it, which rule or control (if any) responds, and what has actually been validated.

### 1.2 What SENTINEL is intended to monitor and detect

- File changes (creation, modification, deletion) under `/home` on the Linux endpoint, through Wazuh File Integrity Monitoring (FIM).
- SSH password-guessing activity directed at the Linux endpoint.
- Suspicious Windows process activity represented by **replayed** Sysmon telemetry (EVTX and JSON).
- Alert quality: whether alerts remain interpretable, or are buried by benign activity.

### 1.3 In scope

| Area | Detail |
|---|---|
| Lab network | `10.10.10.0/24`, internal and isolated, in VirtualBox |
| SENTINEL-WAZUH | Wazuh Manager, Ubuntu 24.04, Wazuh 4.14.8, `10.10.10.10` |
| SENTINEL-LINUX01 | Monitored endpoint, Ubuntu 24.04.5, Wazuh Agent 4.14.8, Agent ID `002`, `10.10.10.40` |
| SENTINEL-KALI | Controlled attack simulation, `10.10.10.20` |
| Telemetry | FIM/Syscheck events, SSH authentication events, replayed Sysmon EVTX/JSON data |
| Detection logic | Custom Rules `100002`, `100003`, `100004` (FIM) and `100200`, `100201` (SSH), plus the built-in Wazuh rules they depend on |
| Analysis tooling | Manual investigation; the separate `python-soc-automation` companion project for file-based, severity-based triage of Wazuh alert JSON |

### 1.4 Explicitly out of scope (current)

- Any live Windows endpoint or Active Directory environment. None is deployed.
- Production systems, real user data, or internet-facing services.
- Automated containment, eradication, or recovery. None is implemented.
- Network-level detection, and telemetry types not listed in Section 1.3 (for example live process-execution telemetry on the Linux endpoint).
- Physical security, the VirtualBox host's own security, and supply-chain threats to Wazuh or the guest operating systems.
- Comprehensive threat coverage. The scenarios in Section 5 are a selected set, not an exhaustive catalogue.

---

## 2. System Overview and Assets

The detection path is: activity on SENTINEL-LINUX01 (file changes, SSH authentication events) is collected by the Wazuh Agent and forwarded to the Wazuh Manager, where rules evaluate it and produce alerts. Kali-generated SSH traffic reaches SENTINEL-LINUX01 over the internal network. Replayed Windows telemetry enters the detection workflow through replay procedures rather than from a live endpoint. Wazuh alert JSON can then be exported and processed by `python-soc-automation`. Architecture detail is in [03-architecture.md](03-architecture.md).

````mermaid
flowchart LR
    K[SENTINEL-KALI<br/>10.10.10.20] -- controlled SSH simulation --> L[SENTINEL-LINUX01<br/>10.10.10.40<br/>Agent 002]
    L -- agent telemetry --> W[SENTINEL-WAZUH<br/>10.10.10.10]
    R[Replayed Sysmon<br/>EVTX / JSON] -.-> W
    W -- exported alert JSON --> P[python-soc-automation<br/>file-based triage]
````

### 2.1 Assets

| Asset | Why it matters to the lab |
|---|---|
| Wazuh Manager (SENTINEL-WAZUH) | Holds the rules, receives agent data, and produces every alert. Compromise or misconfiguration undermines all detection |
| Wazuh Agent and its configuration on Linux01 | Defines what is collected (including the `/home` FIM scope and any exclusions) and how it is forwarded |
| Linux endpoint and `/home` contents | The monitored target for FIM and SSH scenarios |
| SSH service on Linux01 | The entry point exercised by the password-guessing simulation |
| Custom rule definitions | Rules `100002`–`100004`, `100200`, `100201`. Errors or silent changes alter what is detected |
| Alert records and evidence | The basis for investigations. Integrity and provenance matter; see [06-incident-response.md](06-incident-response.md) |
| Replayed telemetry datasets | Inputs for Windows detection testing. They stand in for an endpoint that does not exist |
| Triage tool output | Prioritisation aids. They influence analyst attention but do not act on alerts |

---

## 3. Trust Boundaries

| Boundary | Crossing | Threat relevance |
|---|---|---|
| Lab network edge | Between the isolated `10.10.10.0/24` network and everything else | The lab's main containment assumption. It is an architectural property and is not independently tested in this document |
| Attacker simulation → endpoint | Kali (`10.10.10.20`) to Linux01 over SSH | Models an untrusted source reaching an exposed service |
| User space → monitoring on Linux01 | Whoever can change files under `/home`, or alter agent configuration | Determines whether the monitored party can also blind the monitor |
| Agent → Manager | Telemetry from Linux01 to `10.10.10.10` | Integrity and availability of the telemetry path |
| Replay data → detection pipeline | Recorded Windows telemetry supplied to the Manager-side workflow | Replay is trusted input. It shows what rules do with known data, not what a live endpoint would send |
| Manager → analysis tooling | Exported alert JSON read by `python-soc-automation` | File-based hand-off. Tool output is advisory |
| Hypervisor → guests | VirtualBox host and the three VMs | Assumed trusted and out of scope (Section 7) |

---

## 4. Threat Actors and Capabilities

These are modelled actors, not observed adversaries. All activity to date has been controlled lab activity.

| Actor | Assumed capability | Used in |
|---|---|---|
| **External network attacker** (simulated by Kali) | Network reachability to Linux01's SSH service; can attempt repeated password guesses. No credentials assumed | SSH scenarios |
| **Local user or insider with write access under `/home`** | Can create, change, and delete files in the monitored scope; no assumption of root | FIM scenarios |
| **Post-compromise adversary on Linux01** | Hypothetically holds enough privilege to affect the agent or its configuration. **Not simulated** | Monitoring-tamper scenarios |
| **Adversary with a foothold on the lab network** | Hypothetically able to reach the Manager or observe agent traffic. **Not simulated** | Manager and communication-path scenarios |
| **Replay-represented Windows adversary** | Behaviour captured in recorded Sysmon data. No live endpoint exists | Windows scenarios |
| **Benign activity as a "threat" to signal quality** | Desktop and configuration-file writes generating FIM events | Alert-quality scenario |

---

## 5. Threat Scenarios and Attack Paths

### 5.1 How to read the table

**Validation status** describes what has actually happened, not what is believed:

| Status | Meaning |
|---|---|
| **Demonstrated** | Reproduced in a controlled test with the expected detection observed |
| **Partially tested** | Some controlled tests exist, with limits stated in the row |
| **Replay-only** | Exercised only using replayed telemetry, not a live endpoint |
| **Planned** | Intended future work. Nothing has been exercised |
| **Unvalidated** | A credible threat for which no test has been run |

**Residual risk** is a qualitative judgment, not a measured or scored value. It reflects how much of the scenario's attack surface lacks tested detection or control: **Low** means the scenario is well covered and tested for the lab's purposes, **Medium** means partial coverage or testing, **High** means little or no tested coverage. It does not estimate likelihood or business impact, and it has not been derived from any quantitative method.

### 5.2 Scenario table

| ID | Threat / scenario | Target asset | Attack path or technique | Potential impact | Existing detection or control | Validation status | Residual risk |
|---|---|---|---|---|---|---|---|
| S1 | SSH password guessing | SSH service on Linux01 | Repeated failed authentication attempts from one source (simulated from Kali) | Credential compromise and unauthorised access | Rule `100200` (Level 5) for matching SSH authentication events; Rule `100201` (Level 10) escalates on matching `100200` events from the same source IP within its configured frequency window. Containment is a manual, source-scoped procedure that is documented only | **Demonstrated** (controlled simulation, CASE-003: 21 failed attempts, zero successful logins confirmed manually). One simulation; legitimate authentication activity and other attack patterns not tested | Medium |
| S2 | Unexpected file modification under `/home` | Files in the FIM scope | Edit or overwrite a monitored file | Tampering with configuration, scripts, or user data without notice | Real-time FIM; Rule `100002` (Level 8) | **Partially tested** (controlled modification tests on 11 and 26 October; later controlled probes). Not comprehensive FIM coverage and not a regression suite | Medium |
| S3 | Unexpected file creation under `/home` | Monitored directories | Drop a new file (for example a payload or persistence artifact) | Introduction of malicious or unauthorised content | Rule `100003`; built-in Rule 554 is the underlying "file added" event | **Partially tested** (controlled probe events). The 16 October creation record showed Rule 554 with Rule `100002` absent; the reason is unresolved | Medium |
| S4 | Unexpected file deletion under `/home` | Monitored files | Remove a file (data destruction, evidence removal) | Loss of data or trace evidence | Rule `100004`; built-in Rule 553 is the underlying "file deleted" event | **Partially tested** (controlled probe events). The 16 October deletion record showed Rule 553 with Rule `100002` absent; the reason is unresolved | Medium |
| S5 | Activity outside the FIM scope or inside suppressed paths | Files and directories not under `/home`, or excluded within it | Place or change files where FIM is not watching, or where exclusions suppress events | Undetected changes. Exclusions added to reduce noise could also hide hostile activity | Configured `/home` scope and exclusions only. No coverage outside them | **Unvalidated** | High |
| S6 | Attempt to alter or evade endpoint monitoring | Wazuh Agent and its configuration on Linux01 | Stop or disable the agent, edit its configuration, change FIM settings, or modify the local rule environment | Loss of telemetry and a blind monitored host | No tamper-specific rule or control is documented. Agent disconnection handling has not been tested as a detection | **Unvalidated** | High |
| S7 | Suspicious Windows activity | Windows endpoints (none deployed) | Process and behaviour patterns captured in Sysmon data (EVTX and JSON) | Would depend on a real environment; here, only detection-logic testing is possible | Detection rules exercised against replayed data (CASE-002; JSON replay and Python triage integration in later work) | **Replay-only.** No live Windows endpoint or Active Directory; replay does not show how a live endpoint would behave | High (for any live Windows use) |
| S8 | Alert overload or benign activity degrading FIM signal | Analyst attention, FIM alert quality | Benign desktop and configuration-file writes generating many FIM events that obscure real ones | Missed or delayed recognition of real events | FIM exclusions and rule group isolation (v0.8); noise-filtering observations (CASE-004); severity-based triage | **Partially tested.** Residual noise remains and broader retesting is outstanding. In the v0.11 evidence, seven desktop/configuration-path records have **not** been conclusively established as benign, and the on-disk XML does not establish which configuration the running Manager had loaded at the time | High |
| S9 | Compromise or misuse of the Wazuh Manager | SENTINEL-WAZUH | Exploit or abuse the Manager from a foothold on the lab network, or modify rules and configuration | Silent suppression, alteration, or fabrication of alerts | Network isolation (architectural). No Manager-specific hardening or integrity monitoring is documented here | **Unvalidated** | High |
| S10 | Interception or tampering on the agent–manager path | Agent communication to `10.10.10.10` | Observe, disrupt, or inject on the internal network | Loss or falsification of telemetry | Wazuh's own agent–manager communication. Its protections have not been assessed or tested in this lab | **Unvalidated** | High |
| S11 | Misleading or incomplete triage output | Analyst prioritisation | Missing enrichment or mis-prioritisation by `python-soc-automation` leading to misjudged alerts | Real events deprioritised | Manual review of triage output. Severity-based, file-based triage only; in the v0.11 evidence, process, target-process, and event-time enrichment fields are `None` | **Partially tested** (file-based use on SSH and FIM alert JSON). Tool's own tests are not SENTINEL detection validation | Medium |

Scenarios S5, S6, S9, and S10 are credible threats for which this document records a gap, not a tested control. No scenario here has been shown to be detected in a real incident, because no real incident has occurred.

---

## 6. Existing Security Controls and Detection Coverage

Controls are separated by what has actually been done with them.

| Control / capability | Configured | Exercised in controlled tests | Documented, not exercised | Planned or absent |
|---|---|---|---|---|
| Isolated internal network `10.10.10.0/24` | ✔ (architectural) | Not independently tested | | |
| Real-time FIM on `/home` | ✔ | ✔ (limited controlled tests) | | Complete coverage of relevant paths: **not established** |
| Custom Rules `100002`, `100003`, `100004` | ✔ | ✔ (controlled probes; not a regression suite) | | Verification of the Manager's currently loaded configuration and historical loaded configuration |
| SSH Rules `100200`, `100201` | ✔ | ✔ (one controlled simulation) | | Testing against legitimate authentication and other attack patterns |
| Sysmon rules via replay | ✔ (for replayed data) | ✔ (replay only) | | Live Windows validation |
| Python-assisted triage (file-based, separate project) | n/a (not a Wazuh component) | ✔ (on exported alert JSON) | | Not a SOAR platform; does not respond to alerts |
| Source-scoped SSH containment procedure | | | ✔ (manual) | Not applied as an exercise; no automation |
| Eradication and recovery procedures | | | ✔ | Not exercised |
| Automated containment, eradication, or recovery | | | | Absent |
| Tamper detection for agent and Manager | | | | Absent / unvalidated |
| Live Windows endpoint and Active Directory | | | | Absent |
| Response-time metrics | | | | Not measured |

### 6.1 Coverage caveats

- FIM monitoring of `/home` does not establish complete monitoring of every relevant file change. A configured scope does not guarantee detection of every change under it.
- The v0.11 evidence is still undergoing reconciliation. Its seven desktop/configuration-path records are not established as benign, and are not treated as confirmed noise.
- The on-disk rule or configuration XML does not establish which configuration the running Wazuh Manager had loaded during historical events.
- Rule `100201` counts matching Rule `100200` events from the same source IP within its configured frequency window. It is not described as necessarily counting unique failed-password attempts.
- Controlled test results are validation exercises. They are not evidence of performance against real adversaries and no detection-performance figures are claimed.

Detection methodology and rule status are in [05-detection-engineering.md](05-detection-engineering.md); investigation and response status is in [06-incident-response.md](06-incident-response.md).

---

## 7. Assumptions and Dependencies

- The lab network is isolated, so Kali-originated activity cannot reach anything outside `10.10.10.0/24`. This is assumed from the architecture, not re-verified here.
- The VirtualBox host and hypervisor are trusted and are not modelled as a threat.
- All attacker activity is controlled and performed by the lab owner. No unknown third party is assumed to be present.
- Detection depends on the Wazuh Agent running, forwarding, and configured as expected, and on the Manager loading the intended rules. Neither is continuously verified.
- Replayed Windows data is assumed representative of the behaviour being tested. That assumption is not validated against a live endpoint.
- Triage depends on the separate `python-soc-automation` project and on exported alert JSON being complete and unmodified.
- A Wazuh Manager startup timeout has been reported as an operational observation, not a security incident. Its root cause is unconfirmed. It is noted because Manager availability is a dependency for all detection.

---

## 8. Limitations and Residual Risks

- **Narrow telemetry.** Only FIM, SSH authentication, and replayed Sysmon data are in scope. Live process execution, network, and Windows telemetry are absent.
- **Single-environment testing.** Tests used one Linux endpoint and one attack-simulation host, with small samples. Results do not generalise.
- **Detection against evasion is unproven.** Monitoring-tamper and out-of-scope-path scenarios (S5, S6) have no tested coverage.
- **Signal quality is unresolved.** FIM noise and the unestablished status of seven v0.11 records mean false-positive and false-negative rates are unknown.
- **Replay is not live.** Windows detection has not faced a live endpoint or Active Directory.
- **Configuration provenance is uncertain.** The historical loaded rule configuration may not be recoverable, so some past events cannot be explained with certainty.
- **No automated response.** Any containment, eradication, or recovery depends on manual action, and no response-time metrics exist.
- **No production claims.** SENTINEL is an educational lab and its results should not be read as evidence of production readiness or comprehensive protection.

---

## 9. Future Security Improvements

The following are planned or desirable and are **not implemented or not yet exercised**:

- Reconcile the v0.11 evidence, including the seven desktop/configuration-path records.
- Verify the Manager's current active rule configuration, and reconstruct historical loaded configuration where evidence permits.
- Broaden FIM noise-suppression retesting, and build a repeatable regression suite.
- Test SSH detection against legitimate authentication activity and further attack variations.
- Design and run tests for monitoring-tamper and out-of-scope-path scenarios (S5, S6).
- Assess the Manager and agent communication path (S9, S10).
- Extend Sysmon replay mutation testing and, eventually, validate against a live Windows endpoint.
- Run a controlled containment exercise, then eradication and recovery validation.
- Measure response times.
- Consider response automation only with human approval at each destructive or disruptive step.

---

## 10. Related Documents

| Document | Role |
|---|---|
| [01-project-overview.md](01-project-overview.md) | Project goals and scope |
| [02-requirements.md](02-requirements.md) | Requirements the lab is built to meet |
| [03-architecture.md](03-architecture.md) | Environment and component architecture |
| [05-detection-engineering.md](05-detection-engineering.md) | Detection methodology and current rule status |
| [06-incident-response.md](06-incident-response.md) | Investigation and response methodology and status |
| [07-testing-and-metrics.md](07-testing-and-metrics.md) | How results are tested and measured |
| [CASE-001](../investigations/CASE-001.md) | Controlled FIM investigation |
| [CASE-002](../investigations/CASE-002.md) | Windows Sysmon EVTX replay case |
| [CASE-003](../investigations/CASE-003.md) | SSH password-guessing case |
| [CASE-004](../investigations/CASE-004.md) | Attack mutation and noise-filtering case |
