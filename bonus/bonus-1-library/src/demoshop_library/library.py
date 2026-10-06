from importlib.metadata import version

from robotlibcore import DynamicCore

from .cart import CartKeywords
from .client import ShopClient
from .products import ProductKeywords


class DemoShopLibrary(DynamicCore):
    """Robot Framework library for testing the DemoShop through its REST API.

    DemoShopLibrary gives tests shop-level keywords in place of HTTP requests. `Get Product Count` and
    `Get Product Price` read the catalogue; `Add Product To Cart`, `Get Cart Item Count` and `Get Cart Total` fill
    and inspect a cart. Every ``Get`` keyword can check its value in the same step, see `Assertions`.

    = Shop and workshop space =

    The library is imported with ``url``, the base URL of the shop, and an optional ``space``. When ``space`` is
    given, every request carries it in the ``X-Workshop-Space`` header. Importing the library does not contact the
    shop, so a wrong ``url`` shows only when the first keyword runs. See `Importing` for the arguments.

    | ***** Settings *****
    | Library    demoshop_library.DemoShopLibrary    url=http://localhost:9090    space=team-7

    = Carts and library scope =

    Each library instance keeps one cart of its own. The instance generates a session id and sends it in the
    ``X-Session-ID`` header of every cart request. Two instances never share a cart, and no instance uses the cart
    that the shop shares among callers that send no session id.

    The library uses the ``TEST`` scope, so every test gets a new instance and starts with an empty cart. A test's
    setup and teardown run on the same instance as its body: products added in ``[Setup]`` are in the test's cart.
    Suite setup and suite teardown run on an instance of their own, and their cart is not visible to any test.

    To use two carts in one test, import the library twice, each time with its own alias:

    | ***** Settings *****
    | Library    demoshop_library.DemoShopLibrary    url=${SHOP_URL}    AS    ShopA
    | Library    demoshop_library.DemoShopLibrary    url=${SHOP_URL}    AS    ShopB
    |
    | ***** Test Cases *****
    | Separate Carts
    |     ShopA.Add Product To Cart    1
    |     ShopB.Get Cart Item Count    ==    0
    |     ShopA.Get Cart Item Count    ==    1

    = Assertions =

    Every ``Get`` keyword takes three optional arguments after its own: ``assertion_operator``,
    ``assertion_expected`` and ``message``. Without ``assertion_operator``, the keyword returns its value without
    checking it. With it, the keyword checks the value with
    [https://github.com/MarketSquare/AssertionEngine|AssertionEngine], fails if the check fails and otherwise
    returns the value.

    Every ``Get`` keyword returns a number: counts are integers and amounts of money are floats. Before it compares,
    the keyword converts ``assertion_expected`` to the type of its value, so ``Get Product Price    1    ==    249.99``
    compares two floats, not two strings.

    Supported operators:

    |      = Operator =   |   = Alternative Operators =          |              = Description =                                                       | = Validate Equivalent =  |
    | ``==``              | ``equal``, ``equals``, ``should be`` | Checks if returned value is equal to expected value.                               | ``value == expected``    |
    | ``!=``              | ``inequal``, ``should not be``       | Checks if returned value is not equal to expected value.                           | ``value != expected``    |
    | ``>``               | ``greater than``                     | Checks if returned value is greater than expected value.                           | ``value > expected``     |
    | ``>=``              |                                      | Checks if returned value is greater than or equal to expected value.               | ``value >= expected``    |
    | ``<``               | ``less than``                        | Checks if returned value is less than expected value.                              | ``value < expected``     |
    | ``<=``              |                                      | Checks if returned value is less than or equal to expected value.                  | ``value <= expected``    |
    | ``validate``        |                                      | Checks if given Python expression evaluates to ``True``.                           |                          |
    | ``evaluate``        |  ``then``                            | When using this operator, the keyword does return the evaluated Python expression. |                          |

    In ``validate`` and ``then`` expressions, ``value`` is the keyword's value. The text operators ``*=`` /
    ``contains``, ``not contains``, ``^=`` / ``starts`` / ``should start with``, ``$=`` / ``ends`` /
    ``should end with`` and ``matches`` are not allowed, and an unknown operator fails as an argument conversion
    error. In both cases the keyword fails before it contacts the shop.

    When a check fails, the message names what was checked, for example
    ``Product 1 price '249.99' (float) should be '10.0' (float)``. The ``message`` argument replaces that message.
    In it, ``{value}``, ``{value_type}``, ``{expected}`` and ``{expected_type}`` are replaced with the actual and
    expected values and their types.

    Examples:
    | `Get Product Count`    ==    12
    | `Get Product Price`    1    greater than    100
    | `Get Cart Total`    assertion_operator=>=    assertion_expected=0
    | `Get Product Price`    1    validate    100 < value < 300
    | ${double} =    `Get Product Price`    1    then    value * 2
    | `Get Cart Total`    ==    5    message=Total was {value}, wanted {expected}

    = Shop errors =

    When the shop rejects a request, for example for an unknown product or a quantity outside 1 to 20, the keyword
    fails with the shop's own message and the HTTP status, for example
    ``Getting product 999999 failed: Product not found (HTTP 404)``. When the shop cannot be reached, the message
    names the URL that was tried.
    """

    ROBOT_LIBRARY_SCOPE = "TEST"
    ROBOT_LIBRARY_VERSION = version("demoshop-library")

    def __init__(self, url: str, space: str | None = None):
        """Imports the library for the shop at ``url``.

        | =Arguments= | =Description= |
        | ``url`` | Base URL of the shop, for example ``http://localhost:9090``. Keywords send their requests to paths under it, such as ``/api/products/``. A trailing slash is ignored. |
        | ``space`` | Workshop space. When given, every request carries it in the ``X-Workshop-Space`` header. When not given, the header is not sent. |

        Importing does not contact the shop. Each library instance keeps a cart of its own, see
        `Carts and library scope`.

        Examples:
        | Library    demoshop_library.DemoShopLibrary    url=http://localhost:9090
        | Library    demoshop_library.DemoShopLibrary    url=http://localhost:9090    space=team-7
        """
        self.client = ShopClient(url, space)
        DynamicCore.__init__(self, [ProductKeywords(self.client), CartKeywords(self.client)])
