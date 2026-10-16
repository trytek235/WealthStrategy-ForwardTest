# -*- coding: utf-8 -*-
import json, hashlib, sys
prev = "GENESIS"
n = 0
for line in open("ledger.jsonl", encoding="utf-8"):
    e = json.loads(line)
    h = e.pop("entry_hash")
    if e["prev_hash"] != prev:
        sys.exit(f"BLAD: zerwany lancuch przy {e['signal_date']}")
    calc = hashlib.sha256(json.dumps(e, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
    if calc != h:
        sys.exit(f"BLAD: zly hash przy {e['signal_date']}")
    prev = h
    n += 1
print(f"OK: {n} wpisow, lancuch spojny, ostatni hash {prev[:16]}")
