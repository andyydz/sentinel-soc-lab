# SENTINEL Testing & Metrics

> Does your detection still work when the attacker changes tactics?

This document defines how SENTINEL proves its detections actually work — not just that a rule exists — and tracks what has genuinely been tested so far. **"Configured" does not mean "validated."** A control only counts as validated once it has been tested against controlled activity in the lab and the result has been documented, whether that result is a pass, a fail, or an inconclusive outcome. Validation is always scoped to the specific scenario tested. **Reviewing evidence is also different from validating coverage:** a reviewed record documents what happened in one controlled action; it does not, by itself, show that a detection covers that event type.

This is a testing and measurement document. Detection design and implementation are covered separately in `docs/05-detection-engineering.md`; this document focuses on how results are tested, compared, and measured.

All timestamps in this document are IST (`+0530`).

---

## 1. Testing Methodology

Every test in SENTINEL follows the same workflow:

```
Define the test → Establish expected results → Execute a controlled test →
Observe actual results → Compare outcomes → Record evidence → Fix and retest
```

| Stage | What happens |
|---|---|
| Define the test | State what's being tested and why |
| Establish expected results | Write down the expected outcome *before* running the test |
| Execute | Run the controlled activity in the isolated lab |
| Observe | Capture what actually happened |
| Compare | Check actual results against the expected results |
| Record evidence | Save proof — screenshots, logs, alert output — regardless of outcome |
| Fix and retest | If it failed or was incomplete, address the cause and run it again |

**Successful, failed, and inconclusive tests are different things:**

- **Successful** — the expected telemetry and alert were both observed, matching what was defined up front.
- **Failed** — the expected behavior did not occur. This is recorded and investigated, not hidden.
- **Inconclusive** — part of the expected chain was confirmed, but the specific thing under test was not. This label exists so a partial result is never overstated as a pass.

---

## 2. Current Testing Evidence

**Scope of this section:** The evidence below covers the October 2026 FIM testing and CASE-001 only. Controlled testing in other cases — CASE-002 (Windows Sysmon `.evtx` replay and custom detection-rule validation), CASE-003 (controlled SSH password-guessing simulation, detection, Python triage and manual investigation) and CASE-004 (controlled FIM, Sysmon mutation/evasion and SSH threshold testing) — is documented separately. Those results are not merged into the October evidence tables here, and statements below about what has or has not been tested apply to the FIM/CASE-001 scope unless they say otherwise.

**Environment:**

| Component | Details |
|---|---|
| SENTINEL-WAZUH | Wazuh 4.14.8, `10.10.10.10` |
| SENTINEL-LINUX01 | Wazuh Agent 4.14.8, `10.10.10.40`, Agent ID `002` |
| Lab network | `SENTINEL-LAB`, `10.10.10.0/24` |

**What's actually been verified:**

| Item | Status |
|---|---|
| Wazuh Manager ↔ SENTINEL-LINUX01 communication | Verified |
| Real-time File Integrity Monitoring with `/home` as the configured monitoring scope | Configured; telemetry observed in the documented controlled tests. Complete coverage of the configured scope has not been established. |
| Built-in Wazuh Rule 550 (Level 7, "Integrity checksum changed") | Observed during the 11 October controlled modification test (screenshot-supported) |
| Custom Rule 100002 (Level 8) | **Confirmed to fire for the documented controlled modification scenarios** (below). Not generalized beyond them. |
| Custom Rules 100003 (creation) and 100004 (deletion), Level 8 | **Observed, not validated.** Each was observed once on 31 October 2026 (below), with the trigger origin unestablished. Not combined with the Rule 100002 controlled modification results. |

**Evidence by date.** Each result is limited to its own test and evidence level:

