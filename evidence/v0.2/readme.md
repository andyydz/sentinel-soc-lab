# evidence/

This directory stores the supporting evidence that backs up claims made elsewhere in SENTINEL — screenshots, logs, alert output, test results, and other artifacts that show a claim actually happened rather than just stating that it did.

This README explains how evidence is organized here. It does not restate the testing methodology (`docs/07-testing-and-matrices.md`) or the detection-engineering methodology (`docs/05-detection-engineering.md`) — see those documents for that detail.

## Purpose

SENTINEL's core principle is **evidence over claims**: a milestone, detection, investigation, or test result is only as credible as the evidence behind it. This directory is where that evidence lives, so that any statement elsewhere in the project ("the agent went active," "the detection triggered," "the scenario passed") can be traced back to something concrete.

## Directory structure

Evidence is organized by project version, matching the roadmap in the root `README.md`:

```
evidence/
├── v0.1/
├── v0.2/
├── v0.3/
├── v0.4/
├── v0.5/
└── v0.6/
```

- **`evidence/v0.1/`** — infrastructure verification evidence (Wazuh Dashboard showing the active endpoint, agent-running confirmation, v0.1 verification).
- **`evidence/v0.2/`** — evidence for the current infrastructure/telemetry milestone, including the Wazuh↔Linux01 agent enrollment, the duplicate-registration troubleshooting, and the verified `ACTIVE` agent state covered in the v0.2 integration write-up.
- **`evidence/v0.3/` – `evidence/v0.6/`** — reserved for investigation, response, measurement, and attack-mutation evidence as those phases are reached. These do not currently contain anything, since v0.3–v0.6 work has not started.

Only create a version subdirectory, and only add files to it, once real evidence for that version actually exists — this directory does not get populated ahead of the work it documents.

## What belongs here

Evidence may include:

- Screenshots (e.g. Wazuh Dashboard views, agent status, alert details)
- Wazuh alerts and manager/agent log excerpts
- Logs and command output relevant to a verified step
- Test or scenario execution output
- Detection results
- Investigation timeline evidence
- IOC evidence
- Network observation output
- Before/after comparisons (e.g. pre- and post-fix agent status)
- Metrics output, once real measurements exist

Evidence should be **relevant** (it supports a specific, stated claim), **sanitized** (no secrets), **traceable** (it's clear which claim, milestone, scenario, or case it supports), and **reproducible where possible**.

## What never goes here

Never commit:

- Passwords, including Wazuh admin/dashboard passwords
- API keys, tokens, or session identifiers
- Private keys or certificate material, including the contents of `client.keys`
- Real/production credentials
- Personal information
- Production data or unnecessary raw/sensitive telemetry
- VM disk images or other large unnecessary binary artifacts

If a screenshot or log excerpt contains any of the above, **redact it before committing** rather than omitting the redaction and relying on cropping alone — assume anything not explicitly blacked out is visible.

### Redaction checklist (apply before adding any evidence)

- [ ] No admin/dashboard password visible
- [ ] No `client.keys` or other key material visible
- [ ] No API keys, tokens, or session identifiers visible
- [ ] No private key material visible
- [ ] No unrelated host, browser, or personal information visible in the background
- [ ] File is clearly named and placed under the correct version directory

## Naming and traceability

Evidence filenames should make their contents and context identifiable at a glance, e.g.:

```
evidence/v0.2/wazuh-dashboard-agent002-active.png
evidence/v0.2/manager-log-hc_startup.txt
evidence/v0.2/duplicate-agent-conflict-log.txt
```

Where a piece of evidence supports a specific document (a milestone write-up, a scenario, a case, a detection), that document should link to the evidence using a repository-relative path, and the evidence file itself should be traceable back to what it's proving — not a standalone, uncontextualized file.

## Relationship to other SENTINEL documentation

- **`evidence/README.md`** (this file) — how evidence is organized and handled.
- **`docs/07-testing-and-matrices.md`** — the broader testing and validation methodology.
- **`docs/05-detection-engineering.md`** — how detections are designed and validated.
- **`scenarios/`** — controlled scenario definitions that evidence here may support.
- **`investigations/`** — SOC investigation case records that reference investigation evidence.
- **`metrics/`** — measured results, which should themselves link back to the raw evidence here.
- **`failure-log/`** — failure records, which often reference evidence captured during troubleshooting.
- **`SECURITY.md`** — the full policy on credentials, secrets, and sensitive data handling.
- **`CHANGELOG.md`** — project-level milestones this evidence may support.

## Current status

- `evidence/v0.1/` contains infrastructure verification evidence from the v0.1 Foundation milestone.
- `evidence/v0.2/` has been created and contains evidence for the current Wazuh↔Linux01 agent enrollment and troubleshooting milestone.
- `evidence/v0.3/` through `evidence/v0.6/` do not currently contain any evidence, since the corresponding project phases (SOC investigation, incident response, purple-team measurement, and Attack DNA/Mutation) have not yet started.
-
