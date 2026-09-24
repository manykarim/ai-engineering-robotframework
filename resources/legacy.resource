*** Settings ***
Documentation       Legacy locators, kept deliberately; see docs/conventions.md.
...
...                 These keywords find elements by id, class or data-test hook instead of
...                 the shop's stable contract. Each such locator names exactly one element.

Library             Browser
Resource            catalogue.resource
Resource            checkout.resource


*** Keywords ***
Get Product Grid
    [Documentation]    The element that holds the product cards of the grid.
    ${grid}=    Get Element    ${GRID} >> .product-grid
    RETURN    ${grid}

Get Card Prices
    [Documentation]    The price of every grid card, in page order.
    ${grid}=    Get Product Grid
    @{prices}=    Get Texts    ${grid} >> article >> ${CARD PRICE}
    RETURN    ${prices}

Get Grid Cards
    [Documentation]    The product cards of the grid.
    ${grid}=    Get Product Grid
    @{cards}=    Get Elements    ${grid} >> article
    RETURN    ${cards}

Get Order Total
    [Documentation]    The total the order summary shows, as a number.
    ${text}=    Get Text    [data-test="checkout-total"]
    ${total}=    Amount From Text    ${text}
    RETURN    ${total}

Fill Checkout Form By Field Ids
    [Documentation]    Fills the required fields through their ids.
    [Arguments]    ${email}    ${full_name}    ${address}
    Fill Text    id=checkout-email    ${email}
    Fill Text    id=checkout-name    ${full_name}
    Fill Text    id=checkout-address    ${address}
