# -*- coding: utf-8 -*-
"""Niezależna weryfikacja łańcucha SHA-256 oraz specyfikacji reguł (zero zewnętrznych bibliotek)."""
import json
import hashlib
import sys
from pathlib import Path

GENESIS = "0" * 64

def h(d):
    return hashlib.sha256(json.dumps(d, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()

def verify():
    ledger_path = Path("forward_test_ledger.json")
    if not ledger_path.exists():
        print("BLAD: Brak pliku forward_test_ledger.json")
        sys.exit(1)
        
    data = json.loads(ledger_path.read_text(encoding="utf-8"))
    entries = data.get("entries", [])
    meta = data.get("meta", {})
    
    # 1. Weryfikacja specyfikacji reguł
    spec_path = Path("SPECIFICATION.md")
    if spec_path.exists() and meta.get("rules_specification_sha256"):
        actual_spec_hash = hashlib.sha256(spec_path.read_bytes()).hexdigest()
        expected_spec_hash = meta["rules_specification_sha256"]
        if actual_spec_hash != expected_spec_hash:
            print(f"BLAD: Niezgodnosc hasha SPECIFICATION.md! Oczekiwano {expected_spec_hash}, otrzymano {actual_spec_hash}")
            sys.exit(1)
        print("OK: Specyfikacja reguł (SPECIFICATION.md) w 100% zgodna z pieczęcią:", actual_spec_hash[:16] + "...")
        
    # 2. Weryfikacja łańcucha kryptograficznego wpisów
    prev = GENESIS
    for i, e in enumerate(entries):
        core = {k: e.get(k) for k in [
            "index", "entry_id", "strategy_id", "strategy_name", "cycle_label", "cycle_start_date",
            "cycle_planned_exit_date", "tickers", "weights", "entry_prices", "benchmark_entry_prices",
            "timestamp_logged", "prev_hash"
        ]}
        if e.get("schema_version", 1) >= 2:
            core["schema_version"] = e.get("schema_version")
            core["registration_type"] = e.get("registration_type")
            core["benchmark_entry_dates"] = e.get("benchmark_entry_dates")
            
        calculated_hash = h(core)
        if e.get("prev_hash") != prev or calculated_hash != e.get("entry_hash"):
            print(f"BLAD integralnosci we wpisie #{i} ({e.get('entry_id')})")
            sys.exit(1)
        prev = e["entry_hash"]
        
    print(f"OK: Integralność potwierdzona dla {len(entries)} wpisów. Łańcuch nienaruszony, ostatni hash: {prev[:16]}...")

if __name__ == "__main__":
    verify()
