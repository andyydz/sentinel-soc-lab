SENTINEL v0.3 — Custom FIM Rule Investigation

Investigation: Rule 100002 lifecycle-event scope
Reviewed source records (October 16): /var/ossec/logs/alerts/2026/Oct/ossec-alerts-16.json

Objective

Determine how custom Wazuh Rule 100002 behaves for controlled file modification, creation, and deletion events under /home/, based on the records reviewed.

Findings

All times IST (+0530).

- Modification (11 Oct): Rule 100002 (Level 8) fired for a controlled modification of /home/sentinel-admin/sentinel-fim-validation.txt at 2026-10-11T20:25:14.746+0530. The existing v0.3 screenshots support this result.

- Creation (16 Oct): For /home/sentinel-admin/sentinel-audit-test.txt, the reviewed record showed built-in Rule 554, "File added to the system", at 2026-10-16T11:40:06.007+0530. Rule 100002 was absent from this record.

- Deletion (16 Oct): For the same file, the reviewed record showed built-in Rule 553, "File deleted" (Level 7), at 2026-10-16T12:31:32.819+0530. Rule 100002 was absent from this record.

- Modification (26 Oct): Terminal output showed two Rule 100002 Level 8 alerts from two consecutive modifications of one file, /home/sentinel-admin/sentinel-v02-mod-test.txt. They are not two independent test cases and not a regression suite.

  - 2026-10-26T21:38:27.910+0530: size 0 → 23 bytes.
  - 2026-10-26T21:38:48.473+0530: size 23 → 61 bytes.

  Screenshot: v0.2-oct26-controlled-modification-source-alerts-new.png (stored in evidence/v0.2/, not in the v0.3 evidence directory).

Corrections to earlier versions of this report: the creation timestamp 11:40:06.087 was incorrect and is now 11:40:06.007. The earlier statement that Rule 100002 fired on creation is not supported by the reviewed records and has been removed.

Technical interpretation

Rule 100002 has been reported as depending on built-in Rule 550 through <if_sid>550</if_sid>. Neither the active rule configuration, nor the historical loaded configuration in effect on October 16, nor the rule's matching behavior has been verified for this report, so the dependency is a reported property of the rule and not a confirmed explanation.

The reviewed October 16 records show Rules 554 and 553 without Rule 100002. Why 100002 was absent from those records is unresolved. If the reported dependency is accurate, it could be relevant, but that has not been tested and is not asserted as the cause.

Conclusion

Rule 100002 detected the tested modification scenario on 11 and 26 October 2026. For the two reviewed October 16 records, creation and deletion were alerted on by built-in Rules 554 and 553 only, and 100002 was absent. These are observations about specific records. They do not establish how 100002 behaves for creation or deletion events in general, and they do not establish a root cause. No rule changes were made during this investigation.

Evidence and limitations

- The original 11 October alert log could not be recovered from the currently available logs during the 26 October review. That result rests on the existing v0.3 screenshots.
- The October 16 results come from the reviewed source records at the path named above. No exported copy or additional link is claimed.
- The October 26 results come from terminal output, supported by the evidence/v0.2/ screenshot linked above. They reflect two consecutive modifications of a single file.
- Each lifecycle event was reviewed for a single test file. Other paths, file types, multiple files, and repeated events remain untested.
- No detection rates, false-positive/false-negative results, or complete FIM coverage are claimed.
- Broader coverage claims should follow additional testing and review of the active and historical loaded rule definitions, including the built-in Rules 550, 553, and 554.

Status

Modification detection validated for the tested scenarios (11 and 26 October). The October 16 absence of Rule 100002 from the reviewed creation and deletion records is unresolved. The detection rule is unchanged, and the engineering question of creation/deletion coverage remains open.
