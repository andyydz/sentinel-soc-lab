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
├── readme.md
├── sysmon-replay/
├── v0.1/
├── v0.2/
├── v0.3/
├── v0.5/
├── v0.6/
├── v0.7/
├── v0.9/
└── v0.11/
```

Evidence is organized by project version where a committed version directory exists, kept separate so the project's evolution can be reconstructed later. Some distinctions matter:

- Sysmon replay evidence is stored under `sysmon-replay/`, not under an `evidence/v0.4/` directory.
- There is no `evidence/v0.8/` directory.
- There is no `evidence/v0.10/` directory. The v0.10 evidence archive is stored externally at `~/soc-evidence/v0.10-fim-probe/` and is not committed repository evidence.
- `evidence/v0.11/` exists and contains committed artifacts; its milestone status remains pending reconciliation.

---

## 4. Version & Replay Evidence Directories

| Directory / Scope | Focus & Status |
|---|---|
| `v0.1/` | Infrastructure foundation and Wazuh manager/agent verification |
| `v0.2/` | Linux telemetry, initial FIM activity, and security configuration assessment evidence |
| `v0.3/` | FIM lifecycle evidence and `CASE-001` investigation |
| `sysmon-replay/` | Offline Windows Sysmon replay evidence for `CASE-002` |
| `v0.5/` | SSH brute-force testing and `CASE-003` evidence |
| `v0.6/` | Controlled purple-team measurement evidence |
| `v0.7/` | Mutation-style testing and `CASE-004` evidence |
| `v0.9/` | Sysmon JSON replay and Python triage integration evidence (replay-based; live Windows agent out-of-scope) |
| `v0.11/` | Committed FIM alert records, triage report, and regression-summary artifacts. The v0.11 milestone status remains pending reconciliation |

The v0.10 evidence is held separately in the external archive at `~/soc-evidence/v0.10-fim-probe/`; it is not a committed `evidence/v0.10/` directory.

Evidence scope boundaries are documented alongside each milestone in the root [README.md](../README.md), [CHANGELOG.md](../CHANGELOG.md), and the corresponding [CASE-001](../investigations/CASE-001.md) through [CASE-004](../investigations/CASE-004.md) records.

The repository now contains infrastructure, telemetry, detection, investigation, measurement, and limited mutation-style evidence across multiple project phases. The existence of evidence does not automatically mean that every test or response capability is fully validated, and no complete containment, eradication, or recovery exercise is claimed as evidenced.

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
| Mutation Evidence | *(Limited)* Original vs. mutated attack behavior. Limited mutation-style evidence exists (v0.7, `CASE-004`); a comprehensive mutation framework is future work |

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

| | Top-level `evidence/readme.md` (this file) | `evidence/v0.x/readme.md` |
|---|---|---|
| Explains | Evidence philosophy, directory structure, categories, naming, integrity, security, traceability, version organization | What was implemented in that version, what evidence was captured, what each artifact demonstrates, known limitations, verification status |

Version-specific evidence indexes use lowercase `readme.md`, for example [v0.1/readme.md](v0.1/readme.md), [v0.2/readme.md](v0.2/readme.md), [v0.3/readme.md](v0.3/readme.md), [v0.5/readme.md](v0.5/readme.md), [v0.6/readme.md](v0.6/readme.md) and [v0.9/readme.md](v0.9/readme.md).

This file does not duplicate the detailed, artifact-by-artifact descriptions that belong in each version's own index.

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

Connects to [docs/07-testing-and-metrics.md](../docs/07-testing-and-metrics.md). A test should eventually produce evidence supporting what was tested, expected behavior, actual behavior, detection result, investigation result, response result, and final status:

```
TEST-XXX → Execution → Evidence → Result → Matrix Update
```

No fictional test IDs are used.

---

## 14. Detection Evidence

Detection evidence should support actual detection claims: a Wazuh alert, a relevant event/log, the detection configuration, the test execution, a screenshot, a before/after result, a false-positive test, a false-negative test, or a retest result. It should eventually reference the relevant Detection ID where practical. Connects to `detections/`, [docs/05-detection-engineering.md](../docs/05-detection-engineering.md), and [docs/07-testing-and-metrics.md](../docs/07-testing-and-metrics.md).

---

## 15. Investigation Evidence

Investigation records and supporting evidence exist for [CASE-001](../investigations/CASE-001.md), [CASE-002](../investigations/CASE-002.md), [CASE-003](../investigations/CASE-003.md) and [CASE-004](../investigations/CASE-004.md). The types of artifact vary: some findings rely on screenshots, some on raw JSON/log records, and not every investigation has every possible evidence type. The existence of an investigation record does not mean it includes a complete incident-response record.

Investigation evidence may include alert details, a timeline, relevant logs, IOCs, process information, network information, analyst notes, and investigation conclusions. Connects to `investigations/` and [docs/06-incident-response.md](../docs/06-incident-response.md).

---

## 16. Metric Evidence

Every metric should be traceable to underlying evidence — for example, Detection Time is derived from the timestamp of the activity plus the timestamp of the detection. A metric is never recorded without being able to explain its source. Connects to `metrics/` and [docs/07-testing-and-metrics.md](../docs/07-testing-and-metrics.md). No fabricated metrics are stored.

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

**Status: LIMITED — v0.7 / [CASE-004](../investigations/CASE-004.md); broader work is FUTURE.**

Limited mutation-style testing has already been performed and documented. A tested Sysmon command-line variation (`comsvcs.dll, #24`) bypassed keyword-specific Rule `100112` and matched the Level 0 base Rule `100101` instead. This is a documented detection gap for the tested variation only. It is not a comprehensive, repeatable attack-mutation framework or a broad detection-resilience assessment.

