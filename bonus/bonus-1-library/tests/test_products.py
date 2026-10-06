import pytest
from assertionengine import AssertionOperator

from conftest import json_response
from demoshop_library.client import DemoShopError

CATALOGUE = {"items": [{"id": i, "name": f"Product {i}", "price": 10.0 * i} for i in range(1, 13)]}
PRODUCT_1 = {"product": {"id": 1, "name": "Aurora Neural Headphones", "price": 249.99}}
PRODUCT_5 = {"product": {"id": 5, "name": "Atlas Standing Desk", "price": 799}}
PRODUCT_NOT_FOUND = {"detail": "Product not found"}


@pytest.fixture
def shop(library, fake_shop):
    fake_shop.add("GET", "/api/products/", json_response(200, CATALOGUE))
    fake_shop.add("GET", "/api/products/1", json_response(200, PRODUCT_1))
    fake_shop.add("GET", "/api/products/5", json_response(200, PRODUCT_5))
    fake_shop.add("GET", "/api/products/999999", json_response(404, PRODUCT_NOT_FOUND))
    return library()


# Get Product Count


def test_product_count_sends_get_without_session_id(shop, fake_shop):
    shop.run_keyword("get_product_count", [])

    sent = fake_shop.requests[-1]
    assert (sent.method, sent.path_url) == ("GET", "/api/products/")
    assert "X-Session-ID" not in sent.headers


def test_product_count_returns_number_of_items(shop):
    count = shop.run_keyword("get_product_count", [])

    assert count == 12
    assert type(count) is int


def test_product_count_assertion_passes(shop):
    assert shop.run_keyword("get_product_count", [AssertionOperator["=="], "12"]) == 12


def test_product_count_alternative_operator_name(shop):
    assert shop.run_keyword("get_product_count", [AssertionOperator["greater than"], "0"]) == 12


def test_product_count_mismatch(shop):
    with pytest.raises(AssertionError) as error:
        shop.run_keyword("get_product_count", [AssertionOperator["=="], "13"])

    assert str(error.value) == "Product count '12' (int) should be '13' (int)"


def test_product_count_sends_space_header(library, fake_shop):
    fake_shop.add("GET", "/api/products/", json_response(200, CATALOGUE))

    library(space="team-7").run_keyword("get_product_count", [])

    assert fake_shop.requests[-1].headers["X-Workshop-Space"] == "team-7"


# Get Product Price


def test_product_price_sends_get_without_session_id(shop, fake_shop):
    shop.run_keyword("get_product_price", [1])

    sent = fake_shop.requests[-1]
    assert (sent.method, sent.url) == ("GET", "http://shop.test/api/products/1")
    assert "X-Session-ID" not in sent.headers


def test_product_price_returns_float(shop):
    price = shop.run_keyword("get_product_price", [1])

    assert price == 249.99
    assert type(price) is float


def test_whole_number_price_returned_as_float(shop):
    price = shop.run_keyword("get_product_price", [5])

    assert price == 799.0
    assert type(price) is float


@pytest.mark.parametrize(("product_id", "expected"), [(1, "249.99"), (5, "799")])
def test_product_price_text_expectation_compares_as_number(shop, product_id, expected):
    assert shop.run_keyword("get_product_price", [product_id, AssertionOperator["=="], expected]) == float(expected)


def test_product_price_mismatch(shop):
    with pytest.raises(AssertionError) as error:
        shop.run_keyword("get_product_price", [1, AssertionOperator["=="], "10"])

    assert str(error.value) == "Product 1 price '249.99' (float) should be '10.0' (float)"


def test_product_price_named_assertion_arguments(shop):
    kwargs = {"assertion_operator": AssertionOperator[">="], "assertion_expected": "249.99"}

    assert shop.run_keyword("get_product_price", [1], kwargs) == 249.99


def test_validate_passes(shop, robot_variables):
    assert shop.run_keyword("get_product_price", [1, AssertionOperator["validate"], "100 < value < 300"]) == 249.99


def test_validate_fails(shop, robot_variables):
    with pytest.raises(AssertionError) as error:
        shop.run_keyword("get_product_price", [1, AssertionOperator["validate"], "value < 100"])

    assert "should validate to true with" in str(error.value)


@pytest.mark.parametrize("operator", ["then", "evaluate"])
def test_then_returns_transformed_value(shop, robot_variables, operator):
    assert shop.run_keyword("get_product_price", [1, AssertionOperator[operator], "value * 2"]) == 499.98


@pytest.mark.parametrize(
    ("operator", "name"),
    [("contains", "contains"), ("*=", "contains"), ("not contains", "not contains"), ("^=", "starts"),
     ("should end with", "ends"), ("matches", "matches")],
)
def test_text_operator_not_allowed_and_no_request_sent(shop, fake_shop, operator, name):
    with pytest.raises(ValueError) as error:
        shop.run_keyword("get_product_price", [1, AssertionOperator[operator], "249"])

    assert str(error.value) == f"Operator '{name}' is not allowed."
    assert fake_shop.requests == []


def test_text_operator_on_count_not_allowed(shop, fake_shop):
    with pytest.raises(ValueError, match="Operator 'contains' is not allowed."):
        shop.run_keyword("get_product_count", [AssertionOperator["contains"], "1"])

    assert fake_shop.requests == []


def test_unknown_product(shop):
    with pytest.raises(DemoShopError) as error:
        shop.run_keyword("get_product_price", [999999])

    assert str(error.value) == "Getting product 999999 failed: Product not found (HTTP 404)"
