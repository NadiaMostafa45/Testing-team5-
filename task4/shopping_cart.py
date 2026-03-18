from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict


def _to_decimal_money(value: int | float | str | Decimal) -> Decimal:
    try:
        d = Decimal(str(value))
    except Exception as e:  # pragma: no cover
        raise TypeError("price must be a number") from e

    if d.is_nan() or d.is_infinite():
        raise ValueError("price must be a finite number")

    if d < 0:
        raise ValueError("price must be >= 0")

    return d.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _validate_name(name: str) -> str:
    if not isinstance(name, str):
        raise TypeError("name must be a string")
    cleaned = name.strip()
    if not cleaned:
        raise ValueError("name must not be empty")
    return cleaned


def _validate_quantity(quantity: int) -> int:
    if not isinstance(quantity, int):
        raise TypeError("quantity must be an int")
    if quantity <= 0:
        raise ValueError("quantity must be > 0")
    return quantity


@dataclass
class CartItem:
    name: str
    price: Decimal
    quantity: int

    @property
    def subtotal(self) -> Decimal:
        return (self.price * Decimal(self.quantity)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )


class ShoppingCart:
    def __init__(self) -> None:
        self._items: Dict[str, CartItem] = {}

    def add_item(self, name: str, price: int | float | str | Decimal, quantity: int = 1) -> None:
        name = _validate_name(name)
        price_d = _to_decimal_money(price)
        quantity = _validate_quantity(quantity)

        if name in self._items:
            existing = self._items[name]
            if existing.price != price_d:
                raise ValueError("cannot add same item name with different price")
            existing.quantity += quantity
        else:
            self._items[name] = CartItem(name=name, price=price_d, quantity=quantity)

    def remove_item(self, name: str, quantity: int = 1) -> None:
        name = _validate_name(name)
        quantity = _validate_quantity(quantity)

        if name not in self._items:
            raise KeyError("item not found")

        item = self._items[name]
        if quantity >= item.quantity:
            del self._items[name]
        else:
            item.quantity -= quantity

    def clear(self) -> None:
        self._items.clear()

    def total(self) -> Decimal:
        total = sum((item.subtotal for item in self._items.values()), Decimal("0.00"))
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def item_count(self) -> int:
        return sum(item.quantity for item in self._items.values())

    def unique_items(self) -> int:
        return len(self._items)

    def get_item(self, name: str) -> CartItem:
        name = _validate_name(name)
        if name not in self._items:
            raise KeyError("item not found")
        item = self._items[name]
        return CartItem(name=item.name, price=item.price, quantity=item.quantity)

    def items_snapshot(self) -> Dict[str, CartItem]:
        return {k: self.get_item(k) for k in self._items.keys()}

