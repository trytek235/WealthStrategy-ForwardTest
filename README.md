# WealthStrategy – Publiczny Rejestr Kryptograficzny Forward-Testu

Oficjalne repozytorium publicznego testu w przód (*Forward-Test*) strategii giełdowych GPW autorstwa Grzegorza Blizny (model *Build in Public*).

## Zawartość repozytorium:
1. **`SPECIFICATION.md`** – Pełna specyfikacja matematyczna i reguły inwestycyjne strategii (uniwersum mWIG40, równe wagi, okno momentum 90 sesji, daty rebalansowania).
2. **`forward_test_ledger.json`** – Niezmienny, kryptograficzny rejestr sygnałów (łańcuch skrótów SHA-256). Zawiera wyłącznie dane z dnia wejścia. Plik ten NIE ulega zmianie między rebalansowaniami (posiada stałą sumę kontrolną).
3. **`live_status.json`** – Dynamiczne, codzienne śledzenie wyników na żywo na podstawie oficjalnych kursów zamknięcia GPW (aktualizowane każdej nocy przez Nocnego Agenta).
4. **`HASHES.txt`** – Zestawienie aktualnych sum kontrolnych SHA-256 wszystkich kluczowych komponentów.
5. **`verify_ledger.py`** – Niezależny skrypt weryfikujący integralność całego łańcucha kryptograficznego oraz zgodność specyfikacji (działa bez zewnętrznych bibliotek).

## Niezależna weryfikacja:
Uruchom w konsoli:
```bash
python verify_ledger.py
```
