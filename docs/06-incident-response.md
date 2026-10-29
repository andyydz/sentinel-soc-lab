# SENTINEL Incident Response

> Does your detection still work when the attacker changes tactics?

This document defines how SENTINEL investigates and responds to a detected event. It is a **methodology document** — it describes the process SENTINEL follows, and separately, honestly tracks what has actually been exercised so far. Response work is meant to feed back into detection engineering: every incident should produce a lesson, and that lesson should be retested.

All timestamps in this document are IST (`+0530`).

---

## 1. Current State

**Environment:**

| Component | Details |
|---|---|
| SENTINEL-WAZUH | Ubuntu 24.04, Wazuh 4.14.8, `10.10.10.10` |
| SENTINEL-LINUX01 | Ubuntu 24.04, Wazuh Agent 4.14.8, `10.10.10.40`, Agent ID `002` |
| Lab network | `SENTINEL-LAB`, `10.10.10.0/24` (internal, isolated) |

**Confirmed:**
- Real-time File Integrity Monitoring is configured on SENTINEL-LINUX01 with `/home` as the configured monitoring scope. A configured scope does not guarantee that every change under the path is detected.
- Built-in Wazuh Rule 550 (Level 7, "Integrity checksum changed") was observed during the 11 October controlled modification test.
- Custom Wazuh Rule 100002 (Level 8) is confirmed to fire for the documented controlled modification scenarios — see `docs/05-detection-engineering.md`:
  - **11 October 2026:** `/home/sentinel-admin/sentinel-fim-validation.txt`, `2026-10-11T20:25:14.746+0530`. Supported by screenshot evidence; the original source alert record was not recovered during the later review.
  - **26 October 2026:** `/home/sentinel-admin/sentinel-v02-mod-test.txt`, two recorded Level 8 alerts at `2026-10-26T21:38:27.910+0530` (file size 0 → 23 bytes) and `2026-10-26T21:38:48.473+0530` (file size 23 → 61 bytes). These are two alerts from consecutive modifications of one file, not a repeatable regression suite. Screenshot: [October 26 controlled-modification source alerts](../evidence/v0.2/v0.2-oct26-controlled-modification-source-alerts-new.png).
  - These results do not establish complete FIM coverage or malicious activity. They were controlled lab tests, not real incidents.
- **Investigation `CASE-001`** (`investigations/CASE-001.md`) has started. Real FIM events, including Rule 550 and Rule 100002 event details, have been filtered and reviewed as a first investigation exercise. **Current assessment:**
  - CASE-001's modification-validation objective is closed for the scenarios tested. This is not the same as completing the investigation.
  - CASE-001 evidence reconciliation is closed for the reviewed scope.
  - **CASE-001 remains open overall.** Broader event review, timeline reconstruction, root-cause analysis, attribution, final conclusions, false-positive analysis, and detection tuning remain outstanding.
  - SENTINEL v0.3 is not complete.

**Reviewed source records from 16 October 2026** (controlled creation and deletion of `/home/sentinel-admin/sentinel-audit-test.txt`), reviewed from `/var/ossec/logs/alerts/2026/Oct/ossec-alerts-16.json`. This is a Wazuh runtime log; it is not claimed to be committed to the repository, and no repository path is claimed for it.
- **Creation:** built-in Rule 554 ("File added to the system") at `2026-10-16T11:40:06.007+0530`. Custom Rule 100002 is absent from the reviewed record.
- **Deletion:** built-in Rule 553 ("File deleted") at `2026-10-16T12:31:32.819+0530`. Custom Rule 100002 is absent from the reviewed record.
- These are reviewed source evidence of individual controlled actions. They are **not** successful validations of custom Rule 100002 for creation or deletion, and they are not a confirmed detection miss.
- Why Rule 100002 was absent from these records is **unresolved**, as is whether the custom rule is intended to cover creation and deletion. No cause is asserted.
- An earlier claim that Rules 554 and 100002 fired together during creation is unsupported by the reviewed source record. It is not treated as a result, and no explanation for it is offered.

**Rule configuration (unresolved):** a read-only inspection of `/var/ossec/etc/rules/local_rules.xml` on SENTINEL-WAZUH showed Rule 100002 with Level 8, parent `<if_sid>550</if_sid>`, a `file` field condition containing `/home/`, and group `sentinel_fim`. This establishes the on-disk definition at inspection time. It does not establish which version the running manager had loaded during the historical tests, and the exact matching behavior of the `/home/` condition is unverified. The parent dependency on Rule 550 is relevant context, not a root-cause analysis, and nothing here shows that Rule 100002 cannot fire for creation or deletion events. Rule 100002 has not been changed or tuned.

**Reported operational observation (not a security incident):** a Wazuh Manager startup reportedly timed out, and the Manager subsequently started after a lock directory was removed. The root cause is unconfirmed and is not inferred here. One graceful Manager/endpoint VM restart cycle was reported successful, with Agent `002` reconnecting; this single observation is not evidence of general resilience. Logs have not been independently reviewed or confirmed saved in the repository.

