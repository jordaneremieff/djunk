from __future__ import annotations
from typing import List
from dataclasses import dataclass, field, asdict

import pytest


@dataclass
class Product:
    name: str
    eligible_for_points: bool
    promotions: list

    @classmethod
    def generate(cls) -> List[Product]:
        return [
            cls(
                name="P1",
                eligible_for_points=True,
                promotions=["1", "2"],
            ),
            cls(
                name="P2",
                eligible_for_points=True,
                promotions=[],
            ),
            cls(
                name="P3",
                eligible_for_points=False,
                promotions=["3", "4"],
            ),
        ]


@dataclass
class Item:
    product: Product
    price: int

    @classmethod
    def generate(cls, products: List[Product], price: int) -> List[Item]:
        return [cls(product=product, price=price) for product in products]


@dataclass
class Order:
    items: List[Item]
    eligible_for_points: bool
    total: int
    item_count: int = field(init=False)

    def __post_init__(self):
        self.item_count = len(self.items)

    @classmethod
    def generate(
        cls,
        eligible_for_points: bool,
        total: int,
        membership_type: str,
        membership_points: int,
    ) -> dict:
        products = Product.generate()
        items = Item.generate(products, 30 if total >= 100 else 5)
        order = Order(
            eligible_for_points=eligible_for_points,
            items=items,
            total=total,
        )
        membership = {"type": membership_type, "points": membership_points}

        return {"order": asdict(order), "membership": membership}


@pytest.fixture()
def order_factory():
    return Order.generate
