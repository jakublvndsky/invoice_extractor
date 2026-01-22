# Invoice Extractor

Narzędzie do automatycznego ekstrakcji strukturalnych informacji z faktur przy użyciu OpenAI API. Projekt wykorzystuje GPT-4o-mini do analizy tekstu faktury i zwracania danych w ustrukturyzowanym formacie JSON. Zawiera REST API oparte na FastAPI oraz magazyn wektorowy Qdrant do przechowywania i wyszukiwania faktur.

An AI-powered tool for automatically extracting structured information from invoices using OpenAI API. The project uses GPT-4o-mini to analyze invoice text and return data in a structured JSON format. Includes a FastAPI-based REST API and Qdrant vector storage for storing and searching invoices.

## Funkcjonalności / Features

- 📄 Ekstrakcja danych z faktur (nazwa sprzedawcy, data, pozycje, kwoty)
- 🔍 Walidacja danych przy użyciu Pydantic
- 🌍 Obsługa faktur w języku polskim
- ⚙️ Konfiguracja poprzez zmienne środowiskowe
- 🚀 REST API oparte na FastAPI
- 💾 Magazyn wektorowy Qdrant z embeddingami OpenAI
- ⚡ Asynchroniczna obsługa zapytań

- 📄 Invoice data extraction (vendor name, date, items, amounts)
- 🔍 Data validation using Pydantic
- 🌍 Support for Polish invoices
- ⚙️ Configuration via environment variables
- 🚀 FastAPI-based REST API
- 💾 Qdrant vector storage with OpenAI embeddings
- ⚡ Asynchronous request handling

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
│   ├── api.py           # FastAPI aplikacja / FastAPI application
│   ├── config.py        # Konfiguracja ustawień / Settings configuration
│   ├── extractor.py     # Główna logika ekstrakcji / Main extraction logic
│   ├── schemas.py       # Modele danych Pydantic / Pydantic data models
│   └── storage.py       # Magazyn wektorowy Qdrant / Qdrant vector storage
└── README.md
```

## Użycie / Usage

### REST API

Uruchom serwer API:

Start the API server:

```bash
uvicorn src.api:app --reload
```

API będzie dostępne pod adresem `http://localhost:8000`. Dokumentacja interaktywna dostępna jest pod `http://localhost:8000/docs`.

The API will be available at `http://localhost:8000`. Interactive documentation is available at `http://localhost:8000/docs`.

#### Endpoint `/extract`

Wysyła POST request z tekstem faktury i zwraca wyekstrahowane dane. Faktura jest automatycznie zapisywana w magazynie wektorowym Qdrant.

Send a POST request with invoice text and receive extracted data. The invoice is automatically saved to Qdrant vector storage.

```bash
curl -X POST "http://localhost:8000/extract" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Od: Sklep \"Elektronika i Kawa\" <no-reply@electro-coffee.pl>\nData sprzedaży: 24-01-2025\nNabywca: Jan Kowalski\n\nPozycje na rachunku:\n1. Laptop Gamingowy X500 - 1 szt - 4500.00 PLN\n2. Podkładka pod mysz RGB - 2 szt - 50.00 PLN (razem 100.00)\n3. Kawa ziarnista 1kg - 1 szt - 80.50 PLN\n\nSuma netto: 3805.28\nVAT (23%): 875.22\nŁĄCZNIE DO ZAPŁATY: 4680.50 PLN"
  }'
```

### Podstawowy przykład w Pythonie / Basic Python Example

```python
import src.extractor as invoice_extractor
import asyncio
from openai import AsyncOpenAI
from src.config import settings

# Utwórz instancję ekstraktora / Create extractor instance
extractor = invoice_extractor.InvoiceExtractor(
    AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
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

# Ekstrakcja danych (asynchroniczna) / Extract data (async)
invoice_data = asyncio.run(extractor.extract_info(invoice_text))
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
invoice_data = await extractor.extract_info(invoice_text, model="gpt-4o")
```

### Magazyn wektorowy / Vector Storage

Projekt wykorzystuje Qdrant do przechowywania faktur z embeddingami. Każda wyekstrahowana faktura jest automatycznie zapisywana w magazynie wektorowym z embeddingiem wygenerowanym przez model `text-embedding-3-small` OpenAI. Domyślnie używany jest Qdrant w pamięci (`:memory:`), co oznacza, że dane są tracone po zakończeniu działania aplikacji.

The project uses Qdrant to store invoices with embeddings. Each extracted invoice is automatically saved to vector storage with an embedding generated by OpenAI's `text-embedding-3-small` model. By default, an in-memory Qdrant (`:memory:`) is used, which means data is lost when the application stops.

## Obsługa błędów / Error Handling

Projekt definiuje następujące wyjątki:

The project defines the following exceptions:

- `InvoiceError` - Wywoływany gdy dane faktury są niepoprawne / Raised when invoice data is invalid
- `LLMError` - Wywoływany gdy wystąpi błąd podczas komunikacji z API OpenAI / Raised when an error occurs during OpenAI API communication

## Zależności / Dependencies

- `openai>=2.15.0` - Klient OpenAI API / OpenAI API client
- `pydantic>=2.12.5` - Walidacja danych i strukturyzowane wyjście / Data validation and structured output
- `pydantic-settings>=2.12.0` - Zarządzanie ustawieniami / Settings management
- `fastapi>=0.128.0` - Framework REST API / REST API framework
- `uvicorn>=0.40.0` - Serwer ASGI / ASGI server
- `qdrant-client>=1.16.2` - Klient magazynu wektorowego Qdrant / Qdrant vector storage client


## Autor / Author

jakublvndsky
