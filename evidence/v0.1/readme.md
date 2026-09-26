# SENTINEL Evidence

This directory contains evidence produced during the development, testing, validation, investigation, and measurement of the SENTINEL SOC laboratory. Evidence exists to support the claims the project makes about itself.

> **Core principle:** if SENTINEL claims that something happened, the relevant evidence should exist whenever practical.

---

## 1. Purpose

Evidence preserves proof of actual project activity. It may demonstrate infrastructure configuration, connectivity, Wazuh operation, agent status, telemetry, detection behavior, investigation findings, incident timelines, response actions, test results, metrics, before/after improvements, attack mutation results, or detection resilience.

This directory preserves **what actually happened**, not what the project intended to happen.

---

## 2. Evidence Philosophy

- **Evidence over claims** — written statements alone aren't sufficient.
- **Preserve failures** — a failed test is evidence too.
- **Traceability** — evidence should be traceable to a version, scenario, detection, test, investigation, incident, or metric.
- **Reproducibility** — evidence should contain enough context to understand what was being tested.
- **Integrity** — evidence is never altered to make a result look better than it was.
- **Minimalism** — capture useful evidence without storing unnecessary data.
- **Security** — never store secrets or sensitive information.

---

## 3. Directory Structure

```
evidence/
├── README.md
├── v0.1/
├── v0.2/
├── v0.3/
├── v0.4/
├── v0.5/
└── v0.6/
```

Each project version gets its own evidence directory, kept separate so the project's evolution can be reconstructed later.

---

## 4. Version-Specific Evidence

| Version | Focus |
|---|---|
| v0.1 | Foundation and infrastructure evidence (e.g., Wazuh Dashboard agent status, agent service status, network verification, infrastructure verification) |
| v0.2 | *(Future)* Linux telemetry and initial detection evidence |
| v0.3 | *(Future)* SOC investigation evidence |
| v0.4 | *(Future)* Incident response evidence |
| v0.5 | *(Future)* Purple-team testing, measurement, and validation evidence |
| v0.6 | *(Future)* Attack DNA, mutation, and detection-resilience evidence |

Only v0.1 currently contains real evidence. No future-version evidence is claimed to exist.

---

## 5. Current v0.1 State

**Current project phase:** v0.1 — Foundation.

The repository currently contains actual v0.1 infrastructure evidence, which may include the Wazuh Agent running, the Dashboard showing the agent as active, and final infrastructure verification artifacts. No attack, detection, investigation, response, or mutation evidence exists yet — none is claimed here.

---

## 6. Evidence Categories

| Category | Proof of... |
|---|---|
| Infrastructure Evidence | VM configuration, network configuration, services, agent connectivity, platform availability |
| Telemetry Evidence | Expected telemetry generated and received |
| Detection Evidence | A detection behaving as expected during a controlled test |
| Investigation Evidence | Reconstruction of an event |
| Incident Response Evidence | Containment, eradication, recovery, and response actions |
| Testing Evidence | Test execution and results |
| Metrics Evidence | Measured values |
| Failure Evidence | Failed tests, broken configurations, or unexpected behavior |
| Mutation Evidence | *(Future)* Original vs. mutated attack behavior |

---

## 7. Evidence Traceability

```
Scenario → Test → Detection → Evidence → Investigation → Metric → Lesson
```

Where practical, evidence should reference a Test ID, Detection ID, Scenario ID, Case ID, and project version. Not every screenshot needs every identifier — traceability should be proportionate to the artifact.

---

## 8. Evidence Naming

Current examples: `dashboard-agent-active.png`, `wazuh-agent-running.png`, `final-verification.png`.

Future example conventions (illustrative only — none of these files exist yet): `DET-001-alert.png`, `DET-001-test-result.png`, `INV-001-timeline.png`, `IR-001-containment.png`, `MUT-001-original.png`, `MUT-001-variant.png`.

Prefer lowercase, descriptive names with consistent identifiers where useful. Avoid generic names like `IMG_1234.png` or `Screenshot_2026-09-XX.png` unless the original filename must be preserved for another reason.

---

## 9. Evidence README Files

| | Top-level `evidence/README.md` (this file) | `evidence/v0.x/README.md` |
|---|---|---|
| Explains | Evidence philosophy, directory structure, categories, naming, integrity, security, traceability, version organization | What was implemented in that version, what evidence was captured, what each artifact demonstrates, known limitations, verification status |

This file does not duplicate the detailed, artifact-by-artifact descriptions that belong in each version's own README.

