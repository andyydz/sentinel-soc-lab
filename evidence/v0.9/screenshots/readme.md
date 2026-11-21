# v0.9 Screenshots Index

- `v0.9-nov21-ossec-conf-localfile.png` — Shows the `<localfile>` JSON configuration tailing `/var/ossec/logs/sentinel-sysmon-replay.json` in `/var/ossec/etc/ossec.conf`. Proves configuration syntax on the manager; does not prove live Windows agent collection or long-term log rotation.
- `v0.9-nov21-triage-pytest.png` — Shows commit context and `pytest` output (`169 passed`) in `python-soc-automation`. Proves unit/regression tests passed at that commit; does not by itself prove semantic accuracy of every Sysmon event type or field.
- `v0.9-nov21-triage-cli-output.png` — Shows `--triage` CLI output against `ossec-alerts-21.json` after replay ingestion. Proves CLI triage execution on replayed alerts; subject to `v0.9.1` field/timestamp refinement.
