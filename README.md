# Invoice Extractor

Narzędzie do automatycznego ekstrakcji strukturalnych informacji z faktur przy użyciu OpenAI API. Projekt wykorzystuje GPT-4o-mini do analizy tekstu faktury i zwracania danych w ustrukturyzowanym formacie JSON.

An AI-powered tool for automatically extracting structured information from invoices using OpenAI API. The project uses GPT-4o-mini to analyze invoice text and return data in a structured JSON format.

## Funkcjonalności / Features

- 📄 Ekstrakcja danych z faktur (nazwa sprzedawcy, data, pozycje, kwoty)
- 🔍 Walidacja danych przy użyciu Pydantic
- 🌍 Obsługa faktur w języku polskim
- ⚙️ Konfiguracja poprzez zmienne środowiskowe

- 📄 Invoice data extraction (vendor name, date, items, amounts)
- 🔍 Data validation using Pydantic
- 🌍 Support for Polish invoices
- ⚙️ Configuration via environment variables

## Wymagania / Requirements

- Python >= 3.12
- OpenAI API key

## Instalacja / Installation

1. Sklonuj repozytorium lub pobierz projekt:
```bash
git clone <repository-url>
cd invoice_extractor
```

2. Zainstaluj zależności używając `uv`:
```bash
uv sync
```

3. Utwórz plik `.env` w katalogu głównym projektu:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

## Struktura projektu / Project Structure

```
invoice_extractor/
├── main.py              # Przykład użycia / Usage example
├── pyproject.toml       # Konfiguracja projektu / Project configuration
├── src/
│   ├── __init__.py
│   ├── config.py        # Konfiguracja ustawień / Settings configuration
│   ├── extractor.py     # Główna logika ekstrakcji / Main extraction logic
│   └── schemas.py       # Modele danych Pydantic / Pydantic data models
└── README.md
```

## Użycie / Usage

### Podstawowy przykład / Basic Example

```python
from openai import OpenAI
import src.extractor as invoice_extractor
from src.config import settings

# Utwórz instancję ekstraktora / Create extractor instance
extractor = invoice_extractor.InvoiceExtractor(
    OpenAI(api_key=settings.OPENAI_API_KEY)
)

# Tekst faktury / Invoice text
invoice_text = """
Od: Sklep "Elektronika i Kawa" <no-reply@electro-coffee.pl>
Data sprzedaży: 24-01-2025
Nabywca: Jan Kowalski

Pozycje na rachunku:
1. Laptop Gamingowy X500 - 1 szt - 4500.00 PLN
2. Podkładka pod mysz RGB - 2 szt - 50.00 PLN (razem 100.00)
3. Kawa ziarnista 1kg - 1 szt - 80.50 PLN

Suma netto: 3805.28
VAT (23%): 875.22
ŁĄCZNIE DO ZAPŁATY: 4680.50 PLN
"""

# Ekstrakcja danych / Extract data
invoice_data = extractor.extract_info(invoice_text)
print(invoice_data)
```

### Format wyjściowy / Output Format

Dane są zwracane jako obiekt `Invoice` z następującą strukturą:

Data is returned as an `Invoice` object with the following structure:

```python
class Invoice:
    vendor_name: str          # Nazwa sprzedawcy / Vendor name
    invoice_date: date        # Data faktury / Invoice date
    items: List[Item]         # Lista pozycji / List of items
    total_amount: Decimal     # Łączna kwota / Total amount
    currency: str             # Waluta / Currency

class Item:
    name: str                 # Nazwa produktu / Product name
    quantity: int             # Ilość / Quantity
    price: Decimal            # Cena / Price
```

## Konfiguracja / Configuration

Projekt używa `pydantic-settings` do zarządzania konfiguracją. Klucz API OpenAI jest ładowany z pliku `.env` w katalogu nadrzędnym projektu.

The project uses `pydantic-settings` for configuration management. The OpenAI API key is loaded from the `.env` file in the parent directory.

### Zmienne środowiskowe / Environment Variables

- `OPENAI_API_KEY` - Klucz API OpenAI (wymagany) / OpenAI API key (required)

### Zmiana modelu / Changing Model

Domyślnie używany jest model `gpt-4o-mini`. Możesz zmienić model przekazując parametr:

By default, the `gpt-4o-mini` model is used. You can change the model by passing a parameter:

```python
invoice_data = extractor.extract_info(invoice_text, model="gpt-4o")
```

## Obsługa błędów / Error Handling

Projekt definiuje następujące wyjątki:

The project defines the following exceptions:

- `InvoiceError` - Wywoływany gdy dane faktury są niepoprawne / Raised when invoice data is invalid
- `LLMError` - Wywoływany gdy wystąpi błąd podczas komunikacji z API OpenAI / Raised when an error occurs during OpenAI API communication

## Zależności / Dependencies

- `openai>=2.15.0` - Klient OpenAI API
- `pydantic>=2.12.5` - Walidacja danych i strukturyzowane wyjście
- `pydantic-settings>=2.12.0` - Zarządzanie ustawieniami

## Licencja / License

[Określ licencję projektu / Specify project license]

## Autor / Author

[Twoje imię / Your name]
