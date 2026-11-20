# Specyfikacja Forward-Testu: Konwikcja v2 & Szybka Rotacja Weteranów v1+ (Shadow Portfolio)

Rejestr równoległych portfeli papierowych (**Shadow v2 / v1+ Fast Rotation**), prowadzony niezależnie obok nienaruszonego rejestru `forward_test_public/konwikcja/` (zamrożony półroczny v1).

## 1. Zamrożona Specyfikacja Badawcza (Pre-Registered)
- **Plik specyfikacji:** `audit/konwikcja_v2/spec_v2.json` (`konwikcja_v2.0_frozen_20261120`)
- **SHA-256 pliku `spec_v2.json`:** `043ef77e18eab8e21b5b1dde904ddd2f5ea2d275fc5001ce0794296213b90265`
- **SHA-256 kanonicznego JSON:** `21f191fcd2b70414490b02f4dfa7ddb769d65f870348cde787fc27879ec624aa`

## 2. Reguły Selekcji i Egzekucji
1. **Filtr płynności GPW (wspólny dla wszystkich wariantów w tym rejestrze):** Mediana dziennego obrotu z 20 sesji (`Close × Volume`) `>= 100 000 PLN` (minimum 10 aktywnych sesji w oknie 20d) oraz kurs zamknięcia `>= 1.00 PLN`.
2. **Pula Momentum TOP 30:** Spośród płynnych spółek wybierane jest 30 spółek o najwyższym 60-sesyjnym momentum (`ROC_60d × 1.45`, okno 87 dni kalendarzowych).
3. **Egzekucja i koszty:** Egzekucja na zamknięciu kolejnej sesji **`T+1 Close`**, koszt transakcyjny **`0.5%` w jedną stronę** (`1.0%` przy pełnej wymianie pozycji).

## 3. Śledzone Równolegle Warianty Portfeli (3 Warianty v2 + 3 Warianty Szybkiej Rotacji Weteranów v1+ + 2 Portfele Kontrolne)

### Grupa A — Warianty Konwikcji v2 (bez sztywnej listy `ANALYSTS`, zanik `half_life = 60d`, `>= 3` autorów/90d)
1. **`1_V2_ROLLING_AUTH_SEMI`:** Półroczny (`02-01` i `09-24`), przyczynowa ocena autorów *point-in-time* (waga `2.0` dla autorów z `>= 5` zamkniętymi 60-sesyjnymi sygnałami przed datą decyzji i trafnością `>= 55%` względem WIG `+5 pp`, pozostali `1.0`).
2. **`2_V2_CORE_SEMI` (główny punkt odniesienia „Brzytwa Ockhama”):** Półroczny (`02-01` i `09-24`), równe wagi wszystkich autorów (`1.0`), wybór **TOP 3** spółek (`3 × 33.33%`).
3. **`3_V2_MONTHLY_BUF10_RFVETO`:** Comiesięczny przegląd na koniec miesiąca z buforem utrzymania `TOP 10` oraz dwustopniowym **Red-Flag Veto 14d** (regex słownikowy 14d weryfikowany semantycznie przez lokalny model Ollama `llama3.1:8b`).

### Grupa B — Warianty Szybkiej Rotacji Weteranów v1+ (`ANALYSTS` z v1 + Płynność `>= 100k PLN` + Bufor Utrzymania `TOP 5`)
Zachowują oryginalną formułę konwikcji **v1** z wysokimi wagami 14 weteranów (`obs`, `Prezes`, `elendix`, `Savo` itd., bez wymogu `u90 >= 3`), dodają twardy filtr płynności **`obrót 20d >= 100k PLN`** oraz **bufor utrzymania `TOP 5`** (spółka znajdująca się w portfelu zostaje w nim tak długo, jak utrzymuje się w `TOP 5` płynnego rankingu konwikcji v1; wymieniana jest na nową spółkę z `TOP 3` dopiero po wypadnięciu poza `TOP 5`):
4. **`4_V1_VET_MONTHLY_BUF5` (Rotacja Miesięczna z buforem `TOP 5`):** Przegląd na ostatniej sesji każdego miesiąca (w backteście 2019–2026: `+6761.6%` netto, `Sharpe 1.50`; w Hold-Out 2024–2025: `+180.9%` netto, `Sharpe 1.72`; w Hold-Out 2024–2026: `+457.6%` netto, `Sharpe 1.96`).
5. **`5_V1_VET_BIWEEKLY_BUF5` (Rotacja Dwutygodniowa — co 10 sesji / co 2. piątek z buforem `TOP 5`):** Przegląd co 2 tygodnie (w `TRAIN_EX2020`: `+114.6%` netto, `MaxDD -22.7%`, `Sharpe 0.83`; w 1M live `16.10–20.11.2026`: `+3.91%` netto vs WIG `-4.41%`).
6. **`6_V1_VET_WEEKLY_BUF5` (Rotacja Tygodniowa — w każdy piątek z buforem `TOP 5`):** Przegląd co tydzień na zamknięciu piątku, wejście `T+1` w poniedziałek (w 1M live `16.10–20.11.2026`: **`+8.89%` brutto / `+7.26%` netto** vs WIG `-4.41%`, nadwyżka netto **`+11.67 pp`**).

### Grupa C — Portfele Kontrolne (Czyste Momentum TOP 3)
7. **`CONTROL_TOP3_QUAL_MOM_SEMI`:** TOP 3 najwyższego Momentum spośród spółek spełniających sito aktywności forum `>= 3` autorów/90d.
8. **`CONTROL_TOP3_PURE_MOM_SEMI`:** TOP 3 najwyższego Momentum z płynnego TOP 30 GPW bez sita forum.
