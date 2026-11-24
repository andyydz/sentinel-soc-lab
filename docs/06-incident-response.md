# SENTINEL Incident Response

> Does your detection still work when the attacker changes tactics?

This document defines how SENTINEL investigates and responds to a detected event. It is a **methodology document**: it describes the process SENTINEL follows and, separately, honestly tracks what has actually been exercised so far. Response work is meant to feed back into detection engineering: every incident should produce a lesson, and that lesson should be retested.

All timestamps in this document are IST (`+0530`).

---

## 1. Current State

This section reflects the project state through v0.11. It describes what has been investigated and exercised; it does not claim that the full incident-response lifecycle has been implemented.

**Environment:**

| Component | Details |
|---|---|
| SENTINEL-WAZUH | Ubuntu 24.04, Wazuh 4.14.8, `10.10.10.10` |
| SENTINEL-LINUX01 | Ubuntu 24.04.5, Wazuh Agent 4.14.8, `10.10.10.40`, Agent ID `002` |
| Kali attacker-simulation host | `10.10.10.20` (used for the controlled SSH simulation) |
| Lab network | `SENTINEL-LAB`, `10.10.10.0/24` (internal, isolated) |
| Windows telemetry | Replayed EVTX/JSON Sysmon data only. There is **no live Windows endpoint and no Active Directory environment** |

### 1.1 Telemetry and detection picture

**Linux File Integrity Monitoring (FIM).** Real-time FIM is configured on SENTINEL-LINUX01 with `/home` as the configured monitoring scope. A configured scope does not guarantee that every change under the path is detected. Custom rules cover:

| Rule | Event type |
|---|---|
| `100002` | Modification |
| `100003` | Creation |
| `100004` | Deletion |

Their documented controlled tests are validation exercises. They do not establish complete FIM coverage, malicious activity, or a repeatable regression suite. Details are in [`docs/05-detection-engineering.md`](05-detection-engineering.md).

**SSH authentication.** A controlled SSH password-guessing simulation was run from Kali (`10.10.10.20`) against SENTINEL-LINUX01 and investigated as CASE-003:

- 21 failed authentication attempts were recorded over 2 minutes 46 seconds.
- Rule `100200` produced 21 Level 5 alerts.
- Rule `100201` produced one Level 10 escalation. Rule `100201` counts matching Rule `100200` events from the same source IP within its configured frequency window; it is not described here as counting a specific number of unique failed-password attempts.
- Manual investigation confirmed zero successful logins.
- Python-assisted triage prioritised the higher-severity alert.
- A source-scoped, manual containment procedure is documented (Section 4). It is documented only; this document does not claim it was applied as a containment exercise or left active.

**Windows Sysmon.** Windows Sysmon telemetry has been tested through EVTX replay (v0.4, CASE-002) and JSON replay (v0.9/v0.9.1) workflows. Replayed telemetry is not live endpoint monitoring, and no claim of live Windows detection is made.

**Python-assisted triage.** `python-soc-automation` is a separate companion project. It parses Wazuh alert JSON and supports severity-based triage. It is not a native Wazuh feature and not a production SOAR platform, and it does not automatically perform containment, eradication, or recovery.

### 1.2 Investigations

| Case | Scope | Status |
|---|---|---|
| [`CASE-001`](../investigations/CASE-001.md) | Controlled Linux FIM investigation (Rule 550, Rule 100002 and related events) | **Closed on 18 November 2026 for its reviewed scope.** SENTINEL v0.3 is complete |
| `CASE-002` | Windows Sysmon EVTX replay detection (v0.4) | Replay-based; see the case record |
| `CASE-003` | Controlled SSH password-guessing simulation (v0.5) | See Section 1.1 and the case record |
| `CASE-004` | Attack mutation and noise-filtering observations (v0.7) | See the case record |

