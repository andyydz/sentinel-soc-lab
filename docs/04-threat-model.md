# docs/05-detection-engineering.md: v0.10 inserts

These are insert blocks, not the full document. The full file was not supplied, so nothing outside these blocks is rewritten. Paste each block where indicated, then run the consistency checks at the bottom.

---

## Insert 1: Section 5.3 (FIM family), after the v0.9.1 subsection

```markdown
#### v0.10 — Live Linux FIM Probe and Python Triage Validation (22 November 2026)

A live Linux FIM probe was performed on SENTINEL-LINUX01 using the file `/home/sentinel-admin/.fim_probe_test.txt`:

- Custom Rule `100003` matched creation.
- Custom Rule `100002` matched modification.
- Custom Rule `100004` matched deletion.

The resulting Wazuh alert JSON was processed with the separate `python-soc-automation` project, v1.0 (commit `9696707`). Evidence was archived **outside the SENTINEL repository** at `~/soc-evidence/v0.10-fim-probe/`, containing `fim_probe_alerts.json`, `fim_probe_report.md` and `SHA256SUMS`. Temporary `/tmp` probe files were cleaned up.

**Scope and limitations.** v0.10 is a post-closeout development, not CASE-001 evidence. It is a separate probe, not an automated regression suite, and it does not establish comprehensive FIM coverage or resolve the broader noise-tuning issues. The evidence archive is external to the Git repository and is not claimed to be committed.
```

---

## Insert 2: Section 5.2 (Detection inventory), append to the FIM status text

```markdown
The four controlled lifecycle sessions (2, 18, 20 and 21 November) remain separate records. The v0.10 probe on 22 November is a further, independent probe on a different file. They are not combined into one test and do not form an automated regression suite.
```

If the existing 5.2 text already names the four sessions, shorten the first sentence to match its wording.

---

## Insert 3: Section 5.6 (Python-assisted triage boundary), append after the existing v0.9 text and the 195 pytest tests

```markdown
**v0.9 and v0.10 context.** In v0.9, triage was applied to manager-side Sysmon JSON replay. In v0.10, exported Wazuh alert JSON from the live Linux FIM probe was processed separately using `python-soc-automation` v1.0. This is file-based processing, not a live Wazuh API integration. The tool does not perform containment, eradication or recovery, is not a SOAR platform, and is not continuously or automatically run across repositories. Its 195 passing pytest tests belong to that project's own test suite and are not SENTINEL detection validation.
```

---

## Consistency checks (intro and other references)

- Any "v0.6 through v0.9.1" range of post-closeout developments should read "v0.6 through v0.10".
- Any "latest milestone is v0.9.1" wording is stale. v0.10 (22 Nov 2026) is an official changelog entry.
- Keep v0.10 separate from CASE-001 and from the 18 November session on `fim-sprint-test.txt`.
- Nothing may imply the v0.10 evidence archive is committed to Git.
- Keep the distinction between SENTINEL detection validation and the Python tool's own test suite.

## Not added

No alert counts, timings, test outcomes, extra evidence paths, MITRE ATT&CK mappings, or new detection claims.
