SENTINEL v0.3 — Custom FIM Rule Investigation

Investigation: Rule 100002 lifecycle-event scope
Historical evidence: "/var/ossec/logs/alerts/2026/Oct/ossec-alerts-16.json"

Objective

Resolve whether custom Wazuh Rule 100002 triggers on file creation, modification, and deletion under "/home/".

Findings

- Modification: An earlier October 11 verification indicated that Rule 100002 triggered for a matching file-modification event.
- Creation: The October 16 archived JSON record at "2026-10-16T11:40:06.087+0530" recorded built-in Rule 554, “File added to the system.” Rule 100002 did not trigger in the reviewed record.
- Deletion: The October 16 archived JSON record at "2026-10-16T12:31:32.819+0530" recorded built-in Rule 553, “File deleted.” Rule 100002 did not trigger in the reviewed record.

Technical interpretation

Custom Rule 100002 depends on parent Rule 550 through "<if_sid>550</if_sid>". Creation and deletion events represented by Rules 554 and 553 do not satisfy this parent-rule dependency.

Conclusion

The reviewed evidence is consistent with Rule 100002 being scoped to qualifying modification events rather than file creation or deletion. No rule changes were made during this investigation.

Evidence and limitations

Retain the original archived JSON records and associated screenshots as supporting evidence. The findings apply to the reviewed events; broader coverage should only be claimed after additional testing.

Status: Historical discrepancy resolved; detection rule unchanged.
