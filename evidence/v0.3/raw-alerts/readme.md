# SENTINEL v0.3 – Raw Alert Evidence

## Overview

This directory contains two raw Wazuh alert JSON records collected on October 31, 2026, documenting file creation and deletion events detected by the SENTINEL custom File Integrity Monitoring (FIM) rules.

## Evidence Files

| File | Event | Rule ID | Level | Timestamp (IST) |
|---|---|---|---|---|
| `sentinel-v03-creation-alert.json` | File created | 100003 | 8 | 2026-10-31 22:56:46.988 |
| `sentinel-v03-deletion-alert.json` | File deleted | 100004 | 8 | 2026-10-31 23:27:05.164 |

Both alerts reference:

- Endpoint: `sentinel-linux01`
- Agent ID: `002`
- Agent IP: `10.10.10.40`
- Monitored file: `/home/sentinel-admin/sentinel-v03-controlled-test.txt`
- Detection mode: Realtime

The records show the creation and subsequent deletion observations for the same monitored file. They document these two events only and should not be interpreted as a complete lifecycle validation.

## Integrity Manifest

`SHA256SUMS` contains SHA-256 checksums for both JSON alert files. It provides a way to check whether the stored files match the versions represented by the manifest.

To verify the files, run the following command from the repository root:

```bash
sha256sum -c evidence/v0.3/raw-alerts/SHA256SUMS
```

A successful result should report `OK` for each listed file. No verification result is claimed here.

## Evidence Scope and Limitations

These JSON records document the October 31 creation and deletion observations. They are separate from the November 2 controlled lifecycle validation, which used:

`/home/sentinel-admin/sentinel-v03-final-test.txt`

The November 2 validation is documented separately through screenshot evidence in `evidence/v0.3/screenshots/`. These October 31 JSON records do not establish the results of that later test.

## Related Evidence

- [SENTINEL v0.3 Evidence Index](../readme.md)
- [October 31 Creation Alert](sentinel-v03-creation-alert.json)
- [October 31 Deletion Alert](sentinel-v03-deletion-alert.json)
- [SHA-256 Checksum Manifest](SHA256SUMS)
- [November 2 Lifecycle Validation Screenshot](../screenshots/v0.3-fim-full-lifecycle-custom-rules.png)
