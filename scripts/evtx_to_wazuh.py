import glob, json, os, sys
import Evtx.Evtx as evtx, xmltodict

if len(sys.argv) != 3:
    raise SystemExit("Usage: python3 evtx_to_wazuh.py <input.evtx|dir> <output.ndjson>")
in_p, out_p = sys.argv[1], sys.argv[2]
files = sorted(glob.glob(os.path.join(in_p, "*.evtx"))) if os.path.isdir(in_p) else [in_p]
c = 0
with open(out_p, "w", encoding="utf-8") as f:
    for fp in files:
        with evtx.Evtx(fp) as log:
            for r in log.records():
                ev = xmltodict.parse(r.xml()).get("Event", {})
                ev = ev if isinstance(ev, dict) else {}
                s, ed = ev.get("System", {}), ev.get("EventData", {})
                s = s if isinstance(s, dict) else {}
                eid = s.get("EventID", "")
                eid = eid.get("#text", "") if isinstance(eid, dict) else eid
                tc, p = s.get("TimeCreated", {}), s.get("Provider", {})
                ts = tc.get("@SystemTime", "") if isinstance(tc, dict) else ""
                prov = p.get("@Name", "") if isinstance(p, dict) else ""
                rec = {
                    "timestamp": ts,
                    "source_file": os.path.basename(fp),
                    "provider": prov,
                    "event_id": str(eid),
                    "channel": str(s.get("Channel", "")),
                    "computer": str(s.get("Computer", "")),
                    "event_data": ed,
                }
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                c += 1
print(f"Wrote {c} events to {out_p}")
