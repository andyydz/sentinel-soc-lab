# SENTINEL Evidence — v0.9 (Sysmon JSON Replay Ingestion)

## Scope & Architecture
- **Ingestion Mechanism:** Wazuh `logcollector` tails `/var/ossec/logs/sentinel-sysmon-replay.json` using `<log_format>json</log_format>` configured in `/var/ossec/etc/ossec.conf` (backup at `/var/ossec/etc/ossec.conf.bak.v0.9`).
- **Verified Rules:** Replayed Sysmon events generated live Wazuh alerts in `/var/ossec/logs/alerts/2026/Nov/ossec-alerts-21.json` for rules `100110`, `100130`, and `100140`.
- **Triage Integration:** Verified `python-soc-automation` (`--triage --min-level 8`) against live alerts and added fallback extraction for Sysmon `data.win.eventdata` target/process fields (`targetFilename`, `image`, `targetImage`) when `syscheck.path` is absent (169 `pytest` tests passing).

## Milestone Sequence Note
- `v0.8` (*Reliability Tuning, Triage & Flagship Polish*) remains marked as planned in `README.md` and `CHANGELOG.md`; no fabricated `v0.8` evidence is added here.

## Limitations & Audit Notes
- **Replay vs. Live Windows Telemetry:** Telemetry came from JSON replay on `sentinal-wazuh` rather than a live Windows endpoint agent.
- **Timestamps:** Alert timestamps reflect ingestion time on `sentinal-wazuh` (`2026-11-21`), not original endpoint event execution time.

## Screenshots (`evidence/v0.9/screenshots/`)
- `v0.9-nov21-ossec-conf-localfile.png` — `<localfile>` JSON tailing configuration for `/var/ossec/logs/sentinel-sysmon-replay.json`
- `v0.9-nov21-sysmon-replay-alerts.png` — Live Wazuh alerts for rules `100110`, `100130`, and `100140` in `ossec-alerts-21.json`
- `v0.9-nov21-triage-pytest.png` — Commit and `pytest` verification output (`169 passed`)
- `v0.9-nov21-triage-cli-output.png` — `--triage` JSON output showing rules `100110`, `100130`, and `100140` with extracted fields
