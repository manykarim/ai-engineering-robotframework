*** Settings ***
Documentation       Legacy locators, kept deliberately; see docs/conventions.md.
...
...                 These keywords find elements by id, class or data-test hook instead of
...                 the shop's stable contract.

Library             Browser
Resource            catalogue.resource
Resource            checkout.resource


*** Keywords ***
Get Card Prices
    [Documentation]    The price of every grid card, in page order.
    Wait For Elements State    ${GRID} >> .product-card__price >> nth=0    visible
    @{prices}=    Get Texts    ${GRID} >> .product-card__price
    RETURN    ${prices}

Get Grid Cards
    [Documentation]    The product cards of the grid.
    Wait For Elements State    ${GRID} >> [data-test="product-card"] >> nth=0    visible
    @{cards}=    Get Elements    ${GRID} >> [data-test="product-card"]
    RETURN    ${cards}

Get Summary Amounts
    [Documentation]    Subtotal, tax and total of the order summary, as numbers.
    ${subtotal}=    Get Text    [data-test="checkout-subtotal"]
    ${tax}=    Get Text    [data-test="checkout-tax"]
    ${total}=    Get Text    [data-test="checkout-total"]
    &{amounts}=    Create Dictionary
    ...    subtotal=${{ float($subtotal.strip().lstrip("$").replace(",", "")) }}
    ...    tax=${{ float($tax.strip().lstrip("$").replace(",", "")) }}
    ...    total=${{ float($total.strip().lstrip("$").replace(",", "")) }}
    RETURN    ${amounts}

Fill Checkout Form By Field Ids
    [Documentation]    Fills the required fields through their ids.
    [Arguments]    ${email}    ${full_name}    ${address}
    Fill Text    id=checkout-email    ${email}
    Fill Text    id=checkout-name    ${full_name}
    Fill Text    id=checkout-address    ${address}
