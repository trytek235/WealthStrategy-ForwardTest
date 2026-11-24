# -*- coding: utf-8 -*-
import json
import hashlib
import sys
from pathlib import Path

ledger_path = Path(__file__).resolve().parent / "ledger.jsonl"
if not ledger_path.exists():
    sys.exit("BLAD: brak pliku ledger.jsonl")

prev = "GENESIS"
prev_date = ""
n = 0
for line in open(ledger_path, encoding="utf-8"):
    if not line.strip():
        continue
    e = json.loads(line)
    h = e.pop("entry_hash")
    if e.get("prev_hash") != prev:
        sys.exit(f"BLAD: zerwany lancuch przy {e.get('signal_date')}")
    if e.get("signal_date", "") <= prev_date:
        sys.exit(f"BLAD: niemonotoniczna data przy {e.get('signal_date')}")
    calc = hashlib.sha256(json.dumps(e, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
    if calc != h:
        sys.exit(f"BLAD: zly hash przy {e.get('signal_date')}")
    prev = h
    prev_date = e["signal_date"]
    n += 1

print(f"OK: {n} wpisow, lancuch spojny, ostatni hash {prev[:16]}")
