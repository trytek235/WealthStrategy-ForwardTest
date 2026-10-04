# WealthStrategy – publiczny rejestr forward-testu

Ten katalog zawiera wyłącznie plik `forward_test_ledger.json` (skład portfela, ceny wejścia, łańcuch SHA-256)
oraz `HASHES.txt`. Historia commitów jest dowodem czasu: wpis jest wiarygodnie `EX_ANTE`, jeśli został
wypchnięty do zdalnego repozytorium przed startem cyklu.

Weryfikacja: `python verify_ledger.py`
