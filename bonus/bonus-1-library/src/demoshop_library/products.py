from assertionengine import AssertionOperator, float_str_verify_assertion, int_str_verify_assertion
from robotlibcore import keyword

from .assertions import check_operator
from .client import ShopClient


class ProductKeywords:
    """Keywords that read the shop's product catalogue."""

    def __init__(self, client: ShopClient):
        self._client = client

    @keyword(tags=("Assertion", "Getter", "Products"))
    def get_product_count(
        self,
        assertion_operator: AssertionOperator | None = None,
        assertion_expected: int | str = 0,
        message: str | None = None,
    ) -> int:
        """Returns the number of products in the shop's catalogue.

        | =Arguments= | =Description= |
        | ``assertion_operator`` | See `Assertions` for further details. Defaults to None. |
        | ``assertion_expected`` | Expected value for the assertion |
        | ``message`` | overrides the default error message for assertion. |

        Optionally asserts that the count matches the specified assertion. See
        `Assertions` for further details for the assertion arguments. By default assertion
        is not done.

        Example:
        | ${count} =    `Get Product Count`                  # Returns the count without assertion.
        | `Get Product Count`    ==    12                    # Asserts the count of the seed catalogue.
        | `Get Product Count`    greater than    0           # Asserts that the catalogue is not empty.
        """
        check_operator(assertion_operator)
        body = self._client.request("GET", "/api/products/", "Getting the products")
        return int_str_verify_assertion(
            len(body["items"]), assertion_operator, assertion_expected, "Product count", message
        )

    @keyword(tags=("Assertion", "Getter", "Products"))
    def get_product_price(
        self,
        product_id: int,
        assertion_operator: AssertionOperator | None = None,
        assertion_expected: float | str = 0,
        message: str | None = None,
    ) -> float:
        """Returns the price of the product with ``product_id`` as a float.

        | =Arguments= | =Description= |
        | ``product_id`` | Id of the product, an integer. An unknown id fails the keyword with the shop's ``Product not found``. |
        | ``assertion_operator`` | See `Assertions` for further details. Defaults to None. |
        | ``assertion_expected`` | Expected value for the assertion |
        | ``message`` | overrides the default error message for assertion. |

        A whole-number price is returned as a float too, for example ``799.0``.

        Optionally asserts that the price matches the specified assertion. See
        `Assertions` for further details for the assertion arguments. By default assertion
        is not done.

        Example:
        | ${price} =    `Get Product Price`    1                               # Returns the price without assertion.
        | `Get Product Price`    1    ==    249.99                             # Asserts the price.
        | `Get Product Price`    1    validate    100 < value < 300            # Asserts the price with a Python expression.
        | ${double} =    `Get Product Price`    1    then    value * 2         # Returns twice the price.
        """
        check_operator(assertion_operator)
        body = self._client.request("GET", f"/api/products/{product_id}", f"Getting product {product_id}")
        return float_str_verify_assertion(
            float(body["product"]["price"]),
            assertion_operator,
            assertion_expected,
            f"Product {product_id} price",
            message,
        )
