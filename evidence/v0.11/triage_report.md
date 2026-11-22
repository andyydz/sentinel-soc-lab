# Wazuh FIM Triage Summary Report
**Total Filtered Alerts:** 10 | **Unique Rules:** 3

| Rule ID | Level | Frequency | Description | Monitored Target Path(s) |
|:---:|:---:|:---:|:---|:---|
| `100003` | 8 | 3 | SENTINEL: New file created in monitored home directory. | `/home/sentinel-admin/.config/dconf/user.L606Y3, /home/sentinel-admin/.config/tiling-assistant/.goutputstream-6NZNZ3, /home/sentinel-admin/v011_fim_probe.txt` |
| `100004` | 8 | 3 | SENTINEL: File deleted from monitored home directory. | `/home/sentinel-admin/.config/dconf/user.L606Y3, /home/sentinel-admin/.config/tiling-assistant/.goutputstream-6NZNZ3, /home/sentinel-admin/v011_fim_probe.txt` |
| `100002` | 8 | 4 | SENTINEL: File integrity modification detected in monitored home directory. | `/home/sentinel-admin/.config/dconf/user, /home/sentinel-admin/.config/tiling-assistant/tiledSessionRestore.json, /home/sentinel-admin/v011_fim_probe.txt` |

## Process & Event Timestamp Context

- **`100003`:** Process: `None` | Target Process: `None` | Event Time: `None`
- **`100004`:** Process: `None` | Target Process: `None` | Event Time: `None`
- **`100002`:** Process: `None` | Target Process: `None` | Event Time: `None`

## Extracted Artifacts

- **IP Addresses:** None
- **File Paths:** /home/sentinel-admin/.config/dconf/user, /home/sentinel-admin/.config/dconf/user.L606Y3, /home/sentinel-admin/.config/tiling-assistant/.goutputstream-6NZNZ3, /home/sentinel-admin/.config/tiling-assistant/tiledSessionRestore.json, /home/sentinel-admin/v011_fim_probe.txt
- **Process Images:** None
- **Target Process Images:** None

## v0.7 Triage Context (Noise, Sub-Threshold SSH & Evasion)
- **Likely FIM Noise Paths:** None detected
- **Suspicious / Hidden FIM Paths:** `/home/sentinel-admin/.config/tiling-assistant/.goutputstream-6NZNZ3`, `/home/sentinel-admin/.config/tiling-assistant/tiledSessionRestore.json`, `/home/sentinel-admin/.config/dconf/user`, `/home/sentinel-admin/.config/dconf/user.L606Y3`
- **SSH Rule 100200 Counts by Source IP:** None detected
- **Evasion-Adjacent Indicators:** None detected

## Source Integrity
- **SHA-256:** `bbdf02a2626599123ba871a37a7c4815828f3a457fd63a9a834cb2cc69a30068`

## Enrichment Summary
- **Enriched Triaged Alerts:** 10
