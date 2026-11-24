# Konwikcja v3 — Pre-Rejestrowana Metodologia Shadow Forward-Test (EX_ANTE)

*Data rejestracji specyfikacji: 2026-11-25 (przed zebraniem pierwszej stopy zwrotu na żywo)*

## 1. Cel i Niezależność od v1 / v2
Konwikcja v3 jest całkowicie niezależnym systemem równoległym (*Shadow Forward-Test*), który nie modyfikuje plików ani rejestrów **v1** (`konwikcja_daily.py`) ani **v2** (`konwikcja_v2_daily.py`).
Wszystkie sygnały i stany portfeli v3 są rejestrowane **wyłącznie EX_ANTE** począwszy od pierwszej sesji w `ledger.jsonl` (brak wstecznej rekonstrukcji historii i zero kosztu komercyjnych API — klasyfikacja ESPI odbywa się lokalnie na `llama3.1:8b`, `temperature=0`).

## 2. Uniwersum i Filtr Płynności
- Pula startowa: **TOP 30 Momentum 90-sesyjnego GPW** z identycznym jak w v2 filtrem płynności point-in-time:
  - mediana 20-sesyjnego obrotu na kalendarzu sesji WIG `>= 100 000 PLN` (dni bez obrotu liczone jako `0`),
  - cena zamknięcia `>= 1.00 PLN`.

## 3. Trzy Filary Punktacji (skala 0–100)

### Filar P1 — Konwikcja Forum PortalAnaliz (waga `55%`)
- Normalizacja rangi percentylowej `0–100` wewnątrz kwalifikującej się puli TOP 30:
  - warianty `V3_VET_*`: punktacja weteranów `conv1` (`cnt1 >= 1`, `sent1 > 50%`),
  - wariant `V3_CORE_*`: punktacja demokratyczna v2 `conv2` (półtrwanie `60d`, `>= 3` unikalnych autorów w `90d`).
- Spółki niespełniające kryterium forum otrzymują w wariantach `V3_VET_*` / `V3_CORE_*` `P1 = 0` i nie kwalifikują się do portfela (poza ablacją `4_V3_HARD_SIGNALS_ONLY`).

### Filar P2 — Twarde Sygnały Zewnętrzne (waga `35%`)
Neutralna baza `50.0` modyfikowana przez trzy niezależne strumienie:
1. **ESPI / EBI (ostatnie 45 dni, półtrwanie `21d`):** `clamp(espi_score_raw, -4.0, +4.0) * 6.25` (zakres `±25 pkt`). Komunikaty formalne (WZA, terminy raportów, statut) są pomijane regułowo (`0`), komunikaty merytoryczne klasyfikuje jednorazowo lokalny model `llama3.1:8b` (`{-2, -1, 0, +1, +2}`).
2. **Rekomendacje maklerskie (ostatnie 120 dni, półtrwanie `60d`) + DM BOŚ PDF:** `clamp(broker_score_raw, -1.5, +1.5) * 10.0` (zakres `±15 pkt`). Brak pokrycia analitycznego = `0` (neutralny, brak kary dla small-capów).
3. **Insiderzy MAR Art. 19 & Akcjonariat Art. 69 (ostatnie 60 dni):** `clamp(insider_score_raw, -2.5, +2.5) * 4.0` (zakres `±10 pkt`).

`P2 = clamp(50.0 + ESPI_comp + Broker_comp + Insider_comp, 0.0, 100.0)`

### Filar P3 — Ryzyko, Krótka Sprzedaż KNF i Przepływy Wielorybów (waga `10%`)
Baza `90.0` korygowana w dół/górę:
- **Rejestr KNF krótkich pozycji (`>= 0.5%` netto):** `-40.0 * min(total_short_pct, 2.25)`
- **Radar Wielorybów GPW:** `-15.0` przy dystrybucji instytucjonalnej, `+10.0` przy silnej akumulacji.

`P3 = clamp(90.0 - KNF_penalty - Whale_dist + Whale_acc, 0.0, 100.0)`

### Wynik Złożony i Dwustronne Red-Flag Veto
- `v3_score = 0.55 * P1 + 0.35 * P2 + 0.10 * P3`
- **Dual-Source Red-Flag Veto:** wyklucza spółkę, jeśli lokalny model `llama3.1:8b` (`temperature=0`) potwierdzi realne ryzyko (ABB po dyskoncie, rozwodniająca emisja akcji, kara/dochodzenie KNF lub UOKiK, śledztwo prokuratury/CBŚP, duży odpis, restrukturyzacja/niewypłacalność) w:
  - postach forum z ostatnich 14 dni, **LUB**
  - komunikatach ESPI z ostatnich 45 dni.
- Błąd lub timeout Ollamy (`rf_unverified`) **NIGDY** nie uruchamia cichego weta.

## 4. Śledzone Warianty (k=3, bufor utrzymania TOP 5, T+1 Close, buy-and-hold)
Wszystkie warianty raportują koszty jednostronne `0.15%` i `0.50%` oraz wartość likwidacyjną, z zamrażaniem stanu w `ledger.jsonl`:
1. **`1_V3_VET_MONTHLY_BUF5_FULL`** — główny wariant v3 (weterani + twarde sygnały, przegląd w ostatnią sesję miesiąca).
2. **`2_V3_VET_BIWEEKLY_BUF5_FULL`** — wariant szybki v3 (przegląd w ostatnią sesję co drugiego tygodnia).
3. **`3_V3_CORE_MONTHLY_BUF5_FULL`** — demokratyczna konwikcja v2 + twarde sygnały (przegląd miesięczny).
4. **`4_V3_HARD_SIGNALS_ONLY_MONTHLY_BUF5`** — kontrolna ablacja bez forum (`0.00 * P1 + 0.75 * P2 + 0.25 * P3`, remisy rozstrzygane momentum 90d), weryfikująca czysty wkład ESPI / rekomendacji / insiderów / KNF.