---

## 10. Evidence Quality

Useful evidence is:

- **Relevant** — directly supports the claim
- **Authentic** — represents the actual project state
- **Understandable** — someone unfamiliar with the experiment can understand what it demonstrates
- **Timestamped** — the relevant date/time can be determined where important
- **Contextual** — includes enough surrounding information to interpret it
- **Traceable** — connects to a scenario, test, detection, or case

---

## 11. Screenshot Guidelines

Capture only what's needed. Where practical: include useful context, avoid excessive empty UI, ensure important text is readable, avoid exposing secrets or personal information, use descriptive filenames, and record what the screenshot demonstrates in the relevant version README. Screenshots are never edited in a misleading way — cropping for readability is fine as long as it doesn't change the meaning of the evidence.

---

## 12. Terminal / Log Evidence

Future evidence may include command output, service status, logs, Wazuh events, detection output, or test output. When practical, record the host, the command/action, the timestamp, the expected result, and the actual result. Full raw system logs are not stored when a smaller, relevant excerpt is sufficient.

---

## 13. Test Evidence

Connects to `docs/07-testing-and-matrices.md`. A test should eventually produce evidence supporting what was tested, expected behavior, actual behavior, detection result, investigation result, response result, and final status:

```
TEST-XXX → Execution → Evidence → Result → Matrix Update
```

No fictional test IDs are used.

---

## 14. Detection Evidence

Detection evidence should support actual detection claims: a Wazuh alert, a relevant event/log, the detection configuration, the test execution, a screenshot, a before/after result, a false-positive test, a false-negative test, or a retest result. It should eventually reference the relevant Detection ID where practical. Connects to `detections/`, `docs/05-detection-engineering.md`, and `docs/07-testing-and-matrices.md`.

---

## 15. Investigation Evidence

Future investigation evidence may include alert details, a timeline, relevant logs, IOCs, process information, network information, analyst notes, and investigation conclusions. Connects to `investigations/` and `docs/06-incident-response.md`. No investigation evidence currently exists.

---

## 16. Metric Evidence

Every metric should be traceable to underlying evidence — for example, Detection Time is derived from the timestamp of the activity plus the timestamp of the detection. A metric is never recorded without being able to explain its source. Connects to `metrics/` and `docs/07-testing-and-matrices.md`. No fabricated metrics are stored.

---

## 17. Failure Evidence

Failures are preserved when useful for understanding the engineering process: a failed detection, a false positive, a false negative, an infrastructure failure, an investigation gap, a response failure, or a mutation failure. Connects to `failure-log/`.

> A failed test is still evidence.

Failed evidence is never deleted just because a later implementation succeeded.

---

## 18. Evidence Integrity

Evidence is never altered to change the meaning of a result. Permitted actions: cropping screenshots for readability, redacting secrets, and removing unrelated sensitive information. Redaction never removes information that would change how the evidence is interpreted. When an artifact is transformed, the original is preserved where appropriate and safe to do so.

---

## 19. Security Rules

**Never commit:** passwords, API keys, authentication tokens, private keys, recovery codes, real credentials, sensitive personal information, confidential third-party information, VM disks, full sensitive databases, or unnecessary raw telemetry. Use sanitized evidence when needed, and keep anything too sensitive for the repository outside it, in an appropriately protected location.

---

## 20. Git / Repository Practices

Evidence is committed when it's useful to the project's history and safe to store. Large binary artifacts are not committed automatically. **Never commit:** VM images, huge packet captures, huge raw logs, generated databases, or secrets — use `.gitignore` rules where appropriate. Evidence commits use clear messages, for example:

```
evidence: add v0.1 Wazuh verification artifacts
```

No commit is claimed to exist unless it actually does.

---

## 21. Evidence Retention

Evidence is retained when it contributes to reproducibility, debugging, detection validation, incident investigation, measurement, or historical comparison. Temporary artifacts with no long-term value can be discarded once the useful information has been preserved elsewhere. The repository is not treated as a general storage dump.

---

## 22. Before / After Evidence

Future improvements should sometimes preserve a before/after pair:

```
BEFORE → Change → AFTER → Retest
```

Examples: detection before vs. after tuning, telemetry before vs. after a configuration change, original attack vs. mutated attack. No before/after results are fabricated — they exist only once a real change has actually been tested both ways.

---

## 23. Attack Mutation Evidence

