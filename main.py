import src.extractor as invoice_extractor
import asyncio
from openai import AsyncOpenAI
from src.config import settings


if __name__ == "__main__":
    extractor = invoice_extractor.InvoiceExtractor(
        AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    )
    output = asyncio.run(
        extractor.extract_info(""" Od: Sklep "Elektronika i Kawa" <no-reply@electro-coffee.pl>
Temat: Twoje zamówienie #99281

Cześć! Dzięki za zakupy. Poniżej szczegóły Twojej ostatniej transakcji.

Data sprzedaży: 24-01-2025
Nabywca: Jan Kowalski

Pozycje na rachunku:
1. Laptop Gamingowy X500 - 1 szt - 4500.00 PLN
2. Podkładka pod mysz RGB - 2 szt - 50.00 PLN (razem 100.00)
3. Kawa ziarnista 1kg - 1 szt - 80.50 PLN

Suma netto: 3805.28
VAT (23%): 875.22
ŁĄCZNIE DO ZAPŁATY: 4680.50 PLN

Dziękujemy i zapraszamy ponownie!
Zespół E&K """)
    )
    print(output)