| Date | Action and file | Result | Evidence level |
|---|---|---|---|
| 11 October 2026 | Controlled **modification** of `/home/sentinel-admin/sentinel-fim-validation.txt` | Custom Rule 100002, Level 8, at `2026-10-11T20:25:14.746+0530` | Supported by screenshot evidence. The original source alert record was not recovered during the later review, so this result is not source-log verified. |
| 16 October 2026 | Controlled **creation** of `/home/sentinel-admin/sentinel-audit-test.txt` | Built-in Rule 554 at `2026-10-16T11:40:06.007+0530`. Custom Rule 100002 is **absent** from the reviewed record. | Reviewed from the source alert record at `/var/ossec/logs/alerts/2026/Oct/ossec-alerts-16.json`. This document does not claim the raw log is committed to the repository. |
| 16 October 2026 | Controlled **deletion** of the same file | Built-in Rule 553 at `2026-10-16T12:31:32.819+0530`. Custom Rule 100002 is **absent** from the reviewed record. | Same reviewed source alert record. |
| 26 October 2026 | Controlled **modification** of `/home/sentinel-admin/sentinel-v02-mod-test.txt` | Two custom Rule 100002 Level 8 alerts: `2026-10-26T21:38:27.910+0530` (file size 0 → 23 bytes) and `2026-10-26T21:38:48.473+0530` (file size 23 → 61 bytes) | Recorded alerts from two consecutive modifications of one file, not a repeatable regression suite. Screenshot: [October 26 controlled-modification source alerts](../evidence/v0.2/screenschots/v0.2-oct26-controlled-modification-source-alerts-new.png). |
| 31 October 2026 | **Observed** file creation under `/home/sentinel-admin/snap/firmware-updater/262/.config/bus/`; not established as a controlled test | Custom Rule 100003, Level 8, at approximately 18:51:56 IST | One terminal screenshot supports this and the deletion observation below: [FIM lifecycle custom detections](../evidence/v0.3/screenshots/v0.3-fim-lifecycle-custom-detections.png). It is not a raw alert record; raw alert records are not committed. |
| 31 October 2026 | **Observed** file deletion under the same directory; not established as a controlled test | Custom Rule 100004, Level 8, at approximately 18:51:56 IST | Same single terminal screenshot. |

Full detail is documented in `investigations/CASE-001.md` and `investigations/fim-rule-100002-investigation.md`, with evidence under `evidence/v0.3/` and initial telemetry-pipeline evidence under `evidence/v0.2/`.

**How to read these results:**

- The two 26 October alerts are two recorded alert events from two consecutive modifications of one file. They are not necessarily two independent test cases and are not a regression suite.
- The 11 and 26 October results show that Rule 100002 fires for the documented controlled modification scenarios. They do not show coverage of other paths, file types, or event types.
- The 16 October creation and deletion records are reviewed evidence. They are **not** successful validations of custom Rule 100002 for creation or deletion, and neither is counted toward any metric in Section 3.
- Why Rule 100002 was absent from those two records is **unresolved**. It is an open custom-rule coverage question — not a confirmed detection miss and not an established root cause. Both events were alerted by built-in rules.
- An earlier claim that Rules 554 and 100002 fired together during creation is unsupported by the reviewed source record. It is not treated as a result, and no cause for the earlier claim is asserted.
- The 31 October Rule 100003 and 100004 alerts are **observations, not controlled tests and not validated detections**. Each was observed once, which shows the rule fired in that instance only; it does not establish repeatability or behavior for other paths, file types or events. The paths are in an application configuration directory, and whether the events were deliberately triggered or ordinary application activity has not been established. Process attribution and root cause are unestablished, and the definitions and matching behavior of Rules 100003 and 100004 have not been reviewed. They are not counted as successful controlled test executions.
- The 11, 16, 26 and 31 October results come from separate sessions. They do not constitute one end-to-end lifecycle test, and no claim is made that all three custom rules passed a single lifecycle test. Rule 100002 is not claimed to handle creation or deletion.
- Why custom Rules 100003 and 100004 were observed on 31 October when built-in Rules 554 and 553 were the rules shown in the reviewed 16 October records is **unresolved**; no explanation is asserted.

**Rule 550 dependency and rule configuration (unresolved):** a read-only inspection of the on-disk `local_rules.xml` on SENTINEL-WAZUH showed Rule 100002 at Level 8, group `sentinel_fim`, with parent `<if_sid>550</if_sid>` and a `file` field condition containing `/home/`. The parent dependency is relevant context, but this is not a root-cause analysis. The inspection shows the file as it was at inspection time; it does not establish which version the running manager had loaded during the historical tests. The exact matching semantics of the `/home/` condition remain unverified. The rule has not been changed. This inspection covers Rule 100002 only; the definitions of Rules 100003 and 100004 are not documented here.

**Evidence reconciliation:** CASE-001 was closed on 18 November 2026 for the reviewed scope, and the SENTINEL v0.3 evidence milestone is complete. That closure covers the evidence reviewed in that scope. It does not resolve the historical discrepancies described in this document (including the unresolved Rule 100002 creation and deletion question), and it does not establish comprehensive FIM coverage. Historical discrepancies and broader detection-engineering tasks remain separate follow-up work (Section 6).

