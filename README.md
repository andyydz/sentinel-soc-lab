# SENTINEL — SOC Lab

> **Does your detection still work when the attacker changes tactics?**

SENTINEL is a virtual cybersecurity SOC laboratory built inside isolated virtual machines. It simulates controlled attacks, collects security telemetry, engineers detections, investigates incidents, performs controlled response actions, measures defensive performance, improves security controls, and retests them against changed attacker behavior.

In short: **build a simulated company, attack it, detect the activity, investigate what happened, respond to the incident, measure the defense, improve it, and test it again.**

```
SIMULATE → DETECT → INVESTIGATE → RESPOND → MEASURE → IMPROVE → RETEST 
```

SENTINEL is a controlled cybersecurity laboratory designed to demonstrate practical security operations and detection-engineering workflows — not a production SOC or an enterprise security platform.

---

## Why SENTINEL exists 

SENTINEL is deliberately **not** "Kali + Wazuh + a few screenshots." The project exists to demonstrate a complete defensive engineering feedback loop, ultimately answering:

1. Can the activity be simulated safely?
2. Is the activity visible in telemetry?
3. Can it be detected?
4. Can a SOC analyst investigate it?
5. Can the environment respond appropriately?
6. Can performance be measured?
7. Can weaknesses be identified?
8. Can the detection/defense be improved?
9. Does the improved defense still work when the attacker changes behavior?

The underlying engineering loop is:

```
BUILD → UNDERSTAND → TEST → BREAK → FIX → MEASURE → DOCUMENT → EXPLAIN
```

## The core feedback loop

```
        ┌───────────────┐
        │    SIMULATE      │
        └───────┬───────┘
                ↓
        ┌───────────────┐
        │     DETECT       │
        └───────┬───────┘
                ↓
        ┌───────────────┐
        │  INVESTIGATE     │
        └───────┬───────┘
                ↓
        ┌───────────────┐
        │    RESPOND       │
        └───────┬───────┘
                ↓
        ┌───────────────┐
        │    MEASURE       │
        └───────┬───────┘
                ↓
        ┌───────────────┐
        │    IMPROVE       │
        └───────┬───────┘
                ↓
        ┌───────────────┐
        │    RETEST        │
        └───────┬───────┘
                │
                └──────────→ SIMULATE
```

This loop — not the number of tools installed — is the heart of SENTINEL.

---

## Current architecture

```
                    INTERNET
                       |
                      NAT
                       |
              +----------------+
              | SENTINEL-WAZUH |
              | 10.10.10.10    |
              | Wazuh SOC      |
              +----------------+
                       |
                SENTINEL-LAB
                10.10.10.0/24
                       |
              +--------+--------+
              |                 |
       +-------------+   +-------------+
       | SENTINEL-   |   | SENTINEL-   |
       | KALI        |   | LINUX01     |
       | 10.10.10.20 |   | 10.10.10.40 |
       | Attacker    |   | Target      |
       +-------------+   +-------------+
```

### SENTINEL-WAZUH
SOC / monitoring / detection platform.
- Ubuntu 24.04
- Wazuh all-in-one deployment, version 4.14.8
- Wazuh Dashboard operational
- Lab IP: `10.10.10.10`

### SENTINEL-KALI
Controlled attacker / adversary-emulation environment.
- Kali Linux
- Lab IP: `10.10.10.20`

### SENTINEL-LINUX01
Initial monitored endpoint / target.
- Ubuntu 24.04
- Wazuh agent installed, enabled, and actively running (v4.14.8)
- Visible as an active endpoint in the Wazuh Dashboard
- Syscheck (File Integrity Monitoring) configured, monitoring `/home`
- Lab IP: `10.10.10.40`

### SENTINEL-LAB
Isolated internal lab network, `10.10.10.0/24`, connecting all three systems. NAT may exist on individual VMs for legitimate internet access (package installation, system updates) — this does **not** make the lab fully isolated from the internet at the host level, but the security boundary that matters is that controlled attack traffic is intended to stay inside `SENTINEL-LAB`.

### Data flow (long-term architecture)

```
KALI → controlled activity → LINUX01 → endpoint telemetry → WAZUH
  → detection → SOC investigation → response → metrics
  → detection improvement → retest
```

**Currently**, v0.1 established the foundation of this flow — Kali, Linux01, and Wazuh are connected and the Wazuh agent provides the telemetry pipeline. v0.2 built and validated the first detection on top of that pipeline (Syscheck/FIM → custom Rule `100002`). Investigation, response, and measurement stages are not yet built out; they are the focus of v0.3 onward.

### A note on Windows / Active Directory

