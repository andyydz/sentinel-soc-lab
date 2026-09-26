# SENTINEL Lessons & Failures

> Does your detection still work when the attacker changes tactics?

This document preserves the real engineering history of SENTINEL: what failed, why it failed, how it was investigated, what changed, whether the fix worked, what was learned, and what should be retested. It is not a generic "lessons learned" article — it is a living engineering record, and it only contains failures that actually occurred. Hypothetical scenarios are included only when explicitly labeled **Example** or **Hypothetical**.

---

## 1. Purpose

SENTINEL follows this working cycle:

```
BUILD → UNDERSTAND → TEST → BREAK → FIX → MEASURE → DOCUMENT → EXPLAIN
```

Failures are expected during security engineering, not a sign something went wrong with the project itself:

- A failed detection is useful information.
- A broken VM is useful information.
- A telemetry gap is useful information.
- A false positive is useful information.
- A failed response action is useful information.

The goal of this document is not to eliminate evidence of failure — it's to understand failure and convert it into engineering improvement.

---

## 2. Failure-Driven Engineering Principle

**Failure is data.** For every failure, SENTINEL asks:

- What assumption was wrong?
- What failed?
- Why did it fail?
- What evidence proves the failure?
- What was changed?
- Did the change solve the actual problem?
- Did the fix introduce a new problem?
- How should the result affect future testing?

```
FAIL → CAPTURE → ANALYZE → FIX → RETEST → MEASURE → DOCUMENT → IMPROVE
```

---

## 3. Current v0.1 Project State

### SENTINEL-WAZUH
| Field | Value |
|---|---|
| OS | Ubuntu 24.04 |
| Wazuh | 4.14.8 |
| IP | 10.10.10.10 |
| Role | SOC / monitoring platform |

### SENTINEL-KALI
| Field | Value |
|---|---|
| Role | Controlled attacker VM |
| IP | 10.10.10.20 |

### SENTINEL-LINUX01
| Field | Value |
|---|---|
| OS | Ubuntu 24.04.5 LTS |
| IP | 10.10.10.40 |
| Wazuh Agent | 4.14.8, Agent ID `001`, agent name `sentinel-linux01`, status Active |

**Network:** `SENTINEL-LAB` — `10.10.10.0/24`.

**Current state:** core infrastructure established, Wazuh operational, Kali operational, Linux01 operational, Wazuh Agent connected. **No detection or incident failures are claimed in this document beyond what has actually occurred** — see Section 11 for the verified failure log.

---

## 4. Documented Infrastructure Lessons

### Verified lesson: Windows 11 endpoint deployment

The project initially attempted to include a Windows 11 endpoint as part of the core v0.1 architecture. That VM repeatedly failed to boot/render correctly in the VirtualBox environment.

**Troubleshooting attempted:**
- Fresh VM creation
- NAT-only boot testing
- VirtualBox graphics configuration changes
- UEFI / Secure Boot / TPM configuration adjustments
- VirtualBox version upgrade
- Boot-menu testing

**Result of troubleshooting:** the issue persisted. No definitive technical root cause was conclusively determined — the exact underlying cause (hypervisor interaction, graphics configuration, firmware settings, or something else) was not confirmed, and this document does not speculate beyond what was actually verified.

**Engineering decision:** do not allow the unresolved Windows VM problem to block SENTINEL's overall development.

**Result:** the architecture was revised so that SENTINEL-LINUX01 became the initial monitored endpoint for v0.1. Windows/Active Directory was moved to future expansion (see `architecture.md`, Section 3.4) rather than being treated as a blocker.

This is currently the only verified project-level infrastructure lesson recorded. It is documented factually, without an invented root cause.

---

## 5. Failure Record Format

Every failure should be recorded using this template:

```markdown
# Failure ID

## Date
## Version
## Category
## Component
## Expected Behavior
## Actual Behavior
## Impact
## Evidence
## Initial Hypothesis
## Investigation
## Root Cause
## Corrective Action
## Retest
## Final Result
## Lesson Learned
## Preventive Action
## Related Test
## Related Documentation
```