**Scope of results:**

- Nothing here establishes complete FIM coverage of the configured `/home` scope. A configured monitoring scope does not guarantee that every change under the path is detected.
- The 16 October records do **not** confirm creation or deletion coverage for Rule 100002.
- The 31 October observations do **not** validate Rules 100003 or 100004.
- Nothing in the October evidence documented here confirms behavior under false-positive conditions (legitimate activity within the `/home` scope).
- Nothing in the October evidence documented here confirms behavior under false-negative conditions beyond the scenarios above.
- The 11, 16 and 26 October events were controlled lab actions. The 31 October alerts are observations of unestablished origin. None of these records, by themselves, establishes malicious activity.

Within the historical CASE-001/October FIM testing scope documented in this section, no controlled attack scenario, response action, or repeatable regression/mutation test was executed. This statement is limited to that scope: controlled attack, mutation and detection testing in CASE-002, CASE-003 and CASE-004 is documented separately and is not summarized here. Response-engineering and broader detection-engineering work remain outstanding as follow-up work, separate from the CASE-001 closure (Section 6).

---

## 3. Metrics Framework

The statuses below describe the October FIM/CASE-001 evidence documented in this file. They are not project-wide statements: results from CASE-002, CASE-003 and CASE-004 are documented in those cases and are not counted in this table.

| Metric | What it measures | Status |
|---|---|---|
| Detection Rate / Coverage | Successful detections ÷ applicable test executions | Not measured — the documented modification alerts are recorded events, not a defined set of applicable test executions; the 16 October reviewed records and the 31 October observations are not counted; no rate is calculated |
| Missed Detections | Malicious test activity that should have triggered a detection but didn't | Not measured — the absence of Rule 100002 from the reviewed creation and deletion records is an open coverage question, not a confirmed miss |
| False-Positive Rate | Legitimate activity incorrectly flagged ÷ applicable benign events tested | Not measured in the FIM/CASE-001 evidence documented here — no false-positive testing is documented in this file |
| Mean Time to Detect (MTTD) | Time between activity occurring and a detection firing | Not measured |
| Mean Time to Respond (MTTR) | Time between a confirmed detection and a response action | Not measured in the FIM/CASE-001 scope — no response action or response-time measurement is documented here; broader response engineering remains outstanding |
| Detection-Rule Validation Status | Whether a specific rule has passed its full test lifecycle (not just syntax check) | Rule 100002: **confirmed to fire for the documented controlled modification scenarios only**. Creation and deletion by Rule 100002: not validated — reviewed records show built-in Rules 554 and 553 with Rule 100002 absent; open coverage question. Rules 100003 (creation) and 100004 (deletion): **observed once each on 31 October 2026, not validated** — trigger origin unestablished, definitions not reviewed, and not counted as controlled test executions. Within the October FIM/CASE-001 evidence documented here, no false-positive/false-negative suite, repeatable FIM regression suite, or FIM tuning result is documented. |
| MITRE ATT&CK Coverage | Proportion of relevant techniques with a validated, mapped detection | Candidate/contextual mappings documented in rule/detection/case files; replay/test scope boundaries apply |

No numerical values are reported above, because the October FIM/CASE-001 evidence documented here is not enough to support a rate or trend, and none are calculated from the October records. The 31 October observations are not used to calculate any rate. As more scenarios are tested, this table will be populated with real figures — never estimated or interpolated ones.

---

## 4. Evidence and Reproducibility

Every test should leave behind enough to reproduce it later: the exact procedure, the expected outcome (written before execution), the actual outcome, a timestamp, and supporting artifacts — a screenshot, a relevant log excerpt, or alert output.

Evidence for the Rule 100002 results and CASE-001 is stored under `evidence/v0.3/`; earlier infrastructure/telemetry-pipeline evidence is under `evidence/v0.2/`. This document references those paths without restating their contents — the evidence directories themselves are the source of truth for what was actually captured.

**Evidence level by date:**

