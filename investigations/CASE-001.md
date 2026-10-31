## CASE-001 — FIM Detection Validation and Evidence Reconciliation

| Field | Value |
|---|---|
| Case ID | CASE-001 |
| Project | SENTINEL — SOC Lab |
| Version | v0.3 — SOC Investigation |
| Status | Evidence reconciliation for the reviewed CASE-001 scope: Closed. Broader investigation and detection-engineering work: Open |
| Severity | Low |
| Detection Source | Wazuh File Integrity Monitoring (FIM) |
| Custom Rules | `100002` (modification), `100003` (creation), `100004` (deletion) |
| Endpoint | SENTINEL-LINUX01 (`10.10.10.40`), Agent ID `002` |

> **Severity note:** Case severity Low is an administrative investigation classification for this case's reviewed scope. It is not the severity level assigned to an individual Wazuh alert. The custom detections discussed here generated Level 8 alerts, while the October 16 built-in alerts were Levels 5 and 7.

---

## Executive Summary

This case reviewed Wazuh FIM detections on SENTINEL-LINUX01 across four dates in October 2026.

- **Modification (`100002`, Level 8):** fired for the controlled test on 11 October, and 26 October terminal output showed two further alerts from consecutive modifications of one test file.
- **Creation/deletion, 16 October (historical):** the reviewed records showed built-in Rule `554` (Level 5) for creation and `553` (Level 7) for deletion. `100002` was absent from both; the reason is unresolved. These were not custom-rule validations.
- **Creation/deletion, 31 October (separate observation):** a terminal screenshot showed custom Rule `100003` (creation) and `100004` (deletion), both Level 8, under `/home/sentinel-admin/snap/firmware-updater/262/.config/bus/`. Whether these were deliberately triggered or ordinary application activity is not established.

> These observations do not establish repeatable detection, detection or false-positive/false-negative rates, complete FIM coverage, creation or deletion handling by `100002`, or that the endpoint is free from threats.

### Detection-Validation Summary

| Custom Rule | Event | Observed Result | Evidence Basis |
|---|---|---|---|
| `100002` | Modification | Level 8 alerts on October 11 and 26 | Existing screenshots and terminal evidence |
| `100003` | Creation | Level 8 alert on October 31 | Terminal screenshot |
| `100004` | Deletion | Level 8 alert on October 31 | Terminal screenshot |

These observations span separate sessions and do not represent one end-to-end lifecycle test or a repeatable regression suite. The October 31 creation and deletion events occurred under an application configuration path; deliberate test attribution has not been established.

---

## Objective

- Review custom FIM rules `100002`, `100003` and `100004` against the modification, creation and deletion events observed.
- Reconcile earlier reported results against reviewed source records.
- Document noise, limitations, and follow-up detection-engineering work.

---

## Environment and Scope

| Component | Details |
|---|---|
| Wazuh Manager | SENTINEL-WAZUH — `10.10.10.10` |
| Wazuh Agent | SENTINEL-LINUX01 — `10.10.10.40`, Agent ID `002` |
| Wazuh Version | `4.14.8` |
| Custom rules | `100002` (modification), `100003` (creation), `100004` (deletion); all Level 8 |
| Modification test file (11 Oct) | `/home/sentinel-admin/sentinel-fim-validation.txt` |
| Creation/deletion test file (16 Oct) | `/home/sentinel-admin/sentinel-audit-test.txt` |
| Modification test file (26 Oct) | `/home/sentinel-admin/sentinel-v02-mod-test.txt` |
| Observed paths (31 Oct) | Under `/home/sentinel-admin/snap/firmware-updater/262/.config/bus/` (origin not established) |

Scope: the controlled tests of 11, 16 and 26 October, the 31 October observed alerts, the reviewed alert records, and related FIM events. Operational events are recorded separately and are not detection evidence.

---

## Evidence

