# SENTINEL v0.3: Raw Alert Evidence

## Overview

This directory contains three raw Wazuh alert JSON files forming two separate FIM evidence sets from SENTINEL-LINUX01. All records identify Agent `002` (`sentinel-linux01`, `10.10.10.40`) and real-time Syscheck events.

Alert levels shown are Wazuh rule levels. They are not assessments of case severity or impact. For how these records fit into the wider evidence, see the [v0.3 Evidence Index](../readme.md).

## Evidence Files

| File | Event | Rule | Level | Timestamp |
|---|---|---|---|---|
| [`sentinel-v03-creation-alert.json`](sentinel-v03-creation-alert.json) | Creation | `100003` | 8 | `2026-10-31T22:56:46.988+0530` |
| [`sentinel-v03-deletion-alert.json`](sentinel-v03-deletion-alert.json) | Deletion | `100004` | 8 | `2026-10-31T23:27:05.164+0530` |
| [`fim-lifecycle-evidence.json`](fim-lifecycle-evidence.json) | Creation | `100003` | 8 | `2026-11-18T12:57:06.508+0530` |
| | Modification | `100002` | 8 | `2026-11-18T12:59:29.407+0530` |
| | Deletion | `100004` | 8 | `2026-11-18T13:04:23.506+0530` |

## October 31: Creation and Deletion

- **File:** `/home/sentinel-admin/sentinel-v03-controlled-test.txt`
- **Records:** two alerts (creation, deletion), each in its own JSON file.
- **Continuity:** both records contain inode `2622181` and matching file hashes. This supports the interpretation that they concern the same file.
- **Scope:** creation and deletion only. There is no modification record, so this is not a lifecycle test.
- **Relationship to screenshots:** separate from the October 31 screenshot observation documented in the [Evidence Index](../readme.md). Their relationship has not been established.

## November 18: One Controlled Lifecycle Session

- **File:** `/home/sentinel-admin/fim-sprint-test.txt`
- **Records:** three alerts (creation, modification, deletion) in one JSON file.
- **Continuity:** all three records contain inode `2622203`. The modification record contains before-and-after hashes, and its final SHA-256 matches the SHA-256 in the deletion record. The matching inode and hash transitions support the interpretation that the three records concern the same file across the creation, modification and deletion sequence.
- **Scope:** one controlled session on one dedicated file. It is not a regression suite or a measure of detection coverage.

## Integrity Manifest

[`SHA256SUMS`](SHA256SUMS) has three entries, one for each JSON file in this directory. It lists bare filenames, so run the check from inside this directory:

```bash
cd evidence/v0.3/raw-alerts
sha256sum -c SHA256SUMS
```

A successful run reports `OK` for each of the three files. This README does not claim that the checksums have been independently recomputed or verified.

## Limitations

- The October 31 and November 18 sets involve different files and dates and must not be read as one test.
- These records do not establish complete FIM coverage, repeatability, detection rates, or behavior on other paths, file types or sizes.
- They do not establish process attribution, root cause, or malicious activity.
- The November 2 lifecycle session is documented separately by screenshot in the Evidence Index. These records do not establish its results.