- **11 October 2026:** supported by screenshot evidence. The original source alert record was not recovered, so the result is not source-log verified.
- **16 October 2026:** reviewed from the source alert record at `/var/ossec/logs/alerts/2026/Oct/ossec-alerts-16.json`. This is a Wazuh runtime log on the manager; it is not claimed here to be committed to the repository, and no repository path is claimed for it. Reviewing a source record is separate from storing it as a repository artifact.
- **26 October 2026:** the screenshot [October 26 controlled-modification source alerts](../evidence/v0.2/screenschots/v0.2-oct26-controlled-modification-source-alerts-new.png) documents two custom Rule 100002 Level 8 alerts from consecutive modifications of one file (the alerts are listed in Section 2). These are not independent test cases or a regression suite.
- **31 October 2026:** the screenshot [FIM lifecycle custom detections](../evidence/v0.3/screenshots/v0.3-fim-lifecycle-custom-detections.png) is a single terminal screenshot showing the Rule 100003 and Rule 100004 alerts. A screenshot shows only what is visibly captured; it is **not a raw alert record**, and raw alert records for 31 October are not committed to the repository. It does not establish the trigger, process attribution, root cause, or repeatability.

Screenshots and source records are different levels of evidence, and claims should state which level supports them. Evidence is never edited to make a failed or inconclusive test look like a pass. If a result changes on retest, both the original and the retest are kept on record.

---

## 5. Lessons and Limitations

A few distinctions matter enough to call out directly:

- **Tool availability is not agent connectivity.** Wazuh being installed and running doesn't mean an agent is enrolled and reporting.
- **Agent connectivity is not telemetry validation.** An active agent doesn't guarantee the specific telemetry a detection needs is actually being generated or collected correctly.
- **A rule passing syntax validation is not a validated detection — and a validated scenario is not complete coverage.** A syntax check establishes only that the configuration is syntactically valid. Rule 100002 moved from "syntax-valid only" to "confirmed firing" for the documented controlled modification scenarios — a real step forward, but a narrow one.
- **An observed alert is not a validated detection.** Rules 100003 and 100004 were each observed once on 31 October 2026, under an application configuration path, without an established trigger and from a single terminal screenshot. That shows each rule fired in that instance. Validation requires a controlled test with an expected outcome written in advance.
- **Reviewing evidence is not validating coverage.** The 16 October creation and deletion records were reviewed at source level, and each shows a built-in rule with Rule 100002 absent. Reviewing them clarified what happened; it does not establish that Rule 100002 covers creation or deletion, or why it was absent.
- **A built-in rule alert is not a custom rule alert.** The reviewed creation record showed built-in Rule 554 and the reviewed deletion record showed built-in Rule 553; custom Rule 100002 was absent from both. Rule 100002's documented parent dependency is `<if_sid>550</if_sid>`; Rules 553 and 554 are not its parent rules. A built-in alert for one FIM event type should not be read as coverage by the custom rule.
- **On-disk configuration is not historical runtime configuration.** The inspected `local_rules.xml` does not establish what the manager had loaded during earlier tests.
- **A few recorded alerts are not a regression suite.** Recorded alerts from one file, or one execution per scenario, are not documented, repeatable tests that can be rerun after a rule change. Overstating this would make every other claim in this document less trustworthy.

---

## 6. Future Plans

**Already completed in other cases (documented separately; not part of the October FIM evidence above and not repeated here):** CASE-002 (Windows Sysmon `.evtx` replay and custom detection-rule validation), CASE-003 (controlled SSH password-guessing simulation, detection, Python triage and manual investigation) and CASE-004 (controlled FIM, Sysmon mutation/evasion and SSH threshold testing). Authentication activity, process execution and attack mutation/evasion have therefore already been tested in those cases; the items below are the work that remains.

The following are planned and **not yet completed**:

- Verifying the manager's current active rule configuration, and determining whether the historical loaded configuration for the earlier tests can be reconstructed; the historical state may not be recoverable, in which case it remains unconfirmed
- Verifying the field-condition matching behavior of the `/home/` condition, and reviewing built-in Rules 550, 553, and 554
- Investigating the custom-rule creation and deletion coverage question — whether Rule 100002 is intended to cover those events, and why it was absent from the reviewed records — without presuming a cause
- Reviewing the definitions and matching behavior of custom Rules 100003 and 100004 (read-only), followed by dedicated controlled creation and deletion tests using dedicated test files, with explicit expected outcomes written in advance, before assigning either rule validated status
- Repeatable, documented FIM creation, modification, and deletion test procedures, with expected results written in advance, so they can serve as FIM regression tests
- False-positive testing against legitimate activity and false-negative testing against controlled scenarios expected to trigger the custom FIM rules within the configured /home scope.
- Tuning the custom FIM rules based on the above, only after review and approval, and retesting after any change
- Response-engineering work, which remains outstanding as follow-up separate from the closed CASE-001 investigation
- Broader telemetry coverage beyond the authentication (SSH) and process-execution (Sysmon) testing already documented in CASE-002 and CASE-003
- Further repeatable, documented detection test scenarios beyond those already documented in CASE-001 through CASE-004
- Completing and validating MITRE ATT&CK mappings for implemented detections, building on the candidate/contextual mappings already documented
- A fuller purple-team cycle (red/blue/purple loop) and further attack mutation scenarios, beyond the controlled FIM, Sysmon mutation/evasion and SSH threshold testing already documented in CASE-004
- Before-and-after comparisons following detection tuning, where applicable and once a detection has actually been tuned