| Evidence | Purpose |
|---|---|
| [`v0.3-fim-lifecycle-custom-detections.png`](../evidence/v0.3/screenshots/v0.3-fim-lifecycle-custom-detections.png) | Rules `100003` and `100004` alerts (31 Oct) |
| [`v0.3-custom-rule-100002.png`](../evidence/v0.3/screenshots/v0.3-custom-rule-100002.png) | Rule `100002` validation (11 Oct) |
| [`v0.3-custom-rule-100002-dashboard-json.png`](../evidence/v0.3/screenshots/v0.3-custom-rule-100002-dashboard-json.png) | Alert JSON and event fields (11 Oct) |
| [`v0.3-case001-fim-filtered-events.png`](../evidence/v0.3/screenshots/v0.3-case001-fim-filtered-events.png) | Filtered FIM event view |
| [`v0.3-case001-rule-550-event-details.png`](../evidence/v0.3/screenshots/v0.3-case001-rule-550-event-details.png) | Built-in Rule 550 event details |
| [`v0.3-case001-endpoint-file-metadata.png`](../evidence/v0.3/screenshots/v0.3-case001-endpoint-file-metadata.png) | Endpoint file metadata |
| [`v0.2-oct26-controlled-modification-source-alerts-new.png`](../evidence/v0.2/screenschots/v0.2-oct26-controlled-modification-source-alerts-new.png) | Two Rule `100002` alerts (26 Oct); existing v0.2 directory spelling preserved |

![FIM lifecycle custom detections, 31 October](../evidence/v0.3/screenshots/v0.3-fim-lifecycle-custom-detections.png)

**Evidence basis**

- **11 Oct:** the original alert log could not be recovered during the 26 Oct review; the existing evidence images support the result.
- **16 Oct:** results rest on reviewed source records; no repository evidence path is listed.
- **26 Oct:** two Rule `100002` alerts from consecutive modifications of one file; not independent test cases.
- **31 Oct:** a terminal screenshot only; no raw alert records are committed. It does not establish how the events were triggered or repeatability.
- **31 Oct manager configuration:** a photograph of `ossec.conf` on SENTINEL-WAZUH was supplied but is not committed and is not referenced as repository evidence (see Finding 5).

### Corrections and Evidence-Quality Notes

These are documentation and evidence-quality notes, not security incidents.

1. An earlier version stated `100002` fired for the 16 Oct creation (`11:40:06.105`). This was unsupported and corrected to the reviewed Rule `554` record (`11:40:06.007`).
2. The 31 Oct creation and deletion events are observations, not confirmed deliberate tests.
3. The manager configuration screenshot is not endpoint configuration evidence.
4. The v0.2 directory spelling (`screenschots`) is preserved; a rename requires a coordinated update and has not been approved.
5. The manager-configuration photograph is not yet committed.

---

## Investigation Timeline

All times IST (`+0530`).

| Date / time | Event |
|---|---|
| 11 Oct 2026, ~20:24–20:30 | Reviewed FIM events and Rule 550 details; modified `sentinel-fim-validation.txt`. Rule `100002` alert at `2026-10-11T20:25:14.746+0530`. Additional home-directory events observed. |
| 16 Oct 2026, `11:40:06.007` | Controlled creation of `sentinel-audit-test.txt`. Built-in Rule `554` (Level 5); `100002` absent. |
| 16 Oct 2026, `12:31:32.819` | Controlled deletion of the same file. Built-in Rule `553` (Level 7); `100002` absent. |
| 26 Oct 2026, `21:38:27.910` | `sentinel-v02-mod-test.txt` modified; Rule `100002` (Level 8); 0 → 23 bytes. |
| 26 Oct 2026, `21:38:48.473` | Same file modified again; Rule `100002` (Level 8); 23 → 61 bytes. |
| 31 Oct 2026, ~18:51:56 | Terminal screenshot showed Rule `100004` (deletion, Level 8) and `100003` (creation, Level 8), each with a path under `/home/sentinel-admin/snap/firmware-updater/262/.config/bus/`. Trigger, individual timestamps and order not established. |
| 31 Oct 2026 | Manager-side `ossec.conf` displayed on SENTINEL-WAZUH (photograph supplied; not committed). |

