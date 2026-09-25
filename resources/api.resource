*** Settings ***
Documentation       The shop's API, in the configured workshop space.

Library             Collections
Library             RequestsLibrary


*** Keywords ***
Open Shop API
    [Documentation]    Creates the API session. It sends ${SHOP_SPACE} when one is set.
    &{headers}=    Create Dictionary
    IF    "${SHOP_SPACE}"
        Set To Dictionary    ${headers}    X-Workshop-Space=${SHOP_SPACE}
    END
    Create Session    shop    ${SHOP_URL}    headers=${headers}

Get Shop Health
    [Documentation]    The body of ``GET /health``.
    ${response}=    GET On Session    shop    /health    expected_status=200
    RETURN    ${response.json()}

Get Catalogue From API
    [Documentation]    Every product, as dictionaries, from ``GET /api/products/``.
    ${response}=    GET On Session    shop    /api/products/    expected_status=200
    RETURN    ${response.json()}[items]

Get Product From API
    [Documentation]    The product with the given ID, as a dictionary, from the catalogue listing.
    [Arguments]    ${product_id}
    @{catalogue}=    Get Catalogue From API
    @{matches}=    Evaluate    [product for product in $catalogue if product["id"] == int($product_id)]
    Should Not Be Empty    ${matches}    msg=The catalogue lists no product with the ID ${product_id}.
    RETURN    ${matches}[0]
