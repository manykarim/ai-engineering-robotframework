import json

import pytest
import requests

from conftest import SHOP_URL, json_response, text_response
from demoshop_library.client import DemoShopError, ShopClient

# Bodies copied verbatim from the local shop (version 0.3.0).
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


@pytest.fixture
def client(fake_shop):
    def make(url: str = SHOP_URL, space: str | None = None) -> ShopClient:
        shop_client = ShopClient(url, space)
        shop_client.session.mount("http://", fake_shop)
        return shop_client

    return make


def test_trailing_slash_in_url_gives_no_doubled_slash(client, fake_shop):
    fake_shop.add("GET", "/api/products/", json_response(200, {"items": []}))

    client(SHOP_URL + "/").request("GET", "/api/products/", "Getting the products")

    assert fake_shop.requests[-1].url == "http://shop.test/api/products/"


def test_space_header_sent_when_space_given(client, fake_shop):
    fake_shop.add("GET", "/api/products/", json_response(200, {"items": []}))

    client(space="team-7").request("GET", "/api/products/", "Getting the products")

    assert fake_shop.requests[-1].headers["X-Workshop-Space"] == "team-7"


def test_space_header_absent_when_space_omitted(client, fake_shop):
    fake_shop.add("GET", "/api/products/", json_response(200, {"items": []}))

    client().request("GET", "/api/products/", "Getting the products")

    assert "X-Workshop-Space" not in fake_shop.requests[-1].headers


def test_session_id_sent_only_with_session(client, fake_shop):
    fake_shop.add("GET", "/api/cart/", json_response(200, {"items": [], "total": 0}))
    shop_client = client()

    shop_client.request("GET", "/api/cart/", "Getting the cart")
    shop_client.request("GET", "/api/cart/", "Getting the cart", with_session=True)

    without, with_ = fake_shop.requests
    assert "X-Session-ID" not in without.headers
    assert with_.headers["X-Session-ID"] == shop_client.session_id


def test_two_clients_have_different_session_ids(client):
    assert client().session_id != client().session_id


def test_no_accept_header_beyond_requests_default(client, fake_shop):
    fake_shop.add("GET", "/api/products/", json_response(200, {"items": []}))

    client().request("GET", "/api/products/", "Getting the products")

    assert fake_shop.requests[-1].headers["Accept"] == requests.utils.default_headers()["Accept"]


def test_post_body_sent_as_json(client, fake_shop):
    fake_shop.add("POST", "/api/cart/items", json_response(200, {"items": [], "total": 0}))

    client().request("POST", "/api/cart/items", "Adding", json={"product_id": 1, "quantity": 2}, with_session=True)

    sent = fake_shop.requests[-1]
    assert sent.headers["Content-Type"] == "application/json"
    assert json.loads(sent.body) == {"product_id": 1, "quantity": 2}


def test_request_returns_decoded_json(client, fake_shop):
    fake_shop.add("GET", "/api/products/1", json_response(200, {"product": {"id": 1, "price": 249.99}}))

    body = client().request("GET", "/api/products/1", "Getting product 1")

    assert body == {"product": {"id": 1, "price": 249.99}}


def test_error_detail_reported(client, fake_shop):
    fake_shop.add("GET", "/api/products/999999", json_response(404, PRODUCT_NOT_FOUND))

    with pytest.raises(DemoShopError) as error:
        client().request("GET", "/api/products/999999", "Getting product 999999")

    assert str(error.value) == "Getting product 999999 failed: Product not found (HTTP 404)"


def test_validation_errors_reported(client, fake_shop):
    fake_shop.add("POST", "/api/cart/items", json_response(422, QUANTITY_TOO_HIGH))

    with pytest.raises(DemoShopError) as error:
        client().request("POST", "/api/cart/items", "Adding 21 x product 1 to the cart", json={}, with_session=True)

    assert str(error.value) == (
        "Adding 21 x product 1 to the cart failed: quantity: Input should be less than or equal to 20 (HTTP 422)"
    )


def test_text_error_body_reported(client, fake_shop):
    fake_shop.add("GET", "/api/cart/", text_response(500, "Internal Server Error"))

    with pytest.raises(DemoShopError) as error:
        client().request("GET", "/api/cart/", "Getting the cart", with_session=True)

    assert str(error.value) == "Getting the cart failed: Internal Server Error (HTTP 500)"


def test_non_json_body_is_unexpected(client, fake_shop):
    fake_shop.add("GET", "/api/products/", text_response(200, "<html>shop</html>", "text/html"))

    with pytest.raises(DemoShopError) as error:
        client().request("GET", "/api/products/", "Getting the products")

    assert str(error.value) == "Getting the products failed: unexpected response from the shop"


def test_missing_key_is_unexpected(client, fake_shop):
    fake_shop.add("GET", "/api/products/1", json_response(200, {"product": {"id": 1}}))
    body = client().request("GET", "/api/products/1", "Getting product 1")

    with pytest.raises(DemoShopError) as error:
        body["product"]["price"]

    assert str(error.value) == "Getting product 1 failed: unexpected response from the shop"


def test_unreachable_shop_names_the_url(monkeypatch):
    def refuse(*args, **kwargs):
        raise requests.ConnectionError("Connection refused")

    shop_client = ShopClient("http://localhost:1/")
    monkeypatch.setattr(shop_client.session, "send", refuse)

    with pytest.raises(DemoShopError) as error:
        shop_client.request("GET", "/api/products/", "Getting the products")

    assert str(error.value) == (
        "Getting the products failed: could not reach the shop at http://localhost:1: Connection refused"
    )


def test_error_name_is_suppressed_in_robot():
    assert DemoShopError.ROBOT_SUPPRESS_NAME is True