The 11 Oct window is approximate. No modification-test timestamp is recorded for 31 Oct; all four dates were separate sessions.

---

## Technical Findings

### Finding 1 — Rule 100002 detected the tested modification scenario

Result: Confirmed for the 11 and 26 October tests.

| Field (11 Oct) | Value |
|---|---|
| Rule ID / Level | `100002` / `8` |
| Event type | `modified` |
| File | `/home/sentinel-admin/sentinel-fim-validation.txt` |
| Decoder / location | `syscheck_integrity_changed` / `syscheck` |

The event included file-integrity metadata, including size and hash information. The 26 Oct alerts came from consecutive modifications of one file; they do not extend the result to other paths, file types or event types.

### Finding 2 — 16 October creation and deletion: Rule 100002 absent (historical)

Result: Limited to the reviewed records; cause unresolved.

| Test (16 Oct) | Rule shown | `100002` |
|---|---|---|
| Creation (`11:40:06.007`) | `554` (Level 5) | Absent |
| Deletion (`12:31:32.819`) | `553` (Level 7) | Absent |

`100002` has been described as anchored to built-in Rule `550`; why it was absent is **unresolved**, no root cause is asserted, and the rule has not been changed. These were historical observations, not custom-rule validations, and `100002` is not claimed to handle creation or deletion.

### Finding 3 — Rules 100003 and 100004 observed on 31 October

Result: Single terminal screenshot; trigger origin and scope limited.

| Field | `100003` | `100004` |
|---|---|---|
| Event | Creation | Deletion |
| Alert level | `8` | `8` |
| Approx. time | ~18:51:56 IST | ~18:51:56 IST |
| Path | Under `/home/sentinel-admin/snap/firmware-updater/262/.config/bus/` | Same |

- The paths are in an application configuration directory, not a dedicated test file. The screenshot does not show whether the events were deliberate or ordinary application activity, so they are observations, not controlled tests.
- Each rule is evidenced by a single event; no other paths, file types or repetitions are shown.
- This does not convert the 16 Oct observations into validations. Why `100003`/`100004` appeared on 31 Oct while `554`/`553` appeared on 16 Oct is **unresolved**.

### Finding 4 — Additional home-directory FIM events

On 11 Oct the dashboard showed 19 matching events, including the controlled event; others involved GNOME Tracker cache, desktop configuration and application state, consistent with ordinary desktop activity. Responsible processes were not established. The 31 Oct paths are likewise under an application configuration path; their origin is unconfirmed.

### Finding 5 — Manager-side FIM configuration; endpoint configuration unverified

A supplied photograph shows `/var/ossec/etc/ossec.conf` on SENTINEL-WAZUH with `<disabled>no</disabled>`, `<scan_on_start>yes</scan_on_start>`, `<alert_new_files>yes</alert_new_files>` and `<directories>/etc,/usr/bin,/bin,/usr/sbin</directories>`.

- This is **manager-side** evidence. It does not establish the effective FIM configuration on SENTINEL-LINUX01.
- The listed directories do not include `/home`. That does not prove the endpoint is not monitoring `/home`; its configuration may be local or centrally managed and has not been inspected.
- The `/home` alerts in Findings 1–3 show such events from Agent `002` reached the manager, which is consistent with `/home` being monitored on the endpoint; the mechanism is unidentified.
- The photograph is not committed.

### Finding 6 — Detection scope requires further tuning

As reported, `100002` uses a `file` condition of `/home/` (parent `<if_sid>550</if_sid>`, Level 8, group `sentinel_fim`). This has not been re-checked against the active `local_rules.xml`; matching behavior (substring vs. regex, case handling) is unverified. The `100003` and `100004` definitions have not been reviewed here. If conditions are broad, routine activity may generate noise; this has not been quantified.

---

## Operational Events — Manager Incident and Restart Test (reported)

> Operational recovery only; not detection evidence. Reported observations; raw logs not supplied or independently reviewed. No timestamps recorded.

**Manager startup timeout**

