from datetime import date
from decimal import Decimal
from pydantic import BaseModel
from typing import List


class Item(BaseModel):
    name: str
    quantity: int
    price: Decimal


class Invoice(BaseModel):
    vendor_name: str
    invoice_date: date
    items: List[Item]
    total_amount: Decimal
    currency: str
