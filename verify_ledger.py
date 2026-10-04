# -*- coding: utf-8 -*-
"""Niezalezna weryfikacja lancucha SHA-256 (bez zaleznosci od reszty projektu)."""
import json, hashlib, sys
GENESIS = "0" * 64
def h(d): return hashlib.sha256(json.dumps(d, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
entries = json.load(open("forward_test_ledger.json", encoding="utf-8"))["entries"]
prev = GENESIS
for i, e in enumerate(entries):
    core = {k: e.get(k) for k in ["index","entry_id","strategy_id","strategy_name","cycle_label","cycle_start_date",
            "cycle_planned_exit_date","tickers","weights","entry_prices","benchmark_entry_prices","timestamp_logged","prev_hash"]}
    if e.get("schema_version", 1) >= 2:
        core["schema_version"] = e.get("schema_version"); core["registration_type"] = e.get("registration_type")
        core["benchmark_entry_dates"] = e.get("benchmark_entry_dates")
    if e.get("prev_hash") != prev or h(core) != e.get("entry_hash"):
        print("BLAD integralnosci we wpisie", i, e.get("entry_id")); sys.exit(1)
    prev = e["entry_hash"]
print("OK:", len(entries), "wpisow, ostatni hash", prev)
