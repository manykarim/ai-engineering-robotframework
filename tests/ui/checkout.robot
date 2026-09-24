*** Settings ***
Documentation       Checkout, /checkout (spec: shop/checkout).
...                 Every test starts with Aurora Neural Headphones in its own cart.

Resource            resources/shop.resource
Resource            resources/checkout.resource
Resource            resources/legacy.resource

Suite Setup         Open Shop Browser
Suite Teardown      Close Browser
Test Setup          Start Checkout Test

Test Tags           WEB-006    ui


*** Test Cases ***
WEB-006_AC-1 Order Total Adds Up
    [Documentation]    The order total is subtotal plus shipping plus tax.
    ${subtotal}=    Get Summary Amount    Subtotal
    ${shipping}=    Get Summary Amount    Shipping
    ${tax}=    Get Summary Amount    Tax
    ${total}=    Get Order Total
    ${expected}=    Evaluate    round($subtotal + $shipping + $tax, 2)
    Should Be Equal As Numbers    ${total}    ${expected}
    ...    msg=The order total should be subtotal plus shipping plus tax.

WEB-006_AC-7 Successful Order
    [Documentation]    A valid order shows a confirmation with an order number ORD- plus 8 hex characters.
    Fill Checkout Form By Field Ids    test@example.com    Test User    123 Test Street, City
    Place Order
    ${message}=    Get Order Confirmation
    ${numbers}=    Get Regexp Matches    ${message}    \\bORD-[0-9A-F]{8}\\b
    Length Should Be    ${numbers}    1

WEB-006_AC-11 Validation Errors Next To Fields
    [Documentation]    Invalid fields each get a message next to them, and the shopper stays on the page.
    &{before}=    Create Dictionary
    FOR    ${label}    IN    Email    Full name    Address
        &{messages}=    Get Field Messages    ${label}
        Set To Dictionary    ${before}    ${label}=${messages}
    END
    Fill Checkout Form    notanemail    A    123
    Place Order
    FOR    ${label}    IN    Email    Full name    Address
        ${message}=    Get New Field Message    ${label}    ${before}[${label}]
        Should Not Be Empty    ${message}    msg=The field "${label}" should show a message next to it.
    END
    Get Url    $=    /checkout

WEB-006_AC-12 Cart Cleared After Order
    [Documentation]    After an order, the cart is empty and the header shows no item count.
    Fill Checkout Form    test@example.com    Test User    123 Test Street, City
    Place Order
    Get Order Confirmation
    Go To Cart Page
    Cart Should Say It Is Empty
    ${cart}=    Get Cart Link Text
    Should Not Match Regexp    ${cart}    \\d


*** Keywords ***
Start Checkout Test
    Start Shop Test
    Add Product To Cart From Its Page    1    Aurora Neural Headphones
    Go To Checkout