An earlier version of this project attempted a Windows endpoint (`SENTINEL-WIN01`). Repeated deployment/boot reliability problems made it unsuitable as a dependency for the initial build. Rather than let one unreliable, optional component block the rest of the lab, the architecture was changed: Linux became the initial monitored endpoint, and Windows/Active Directory became a future expansion rather than a core requirement. The exact technical root cause of the Windows VM's issues was not pursued and is not claimed here — it's recorded simply as a deployment/boot reliability issue that led to an architecture decision, which is itself a small example of the project's engineering philosophy in action.

---

## Current status

SENTINEL is currently at **v0.2 — Detection Engineering**.

| Component | Status |
|---|---|
| Wazuh SOC | Completed |
| Kali attacker VM | Completed |
| Linux monitored endpoint | Completed |
| Isolated lab network | Completed |
| Wazuh agent (Linux01) | Completed |
| Initial telemetry pipeline | Completed |
| Detection engineering | Completed (first detection validated) / v0.2 |
| SOC investigation | Next / v0.3 |
| Incident response | Planned / v0.4 |
| Purple-team measurement | Planned / v0.5 |
| Attack DNA | Planned / v0.6 |
| Attack Mutation | Planned / v0.6 |
| Custom SENTINEL Console | Future |

**Verified in v0.1:** Wazuh deployment and dashboard, Kali and Linux01 deployment, the isolated lab network, Wazuh agent enrollment and connectivity (Wazuh↔Linux01, Kali↔Wazuh), the documentation set under `docs/`, the repository structure (`detections/`, `investigations/`, `metrics/`, `scenarios/`, `evidence/`, `failure-log/`), and initial infrastructure evidence (dashboard showing the active endpoint, agent running, v0.1 verification).

**Verified in v0.2:** Wazuh Syscheck (File Integrity Monitoring) configured on SENTINEL-LINUX01, scoped to `/home`; a controlled file-modification test performed against that path; the resulting `syscheck_integrity_changed` telemetry event observed; a custom Wazuh detection rule (Rule ID `100002`) created and validated against that event, producing a Level 8 alert. This is SENTINEL's first end-to-end validated detection: telemetry → rule → alert. Evidence for this work is under `evidence/v0.2/`.

**Not yet in place:** additional detection scenarios beyond File Integrity Monitoring, broader telemetry sources (authentication, process execution, command execution), false-positive/missed-detection analysis beyond this single validated test, MITRE ATT&CK mapping, completed incident investigations, validated response workflows, measured detection rates or other performance metrics, purple-team results, Attack DNA, Attack Mutation, or a custom console. These belong to later roadmap stages.

---

## Roadmap

```
v0.1                v0.2              v0.3                v0.4              v0.5                    v0.6                       FUTURE
FOUNDATION    →    DETECTION    →   INVESTIGATION   →   RESPONSE    →   MEASUREMENT       →   ATTACK DNA + MUTATION   →   SENTINEL CONSOLE
```

**v0.1 — Foundation** *(completed)*
Virtual SOC infrastructure, isolated lab network, Wazuh deployment, Kali attacker environment, Linux monitored endpoint, Wazuh agent, initial telemetry pipeline, evidence and documentation structure, failure tracking.

**v0.2 — Detection Engineering** *(completed)*
Configured Syscheck/FIM telemetry on SENTINEL-LINUX01, built and validated a custom detection rule (Rule `100002`) against a controlled file-modification test, and confirmed the resulting Level 8 alert. Further detection scenarios, broader telemetry sources, false-positive/missed-detection analysis, and MITRE ATT&CK mapping remain open for continued v0.2 work and v0.3.
```
ATTACK → TELEMETRY → DETECTION → TEST → MEASURE → IMPROVE
```

**v0.3 — SOC Investigation** *(next)*
Alert triage, evidence collection, timeline reconstruction, IOC extraction, threat hunting, investigation case records, root-cause analysis, first complete incident case, formal investigation report. Core question: *what happened, how do we know, and what evidence supports the conclusion?*

**v0.4 — Incident Response** *(planned)*
Controlled response actions, containment, recovery, response validation, human-in-the-loop response, response performance measurement. Automated response is not currently implemented and is not assumed by this stage.

**v0.5 — Purple-Team Validation** *(planned)*
Detection coverage, detection rate, detection time, response time, false positives, missed detections, regression testing, before/after comparisons, purple-team feedback loop.
```
ATTACK → DETECT → INVESTIGATE → RESPOND → MEASURE → IMPROVE → RETEST
```

**v0.6 — Attack DNA & Mutation** *(planned)*
One of SENTINEL's key differentiators. **Attack DNA** represents the structure/behavior of an attack chain. **Attack Mutation** changes aspects of attacker behavior while preserving the underlying objective, to test whether a detection still catches it.
```
ORIGINAL ATTACK → DETECTION → MODIFY BEHAVIOR → MUTATED ATTACK → DETECTION
  → COMPARE RESULTS → IMPROVE DETECTION → RETEST
```
Possible future measurements include original vs. mutated detection results, detection degradation, and retest outcomes. None of this is currently implemented.

