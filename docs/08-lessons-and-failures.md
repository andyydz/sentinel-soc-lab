# failure-log/

This directory contains the operational guidance for SENTINEL's future individual failure records. It explains how meaningful failures and unexpected behavior should be captured and documented.

At present, this directory contains only this README; no individual failure-record files have been added. The formal FAIL-001 entry (the Windows 11 endpoint boot failure) and the other verified findings are currently documented in [`docs/08-lessons-and-failures.md`](../docs/08-lessons-and-failures.md), not in separate files here.

For the broader narrative discussion of lessons learned across the project, see [`docs/08-lessons-and-failures.md`](../docs/08-lessons-and-failures.md). That file records the project's verified failures, detection gaps, benign noise, scope limitations, and unresolved questions.

---

## Why SENTINEL keeps a failure log

SENTINEL does not consider a security control successful merely because it exists. A control should eventually be:

```
TESTED → EVIDENCED → MEASURED → IMPROVED → RETESTED
```

Failures encountered along the way — infrastructure problems, telemetry gaps, detection misses, false positives, investigation dead ends, response issues, broken tests, and mutation-testing findings — are treated as valuable engineering evidence, not as things to hide. This directory provides the structure for preserving that evidence in individual records.

The project's overall development methodology is:

```
BUILD → UNDERSTAND → TEST → BREAK → FIX → MEASURE → DOCUMENT → EXPLAIN
```

`failure-log/` exists to support the "BREAK → FIX → DOCUMENT" part of that cycle.

---

## What belongs here

Record a failure here when it:

- affects project progress,
- changes an implementation or architecture decision,
- reveals a weakness,
- invalidates a test,
- causes a detection miss,
- affects reproducibility,
- exposes a security issue, or
- provides a meaningful engineering lesson.

This is not a place for trivial mistakes or typos. If it didn't change anything, didn't reveal anything, and isn't worth remembering, it doesn't need a record.

---

## Failure philosophy

SENTINEL follows a consistent response to meaningful failures:

```
STOP → CAPTURE → DOCUMENT → CONTINUE
```

1. **STOP** the affected test or activity.
2. **CAPTURE** relevant evidence before it is lost.
3. **DOCUMENT** what actually happened.
4. **CONTINUE** only once the environment is understood or made safe.

Evidence should not be erased, overwritten, or "fixed away" before it has been captured, if doing so would destroy information needed for analysis. Preserving failures is part of how SENTINEL demonstrates real engineering work, not just working end states.

---

## Failure categories

Each record in this directory should fall into one of the following categories:

- **Infrastructure** — e.g. VM boot failure, installation failure, VirtualBox configuration problem, resource exhaustion, networking configuration failure.
- **Telemetry** — e.g. agent not reporting, logs not arriving, missing event data, incorrect telemetry configuration, unexpected telemetry gaps.
- **Detection** — e.g. a detection did not trigger, triggered incorrectly, matched the wrong event, or was too broad/narrow. Includes the specific sub-cases of false positives (benign activity triggered a detection) and missed detections / false negatives (an expected detection did not fire during a controlled test).
- **Investigation** — e.g. insufficient evidence, a timeline that could not be reconstructed, an IOC that could not be determined, an alert lacking useful context, or an investigation that reached an inconclusive state.
- **Response** — e.g. a containment action failed, produced unexpected behavior, recovery did not work as expected, or a human-approval step was unclear.
- **Testing / Regression** — e.g. a test could not be reproduced, a previously passing detection stopped working, an environment change invalidated a test, or a detection improvement broke another test.
- **Mutation** — used for findings from controlled attack variations that test whether detections remain effective when an attacker changes tactics. A formal, repeatable Attack Mutation testing process has not been established. However, a mutation-style variation was tested in CASE-004: the Sysmon command-line variation `comsvcs.dll, #24` bypassed keyword-specific Rule `100112` and matched base Rule `100101` at Level 0. This is a documented detection gap for the tested variation only. See [`docs/08-lessons-and-failures.md`](../docs/08-lessons-and-failures.md) for the finding.
- **Documentation / Process** — e.g. missing evidence, unreproducible steps, documentation that contradicted actual configuration, or a test result that could not be traced back to evidence.

---

## Standard failure record format

Each future failure gets its own file in this directory (e.g. `FAIL-NNN-short-title.md`, where NNN is the next unused failure number). Use the following structure, filling in only what is actually known:

```markdown
# Failure ID / Title

## Status
Open | Investigating | Mitigated | Resolved | Retesting | Closed | Accepted Limitation

## Category
Infrastructure | Telemetry | Detection | Investigation | Response | Testing | Mutation | Documentation

## Severity / Impact
Low | Medium | High | Critical
(Assign based on actual project impact — do not default to a severity without considering it.)

## Date
(Only include a date if it is actually known. Never invent one.)

## Environment
Affected SENTINEL component(s), e.g. SENTINEL-WAZUH, SENTINEL-KALI, SENTINEL-LINUX01, SENTINEL-LAB.

## Expected Behavior
What should have happened.

## Actual Behavior
What actually happened. Factual observations only.

## Evidence
Links to relevant screenshots, logs, test output, detection alerts, configuration, or other evidence files (repository-relative links where appropriate).

## Impact
What the failure affected — project progress, a specific test, a detection, etc.

## Investigation
What was checked while investigating the issue.

## Root Cause
Only state a root cause once it has been sufficiently verified.
If unknown, write exactly: "Root cause not yet determined."
Never guess.

## Corrective Action
What was changed to address the issue.

## Validation
How the fix was tested.

## Retest Result
Passed | Failed | Partial | Not yet retested

## Lesson Learned
What should be remembered for future SENTINEL development.

## Follow-up
Any remaining work.
```

---

## Failure lifecycle

Failures recorded in this directory move through the following lifecycle:

```
DISCOVER
   |
STOP
   |
CAPTURE EVIDENCE
   |
DOCUMENT
   |
CLASSIFY
   |
INVESTIGATE
   |
IDENTIFY ROOT CAUSE
   |
CORRECT
   |
RETEST
   |
MEASURE
   |
CLOSE / ACCEPT LIMITATION
   |
UPDATE DOCUMENTATION
```

If a retest fails, the record returns to the INVESTIGATE or CORRECT stage rather than being closed. A record's "Status" field should reflect where it currently sits in this lifecycle.

---

## Root cause discipline

Failure records must distinguish between:

- **Symptom** — what was observed.
- **Immediate cause** — the direct trigger of the symptom, if known.
- **Root cause** — the underlying reason, only stated once verified.
- **Contributing factors** — other conditions that made the failure more likely, if known.

A symptom is not automatically its root cause. For example, "the VM did not boot correctly" does not by itself establish that "VirtualBox is broken" — that would need to be confirmed through evidence before being recorded as a root cause. When the root cause is not yet established, the record should say so explicitly ("Root cause not yet determined") rather than speculate.

---

## From failure to engineering decision

Failures recorded here are expected to feed back into the project, generally along these lines:

| Failure type | Typical resulting action |
|---|---|
| Infrastructure failure | Architecture change |
| Telemetry failure | Telemetry configuration change |
| Detection failure | Detection rule improvement |
| False positive | Detection tuning |
| Missed detection | Telemetry or detection redesign |
| Investigation failure | Additional evidence/context collection |
| Response failure | Response workflow improvement |
| Regression failure | Test-suite improvement |
| Mutation finding | Detection resilience improvement |

A failure record is complete when it has produced, or explicitly ruled out, a corresponding engineering decision — not merely when the immediate symptom stops occurring.

---

## Verified example: the SENTINEL-WIN01 architecture decision

The clearest example of this process so far involved the originally planned Windows endpoint, `SENTINEL-WIN01`. During the initial v0.1 infrastructure buildout, this VM repeatedly failed to boot and render a usable guest display in the VirtualBox environment.

Troubleshooting was attempted, including fresh VM creation, NAT-only boot testing, graphics configuration changes, UEFI / Secure Boot / TPM adjustments, a VirtualBox version upgrade, and boot-menu testing. The issue persisted, but no definitive technical root cause was determined.

Rather than let an unreliable, non-essential component block progress, the project made an architecture decision:

- Linux (`SENTINEL-LINUX01`) became the initial monitored endpoint.
- Windows was removed as a dependency for the core v0.1 build.
- Windows/Active Directory remain planned future expansion, not current infrastructure.

This followed the pattern:

```
FAILURE → ANALYZE → ARCHITECTURE DECISION → CONTINUE → RETEST
```

The Windows VM itself was not retested after the architecture change; the "retest" in this case was that v0.1 was completed successfully with Linux01 as the monitored endpoint. The original boot issue remains unresolved.

It is recorded in [`docs/08-lessons-and-failures.md`](../docs/08-lessons-and-failures.md) as FAIL-001, the project's first significant example of treating an infrastructure failure as engineering input rather than a blocker or an embarrassment to be hidden.

---

## Current status of this directory

SENTINEL testing has progressed through v0.10. CASE-004 documented a Sysmon detection gap involving the tested `comsvcs.dll, #24` variation, which bypassed keyword-specific Rule `100112` and matched base Rule `100101` at Level 0. Benign FIM noise and a known FIM monitoring-scope limitation have also been documented.

This directory currently contains only this README; no individual failure-record files have been added. FAIL-001 and the other verified findings are currently documented in [`docs/08-lessons-and-failures.md`](../docs/08-lessons-and-failures.md). The absence of individual files here must not be read as evidence that no failures, gaps, or findings have occurred.