These remaining items are labeled planned or unresolved because they have not yet produced a documented result — this section exists so the roadmap stays visible without being mistaken for current capability. Completed work in other cases is listed above and is not part of this roadmap.

---

## 7. Post-Closeout Validation: v0.10 Live Linux FIM & Python Triage Integration

This section records post-closeout validation of live Linux File Integrity Monitoring (FIM) alert triage using `python-soc-automation` `v1.0` (commit `9696707`) on alerts generated by `sentinel-linux01` (`10.10.10.40`, agent `002`) and processed on `SENTINEL-WAZUH` (`10.10.10.10`). It is separate from `v0.9` (Sysmon JSON replay) and does not close open FIM noise-tuning items.

**Workflow clarification:** The FIM events were generated through a live probe on the Linux endpoint. Wazuh generated the resulting alerts and the alert JSON was exported. That exported JSON was then processed separately using the Python SOC Automation CLI. This was a file-based validation workflow. It was not a live Wazuh API integration, a continuous pipeline, a SOAR workflow, or an automated response system.

### Probe Execution & Archived Evidence
- **Monitored Scope & Rules:** Real-time `/home` (`inotify`) FIM tested with `/home/sentinel-admin/.fim_probe_test.txt` across creation (`100003`), modification (`100002`), and deletion (`100004`) at rule level `8`.
- **CLI Invocation (`SENTINEL-WAZUH`):** `PYTHONPATH=src python3 -m soc_automation.cli /tmp/fim_probe_alerts.json --sha256 --enrich --triage --min-level 8 --report-format markdown -o /tmp/fim_probe_report.md`
- **Archived Evidence (`~/soc-evidence/v0.10-fim-probe/`):**
  - `fim_probe_alerts.json` (4,181 bytes) — SHA-256: `7537b1861577be18c89a86fc8f2f49efcb746d39e1a886e4995dadf3830790aa`
  - `fim_probe_report.md` (1,313 bytes) — SHA-256: `a558d9f605a652019a9e9038472e4149011806658c9382c2d909b7e601ed45b2`
  - `SHA256SUMS` (174 bytes) — SHA-256 checksum manifest; temporary `/tmp/fim_probe_*` files removed after archiving.

**Archive location:** This archive is stored outside the SENTINEL repository at `~/soc-evidence/v0.10-fim-probe/`. It was not committed under `evidence/v0.10/` in the repository, so it should not be treated as committed repository evidence.

### Validation Findings
- **Triage & Artifact Extraction:** All 3 level-8 alerts (`100003`, `100002`, `100004`) were triaged (`count: 1` each), `/home/sentinel-admin/.fim_probe_test.txt` was extracted under file paths, and the hidden dotfile was flagged under suspicious/hidden FIM paths.
- **JSON vs. Markdown Output:** Running `--report-format json` on the archived `fim_probe_alerts.json` confirmed `total_alerts: 3` and `unique_rules: 3`, added `first_seen` and `last_seen` timestamps per rule, and kept `process_images: []`, `target_process_images: []`, and `event_timestamps: []` empty. Neither report format currently surfaces raw Wazuh alert IDs or agent metadata (`002` / `sentinel-linux01` / `10.10.10.40`).
- **Linux `syscheck` Field Behavior:** `Process: None | Target Process: None | Event Time: None` in Markdown output reflects fields absent from Linux FIM alert payloads rather than a parser failure.

### Open Boundaries & Remaining Work
- **FIM Noise & Exclusions:** Residual `dconf` noise and Tracker3/Nautilus exclusion testing remain open in `docs/05-detection-engineering.md` and are not marked resolved by this 3-event probe.
- **Workflow Scope:** Successful triage of three probe alerts validates this end-to-end run; it does not substitute for full FIM regression suites or broader telemetry validation.
