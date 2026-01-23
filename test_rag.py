import requests
import time

BASE_URL = "http://127.0.0.1:8000"


def run_test():
    # 1. Wrzucamy fakturę (zwróć uwagę: nie ma tu słowa 'biuro', jest 'fotel' i 'biurko')
    print("1️⃣  Wysyłam fakturę do analizy...")
    invoice_text = """
    Sprzedawca: MebleX Sp. z o.o.
    Data: 2025-02-01
    1. Fotel Ergonomiczny 'Prezes' - 1 szt - 1200 PLN
    2. Biurko regulowane elektrycznie - 1 szt - 3000 PLN
    Razem: 4200 PLN
    """

    r = requests.post(f"{BASE_URL}/extract", json={"content": invoice_text})
    if r.status_code != 200:
        print(f"❌ Błąd ekstrakcji: {r.text}")
        return
    print("✅ Faktura przetworzona i (mam nadzieję) zapisana w Qdrant.")

    # Dajemy chwilę bazie (choć przy memory to natychmiastowe)
    time.sleep(1)

    # 2. Szukamy po ZNACZENIU (Semantic Search)
    query = "zakup wyposażenia do biura"
    print(f"\n2️⃣  Szukam w bazie frazy: '{query}'...")

    r = requests.post(f"{BASE_URL}/search", json={"query": query, "limit": 1})
    results = r.json()

    # 3. Analiza wyników
    if results:
        top_match = results["points"][0]
        score = top_match.get("score", 0)
        payload = top_match.get("payload", {})

        print(f"\n🎉 SUKCES! Znaleziono fakturę!")
        print(f"   Dopasowanie (Score): {score:.4f}")
        print(f"   Sprzedawca z bazy: {payload.get('vendor_name')}")
        print(f"   Produkty: {payload.get('items')}")
    else:
        print("❌ Pusty wynik. Archiwista zgubił fakturę.")


if __name__ == "__main__":
    run_test()
