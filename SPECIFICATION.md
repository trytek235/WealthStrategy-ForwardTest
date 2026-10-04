# Specyfikacja Matematyczna Strategii – WealthStrategy

Dokument specyfikacji technicznej i reguł inwestycyjnych podlegających publicznemu rejestrowi Forward-Test.
Skrót kryptograficzny SHA-256 niniejszego dokumentu jest na stałe zakotwiczony w rejestrze `forward_test_ledger.json`.

> **Nota o dacie wejścia w życie:** Niniejsza specyfikacja została spisana i zapieczętowana dnia 04.10.2026 r. Cykl z 24.09.2026 r. wystartował przed jej formalnym zapieczętowaniem na GitHubie, dlatego jest w pełni jawnie i rzetelnie oznaczony w rejestrze jako **`RETROACTIVE`**. Pełny, zewnętrznie potwierdzony rygor **`EX_ANTE`** obowiązuje dla wszystkich kolejnych cykli (najbliższy: 01.02.2027 r.).

---

## 1. Uniwersum Inwestycyjne i Płynność

* **Uniwersum bazowe:** Spółki wchodzące w skład oficjalnego indeksu **mWIG40** Giełdy Papierów Wartościowych w Warszawie w dniu wyznaczania sygnału rebalansowania.
* **Źródło notowań:** Oficjalne kursy dzienne GPW (Stooq / GPW). W przypadku splitów akcji lub asymilacji stosowane są kursy skorygowane o operacje na kapitale.
* **Ceny transakcyjne:** Kursy zamknięcia (*Close*) w oficjalnym dniu rebalansowania (cena fixingowa na koniec sesji).
* **Płynność:** Z racji doboru wyłącznie spośród 40 komponentów indeksu mWIG40, średni dzienny obrót każdej spółki z koszyka wynosi od kilkuset tysięcy do kilkunastu milionów PLN, co chroni przed poślizgiem cenowym (*slippage*) dla kapitałów indywidualnych i portfela testowego.

---

## 2. Strategia 1: Momentum mWIG40 TOP 3 (Wariant Skoncentrowany)

* **Identyfikator:** `mwig40_top3_90_130`
* **Metryka rankingu:** Nominalna stopa zwrotu z ostatnich 90 sesji giełdowych:
  $$R_{90} = \frac{P_t}{P_{t-90}} - 1$$
* **Selekcja:** 3 spółki o najwyższej wartości $R_{90}$ spośród komponentów mWIG40. W przypadku remisu decyduje wyższy wolumen obrotu z ostatnich 20 sesji.
* **Alokacja:** Równe wagi kapitałowe ($w_i = \frac{1}{3} \approx 33.3333\%$). Brak dźwigni ($L = 1.0$), brak pozycji krótkich.
* **Harmonogram cykli (Holding Period):**
  * **Cykl Jesień–Zima:** Wejście na zamknięciu sesji 24 września (lub ostatniej sesji przed/w tym dniu) → Wyjście na zamknięciu sesji 1 lutego (lub najbliższej sesji giełdowej).
  * **Cykl Wiosna–Lato:** Wejście na zamknięciu sesji 1 lutego → Wyjście na zamknięciu sesji 24 września.

---

## 3. Strategia 2: Momentum mWIG40 TOP 5 (Wariant Stabilny)

* **Identyfikator:** `mwig40_top5_90_130`
* **Metryka rankingu:** Identyczna jak w strategii TOP 3 ($R_{90}$).
* **Selekcja:** 5 spółek o najwyższej wartości $R_{90}$.
* **Alokacja:** Równe wagi kapitałowe ($w_i = \frac{1}{5} = 20.00\%$).
* **Zależność testów:** Zgodnie z metodologią statystyczną zaznacza się, że koszyk TOP 5 zawiera w sobie spółki z TOP 3, w związku z czym wyniki obu portfeli wykazują wysoką korelację i nie stanowią w pełni niezależnych prób statystycznych.

---

## 4. Benchmarki i Metodologia Mierzenia Wyników

1. **Podstawowy benchmark („Jabłka do jabłek”): Indeks Cenowy mWIG40**
   * Ponieważ portfele forward-testu nie reinwestują dywidend w trakcie trwania pojedynczego okna trzymania, podstawowym punktem odniesienia jest **cenowy indeks mWIG40**.
2. **Pomocniczy benchmark: mWIG40TR (Total Return)**
   * Uwzględnia dochody z dywidend, raportowany pomocniczo dla pełnej przejrzystości.
3. **Mierzenie przewagi:**
   * Nadwyżka stopy zwrotu raportowana jest precyzyjnie jako:
     $$\text{Excess Return} = R_{\text{portfel}} - R_{\text{mWIG40}}$$

---

## 5. Rygor Protokolarny i Dowód Nienaruszalności

* **Wpisy `EX_ANTE`:** Sygnał, wagi i ceny wejścia zarejestrowane, zahashowane i wypchnięte do publicznego repozytorium GitHub najpóźniej w dniu startu cyklu przed zamknięciem sesji.
* **Wpisy `RETROACTIVE`:** Sygnały historyczne lub zarejestrowane po starcie cyklu – jawnie oznaczone jako niemające zewnętrznego dowodu czasu ex-ante.
* **Separacja danych:**
  * `forward_test_ledger.json` zawiera wyłącznie niezmienne wpisy zarejestrowanych cykli (tryb append-only, stały hash pliku między rebalansowaniami).
  * `live_status.json` zawiera dynamiczne śledzenie live generowane po każdej sesji.
