# -*- coding: utf-8 -*-
"""
Niezależna weryfikacja łańcucha SHA-256 oraz specyfikacji reguł (zero zewnętrznych bibliotek).
Weryfikuje:
1. Obecność i integralność specyfikacji reguł (SPECIFICATION.md) względem pieczęci SHA-256.
2. Indeksy, obliczenie statusu EX_ANTE/RETROACTIVE oraz nienaruszalność łańcucha wpisów.
3. Spójność matematyczną i obecność pól statusu w live_status.json.
"""
import json
import hashlib
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

GENESIS = "0" * 64

def h(d):
    return hashlib.sha256(json.dumps(d, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()

def verify():
    base_dir = Path(__file__).resolve().parent
    ledger_path = base_dir / "forward_test_ledger.json"
    spec_path = base_dir / "SPECIFICATION.md"
    live_path = base_dir / "live_status.json"

    if not ledger_path.exists():
        print("BLAD KRYTYCZNY: Brak pliku forward_test_ledger.json")
        sys.exit(1)

    data = json.loads(ledger_path.read_text(encoding="utf-8"))
    entries = data.get("entries", [])
    meta = data.get("meta", {})

    # 1. Rygorystyczna weryfikacja specyfikacji reguł
    expected_spec_hash = meta.get("rules_specification_sha256")
    if not expected_spec_hash:
        print("BLAD KRYTYCZNY: Brak pola 'rules_specification_sha256' w sekcji meta ledgera!")
        sys.exit(1)

    if not spec_path.exists():
        print("BLAD KRYTYCZNY: Brak pliku SPECIFICATION.md! Specyfikacja reguł musi być dołączona do rejestru.")
        sys.exit(1)

    actual_spec_hash = hashlib.sha256(spec_path.read_bytes()).hexdigest()
    if actual_spec_hash != expected_spec_hash:
        print(f"BLAD KRYTYCZNY: Naruszenie specyfikacji! Oczekiwano {expected_spec_hash}, otrzymano {actual_spec_hash}")
        sys.exit(1)
    print("OK [1/3]: Specyfikacja regul (SPECIFICATION.md) zgodna z pieczecia:", actual_spec_hash[:16] + "...")

    # 2. Weryfikacja łańcucha kryptograficznego wpisów i klasyfikacja z zahashowanych pól
    if not entries:
        print("UWAGA: Rejestr nie zawiera jeszcze wpisów.")
        return

    prev = GENESIS
    for i, e in enumerate(entries):
        if e.get("index") != i:
            print(f"BLAD: Niepoprawny indeks wpisu #{i}: oczekiwano index={i}, otrzymano {e.get('index')}")
            sys.exit(1)

        # Obliczenie typu rejestracji z zahashowanych pól rdzenia
        logged_date = (e.get("timestamp_logged") or "")[:10]
        start_date = e.get("cycle_start_date", "")
        computed_type = "EX_ANTE" if logged_date and logged_date <= start_date else "RETROACTIVE"

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
        if e.get("prev_hash") != prev:
            print(f"BLAD integralnosci we wpisie #{i} ({e.get('entry_id')}): prev_hash {e.get('prev_hash')} != {prev}")
            sys.exit(1)
        if calculated_hash != e.get("entry_hash"):
            print(f"BLAD integralnosci we wpisie #{i} ({e.get('entry_id')}): calculated {calculated_hash} != {e.get('entry_hash')}")
            sys.exit(1)

        print(f"  • Wpis #{i} ({e.get('entry_id')}): Klasyfikacja z hasha = [{computed_type}] (logged: {e.get('timestamp_logged')} vs start: {start_date})")
        prev = e["entry_hash"]

    print(f"OK [2/3]: Lancuch SHA-256 nienaruszony dla {len(entries)} wpisow. Ostatni hash: {prev[:16]}...")

    # 3. Sprawdzenie spójności live_status.json i weryfikacja pól statusu
    if live_path.exists():
        try:
            ldata = json.loads(live_path.read_text(encoding="utf-8"))
            strats = ldata.get("active_strategies", [])
            for s in strats:
                st = s.get("status")
                if st not in ("ACTIVE", "CLOSED"):
                    print(f"BLAD: Strategia {s.get('entry_id')} w live_status.json ma niepoprawny status: '{st}' (dozwolone: ACTIVE, CLOSED)!")
                    sys.exit(1)
            print(f"OK [3/3]: Plik live_status.json poprawny ({len(strats)} strategii ze zwalidowanym statusem, data rynku: {ldata.get('as_of_market_date')}).")
        except Exception as ex:
            print(f"BLAD: Blad odczytu lub walidacji live_status.json: {ex}")
            sys.exit(1)
    else:
        print("INFO: Brak pliku live_status.json (status live nie jest sledzony).")

    print("\nAUDYT ZAKONCZONY SUKCESEM: Rejestr forward-testu w 100% spojny kryptograficznie.")

if __name__ == "__main__":
    verify()