Closing CASE-001 is distinct from completing all future detection engineering. Post-closeout engineering, validation, tuning, and historical evidence-recovery work remains open (Section 6), and those follow-up tasks do not reopen CASE-001. Closure applies to the reviewed scope only and is not a claim of full FIM coverage, attribution of any real malicious activity, or completed tuning.

### 1.3 Milestone context

| Milestone | Relevance to incident response |
|---|---|
| v0.3 | CASE-001 FIM investigation closed for its reviewed scope |
| v0.4 | Windows Sysmon EVTX replay detection (CASE-002) |
| v0.5 | SSH detection, investigation, and Python-assisted triage (CASE-003) |
| v0.6 | Controlled purple-team measurements; small sample sizes limit what can be concluded |
| v0.7 | Attack mutation and noise-filtering observations (CASE-004) |
| v0.8 | FIM exclusions and group isolation; residual noise and broader retesting remain outstanding |
| v0.9 / v0.9.1 | Sysmon JSON replay and Python triage integration |
| v0.10 | Live Linux FIM probe with Python-assisted triage; the evidence archive was external to the repository |
| v0.11 | Evidence committed to the repository; reconciliation still pending |

### 1.4 v0.11 evidence summary

- 10 filtered alert records.
- Three custom FIM rules represented.
- Three controlled probe events: creation, modification, and deletion of one file.
- Seven additional desktop/configuration-path records whose origin and benign status are **not conclusively established**. They are not described here as confirmed benign noise.
- Triage process, target-process, and event-time enrichment fields are `None`.
- The on-disk rule XML does not by itself prove which exclusions the manager had loaded when those events occurred.
- The aggregate regression summary is not proof of a completed regression suite.

### 1.5 Earlier reviewed source records and findings

These historical records are retained with their original evidence qualifications.

**Controlled modification tests (Rule 100002):**
- **11 October 2026:** `/home/sentinel-admin/sentinel-fim-validation.txt`, `2026-10-11T20:25:14.746+0530`. Built-in Rule 550 (Level 7, "Integrity checksum changed") was observed. Supported by screenshot evidence; the original source alert record was not recovered during the later review.
- **26 October 2026:** `/home/sentinel-admin/sentinel-v02-mod-test.txt`, two recorded Level 8 alerts at `2026-10-26T21:38:27.910+0530` (file size 0 → 23 bytes) and `2026-10-26T21:38:48.473+0530` (file size 23 → 61 bytes). These are two alerts from consecutive modifications of one file, not a repeatable regression suite. Screenshot: [October 26 controlled-modification source alerts](../evidence/v0.2/screenschots/v0.2-oct26-controlled-modification-source-alerts-new.png).

**16 October 2026 records** (controlled creation and deletion of `/home/sentinel-admin/sentinel-audit-test.txt`), reviewed from `/var/ossec/logs/alerts/2026/Oct/ossec-alerts-16.json`. This is a Wazuh runtime log; it is not claimed to be committed to the repository, and no repository path is claimed for it.
- **Creation:** built-in Rule 554 ("File added to the system") at `2026-10-16T11:40:06.007+0530`. Custom Rule 100002 is absent from the reviewed record.
- **Deletion:** built-in Rule 553 ("File deleted") at `2026-10-16T12:31:32.819+0530`. Custom Rule 100002 is absent from the reviewed record.
- These are reviewed source evidence of individual controlled actions. They are not validations of Rule 100002 for creation or deletion and not a confirmed detection miss. Why Rule 100002 was absent is unresolved, and no cause is asserted. An earlier claim that Rules 554 and 100002 fired together during creation is unsupported by the reviewed source record and is not treated as a result.

**Rule configuration (unresolved):** a read-only inspection of `/var/ossec/etc/rules/local_rules.xml` on SENTINEL-WAZUH showed Rule 100002 with Level 8, parent `<if_sid>550</if_sid>`, a `file` field condition containing `/home/`, and group `sentinel_fim`. This establishes the on-disk definition at inspection time. It does not establish which version the running manager had loaded during the historical tests, and the exact matching behavior of the `/home/` condition remains unverified. The parent dependency on Rule 550 is relevant context, not a root-cause analysis.