Unknown fields are recorded as `Unknown`, `Not yet determined`, or `Not tested` — never filled with invented information.

---

## 6. Failure Categories

### Infrastructure Failure
VM, OS, networking, storage, VirtualBox, or configuration issues.

### Telemetry Failure
Expected telemetry not generated, collected, or received.

### Detection Failure
Expected malicious/suspicious behavior not detected.

### False Positive
Benign activity incorrectly detected.

### Investigation Failure
Available evidence insufficient to answer the required investigation questions.

### Response Failure
A response action failed or produced an unexpected result.

### Mutation Failure
A detection failed after a controlled attack variation.

### Documentation Failure
Important information was not recorded correctly at the time.

### Process Failure
The methodology itself caused an avoidable problem.

---

## 7. Failure Severity / Impact

These are **project engineering impact** categories, not formal incident-severity ratings:

| Level | Meaning |
|---|---|
| LOW | Minor inconvenience; no meaningful project blockage |
| MEDIUM | Delays a development task; requires troubleshooting |
| HIGH | Blocks an important project capability; requires an architectural or implementation change |
| CRITICAL | Threatens lab safety or host/environment integrity |

The Windows 11 boot failure documented in Section 4 is classified as **HIGH** under this scale: it blocked the originally planned architecture and required an architecture change, but did not threaten lab safety or host integrity.

---

## 8. Failure Triage

1. Identify the failure.
2. Stop unsafe activity if necessary.
3. Capture evidence.
4. Record exact symptoms.
5. Identify the affected component.
6. Form hypotheses.
7. Test hypotheses.
8. Identify root cause where possible.
9. Apply corrective action.
10. Retest.
11. Record the final result.
12. Update related documentation.

Guiding principle:

```
STOP → CAPTURE → DOCUMENT → CONTINUE
```

---

## 9. Root Cause Analysis

The first symptom observed is not necessarily the root cause. Useful methods include:

- 5 Whys
- Timeline analysis
- Configuration comparison
- Controlled reproduction
- Dependency analysis
- Before/after comparison

A root cause is never forced when the evidence doesn't support one. A valid, honest result is:

> "Root cause not conclusively determined."

— as is the case for the Windows 11 boot failure in Section 4.

---

## 10. Corrective Action

Corrective actions may include:

- Configuration change
- Code change
- Detection-rule change
- Telemetry change
- Network change
- VM configuration change
- Documentation change
- Test improvement
- Process improvement
- Architecture change

Every significant corrective action should be recorded against the failure it addresses, including whether it was retested and whether the retest confirmed the fix. A corrective action is not considered complete until its retest result has been documented — "we made a change" is not the same as "we confirmed the change worked."

For the Windows 11 case (Section 4), the corrective action was architectural: removing the Windows endpoint from the current scope and substituting SENTINEL-LINUX01 as the v0.1 monitored endpoint. This action has been confirmed effective in the sense that v0.1 was completed successfully with Linux01 in that role; it does not resolve the original Windows boot issue itself, which remains unresolved and out of current scope.

---

## 11. Verified Failure Log

This is the authoritative log of failures that have actually occurred in SENTINEL. Entries are added only as real failures happen — nothing here is invented in advance.

### FAIL-001

