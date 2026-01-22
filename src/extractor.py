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
                            "content": "Analizujesz dane z faktury i zwracasz ustrukutyrozwaną formę zgodną z formatem",
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
