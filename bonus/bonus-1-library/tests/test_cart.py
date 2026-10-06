import json

import pytest
from assertionengine import AssertionOperator

from conftest import json_response
from demoshop_library.client import DemoShopError

# Bodies copied verbatim from the local shop (version 0.3.0); the session is replaced by the fake's.
EMPTY_CART = {"session": "fake", "items": [], "total": 0}
TWO_LINES = {
    "session": "fake",
    "items": [
        {"product_id": 1, "name": "Aurora Neural Headphones", "quantity": 2, "unit_price": 249.99, "total_price": 499.98},
        {"product_id": 2, "name": "Insight Smart Notebook", "quantity": 1, "unit_price": 39.5, "total_price": 39.5},
    ],
    "total": 539.48,
}
PRODUCT_NOT_FOUND = {"detail": "Product not found"}
QUANTITY_TOO_HIGH = {
    "detail": [
        {
            "type": "less_than_equal",
            "loc": ["body", "quantity"],
            "msg": "Input should be less than or equal to 20",
            "input": 21,
            "ctx": {"le": 20},
        }
    ]
}
QUANTITY_TOO_LOW = {
    "detail": [
        {
            "type": "greater_than_equal",
            "loc": ["body", "quantity"],
            "msg": "Input should be greater than or equal to 1",
            "input": 0,
            "ctx": {"ge": 1},
        }
    ]
}


@pytest.fixture
def shop(library, fake_shop):
    fake_shop.add("POST", "/api/cart/items", json_response(200, TWO_LINES))
    fake_shop.add("GET", "/api/cart/", json_response(200, EMPTY_CART))
    return library()


# Add Product To Cart


def test_add_sends_default_quantity(shop, fake_shop):
    assert shop.run_keyword("add_product_to_cart", [1]) is None

    sent = fake_shop.requests[-1]
    assert (sent.method, sent.url) == ("POST", "http://shop.test/api/cart/items")
    assert json.loads(sent.body) == {"product_id": 1, "quantity": 1}


def test_add_sends_explicit_quantity(shop, fake_shop):
    shop.run_keyword("add_product_to_cart", [2], {"quantity": 3})

    assert json.loads(fake_shop.requests[-1].body) == {"product_id": 2, "quantity": 3}


def test_add_and_get_use_the_instance_session_id(shop, fake_shop):
    shop.run_keyword("add_product_to_cart", [1])
    shop.run_keyword("get_cart_item_count", [])
    shop.run_keyword("get_cart_total", [])

    session_ids = {request.headers["X-Session-ID"] for request in fake_shop.requests}
    assert session_ids == {shop.client.session_id}


def test_two_instances_send_different_session_ids(library, fake_shop):
    fake_shop.add("GET", "/api/cart/", json_response(200, EMPTY_CART))
    first, second = library(), library()

    first.run_keyword("get_cart_item_count", [])
    second.run_keyword("get_cart_item_count", [])

    first_id, second_id = (request.headers["X-Session-ID"] for request in fake_shop.requests)
    assert first_id != second_id


def test_cart_requests_send_space_header(library, fake_shop):
    fake_shop.add("POST", "/api/cart/items", json_response(200, TWO_LINES))
    fake_shop.add("GET", "/api/cart/", json_response(200, TWO_LINES))
    shop = library(space="team-7")

    shop.run_keyword("add_product_to_cart", [1])
    shop.run_keyword("get_cart_total", [])

    assert [request.headers["X-Workshop-Space"] for request in fake_shop.requests] == ["team-7", "team-7"]


def test_add_unknown_product(shop, fake_shop):
    fake_shop.add("POST", "/api/cart/items", json_response(404, PRODUCT_NOT_FOUND))

    with pytest.raises(DemoShopError) as error:
        shop.run_keyword("add_product_to_cart", [999999])

    assert str(error.value) == "Adding 1 x product 999999 to the cart failed: Product not found (HTTP 404)"


@pytest.mark.parametrize(
    ("quantity", "body", "text"),
    [
        (21, QUANTITY_TOO_HIGH, "Input should be less than or equal to 20"),
        (0, QUANTITY_TOO_LOW, "Input should be greater than or equal to 1"),
    ],
)
def test_add_quantity_rejected_by_shop(shop, fake_shop, quantity, body, text):
    fake_shop.add("POST", "/api/cart/items", json_response(422, body))

    with pytest.raises(DemoShopError) as error:
        shop.run_keyword("add_product_to_cart", [1, quantity])

    assert str(error.value) == f"Adding {quantity} x product 1 to the cart failed: quantity: {text} (HTTP 422)"


# Get Cart Item Count


def test_empty_cart_item_count(shop, fake_shop):
    count = shop.run_keyword("get_cart_item_count", [AssertionOperator["=="], "0"])

    assert count == 0
    assert type(count) is int
    sent = fake_shop.requests[-1]
    assert (sent.method, sent.url) == ("GET", "http://shop.test/api/cart/")


def test_item_count_sums_quantities_across_lines(shop, fake_shop):
    fake_shop.add("GET", "/api/cart/", json_response(200, TWO_LINES))

    assert shop.run_keyword("get_cart_item_count", []) == 3


def test_item_count_mismatch(shop):
    with pytest.raises(AssertionError) as error:
        shop.run_keyword("get_cart_item_count", [AssertionOperator[">"], "0"])

    assert str(error.value) == "Cart item count '0' (int) should be greater than '0' (int)"


# Get Cart Total


def test_empty_cart_total_is_float(shop):
    total = shop.run_keyword("get_cart_total", [])

    assert total == 0.0
    assert type(total) is float


def test_total_of_several_lines(shop, fake_shop):
    fake_shop.add("GET", "/api/cart/", json_response(200, TWO_LINES))

    assert shop.run_keyword("get_cart_total", [AssertionOperator["=="], "539.48"]) == 539.48


def test_total_named_assertion_arguments(shop):
    kwargs = {"assertion_operator": AssertionOperator[">="], "assertion_expected": "0"}

    assert shop.run_keyword("get_cart_total", [], kwargs) == 0.0


def test_total_custom_message(shop):
    with pytest.raises(AssertionError) as error:
        shop.run_keyword(
            "get_cart_total", [AssertionOperator["=="], "5"], {"message": "Total was {value}, wanted {expected}"}
        )

    assert str(error.value) == "Total was 0.0, wanted 5.0"


def test_custom_message_type_placeholders(shop):
    with pytest.raises(AssertionError) as error:
        shop.run_keyword("get_cart_item_count", [AssertionOperator["=="], "2", "{value_type} vs {expected_type}"])

    assert str(error.value) == "int vs int"


def test_total_then_returns_transformed_value(shop, fake_shop, robot_variables):
    fake_shop.add("GET", "/api/cart/", json_response(200, TWO_LINES))

    assert shop.run_keyword("get_cart_total", [AssertionOperator["then"], "round(value / 2, 2)"]) == 269.74


def test_text_operator_on_cart_not_allowed_and_no_request_sent(shop, fake_shop):
    with pytest.raises(ValueError, match="Operator 'starts' is not allowed."):
        shop.run_keyword("get_cart_total", [AssertionOperator["^="], "5"])

    assert fake_shop.requests == []


def test_unexpected_cart_body(shop, fake_shop):
    fake_shop.add("GET", "/api/cart/", json_response(200, {"session": "fake"}))

    with pytest.raises(DemoShopError, match="^Getting the cart failed: unexpected response from the shop$"):
        shop.run_keyword("get_cart_item_count", [])
