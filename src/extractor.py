from openai import AsyncOpenAI
from src.schemas import Invoice


class LLMError(Exception):
    pass


class InvoiceError(Exception):
    pass


class InvoiceExtractor:
    def __init__(self, client: AsyncOpenAI):
        self.client = client

    async def extract_info(
        self, invoice_data: str, model: str = "gpt-4o-mini"
    ) -> Invoice:
        if not invoice_data.strip():
            raise InvoiceError("Nie poprawnie przesłana faktura")
        else:
            try:
                response = await self.client.chat.completions.parse(
                    model=model,
                    messages=[
                        {"role": "user", "content": invoice_data},
                        {
                            "role": "system",
                            "content": """ ### ROLA
Jesteś ekspertem ds. ekstrakcji danych z dokumentów finansowych (AI Invoice Parser). Twoim zadaniem jest przeanalizowanie surowego tekstu faktury i mapowanie go na ściśle określony schemat danych.

### CEL
Wyodrębnij dane do obiektu `Invoice`, dbając o poprawność typów danych (Decimal, int, date) i logikę biznesową.

### INSTRUKCJE DOTYCZĄCE PÓL (MAPOWANIE)

**1. vendor_name (str)**
* Zidentyfikuj sprzedawcę (wystawcę). Szukaj sekcji "Sprzedawca", "Wystawca" lub głównego logo/nagłówka na górze dokumentu.
* Nie pomyl sprzedawcy z "Nabywcą" (Odbiorcą).
* Podaj pełną nazwę firmy.

**2. invoice_date (date)**
* Znajdź "Datę wystawienia" (Invoice Date).
* Jeśli dokument zawiera "Datę sprzedaży" różną od daty wystawienia, priorytet ma **Data wystawienia**.
* Sformatuj wynik zgodnie ze standardem ISO 8601 (YYYY-MM-DD), niezależnie od formatu wejściowego (np. "24 sty 2025" -> "2025-01-24").

**3. items (List[Item])**
Przeanalizuj tabelę pozycji na fakturze. Dla każdego wiersza utwórz obiekt `Item`:
* **name (str):** Przepisz nazwę towaru lub usługi. Pomiń kody produktu (np. PKWiU, EAN), chyba że są integralną częścią nazwy.
* **quantity (int):**
    * Wyodrębnij ilość.
    * UWAGA: Model wymaga liczby całkowitej (`int`). Jeśli na fakturze ilość jest ułamkowa (np. 1.5 kg), zaokrąglij ją matematycznie do najbliższej liczby całkowitej lub potraktuj jako 1 (sztukę usługi), jeśli zaokrąglenie zmieniłoby sens. W większości przypadków szukaj liczby w kolumnie "Ilość".
* **price (Decimal):**
    * To powinna być cena **jednostkowa** (Unit Price), zazwyczaj netto, chyba że faktura jest wystawiona tylko w brutto (np. paragon).
    * Upewnij się, że format liczby jest poprawny dla typu Decimal (kropka jako separator dziesiętny).

**4. total_amount (Decimal)**
* To ostateczna kwota **do zapłaty** (Total Gross / Brutto).
* Szukaj podsumowania faktury (np. "Do zapłaty", "Razem brutto").
* Jeśli występuje podział na waluty, wybierz kwotę główną dokumentu.

**5. currency (str)**
* Kod waluty w formacie ISO 4217 (np. PLN, EUR, USD).
* Jeśli brak wyraźnego kodu, wywnioskuj go z symboli (zł -> PLN, € -> EUR, $ -> USD).

### ZASADY FORMATOWANIA I OBSŁUGI OCR

1.  **Liczby i Separatory (Kluczowe dla Decimal):**
    * Dokumenty mogą używać formatu polskiego (`1 200,50`) lub międzynarodowego (`1,200.50`).
    * Twoim zadaniem jest znormalizowanie liczby do formatu `XXXX.YY` (bez spacji, kropka jako separator dziesiętny) przed przekazaniem jej do modelu Pydantic.
    * Przykład: Tekst "1.000,00 zł" -> Wartość `1000.00`.

2.  **Szum informacyjny:**
    * Ignoruj numery stron, stopki, numery kont bankowych (chyba że są potrzebne do weryfikacji sprzedawcy) oraz teksty marketingowe.
    * Nie traktuj wierszy "Suma", "Podsumowanie VAT" jako pozycji na liście `items`.

### LOGIKA WERYFIKACJI
Jeśli jakość OCR jest niska, użyj kontekstu:
* Jeśli `quantity` * `price` drastycznie różni się od wartości wiersza, sprawdź, czy nie pomyliłeś ceny netto z brutto. Preferuj kwoty, które matematycznie sumują się do `total_amount`. """,
                        },
                    ],
                    response_format=Invoice,
                )
                output = response.choices[0].message
                if output.refusal:
                    raise LLMError(f"Model refused: {output.refusal}")
                else:
                    return output.parsed
            except Exception as e:
                raise LLMError("Wystąpił błąd przy generowaniu odpowiedzi") from e