**Future — SENTINEL Console**
A future custom console, sitting **on top of** Wazuh (not replacing it), potentially covering incident dashboards, detection timelines, ATT&CK visualization, IOC tracking, investigation cases, coverage/metrics, Attack DNA and mutation visualization, response status, and reports. Possible technology directions include Python/FastAPI, Streamlit for prototyping, and React for a later interface — none of this has been finalized or implemented. The intended project balance is roughly 70–80% security engineering and 20–30% custom presentation/engineering; the console is not meant to replace the core SOC work.

---

## What makes SENTINEL different

SENTINEL isn't defined by the number of tools it uses — it's defined by the validation process built around them: detection validation, failure-driven improvement, measurement, investigation, retesting, detection resilience, and attack mutation. The central differentiator is the loop itself:

```
ATTACK → DETECT → INVESTIGATE → MEASURE → BREAK → IMPROVE → RETEST
```

## Signature capabilities

| Capability | What it means |
|---|---|
| Adversary Simulation | Controlled attacks executed inside the isolated lab |
| Detection Engineering | Building and validating detections against real telemetry |
| SOC Investigation | Turning alerts into structured, evidence-backed investigations |
| Incident Response | Practicing controlled, deliberate response workflows |
| Purple-Team Measurement | Measuring whether defensive controls actually work |
| Attack DNA | Representing the structure of an attack chain |
| Attack Mutation | Changing attacker behavior to test whether detection survives |
| Detection Resilience | Understanding *why* a detection fails and improving it |

