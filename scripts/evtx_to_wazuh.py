import glob
import json
import os
import sys


def _to_camel_key(name: str) -> str:
    if not name:
        return ""
    return name[0].lower() + name[1:]


def _extract_eventdata(raw_eventdata) -> dict:
    eventdata = {}
    if not isinstance(raw_eventdata, dict):
        return eventdata

    data_items = raw_eventdata.get("Data", [])
    if isinstance(data_items, dict):
        data_items = [data_items]
    elif not isinstance(data_items, list):
        data_items = []

    for item in data_items:
        if isinstance(item, dict) and "@Name" in item:
            key = _to_camel_key(str(item["@Name"]))
            val = item.get("#text", "")
            eventdata[key] = "" if val is None else str(val)

    for k, v in raw_eventdata.items():
        if k == "Data" or k.startswith("@"):
            continue
        key = _to_camel_key(str(k))
        if key not in eventdata:
            eventdata[key] = "" if v is None else str(v)

    return eventdata


def convert_event(ev: dict) -> dict:
    ev = ev if isinstance(ev, dict) else {}
    s = ev.get("System", {})
    s = s if isinstance(s, dict) else {}
    ed = ev.get("EventData", {})

    eid = s.get("EventID", "")
    if isinstance(eid, dict):
        eid = eid.get("#text", "")

    tc = s.get("TimeCreated", {})
    sys_time = tc.get("@SystemTime", "") if isinstance(tc, dict) else ""

    prov = s.get("Provider", {})
    prov_name = prov.get("@Name", "") if isinstance(prov, dict) else ""

    channel = s.get("Channel", "")
    if isinstance(channel, dict):
        channel = channel.get("#text", "")

    computer = s.get("Computer", "")
    if isinstance(computer, dict):
        computer = computer.get("#text", "")

    return {
        "win": {
            "system": {
                "providerName": str(prov_name),
                "eventID": str(eid),
                "channel": str(channel),
                "computer": str(computer),
                "systemTime": str(sys_time),
            },
            "eventdata": _extract_eventdata(ed),
        }
    }


def main() -> None:
    try:
        import Evtx.Evtx as evtx
        import xmltodict
    except ImportError as exc:
        raise SystemExit(f"Missing dependency ({exc.name}). Install python-evtx and xmltodict.") from exc

    if len(sys.argv) != 3:
        raise SystemExit("Usage: python3 evtx_to_wazuh.py <input.evtx|dir> <output.ndjson>")

    in_p, out_p = sys.argv[1], sys.argv[2]
    files = sorted(glob.glob(os.path.join(in_p, "*.evtx"))) if os.path.isdir(in_p) else [in_p]
    count = 0

    with open(out_p, "w", encoding="utf-8") as out_f:
        for fp in files:
            with evtx.Evtx(fp) as log:
                for record in log.records():
                    parsed = xmltodict.parse(record.xml()).get("Event", {})
                    rec = convert_event(parsed)
                    out_f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    count += 1

    print(f"Wrote {count} events to {out_p}")


if __name__ == "__main__":
    main()
