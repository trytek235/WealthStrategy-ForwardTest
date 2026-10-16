# Forward-test: TOP 30 Momentum -> TOP 3 Konwikcja (GPW)

Codzienny, publiczny zapis sygnalu strategii, ktorej backtest jest hipotetyczny i obciazony
znanymi problemami (jedna spolka w 2020 r. robi wiekszosc wyniku, uniwersum tylko spolek z watkiem na forum,
lista wazonych autorow wybrana z wiedza wsteczna). Ten rejestr ma sprawdzic strategie na danych, ktorych nie bylo
w chwili jej projektowania.

## Reguly
- Uniwersum: spolki GPW z watkiem na Forum Portal Analiz (mapa z 29.09.2026).
- Krok 1: 30 spolek o najwyzszej stopie zwrotu z ~60 sesji (60 x 1.45 dnia kalendarzowego).
- Krok 2: z tej trzydziestki 3 spolki o najwyzszej konwikcji (sentyment postow z 365 dni do dnia sygnalu
  wlacznie, wagi autorow i slownik zamrozone - ich hash to `params_sha256`).
- Sygnal liczony po zamknieciu sesji, publikowany w nocy. Wejscie papierowego portfela: zamkniecie pierwszej sesji
  po dniu zapisu sygnalu (jesli dane byly opoznione, wejscie przesuwa sie, nigdy nie cofa).
- Rebalans portfela: 1 lutego i 24 wrzesnia (pierwsza sesja w tym dniu lub po nim). Rowne wagi, bez kosztow.

## Pliki
- `ledger.jsonl` - jeden wpis na sesje, lancuch SHA-256 (`prev_hash` -> `entry_hash`).
- `latest.json` - ostatni ranking.
- `portfolio.json` - cykle papierowego portfela i wynik vs WIG.

Weryfikacja lancucha: `python verify_konwikcja.py`
