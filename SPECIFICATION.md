# Specyfikacja Matematyczna Strategii – WealthStrategy

Dokument specyfikacji technicznej i reguł inwestycyjnych podlegających publicznemu rejestrowi Forward-Test.
Skrót kryptograficzny SHA-256 niniejszego dokumentu jest na stałe zakotwiczony w rejestrze `forward_test_ledger.json`.

---

## 1. Uniwersum Inwestycyjne i Filtry Płynności

* **Uniwersum:** Spółki wchodzące w skład oficjalnego indeksu **mWIG40** Giełdy Papierów Wartościowych w Warszawie na dzień wyznaczania sygnału rebalansowania.
* **Filtr płynności:** Wybór z komponentów mWIG40 gwarantuje obroty dzienne na poziomie od kilkuset tysięcy do kilkunastu milionów PLN, co eliminuje problem poślizgu cenowego (*slippage*) dla kapitałów indywidualnych i portfeli testowych.
* **Ceny transakcyjne:** Kursy zamknięcia (*Close*) w oficjalnym dniu rebalansowania.

---

## 2. Strategia 1: Momentum mWIG40 TOP 3 (Wariant Skoncentrowany)

* **Identyfikator:** `mwig40_top3_90_130`
* **Metryka rankingu:** Nominalna stopa zwrotu z ostatnich 90 sesji giełdowych:
  $$R_{90} = \frac{P_t}{P_{t-90}} - 1$$
* **Selekcja:** 3 spółki o najwyższej wartości $R_{90}$ spośród uniwersum mWIG40.
* **Alokacja:** Równe wagi kapitałowe ($w_i = \frac{1}{3} \approx 33.3333\%$). Brak dźwigni finansowej ($L = 1.0$), brak pozycji krótkich.
* **Horyzont trzymania (Holding Period):** ~130 sesji (ok. 4 miesiące).
* **Cykle stałe:**
  * Cykl Jesień–Zima: ok. 24 września → 1 lutego.
  * Cykl Wiosna–Lato: ok. 1 lutego → przełom maja/czerwca / września.

---

## 3. Strategia 2: Momentum mWIG40 TOP 5 (Wariant Stabilny)

* **Identyfikator:** `mwig40_top5_90_130`
* **Metryka rankingu:** Identyczna jak w strategii TOP 3 ($R_{90}$).
* **Selekcja:** 5 spółek o najwyższej wartości $R_{90}$.
* **Alokacja:** Równe wagi kapitałowe ($w_i = \frac{1}{5} = 20.00\%$).
* **Cel:** Ograniczenie ryzyka specyficznego (idiosynkratycznego) pojedynczej spółki oraz redukcja tracking error względem indeksu bazowego.

---

## 4. Benchmarki i Metodologia Mierzenia Wyników

1. **Podstawowy benchmark („Jabłka do jabłek”): Indeks Cenowy mWIG40**
   * Portfele forward-testu mierzone są na podstawie czystych kursów giełdowych (bez reinwestycji dywidend w trakcie trwania cyklu).
   * Prawidłowym punktem odniesienia jest **cenowy indeks mWIG40**.
2. **Pomocniczy benchmark: mWIG40TR (Total Return)**
   * Uwzględnia dochody z dywidend, raportowany pomocniczo.
3. **Mierzenie przewagi:**
   * Zgodnie z rygorem ekonometrycznym nadwyżka stopy zwrotu portfela ponad indeks cenowy raportowana jest precyzyjnie jako:
     $$\text{Excess Return} = R_{\text{portfel}} - R_{\text{mWIG40}}$$
   * Pojęcie „Alfa” stosowane jest wyłącznie potocznie jako synonim Excess Return, chyba że podano współczynniki regresji CAPM.

---

## 5. Rygor Protokolarny Forward-Testu

* **Wpisy `EX_ANTE`:** Sygnał, wagi i ceny wejścia zarejestrowane, zahashowane i wypchnięte do zdalnego repozytorium GitHub najpóźniej w dniu startu cyklu przed zamknięciem sesji.
* **Wpisy `RETROACTIVE`:** Sygnały z przeszłości lub zarejestrowane po starcie cyklu – jawnie oznaczone jako niemające zewnętrznego dowodu czasu ex-ante.
* **Niezmienność:** Wpisy historyczne tworzą łańcuch SHA-256 w pliku `forward_test_ledger.json` (tryb append-only). Bieżące wyniki rynkowe raportowane są w osobnym, dynamicznym pliku `live_status.json`.