**Reported operational observation (not a security incident):** a Wazuh Manager startup reportedly timed out, and the Manager subsequently started after a lock directory was removed. The root cause is unconfirmed and is not inferred here. One graceful Manager/endpoint VM restart cycle was reported successful, with Agent `002` reconnecting; this single observation is not evidence of general resilience. Logs have not been independently reviewed or confirmed saved in the repository.

### 1.6 What is not yet complete

- Reconciliation of the v0.11 evidence.
- Verification of the manager's current active rule configuration, and any reconstruction of its historical loaded configuration (which may not be recoverable).
- Verification of the `/home/` matching behavior and the unresolved 16 October question above.
- Broader FIM noise-suppression retesting and a repeatable regression suite.
- Broader SSH testing, including legitimate authentication activity.
- Further Sysmon replay mutation testing and eventual live Windows validation.
- A controlled containment exercise; eradication and recovery validation. No such exercise has been performed in this lab.
- Response metrics. None have been measured.
- Any automated response. None is implemented.

Everything from Section 2 onward is methodology. Where something has actually been done it is labeled **verified**; everything else is **documented** (defined, but not yet exercised) or **planned**.

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
| **Preparation** | Infrastructure, telemetry, and documented procedures are in place before an incident occurs | Partially complete. Wazuh, Linux FIM (Rules 100002–100004), SSH detection (Rules 100200/100201), and replayed Sysmon telemetry are available. Live Windows telemetry, repeatable regression testing, and residual FIM noise handling remain outstanding ([`docs/05-detection-engineering.md`](05-detection-engineering.md)) |
| **Detection & Analysis** | An alert or anomaly is triaged and investigated to determine scope and whether it is a real incident | **Exercised** through controlled investigations: CASE-001 (FIM, closed for its reviewed scope), CASE-003 (SSH detection, Python-assisted triage, manual investigation confirming zero successful logins), plus replay-based CASE-002 and CASE-004 work. All were controlled lab activity, not real incidents |
| **Containment** | Limit the spread or impact of confirmed malicious activity | **Documented only.** A source-scoped manual procedure exists for CASE-003; it is not claimed to have been applied or left active. No containment exercise has been performed |
| **Eradication** | Remove the cause (persistence, malicious files, bad config) | Documented only. None has been exercised in the lab |
| **Recovery** | Restore normal operation and confirm monitoring/detection work again | Documented only. The CASE-003 SSH service verification is not treated as a recovery phase exercise |
| **Lessons Learned** | Capture what worked, what did not, and feed it back into detection engineering | Applied informally to detection engineering (for example, v0.7–v0.8 noise-filtering work). Not yet exercised as a completed post-incident phase following containment and recovery |

This is the standard six-phase model SENTINEL measures itself against. Investigation (Detection & Analysis) and response (Containment onward) are distinct: the work done to date is investigation and detection validation, and no response action has been completed as an exercise. No automated containment or response is implemented, and no response-time metrics have been measured.

---

## 3. Detection & Analysis: Telemetry and Evidence

Wazuh alerts and endpoint telemetry are the starting point for analysis, not a conclusion. An alert, whether a built-in rule (for example 550, 553, 554) or a custom rule (100002–100004, 100200, 100201), confirms that a rule matched a condition. It does not by itself confirm malicious intent, process attribution, who was responsible, or what else happened around it. Likewise, a built-in rule alert does not establish whether a custom rule should cover the same event.

**Evidence sources currently available:**
- Wazuh FIM/Syscheck events from SENTINEL-LINUX01 (`/home` scope), including built-in rules and custom Rules 100002–100004.
- SSH authentication events from SENTINEL-LINUX01 feeding Rules 100200 and 100201.
- Replayed Windows Sysmon telemetry (EVTX and JSON). This is replay, not live monitoring.
- Python-assisted triage output from the `python-soc-automation` companion project, which parses Wazuh alert JSON. Its enrichment is limited: in the v0.11 evidence, process, target-process, and event-time enrichment fields are `None`.