- **Date:** Not precisely recorded at the time; occurred during v0.1 infrastructure buildout
- **Version:** v0.1
- **Category:** Infrastructure Failure
- **Component:** Planned Windows 11 endpoint (SENTINEL-WIN01, VirtualBox)
- **Expected Behavior:** Windows 11 VM boots normally and renders a usable guest display
- **Actual Behavior:** VirtualBox displayed a gray window with a small, non-functional guest display area; the VM did not reach a usable boot state
- **Impact:** HIGH — blocked the originally planned three-OS architecture (Wazuh, Kali, Windows)
- **Evidence:** Observed VirtualBox display behavior (not preserved as a stored artifact at the time)
- **Initial Hypothesis:** Graphics/display configuration or firmware (UEFI/Secure Boot/TPM) interaction issue
- **Investigation:** Fresh VM creation, NAT-only boot testing, graphics configuration changes, UEFI/Secure Boot/TPM configuration adjustments, VirtualBox version upgrade, boot-menu testing
- **Root Cause:** Not yet determined
- **Corrective Action:** Removed Windows from the current v0.1 architecture; substituted SENTINEL-LINUX01 as the initial monitored endpoint; moved Windows/AD to future expansion
- **Retest:** Not applicable to the original issue — the Windows VM itself was not retested after the architecture change
- **Final Result:** v0.1 completed successfully using the revised (Linux-based) architecture
- **Lesson Learned:** An unresolved infrastructure blocker should not stall the whole project — the architecture can be adapted around it while the original problem is deferred rather than ignored
- **Preventive Action:** Windows/AD reintroduction is documented as future work with no fixed timeline, so it isn't silently reattempted without accounting for this history
- **Related Test:** None (pre-dates the formal test framework in `test-and-matrices.md`)
- **Related Documentation:** `architecture.md` (Section 3.4, Future Windows / Active Directory Expansion), `Requirements.md`

No other failures are currently recorded. Detection failures, false positives, false negatives, investigation failures, response failures, and mutation failures will be added here only once v0.2 and later testing actually produces them.

---

## 12. Lessons Learned Summary

| Lesson | Source | Applies To |
|---|---|---|
| Don't let one blocked component stall the whole project — adapt the architecture and defer the blocker explicitly | FAIL-001 | Future infrastructure changes, especially Windows/AD reintroduction |
| Root cause is sometimes genuinely "not determined" — document that honestly rather than guessing | FAIL-001 | All future failure records |

This table will grow as new verified failures are added to Section 11.

---

## 13. Preventive Actions Registry

| Preventive Action | Originating Failure | Status |
|---|---|---|
| Do not reintroduce Windows/AD without accounting for the unresolved VirtualBox boot issue from FAIL-001 | FAIL-001 | Active — applies whenever Windows expansion is revisited |

---

## 14. Relationship to Other SENTINEL Documents

| Document | Relationship |
|---|---|
| `architecture.md` | Documents the current implementation that failures may have shaped (e.g., the Linux-first v0.1 architecture) |
| `Requirements.md` | Reflects infrastructure decisions informed by past failures |
| `test-and-matrices.md` | Defines how future tests are executed; failed tests from that framework feed into this document |
| `detection-engineering.md` | Detection-specific failures (false positives/negatives) will be logged here once they occur |
| `incident-response.md` | Response failures encountered during future incident-response exercises will be logged here |
| `threat-modeling.md` | Threat-model assumptions that prove wrong in practice should be captured as lessons here |

This document is the shared destination for failure evidence surfaced by all of the above — it does not duplicate their methodology, only records what actually happened when that methodology was applied.

---

## 15. Maintenance

This document should be updated when:

- A real failure occurs anywhere in the project (infrastructure, telemetry, detection, investigation, response, or process).
- A corrective action is applied and its retest result becomes known.
- A previously "not determined" root cause is later confirmed.
- A lesson changes a standing assumption recorded elsewhere (e.g., in `threat-modeling.md`).
- A preventive action needs to be added, updated, or retired.

This document is **not** rewritten for cosmetic reasons or minor day-to-day activity — only for genuine, verified engineering failures and their resolution.

---

## 16. Current Status

**Verified failures logged:** 1 (FAIL-001 — Windows 11 endpoint boot failure, v0.1)

**Categories with no recorded failures yet:** Telemetry, Detection, False Positive, Investigation, Response, Mutation, Documentation, Process

**Next expected source of new entries:** v0.2 detection engineering and Linux telemetry work, once controlled testing begins and produces its first real results (successful or not).