Further evidence is future work. It may compare an original attack against a mutated attack more broadly, recording the attack objective, the behavioral difference, the telemetry difference, the detection result, the investigation result, and the response result — to evaluate detection resilience.

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
├── readme.md
├── sysmon-replay/
├── v0.1/
├── v0.2/
├── v0.3/
├── v0.5/
├── v0.6/
├── v0.7/
├── v0.9/
└── v0.11/
```

The v0.1 directory includes infrastructure verification screenshots such as `dashboard-agent-active.png`, `final-verification.png` and `wazuh-agent-running.png`. The v0.2 directory's screenshot subdirectory is named `screenschots` as committed; it is not renamed here.

There is no `evidence/v0.8/` or `evidence/v0.10/` directory. The v0.10 archive is stored externally at `~/soc-evidence/v0.10-fim-probe/`. `evidence/v0.11/` contains committed artifacts, but its milestone status remains pending reconciliation.

If the actual repository contains additional verified files beyond those described here, they are preserved as-is rather than removed or reinterpreted. New version directories are populated only as that work is actually implemented.

---

## 29. Version Roadmap

Current evidence status by version:

| Version / Scope | Evidence Scope | Status Notes |
|---|---|---|
| v0.1 | Infrastructure foundation; Wazuh manager/agent verification | Committed in `v0.1/` |
| v0.2 | Linux telemetry, initial FIM activity, security configuration assessment | Committed in `v0.2/` |
| v0.3 | FIM lifecycle evidence; `CASE-001` investigation | Committed in `v0.3/` |
| v0.4 (replay) | Offline Windows Sysmon replay evidence (`CASE-002`) | Committed in `sysmon-replay/`, not `evidence/v0.4/`; replayed telemetry, not a live Windows endpoint |
| v0.5 | SSH brute-force testing; `CASE-003` evidence | Committed in `v0.5/` |
| v0.6 | Controlled purple-team measurement | Committed in `v0.6/`; small controlled samples |
| v0.7 | Mutation-style testing; `CASE-004` evidence | Committed in `v0.7/`; limited, not a comprehensive mutation framework |
| v0.8 | — | No committed `evidence/v0.8/` directory |
| v0.9 | Sysmon JSON replay; Python triage integration | Committed in `v0.9/`; replay-based |
| v0.10 | Evidence archive | Externally archived at `~/soc-evidence/v0.10-fim-probe/`; no committed `evidence/v0.10/` directory |
| v0.11 | FIM alert records, triage report, regression-summary artifacts | Committed in `v0.11/`; milestone status pending reconciliation |

Existing evidence is not automatically proof of a complete regression suite, comprehensive coverage, or a fully validated capability. Further evidence remains dependent on actual testing, and future work is not presented as completed.

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

Evidence is what turns SENTINEL's documented methodology into something a reviewer, recruiter, or interviewer can actually verify rather than take on faith. A written claim that "a detection was validated" is easy to make and hard to trust; a linked screenshot of the Wazuh Dashboard, a test's recorded before/after comparison, or a documented false positive shows the underlying work actually happened, and shows it honestly — failures and all. This is what separates SENTINEL from a project that simply lists tools and claims outcomes: the evidence directory is the receipts.

---

## 32. Final Status

SENTINEL has progressed well beyond its initial infrastructure phase. Multiple evidence sets exist across the committed version directories and the `sysmon-replay/` directory. The v0.10 evidence is externally archived at `~/soc-evidence/v0.10-fim-probe/`. The v0.11 artifacts are committed under `v0.11/`, but the milestone is pending reconciliation and is not labeled completed or validated. Further evidence and validation remain dependent on actual testing.

This file describes SENTINEL's overall evidence strategy. It does not duplicate the detailed, per-artifact descriptions that belong in each version's own `readme.md`, and it does not claim any evidence exists beyond what is actually present in the repository.
