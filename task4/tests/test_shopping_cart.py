import pytest

from shopping_cart import ShoppingCart


def test_new_cart_is_empty():
    cart = ShoppingCart()
    assert cart.total() == pytest.approx(0)
    assert cart.item_count() == 0
    assert cart.unique_items() == 0


def test_add_item_increases_counts_and_total():
    cart = ShoppingCart()
    cart.add_item("Apple", 10, quantity=2)
    cart.add_item("Banana", "2.50", quantity=3)

    assert cart.item_count() == 5
    assert cart.unique_items() == 2
    assert float(cart.total()) == pytest.approx(10 * 2 + 2.5 * 3)


def test_add_same_item_accumulates_quantity_if_same_price():
    cart = ShoppingCart()
    cart.add_item("Milk", 12.0, quantity=1)
    cart.add_item("Milk", "12.00", quantity=2)
    assert cart.item_count() == 3
    assert cart.unique_items() == 1
    assert float(cart.total()) == pytest.approx(36.0)


def test_add_same_item_with_different_price_raises():
    cart = ShoppingCart()
    cart.add_item("Milk", 12.0, quantity=1)
    with pytest.raises(ValueError):
        cart.add_item("Milk", 13.0, quantity=1)


def test_remove_partial_quantity():
    cart = ShoppingCart()
    cart.add_item("Orange", 3, quantity=5)
    cart.remove_item("Orange", quantity=2)
    assert cart.item_count() == 3
    assert cart.unique_items() == 1
    assert float(cart.total()) == pytest.approx(9.0)


def test_remove_more_than_exists_removes_item():
    cart = ShoppingCart()
    cart.add_item("Orange", 3, quantity=2)
    cart.remove_item("Orange", quantity=5)
    assert cart.item_count() == 0
    assert cart.unique_items() == 0
    assert float(cart.total()) == pytest.approx(0.0)


def test_remove_nonexistent_item_raises_keyerror():
    cart = ShoppingCart()
    with pytest.raises(KeyError):
        cart.remove_item("Ghost", quantity=1)


@pytest.mark.parametrize(
    "name,price,quantity,exc",
    [
        ("", 10, 1, ValueError),
        ("   ", 10, 1, ValueError),
        (123, 10, 1, TypeError),
        ("A", -1, 1, ValueError),
        ("A", float("inf"), 1, ValueError),
        ("A", 10, 0, ValueError),
        ("A", 10, -2, ValueError),
        ("A", 10, 1.5, TypeError),
    ],
)
def test_add_invalid_inputs(name, price, quantity, exc):
    cart = ShoppingCart()
    with pytest.raises(exc):
        cart.add_item(name, price, quantity=quantity)


@pytest.mark.parametrize(
    "name,quantity,exc",
    [
        ("", 1, ValueError),
        ("A", 0, ValueError),
        ("A", -1, ValueError),
        ("A", 1.2, TypeError),
    ],
)
def test_remove_invalid_inputs(name, quantity, exc):
    cart = ShoppingCart()
    cart.add_item("A", 1, quantity=1)
    with pytest.raises(exc):
        cart.remove_item(name, quantity=quantity)


def test_get_item_returns_copy_not_internal_reference():
    cart = ShoppingCart()
    cart.add_item("Egg", 2, quantity=2)
    item = cart.get_item("Egg")
    assert item.quantity == 2
    item.quantity = 999
    assert cart.get_item("Egg").quantity == 2


def test_clear_empties_cart():
    cart = ShoppingCart()
    cart.add_item("A", 1, quantity=1)
    cart.add_item("B", 2, quantity=2)
    cart.clear()
    assert cart.total() == pytest.approx(0)
    assert cart.item_count() == 0
    assert cart.unique_items() == 0

