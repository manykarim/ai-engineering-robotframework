import pytest
import requests
from assertionengine import AssertionOperator
from robot.api import TypeInfo

import demoshop_library
from conftest import SHOP_URL
from demoshop_library import DemoShopLibrary

ASSERTION_ARGUMENTS = [("assertion_operator", None), ("assertion_expected", 0), ("message", None)]
PRODUCT_GETTER = ("Assertion", "Getter", "Products")
CART_GETTER = ("Assertion", "Getter", "Cart")
# Keyword: (arguments, types of its own arguments, type of its value, tags)
KEYWORDS = {
    "get_product_count": (ASSERTION_ARGUMENTS, {}, int, PRODUCT_GETTER),
    "get_product_price": (["product_id", *ASSERTION_ARGUMENTS], {"product_id": int}, float, PRODUCT_GETTER),
    "add_product_to_cart": (["product_id", ("quantity", 1)], {"product_id": int, "quantity": int}, None, ("Setter", "Cart")),
    "get_cart_item_count": (ASSERTION_ARGUMENTS, {}, int, CART_GETTER),
    "get_cart_total": (ASSERTION_ARGUMENTS, {}, float, CART_GETTER),
}


def test_import_sends_no_request(monkeypatch):
    def fail(*args, **kwargs):
        raise AssertionError("the library sent a request at import")

    monkeypatch.setattr(requests.Session, "send", fail)

    DemoShopLibrary(SHOP_URL, space="team-7")


def test_scope_is_test():
    assert DemoShopLibrary.ROBOT_LIBRARY_SCOPE == "TEST"


def test_version_comes_from_package_metadata():
    assert DemoShopLibrary.ROBOT_LIBRARY_VERSION == demoshop_library.__version__ == "0.1.0"


def test_two_instances_have_different_session_ids(library):
    assert library().client.session_id != library().client.session_id


def test_package_exports_library():
    assert demoshop_library.DemoShopLibrary is DemoShopLibrary
    assert not hasattr(demoshop_library, "hello")


def test_intro_covers_import_carts_scope_and_assertions(library):
    intro = library().get_keyword_documentation("__intro__")

    for text in ["``url``", "``space``", "X-Workshop-Space", "one cart of its own", "``TEST`` scope"]:
        assert text in intro
    assert "= Assertions =" in intro


def test_import_documentation_names_both_arguments(library):
    doc = library().get_keyword_documentation("__init__")

    assert "| ``url`` |" in doc
    assert "| ``space`` |" in doc


def test_keyword_names_are_exactly_the_five_keywords(library):
    assert sorted(library().get_keyword_names()) == sorted(KEYWORDS)


@pytest.mark.parametrize("name", KEYWORDS)
def test_keyword_arguments_types_and_tags(library, name):
    arguments, own_types, value_type, tags = KEYWORDS[name]
    lib = library()

    assert lib.get_keyword_arguments(name) == arguments
    assert set(lib.get_keyword_tags(name)) == set(tags)
    types = lib.get_keyword_types(name)
    for argument, expected_type in own_types.items():
        assert types[argument] is expected_type
    if "Getter" in tags:
        assert types["assertion_operator"] == AssertionOperator | None
        assert types["assertion_expected"] == value_type | str
        assert types["message"] == str | None


def test_declared_types_make_robot_reject_bad_values(library):
    types = library().get_keyword_types("get_product_price")

    with pytest.raises(ValueError, match="'product_id' got value 'abc' that cannot be converted to integer"):
        TypeInfo.from_type_hint(types["product_id"]).convert("abc", name="product_id")
    with pytest.raises(ValueError, match="'assertion_operator' got value '===' that cannot be converted"):
        TypeInfo.from_type_hint(types["assertion_operator"]).convert("===", name="assertion_operator")
    assert TypeInfo.from_type_hint(types["assertion_operator"]).convert("should be") is AssertionOperator["=="]


@pytest.mark.parametrize("space", [None, "team-7"])
def test_import_arguments_reach_client(space):
    lib = DemoShopLibrary(SHOP_URL + "/", space=space)

    assert lib.client.url == SHOP_URL
    assert lib.client.session.headers.get("X-Workshop-Space") == space
