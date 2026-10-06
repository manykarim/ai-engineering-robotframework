from assertionengine import AssertionOperator, float_str_verify_assertion, int_str_verify_assertion
from robotlibcore import keyword

from .assertions import check_operator
from .client import ShopClient


class CartKeywords:
    """Keywords that fill and inspect the cart of the library instance."""

    def __init__(self, client: ShopClient):
        self._client = client

    @keyword(tags=("Setter", "Cart"))
    def add_product_to_cart(self, product_id: int, quantity: int = 1) -> None:
        """Adds ``quantity`` of the product with ``product_id`` to the cart.

        | =Arguments= | =Description= |
        | ``product_id`` | Id of the product, an integer. |
        | ``quantity`` | How many to add, an integer. The shop accepts 1 to 20. Defaults to 1. |

        When the product is already in the cart, the shop increases that line's quantity instead of adding a
        second line. The shop validates ``product_id`` and ``quantity``: an unknown product or a quantity outside
        1 to 20 fails the keyword with the shop's message.

        The cart belongs to the library instance, see `Carts and library scope`.

        Example:
        | `Add Product To Cart`    1                   # Adds one of product 1.
        | `Add Product To Cart`    2    quantity=3     # Adds three of product 2.
        | `Get Cart Item Count`    ==    4
        """
        self._client.request(
            "POST",
            "/api/cart/items",
            f"Adding {quantity} x product {product_id} to the cart",
            json={"product_id": product_id, "quantity": quantity},
            with_session=True,
        )

    @keyword(tags=("Assertion", "Getter", "Cart"))
    def get_cart_item_count(
        self,
        assertion_operator: AssertionOperator | None = None,
        assertion_expected: int | str = 0,
        message: str | None = None,
    ) -> int:
        """Returns the number of items in the cart: the sum of the quantities of all cart lines.

        | =Arguments= | =Description= |
        | ``assertion_operator`` | See `Assertions` for further details. Defaults to None. |
        | ``assertion_expected`` | Expected value for the assertion |
        | ``message`` | overrides the default error message for assertion. |

        The count is what the shop's cart badge shows: two of one product and one of another count as 3.

        Optionally asserts that the count matches the specified assertion. See
        `Assertions` for further details for the assertion arguments. By default assertion
        is not done.

        Example:
        | `Get Cart Item Count`    ==    0                  # Asserts that the cart is empty.
        | `Add Product To Cart`    1    2
        | `Add Product To Cart`    2
        | ${count} =    `Get Cart Item Count`               # Returns 3 without assertion.
        """
        check_operator(assertion_operator)
        count = sum(item["quantity"] for item in self._get_cart()["items"])
        return int_str_verify_assertion(count, assertion_operator, assertion_expected, "Cart item count", message)

    @keyword(tags=("Assertion", "Getter", "Cart"))
    def get_cart_total(
        self,
        assertion_operator: AssertionOperator | None = None,
        assertion_expected: float | str = 0,
        message: str | None = None,
    ) -> float:
        """Returns the total of the cart, as the shop computes it, as a float.

        | =Arguments= | =Description= |
        | ``assertion_operator`` | See `Assertions` for further details. Defaults to None. |
        | ``assertion_expected`` | Expected value for the assertion |
        | ``message`` | overrides the default error message for assertion. |

        The total of an empty cart is ``0.0``.

        Optionally asserts that the total matches the specified assertion. See
        `Assertions` for further details for the assertion arguments. By default assertion
        is not done.

        Example:
        | `Add Product To Cart`    1    2
        | `Get Cart Total`    ==    499.98                                    # Asserts the total.
        | `Get Cart Total`    assertion_operator=>=    assertion_expected=0   # Asserts with named arguments.
        | ${total} =    `Get Cart Total`                                      # Returns the total without assertion.
        """
        check_operator(assertion_operator)
        total = float(self._get_cart()["total"])
        return float_str_verify_assertion(total, assertion_operator, assertion_expected, "Cart total", message)

    def _get_cart(self) -> dict:
        return self._client.request("GET", "/api/cart/", "Getting the cart", with_session=True)