**What's not yet complete:**
- CASE-001's broader investigation: timeline, root cause, attribution, and final conclusions.
- Containment, eradication, or recovery — no exercise has been performed in this lab.
- Verification of the manager's current active rule configuration, and any reconstruction of its historical loaded configuration (which may not be recoverable).
- Verification of the `/home/` matching behavior, and resolution of why Rule 100002 was absent from the reviewed creation and deletion records.
- Broader false-positive/false-negative testing and tuning for Rule 100002.
- Response metrics — none have been measured.

Everything from Section 2 onward is the methodology SENTINEL follows. Where something has actually been done, it's labeled **verified**; everything else is **documented** (defined, but not yet exercised) or **planned**.

---

## 2. Incident Response Lifecycle

````mermaid
flowchart LR
    P[Preparation] --> DA[Detection & Analysis]
    DA --> C[Containment]
    C --> E[Eradication]
    E --> R[Recovery]
    R --> L[Lessons Learned]
    L -.-> P
````

| Phase | Objective | Status in SENTINEL |
|---|---|---|
| **Preparation** | Infrastructure, telemetry, and documented procedures are in place before an incident occurs | Partially complete — the Wazuh environment and FIM telemetry are available and Rule 100002 is confirmed to fire for the documented controlled modification scenarios; broader telemetry and repeatable validation remain outstanding (`docs/05-detection-engineering.md`) |
| **Detection & Analysis** | An alert or anomaly is triaged and investigated to determine scope and whether it's a real incident | In progress — CASE-001 is the first exercise of this phase; its modification-validation objective and reviewed-scope evidence reconciliation are closed, but the overall investigation remains open |
| **Containment** | Limit the spread or impact of confirmed malicious activity | Documented only — none has been exercised in the lab |
| **Eradication** | Remove the cause (persistence, malicious files, bad config) | Documented only — none has been exercised in the lab |
| **Recovery** | Restore normal operation and confirm monitoring/detection work again | Documented only — none has been exercised in the lab |
| **Lessons Learned** | Capture what worked, what didn't, and feed it back into detection engineering | Not yet exercised as a completed post-incident phase — no case has reached it |

This is the standard six-phase model SENTINEL will measure itself against as later milestones (v0.4+) are built out. The controlled tests documented above are validation exercises, not confirmed security incidents, and are treated as such throughout this document. Investigation (Detection & Analysis) and response (Containment onward) are distinct: the work done to date is investigation and detection validation only, and no response action has been performed.

---

## 3. Detection & Analysis — Telemetry and Evidence

Wazuh alerts and endpoint telemetry are the starting point for analysis, not a conclusion. A Wazuh alert — whether built-in Rule 550 or custom Rule 100002 — confirms that a rule matched a condition. It does not by itself confirm malicious intent, process attribution, who was responsible, or what else happened around it. Likewise, a built-in rule alert (for example Rules 554 and 553 in the reviewed 16 October records) does not establish whether custom Rule 100002 should cover the same event.

**Evidence sources currently available:** Wazuh FIM/Syscheck events from SENTINEL-LINUX01 (`/home` monitoring scope), including Rule 550 and the Rule 100002 output for the documented modification scenarios, which supports the CASE-001 investigation. The 16 October creation and deletion records were reviewed from the source alert record: built-in Rule 554 for creation and built-in Rule 553 for deletion, with custom Rule 100002 absent from each. Other telemetry (authentication, process execution, command context) is not yet configured — see `docs/05-detection-engineering.md` for current telemetry status. CASE-001 currently relies on FIM event data only.

**Analysis questions a triage/investigation step should answer:**

| Question | Notes |
|---|---|
| What happened? | Describe the observed event, not an assumed cause |
| Which asset, user, process, timestamp? | Fill in only what the telemetry actually supports |
| Is this expected, suspicious, or malicious? | A judgment call, not an automatic classification from the alert alone |
| What evidence is available vs. missing? | Document gaps as explicitly as findings |
| Does this warrant further investigation or escalation? | See Section 4 |

**Evidence handling:** every piece of evidence should be timestamped, traceable to its source, and preserved rather than overwritten. CASE-001 evidence and supporting artifacts are organized under `evidence/v0.3/`, with earlier pipeline/infrastructure evidence under `evidence/v0.2/`. The evidence level for each result is stated explicitly:
- **11 October:** screenshot-supported; the original source alert record was not recovered.
- **16 October:** reviewed from the source alert record at the Wazuh runtime log path documented in Section 1. Reviewing a source record is separate from storing it in the repository; the raw log is not claimed to be committed.
- **26 October:** the screenshot [October 26 controlled-modification source alerts](../evidence/v0.2/v0.2-oct26-controlled-modification-source-alerts-new.png) documents two Level 8 Rule 100002 alerts from consecutive modifications of one file. These are not two independent test cases or a regression suite.
- **Manager startup observation:** operational artifacts have not been confirmed as saved in the repository, and no evidence path is claimed.

