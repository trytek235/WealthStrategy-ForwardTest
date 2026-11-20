# Specyfikacja Forward-Testu: Konwikcja v2 (Shadow Portfolio — 3 Warianty + Kontrola)

Rejestr równoległego portfela papierowego (**Shadow v2**), prowadzonego niezależnie obok nienaruszonego rejestru `forward_test_public/konwikcja/` (v1).

## 1. Zamrożona Specyfikacja Badawcza (Pre-Registered)
- **Plik specyfikacji:** `audit/konwikcja_v2/spec_v2.json` (`konwikcja_v2.0_frozen_20261120`)
- **SHA-256 pliku `spec_v2.json`:** `043ef77e18eab8e21b5b1dde904ddd2f5ea2d275fc5001ce0794296213b90265`
- **SHA-256 kanonicznego JSON:** `21f191fcd2b70414490b02f4dfa7ddb769d65f870348cde787fc27879ec624aa`

## 2. Reguły Selekcji i Egzekucji
1. **Filtr płynności GPW:** Mediana dziennego obrotu z 20 sesji (`Close × Volume`) `>= 100 000 PLN` (minimum 10 aktywnych sesji w oknie 20d) oraz kurs zamknięcia `>= 1.00 PLN`.
2. **Pula Momentum TOP 30:** Spośród płynnych spółek wybierane jest 30 spółek o najwyższym 60-sesyjnym momentum (`ROC_60d × 1.45`, okno 87 dni kalendarzowych).
3. **Sito aktywności na Forum Analiz:** Minimum `3` unikalnych autorów w ostatnich `90` dniach oraz minimum `3` posty w ostatnich `365` dniach.
4. **Formuła Konwikcji v2:**
   - Wykładniczy zanik czasu z okresem połowicznego zaniku `half_life = 60 dni`: $w(\Delta t) = \exp(-\ln(2)\cdot \Delta t / 60) \cdot \min(3.0, 1 + 0.2\ln(1 + \text{lajki}))$.
5. **Śledzone równolegle 3 warianty Konwikcji v2 + 2 portfele kontrolne:**
   - **Wariant 1 (`V2_ROLLING_AUTH_SEMI`):** Półroczny (`02-01` i `09-24`), przyczynowa ocena autorów *point-in-time* (waga `2.0` dla autorów z `>= 5` zamkniętymi 60-sesyjnymi sygnałami przed datą decyzji i trafnością `>= 55%` względem WIG `+5 pp`, pozostali `1.0`).
   - **Wariant 2 (`V2_CORE_SEMI` — główny punkt odniesienia „Brzytwa Ockhama”):** Półroczny (`02-01` i `09-24`), równe wagi wszystkich autorów (`1.0`, całkowite usunięcie listy `ANALYSTS` z v1), wybór **TOP 3** spółek (`3 × 33.33%`).
   - **Wariant 3 (`V2_MONTHLY_BUF10_RFVETO`):** Comiesięczny przegląd na koniec miesiąca z buforem utrzymania `TOP 10` (pozycja z poprzedniego miesiąca zostaje w portfelu, jeśli nadal jest w `TOP 10` konwikcji i ma sentyment `>= 50%`) oraz dwustopniowym **Red-Flag Veto 14d** (regex słownikowy 14d weryfikowany semantycznie przez lokalny model Ollama `llama3.1:8b`).
   - **Portfele kontrolne (półroczne `02-01` i `09-24`):** `CONTROL_TOP3_QUAL_MOM_SEMI` (TOP 3 najwyższego Momentum spośród spółek spełniających sito aktywności forum `>= 3` autorów/90d) oraz `CONTROL_TOP3_PURE_MOM_SEMI` (TOP 3 najwyższego Momentum z płynnego TOP 30 GPW bez sita forum).
6. **Egzekucja i koszty:** Egzekucja na zamknięciu kolejnej sesji **`T+1 Close`**, koszt transakcyjny **`0.5%` w jedną stronę** (`1.0%` przy pełnej wymianie pozycji).
