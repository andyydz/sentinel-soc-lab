# SENTINEL Evidence — v0.9 (Sysmon JSON Replay Ingestion)

## Scope & Architecture
- **Ingestion Mechanism:** Wazuh `logcollector` tails `/var/ossec/logs/sentinel-sysmon-replay.json` using `<log_format>json</log_format>` configured in `/var/ossec/etc/ossec.conf` (backup at `/var/ossec/etc/ossec.conf.bak.v0.9`).
- **Verified Rules:** Replayed Sysmon JSON events were ingested by Wazuh on SENTINEL-WAZUH and generated alerts in `/var/ossec/logs/alerts/2026/Nov/ossec-alerts-21.json` for rules `100110`, `100130`, and `100140`.
- **Triage Integration:** `python-soc-automation` (`--triage --min-level 8`) was run against replayed alerts with fallback extraction for Sysmon `data.win.eventdata` fields (`targetFilename`, `image`, `targetImage`) when `syscheck.path` is absent (169 `pytest` tests passing; see `v0.9.1` follow-up for field/timestamp separation).

## Limitations & Audit Notes
- **Replay vs. Live Windows Telemetry:** Telemetry came from JSON replay on SENTINEL-WAZUH rather than a live Windows endpoint agent.
- **Timestamps:** Alert timestamps reflect ingestion time on SENTINEL-WAZUH (`2026-11-21`), not original endpoint event execution time.
- **Separate Alert Capture:** A standalone `v0.9-nov21-sysmon-replay-alerts.png` file is not committed in `screenshots/`; alert output is captured via the CLI/triage workflow and `ossec-alerts-21.json` on the manager.

## Screenshots (`evidence/v0.9/screenshots/`)
- `v0.9-nov21-ossec-conf-localfile.png` — `<localfile>` JSON tailing configuration for `/var/ossec/logs/sentinel-sysmon-replay.json`
- `v0.9-nov21-triage-pytest.png` — Commit and `pytest` verification output (`169 passed` in `python-soc-automation`)
- `v0.9-nov21-triage-cli-output.png` — `--triage` output after Sysmon JSON replay ingestion