Nothing sensitive (credentials, secrets, VM disks, large raw datasets) is committed alongside evidence.

---

## 4. Decision-Making and Escalation

Not every alert or anomaly needs the same depth of response. SENTINEL's escalation path:

````
Alert/Anomaly → Triage → [Escalate to full investigation?] → Investigation
   → [Confirmed malicious?] → Containment decision
````

- **Escalate to investigation** when triage can't rule out malicious activity from available context, or when the affected asset/data matters enough to be worth the time even if the activity is probably benign.
- **Escalate to containment** only once investigation has established enough confidence that inaction carries more risk than action — containment is not a default reaction to every alert, including a confirmed Rule 100002 alert.
- **Human review is required** before any destructive or disruptive action (isolating an endpoint, killing a process, reverting a snapshot) — this lab has no automated response, and any future automation must still include a human decision point here (Section 6).
- When evidence is genuinely ambiguous, the honest outcome is "unresolved, more telemetry needed" — not a forced conclusion in either direction.

---

## 5. Post-Incident Review and Detection Improvement

Every case that reaches this phase should answer: what happened, how it was detected, what evidence confirmed it, what was missed, and what should change. The core loop:

````
Incident → Lesson → Detection Improvement → Retest
````

This is the mechanism that connects incident response back to `docs/05-detection-engineering.md`: a gap found during investigation (missing telemetry, a rule that didn't fire, insufficient alert context) becomes a concrete engineering task, not just a note.

The reviewed 16 October records illustrate the distinction between reviewing evidence and drawing conclusions. In both, a built-in rule (554 for creation, 553 for deletion) appeared and custom Rule 100002 did not. That is a coverage question that may or may not turn out to be a gap; it is not established as a detection miss, and no root cause is asserted. The Rule 550 parent dependency is relevant context only. Reviewing these records closed their evidence reconciliation; it did not validate custom-rule coverage for creation or deletion, and it did not complete the investigation.

No case has completed the full post-incident review phase. CASE-001 is still in Detection & Analysis: its modification-validation objective and reviewed-scope evidence reconciliation are closed, but the case is open overall.

**Case report format** (used once a case is complete):

````markdown
# Case-XXX
## Incident Summary
## Severity
## Affected Assets
## Timeline
## Evidence
## Indicators of Compromise
## Investigation
## Root Cause
## Containment / Eradication / Recovery
## Lessons Learned
````

`investigations/CASE-001.md` is an investigation record documenting the controlled-validation work completed so far. It is not a completed incident report in the sense above — its broader timeline, root cause, attribution, and final conclusions remain open.

---

## 6. Future Plans

The following are planned and not yet implemented or exercised:

- Completing CASE-001: broader event review, false-positive analysis, detection tuning, timeline reconstruction, and a finished case report, without claiming a root cause or attribution that has not been established
- Verifying the manager's current active rule configuration, and determining whether its historical loaded configuration for the earlier tests can be reconstructed; the historical state may not be recoverable, in which case it remains unconfirmed
- Verifying the field-condition matching behavior of the `/home/` condition, and reviewing built-in Rules 550, 553, and 554 (see `docs/05-detection-engineering.md`)
- Investigating the custom-rule creation and deletion coverage question — whether Rule 100002 is intended to cover those events, and why it was absent from the reviewed records — without presuming a cause
- Reviewing and recording the reported Wazuh Manager startup observation and restart cycle through the project's failure/lessons documentation, with root cause treated as unconfirmed until evidence supports one
- A controlled containment exercise (e.g., isolating SENTINEL-LINUX01 or stopping a test process), followed later by eradication and recovery validation, including verifying detection/telemetry still work post-recovery
- Broader telemetry (authentication, process execution) to support richer investigations
- Response metrics (time to detect, time to triage, time to contain/respond) — no values exist yet
- Any response automation, which will always require a human decision point per Section 4
- Purple-team and attack-mutation connections (v0.5–v0.6): using incident response findings to test whether detections hold up against varied attacker behavior

None of the above are claimed as current capability — they're the direction this document and the lab are headed.

---

## 7. Related Documents

| Document | Role |
|---|---|
| `docs/04-threat-model.md` | Identifies the threats this process responds to |
| `docs/05-detection-engineering.md` | Detection methodology and current rule status (Rule 550, Rule 100002) |
| `docs/07-testing-and-metrics.md` | How results are tested and measured |
| `investigations/CASE-001.md` | The current SOC investigation case record |
| `evidence/v0.2/`, `evidence/v0.3/` | Evidence supporting CASE-001 and other work, organized by version |
````

I made no other changes. The 11 October result is still screenshot-supported, the 16 October results are still tied to the reviewed source record with the absence of Rule `100002` unresolved, and CASE-001 is open overall. No containment, eradication, recovery, or metrics are claimed, and the raw runtime log is not claimed to be committed.

I haven't verified that the linked screenshot exists at that path. The `../evidence/…` link only works because this file lives in `docs/`, so click it on GitHub after pushing.\
