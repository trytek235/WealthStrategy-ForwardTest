# Specyfikacja Matematyczna Strategii – WealthStrategy

Dokument specyfikacji technicznej i reguł inwestycyjnych podlegających publicznemu rejestrowi Forward-Test.
Skrót kryptograficzny SHA-256 niniejszego dokumentu jest na stałe zakotwiczony w rejestrze `forward_test_ledger.json`.

> **Nota o dacie wejścia w życie:** Niniejsza specyfikacja została spisana i zapieczętowana dnia 04.10.2026 r. Cykl z 24.09.2026 r. wystartował przed jej formalnym zapieczętowaniem na GitHubie, dlatego jest w pełni jawnie i rzetelnie oznaczony w rejestrze jako **`RETROACTIVE`**. Pełny, zewnętrznie potwierdzony rygor **`EX_ANTE`** obowiązuje dla wszystkich kolejnych cykli (najbliższy: 01.02.2027 r.).

---

## 1. Uniwersum Inwestycyjne i Płynność

* **Uniwersum bazowe:** Spółki wchodzące w skład oficjalnego indeksu **mWIG40** Giełdy Papierów Wartościowych w Warszawie w dniu wyznaczania sygnału rebalansowania.
* **Źródło notowań:** Oficjalne kursy dzienne GPW (Stooq / GPW). W przypadku splitów akcji lub asymilacji stosowane są kursy skorygowane o operacje na kapitale.
* **Płynność:** Z racji doboru wyłącznie spośród 40 komponentów indeksu mWIG40, średni dzienny obrót każdej spółki z koszyka wynosi od kilkuset tysięcy do kilkunastu milionów PLN, co chroni przed poślizgiem cenowym (*slippage*) dla kapitałów indywidualnych i portfela testowego.

---

## 2. Kalkulacja Sygnału i Protokół Egzekucji EX_ANTE

Aby wyeliminować błąd logiczny (niemożność znajomości ceny zamknięcia przed zakończeniem sesji), protokół EX_ANTE dzieli proces na dwa etapy:

1. **Kalkulacja Sygnału (Sesja $t-1$):**
   * Sygnał rebalansowania i ranking momentum obliczane są na podstawie oficjalnych kursów zamknięcia sesji poprzedzającej dzień rebalansowania ($t-1$).
   * Nominalna stopa zwrotu z 90 sesji liczona jest jako:
     $$R_{90} = \frac{P_{t-1}}{P_{t-91}} - 1$$
   * W przypadku remisu decyduje wyższy wolumen obrotu z ostatnich 20 sesji.
2. **Publikacja Sygnału EX_ANTE (Przed otwarciem sesji $t$):**
   * Wpis EX_ANTE zawierający tickery, wagi oraz datę sygnału jest generowany, pieczętowany kryptograficznie i wypychany do publicznego repozytorium GitHub **przed otwarciem sesji giełdowej w dniu $t$** (do godz. 08:50).
3. **Cena Wejścia i Realizacja (Sesja $t$):**
   * Transakcje wejścia do portfela realizowane są po oficjalnym kursie zamknięcia sesji $t$ (fixing godz. 17:05). Ceny te są po sesji dopisywane do rejestru jako oficjalne ceny wejścia.

---

## 3. Strategie Inwestycyjne

### Strategia 1: Momentum mWIG40 TOP 3 (Wariant Skoncentrowany)
* **Identyfikator:** `mwig40_top3_90_130`
* **Selekcja:** 3 spółki o najwyższej wartości $R_{90}$ spośród komponentów mWIG40.
* **Alokacja:** Równe wagi kapitałowe ($w_i = \frac{1}{3} \approx 33.3333\%$). Brak dźwigni ($L = 1.0$), brak pozycji krótkich.

### Strategia 2: Momentum mWIG40 TOP 5 (Wariant Stabilny)
* **Identyfikator:** `mwig40_top5_90_130`
* **Selekcja:** 5 spółek o najwyższej wartości $R_{90}$.
* **Alokacja:** Równe wagi kapitałowe ($w_i = \frac{1}{5} = 20.00\%$).
* **Zależność testów:** Koszyk TOP 5 zawiera w sobie spółki z TOP 3, w związku z czym wyniki obu portfeli wykazują wysoką korelację i nie stanowią w pełni niezależnych prób statystycznych.

---

## 4. Harmonogram Cykli (Holding Period)

* **Cykl Jesień–Zima:** Wejście na zamknięciu sesji 24 września (lub najbliższej sesji giełdowej w tym dniu bądź po nim, jeśli 24.09 wypada w dzień wolny) → Wyjście na zamknięciu sesji 1 lutego (lub najbliższej sesji giełdowej w tym dniu bądź po nim).
* **Cykl Wiosna–Lato:** Wejście na zamknięciu sesji 1 lutego (lub najbliższej sesji po nim) → Wyjście na zamknięciu sesji 24 września (lub najbliższej sesji po nim).
* Czas trwania cyklu wynosi ok. 130 sesji giełdowych (~4 miesiące).

---

## 5. Benchmarki i Metodologia Mierzenia Wyników

1. **Podstawowy benchmark („Jabłka do jabłek”): Indeks Cenowy mWIG40**
   * Ponieważ portfele forward-testu nie reinwestują dywidend w trakcie trwania pojedynczego okna trzymania, podstawowym punktem odniesienia jest **cenowy indeks mWIG40**.
2. **Pomocniczy benchmark: mWIG40TR (Total Return)**
   * Uwzględnia dochody z dywidend, raportowany pomocniczo dla pełnej przejrzystości.
3. **Mierzenie przewagi:**
   * Nadwyżka stopy zwrotu raportowana jest precyzyjnie jako:
     $$\text{Excess Return} = R_{\text{portfel}} - R_{\text{mWIG40}}$$

---

## 6. Rygor Protokolarny i Dowód Nienaruszalności

* **Wpisy `EX_ANTE`:** Skład koszyka i wagi opublikowane i zapieczętowane w repozytorium GitHub przed sesją startową.
* **Wpisy `RETROACTIVE`:** Sygnały z przeszłości lub zarejestrowane po starcie cyklu – jawnie oznaczone jako niemające zewnętrznego dowodu czasu ex-ante.
* **Separacja danych:**
  * `forward_test_ledger.json` zawiera wyłącznie niezmienne wpisy zarejestrowanych cykli (tryb append-only, stały hash pliku między rebalansowaniami).
  * `live_status.json` zawiera dynamiczne śledzenie live generowane po każdej sesji.