- Manager startup timed out (about 45 seconds per earlier session notes; to be confirmed).
- `/var/ossec/var/start-script-lock` was a directory containing a PID file for PID `1440`, then associated with the Wazuh Indexer Java process (per earlier notes; to be confirmed).
- No active Manager processes were found; the lock directory was removed, `systemctl daemon-reload` was run, and the Manager started. Later checks showed Manager and Dashboard active, API and agent ports listening, and Agent `002` Active.

Root cause: **not established.** "Stale" only reflects that no Manager process was found; successful startup after removal does not prove the lock caused the failure. The lock directory should not be deleted without fresh diagnostics.

**Restart-persistence test**

One graceful shutdown and restart of both VMs (`SENTINEL-WAZUH` first, then `SENTINEL-LINUX01`) was reported successful: `wazuh-manager` and `wazuh-dashboard` active; listeners on `0.0.0.0:55000` (API), `1514` (agent communication) and `1515` (enrollment); Agent `002` Disconnected, then Active. A single cycle; it does not demonstrate resilience under other failures or boot orders.

---

## Assessment and Disposition

Evidence reconciliation for the reviewed CASE-001 scope is **closed**: the 11 and 26 Oct modification results are recorded, the 16 Oct results are corrected to the reviewed records, and the 31 Oct alerts are recorded as observations of unestablished origin.

**Still open:** broader investigation and detection-engineering work; endpoint FIM configuration verification; active custom-rule definition review; explanation of the 16 vs. 31 Oct differences; repeatable lifecycle testing; false-positive/false-negative assessment. Follow-up actions are future work, not prerequisites for the limited closure.

Rule `100002` detected the tested modification scenario at Level 8; `100003` and `100004` were each observed once at Level 8. The 16 Oct records showed built-in `554` (Level 5) and `553` (Level 7). Case severity Low is the administrative classification for this scope and is distinct from these alert levels. No malicious indicators were identified in the reviewed events; this is limited to the events examined, a FIM alert alone does not indicate malicious activity, and this is not a comprehensive forensic assessment. No containment, eradication or recovery is claimed or was required.

---

## Limitations

- No detection rates, false-positive/false-negative results, or complete FIM coverage are claimed.
- Observations span separate sessions; they are not an end-to-end lifecycle test or regression suite.
- `100003`/`100004` rest on one terminal screenshot, with trigger origin unestablished; no raw alert records are committed.
- Reasons for `100002` being absent on 16 Oct and for `100003`/`100004` appearing on 31 Oct are unresolved.
- Manager-side configuration evidence does not establish endpoint configuration and is not committed.
- The original 11 Oct alert log is unavailable.
- Background home-directory events were not attributed to processes.
- The `/home/` condition's matching and noise level are unverified; `100003`/`100004` definitions are unreviewed.
- Operational events are reported only; the startup-timeout root cause is unconfirmed.

---

## Follow-Up Actions

Future work; none has been completed.

- Verify the effective FIM configuration on SENTINEL-LINUX01.
- Review custom Rules `100002`, `100003` and `100004`.
- Review built-in Rules `550`, `553` and `554`.
- Export raw alert records for 16, 26 and 31 October where available.
- Develop repeatable creation, modification and deletion regression tests using dedicated test files.
- Evaluate path matching and noise reduction without breaking existing detections.
- Document false-positive and false-negative results once measured.
- Capture diagnostics before any change if the Manager startup failure recurs.
- Update detection-engineering documentation and changelog after validation.

---

## Conclusion

CASE-001 documents validation of custom rule `100002` for the tested modification scenario (11 and 26 October 2026) and the separate observation of `100003` (creation) and `100004` (deletion) at Level 8 on 31 October 2026, under an application configuration path with trigger origin not established. The 16 October records showed built-in Rules `554` and `553` with `100002` absent, preserved as a historical observation with the reason unresolved. Manager-side configuration evidence does not establish the endpoint's effective FIM configuration. Next steps are endpoint configuration verification, rule-definition review, dedicated repeatable lifecycle tests and false-positive/false-negative assessment, without disturbing working detections.

---

CASE-001 — evidence first, uncertainty preserved.