**Status: FUTURE — v0.6.** Future evidence may compare an original attack against a mutated attack, recording the attack objective, the behavioral difference, the telemetry difference, the detection result, the investigation result, and the response result — to evaluate detection resilience. No mutation evidence exists today.

---

## 24. Evidence → Portfolio

Evidence may eventually support public project documentation, but sensitive internal information is never published. Before any public release, artifacts are reviewed for credentials, tokens, host information, personal information, sensitive network details, unnecessary logs, and private infrastructure information. Public case studies use sanitized evidence where necessary.

---

## 25. Evidence Checklist

Before storing evidence:

- [ ] Does it support a real project claim?
- [ ] Is the source known?
- [ ] Is the context understood?
- [ ] Is the timestamp relevant?
- [ ] Is the artifact traceable?
- [ ] Does it contain secrets?
- [ ] Does it contain sensitive information?
- [ ] Does it need redaction?
- [ ] Is it stored in the correct version directory?
- [ ] Is a README description required?

---

## 26. Evidence Workflow

```
ACTION → CAPTURE → VERIFY → SANITIZE → NAME → STORE → REFERENCE → COMMIT
```

- **Action** — the real event occurs (a test, a configuration change, a verification step)
- **Capture** — a screenshot, log excerpt, or output is taken
- **Verify** — confirm the artifact actually reflects what happened
- **Sanitize** — remove secrets or sensitive information
- **Name** — apply the naming convention from Section 8
- **Store** — place it in the correct version directory
- **Reference** — link it from the relevant README, test, or detection record
- **Commit** — commit with a clear, descriptive message

---

## 27. Relationship with Other Directories

| Directory | Relationship |
|---|---|
| `docs/` | Defines methodology |
| `detections/` | Contains actual detection implementations |
| `scenarios/` | Contains controlled test/attack scenarios |
| `evidence/` | Contains proof produced by those activities |
| `investigations/` | Contains investigation records |
| `metrics/` | Contains measured results |
| `failure-log/` | Contains documented failures and lessons |

Overall flow:

```
Scenario → Detection → Test → Evidence → Investigation → Metrics → Lessons → Improvement → Retest
```

---

## 28. Current Directory State

```
evidence/
├── README.md
└── v0.1/
    ├── README.md
    ├── dashboard-agent-active.png
    ├── final-verification.png
    └── wazuh-agent-running.png
```

If the actual repository contains additional verified files beyond this list, they are preserved as-is rather than removed or reinterpreted here. This v0.1 evidence represents infrastructure verification only. Future version directories are populated as those versions are actually implemented.

---

## 29. Version Roadmap

| Version | Expected Evidence |
|---|---|
| v0.1 | Infrastructure foundation |
| v0.2 | *(Planned)* Linux telemetry and detection testing |
| v0.3 | *(Planned)* Investigation and case evidence |
| v0.4 | *(Planned)* Incident response evidence |
| v0.5 | *(Planned)* Measurement and purple-team evidence |
| v0.6 | *(Planned)* Attack mutation and detection-resilience evidence |

---

## 30. Documentation Rules

1. Never fabricate evidence.
2. Never modify evidence to change the result.
3. Keep evidence traceable.
4. Separate evidence by project version.
5. Protect secrets and sensitive information.
6. Preserve meaningful failures.
7. Avoid unnecessary repository bloat.
8. Keep filenames descriptive.
9. Link evidence to tests/detections/cases where practical.
10. Update version-specific README files when new evidence is added.

---

## 31. Interview / Engineering Value

Evidence allows SENTINEL to demonstrate rather than merely claim:

- Infrastructure works
- Telemetry exists
- Detections work
- Investigations are possible
- Response actions work
- Improvements are measurable
- Failures were actually encountered and resolved
- Detection resilience was tested

None of the future capabilities in this list are claimed to currently exist — they describe what evidence will eventually be able to demonstrate as SENTINEL's later phases are completed.

---

## 32. Final Principle

> Evidence is the bridge between what SENTINEL says it can do and what SENTINEL can actually prove.

> Capture the result, not the story.

---

## 33. Final Status

**Current phase:** v0.1 — Foundation

**Current evidence:** Infrastructure verification artifacts exist under `evidence/v0.1/`.

**Next evidence focus:** v0.2 — Linux telemetry and first detection validation.

**Final rule:** Do not invent evidence. Do not invent filenames. Do not invent test results. Do not invent metrics. Do not claim future evidence exists. Do not duplicate version-specific README content unnecessarily.

This file is the top-level evidence management and navigation guide for SENTINEL.