Not all of these are implemented yet — see [Current status](#current-status) and the [Roadmap](#roadmap) above for what's real today versus planned.

## Controlled security scenarios

Scenarios are planned, controlled experiments that connect adversary simulation to SOC validation:

```
Scenario → Expected Telemetry → Expected Detection → Investigation → Measurement → Improvement → Retest
```

Planned scenario families:

1. Authentication Abuse
2. Network Reconnaissance
3. Endpoint Execution / Suspicious Process Activity
4. Detection Resilience / Attack Variation

These are documented as planned scenario families in `scenarios/README.md`. The one controlled test executed so far — a file modification against `/home` to validate the FIM detection — is documented under `evidence/v0.2/` rather than as a formal scenario; this README does not include offensive attack commands.

## Detection engineering

SENTINEL treats detection engineering as a validated process, not just writing rules:

```
TELEMETRY → DETECTION DESIGN → CONTROLLED TEST → VALIDATION
  → FALSE POSITIVE ANALYSIS → MISSED DETECTION ANALYSIS → TUNING → RETEST
```

Detection lifecycle: `DRAFT → TELEMETRY VERIFIED → TESTED → TUNED → VALIDATED → MONITORED → RETESTED`, with possible end states `FAILED` or `RETIRED`.

**Current output:** one validated detection exists — Rule `100002`, built on Wazuh Syscheck/FIM telemetry from `/home` on SENTINEL-LINUX01, confirmed via a controlled file-modification test that produced a `syscheck_integrity_changed` event and a Level 8 alert. A key lesson from this work: a file-modification alert is not automatically malicious — it must be correlated with the user, process, path, timestamp, and surrounding context before being treated as suspicious, which will shape how FIM-based alerts are triaged in v0.3 investigation work.

See `docs/05-detection-engineering.md` and `detections/README.md` for the full methodology.

## SOC investigation (methodology, not current output)

The planned investigation workflow:

```
ALERT → TRIAGE → SCOPE → EVIDENCE → TIMELINE → IOCS → ATT&CK MAPPING
  → ROOT CAUSE → IMPACT → RESPONSE → LESSONS → RETEST
```

Investigations are meant to separate fact, hypothesis, interpretation, confirmed conclusion, and unknowns — evidence before assumptions. No investigation case (e.g. `case-001`) currently exists; see `investigations/README.md`.

## Measurement

SENTINEL aims to measure defensive performance rather than just show screenshots. Future measurements may include detection rate, detection latency, missed detections, false positives, investigation time, response time, coverage, regression, detection resilience, and before/after improvement — all tied to actual tests and evidence, never invented. See `metrics/README.md`.

## Failure-driven engineering

SENTINEL treats failure as useful engineering evidence rather than something to hide:

```
STOP → CAPTURE → DOCUMENT → INVESTIGATE → FIX → RETEST
```

Failures that may be documented include infrastructure, telemetry, detection, false-positive, missed-detection, investigation, response, regression, and (eventually) mutation failures. The Windows-endpoint architecture decision described above is the clearest current example of this philosophy in practice. See `failure-log/README.md`.

> "SENTINEL does not hide failure. It uses failure to improve the defense."

## Evidence

Claims in this project are meant to be backed by evidence, organized by version:

```
evidence/
├── v0.1/
├── v0.2/
├── v0.3/
├── v0.4/
├── v0.5/
└── v0.6/
```

v0.1 evidence covers infrastructure verification (dashboard, active agent). v0.2 evidence covers the Syscheck/FIM configuration, the controlled file-modification test, the `syscheck_integrity_changed` event, and the Level 8 alert produced by Rule `100002` — SENTINEL's first detection-specific evidence. Future evidence — investigation timelines, IOCs, response evidence, metrics, before/after comparisons, mutation results — will be added as those stages are actually completed, never in advance. Sensitive information is never committed (see `SECURITY.md`).

---

## Documentation

| Document | Covers |
|---|---|
| `docs/01-project-overview.md` | Project overview and goals |
| `docs/02-requirements.md` | Functional and lab requirements |
| `docs/03-architecture.md` | Detailed lab architecture |
| `docs/04-threat-model.md` | Threat model for the lab |
| `docs/05-detection-engineering.md` | Detection design and validation methodology |
| `docs/06-incident-response.md` | Incident response methodology |
| `docs/07-testing-and-matrices.md` | Testing and validation methodology |
| `docs/08-lessons-and-failures.md` | Failure-driven engineering narrative |
| `detections/README.md` | How detections are organized |
| `investigations/README.md` | How SOC investigations are organized |
| `metrics/README.md` | How measurement is organized |
| `scenarios/README.md` | How controlled scenarios are organized |
| `failure-log/README.md` | How failures are recorded |
| `SECURITY.md` | Security policy and safe-testing boundaries |
| `CHANGELOG.md` | Project-level milestones and architecture changes |

This README stays high-level by design — detailed methodology lives in the documents above.

## Repository structure

```
sentinel-soc-lab/
├── detections/       # Detection implementations
├── docs/             # Project documentation
├── evidence/         # Supporting evidence, organized by version
├── failure-log/      # Meaningful failure records
├── investigations/   # SOC investigation case records
├── metrics/          # Measured performance and validation results
├── scenarios/        # Controlled security scenario definitions
├── .gitignore
├── CHANGELOG.md
├── LICENSE
├── README.md
└── SECURITY.md
```

---

## Security and safety

SENTINEL is an authorized, isolated security laboratory:

- Attack simulations remain inside `SENTINEL-LAB`.
- Only authorized systems are tested.
- No real credentials or production secrets are used.
- No attacks are performed against external or production systems.
- No VM disks are committed to the repository.
- Sensitive evidence is sanitized before committing.

See `SECURITY.md` for the full policy. This README does not contain offensive attack instructions.

## Technology stack

| Current | Planned / Future |
|---|---|
| Wazuh (incl. Syscheck/FIM) | Sysmon (once Windows is introduced) |
| Ubuntu 24.04 | Windows / Active Directory |
| Kali Linux | Attack-emulation frameworks, if adopted |
| VirtualBox | Custom SENTINEL Console |
| Linux endpoint telemetry | Additional investigation/response integrations, if justified |
| Git / GitHub | |
| MITRE ATT&CK *(validation framework)* | |
| Python *(planned engineering language)* | |

Tools are added only when they provide clear security value — SENTINEL does not claim tools like Splunk, Security Onion, TheHive, Shuffle, OpenCTI, or Suricata unless they are actually adopted.

## Engineering principles

- **Evidence over claims** — show what happened.
- **Test over assumption** — a rule isn't proven until it's tested.
- **Failure is data** — failures are recorded and analyzed, not hidden.
- **Reproducibility** — scenarios should be repeatable.
- **Traceability** — scenario → detection → investigation → evidence → metrics → improvement.
- **Security first** — no complexity without a security purpose.
- **Engineering over decoration** — the custom UI never replaces real security work.
- **Understand what you build** — every component's purpose, failure modes, and validation should be explainable.

No component is added just to look impressive: Wazuh provides telemetry and detection, Kali provides controlled adversary simulation, Linux01 is the monitored endpoint, MITRE ATT&CK gives a shared behavior/technique language, metrics measure defensive performance, the failure log captures weaknesses, investigation records analyze incidents, and a future console is purely a visualization/integration layer on top of all of it.

## Portfolio value

SENTINEL is meant to demonstrate practical, hands-on understanding of Linux, networking, security monitoring, SIEM concepts, Wazuh, telemetry, detection engineering, MITRE ATT&CK, SOC investigation, incident response, testing, metrics, purple-team methodology, failure analysis, and security engineering as a whole.

The strongest story here isn't *"I installed Wazuh."* It's:

> "I built a controlled environment, generated security activity, collected telemetry, engineered a detection, validated it end to end, measured what it actually caught, and I'm now moving into investigating and responding to what it finds."

That full lifecycle is not complete yet — this README reflects the current v0.2 status honestly while explaining where the project is headed.