Process execution and command context telemetry from a live endpoint is not configured; see [`docs/05-detection-engineering.md`](05-detection-engineering.md) for current telemetry status.

**Analysis questions a triage/investigation step should answer:**

| Question | Notes |
|---|---|
| What happened? | Describe the observed event, not an assumed cause |
| Which asset, user, process, timestamp? | Fill in only what the telemetry actually supports |
| Is this expected, suspicious, or malicious? | A judgment call, not an automatic classification from the alert alone. Legitimate activity (for example, normal SSH logins or desktop configuration writes) must be considered |
| What evidence is available vs. missing? | Document gaps as explicitly as findings |
| Does this warrant further investigation or escalation? | See Section 4 |

**Evidence handling:** every piece of evidence should be timestamped, traceable to its source, and preserved rather than overwritten. The evidence level for each result is stated explicitly:
- **11 October:** screenshot-supported; the original source alert record was not recovered.
- **16 October:** reviewed from the source alert record at the Wazuh runtime log path in Section 1.5. Reviewing a source record is separate from storing it in the repository; the raw log is not claimed to be committed.
- **26 October:** screenshot [October 26 controlled-modification source alerts](../evidence/v0.2/screenschots/v0.2-oct26-controlled-modification-source-alerts-new.png) documents two Level 8 Rule 100002 alerts from consecutive modifications of one file; they are not independent test cases.
- **v0.10:** the live Linux FIM probe evidence archive was external to the repository.
- **v0.11:** the filtered evidence was committed to the repository (`evidence/v0.11/`); reconciliation is pending, and the seven desktop/configuration-path records are unresolved.
- **Manager startup observation:** operational artifacts have not been confirmed as saved in the repository, and no evidence path is claimed.

Evidence is organized by version under `evidence/` (for example [`evidence/v0.2/`](../evidence/v0.2/), [`evidence/v0.3/`](../evidence/v0.3/), `evidence/v0.11/`). Nothing sensitive (credentials, secrets, VM disks, large raw datasets) is committed alongside evidence.

---

## 4. Decision-Making and Escalation

Not every alert or anomaly needs the same depth of response. SENTINEL's escalation path:

````
Alert/Anomaly → Triage → [Escalate to full investigation?] → Investigation
   → [Confirmed malicious?] → Containment decision
````

- **Escalate to investigation** when triage cannot rule out malicious activity from available context, or when the affected asset or data matters enough to be worth the time even if the activity is probably benign. In CASE-003, the Level 10 Rule 100201 escalation was prioritised over the 21 Level 5 Rule 100200 alerts, and manual investigation then checked for successful logins.
- **Escalate to containment** only once investigation has established enough confidence that inaction carries more risk than action. Containment is not a default reaction to every alert, including a Level 10 escalation.
- **Containment scope:** the documented CASE-003 procedure is manual and source-scoped, limited to the offending source IP rather than broad network or host changes. It is a procedure, not a record of an action taken.
- **Human review is required** before any destructive or disruptive action (isolating an endpoint, blocking a source, killing a process, reverting a snapshot). This lab has no automated response, and any future automation must still include a human approval point (Section 6). Python-assisted triage prioritises alerts; it does not act on them.
- When evidence is genuinely ambiguous, the honest outcome is "unresolved, more telemetry needed", not a forced conclusion in either direction.

---

## 5. Post-Incident Review and Detection Improvement

Every case that reaches this phase should answer: what happened, how it was detected, what evidence confirmed it, what was missed, and what should change. The core loop:

````
Incident → Lesson → Detection Improvement → Retest
````

This connects incident response back to [`docs/05-detection-engineering.md`](05-detection-engineering.md): a gap found during investigation (missing telemetry, a rule that did not fire, noisy alerts, insufficient alert context) becomes a concrete engineering task, not just a note. Examples of this loop in the project so far include the creation/deletion coverage question that led to Rules 100003 and 100004, and the v0.7–v0.8 noise-filtering observations that led to FIM exclusions and group isolation.

The reviewed 16 October records illustrate the distinction between reviewing evidence and drawing conclusions. In both, a built-in rule (554 for creation, 553 for deletion) appeared and custom Rule 100002 did not. That is a coverage question that is not established as a detection miss, and no root cause is asserted. Reviewing these records closed their evidence reconciliation; it did not establish why Rule 100002 was absent.

**Closing a case versus continuing engineering.** CASE-001 was closed on 18 November 2026 for its reviewed scope. Follow-up engineering, validation, tuning, and historical evidence-recovery work is tracked separately (Section 6) and does not reopen the case. No case has yet completed a post-incident review that includes exercised containment, eradication, and recovery.

**Case report format** (used for completed case reports):

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

Case records under `investigations/` document controlled-validation work. They record what was investigated and concluded for the reviewed scope; they are not reports of real incidents, and sections such as Containment / Eradication / Recovery must not be read as describing actions that were not performed.

---

## 6. Future Plans

The following are outstanding, planned, and **not implemented or not yet exercised**:

- Reconciling the v0.11 evidence, including the origin and benign status of the seven desktop/configuration-path records and the empty enrichment fields.
- Verifying the manager's current active rule configuration, and determining whether the historical loaded configuration for earlier tests can be reconstructed where evidence permits; it may not be recoverable and then remains unconfirmed.
- Verifying the `/home/` field-condition matching behavior and reviewing built-in Rules 550, 553, and 554 (see [`docs/05-detection-engineering.md`](05-detection-engineering.md)).
- Broader FIM noise-suppression retesting and a repeatable regression suite.
- Broader SSH testing, including legitimate authentication activity, to examine false positives for Rules 100200 and 100201.
- Further Sysmon replay mutation testing and, eventually, live Windows validation.
- A controlled containment exercise (for example, a source-scoped block for the SSH scenario, or isolating SENTINEL-LINUX01), followed by eradication and recovery validation, including confirming detection and telemetry still work post-recovery.
- Reviewing and recording the reported Wazuh Manager startup observation and restart cycle through the project's failure/lessons documentation, with root cause treated as unconfirmed until evidence supports one.
- Response metrics (time to detect, time to triage, time to contain/respond). No values exist yet.
- Carefully controlled future response automation, always with a human approval point per Section 4.
- Using incident response findings in further purple-team and attack-mutation testing to check whether detections hold up against varied attacker behavior.

None of the above are claimed as current capability. They describe the direction of this document and the lab, and nothing here should be read as production readiness.

---

## 7. Related Documents

| Document | Role |
|---|---|
| [`docs/04-threat-model.md`](04-threat-model.md) | Identifies the threats this process responds to |
| [`docs/05-detection-engineering.md`](05-detection-engineering.md) | Detection methodology and current rule status (Rules 550, 100002–100004, 100200, 100201) |
| [`docs/07-testing-and-metrics.md`](07-testing-and-metrics.md) | How results are tested and measured |
| [`investigations/CASE-001.md`](../investigations/CASE-001.md) | FIM investigation, closed 18 November 2026 for its reviewed scope |
| `investigations/CASE-002.md` | Windows Sysmon EVTX replay case |
| `investigations/CASE-003.md` | SSH password-guessing simulation case |
| `investigations/CASE-004.md` | Attack mutation and noise-filtering case |
| [`evidence/v0.2/`](../evidence/v0.2/) | Pipeline/infrastructure evidence, including the October 26 screenshot |
| [`evidence/v0.3/`](../evidence/v0.3/) | CASE-001 evidence and supporting artifacts |
| `evidence/v0.11/` | Evidence committed for the v0.11 live FIM probe |
