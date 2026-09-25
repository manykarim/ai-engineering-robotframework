*** Settings ***
Documentation       The cart: the header's cart badge and the cart page, /cart (spec: shop/cart).
...                 Every test fills its own cart from the products' detail pages.

Resource            resources/shop.resource
Resource            resources/api.resource
Resource            resources/cart.resource

Suite Setup         Run Keywords    Open Shop Browser    AND    Open Shop API
Suite Teardown      Close Browser
Test Setup          Start Shop Test

Test Tags           WEB-005    ui


*** Test Cases ***
WEB-005_AC-2 Cart Badge Counts Added Items
    [Documentation]    At desktop size, the header's cart badge shows the total item count after each add, without a reload.
    Go To Product Page    1
    Product Detail Should Show    Aurora Neural Headphones
    Click Add To Cart And Confirm    1    Aurora Neural Headphones
    Cart Badge Should Show    1
    Click Add To Cart And Confirm    1    Aurora Neural Headphones
    Cart Badge Should Show    2

WEB-005_AC-2 Cart Badge Shows In Mobile Menu
    [Documentation]    On a small screen, the cart badge shows the updated count once the navigation menu is open.
    Use Small Screen
    Go To Product Page    1
    Product Detail Should Show    Aurora Neural Headphones
    Click Add To Cart And Confirm    1    Aurora Neural Headphones
    Open Navigation Menu
    Cart Badge Should Show    1

WEB-005_AC-3 Cart Page Lists Name Quantity And Prices
    [Documentation]    After two adds of Aurora Neural Headphones, /cart lists its name, quantity, unit price and line total.
    Add Product To Cart    1    Aurora Neural Headphones    times=2
    Go To Cart Page
    Cart Line Should Show    Aurora Neural Headphones    2    $249.99    $499.98

WEB-005_AC-4 Cart Summary Shows Subtotal Shipping Tax And Total
    [Documentation]    The summary shows the sum of the line totals, "Complimentary" shipping, "Calculated at checkout" tax and that sum as total.
    ${first}=    Get Product From API    1
    ${second}=    Get Product From API    2
    Add Product To Cart    1    ${first}[name]    times=2
    Add Product To Cart    2    ${second}[name]
    ${subtotal}=    Evaluate    round(2 * $first["price"] + $second["price"], 2)
    Go To Cart Page
    Cart Summary Amount Should Be    subtotal    ${subtotal}
    Cart Summary Should Show    shipping    Complimentary
    Cart Summary Should Show    tax    Calculated at checkout
    Cart Summary Amount Should Be    total    ${subtotal}

WEB-005_AC-9 Adding Product Again Increments Quantity
    [Documentation]    Adding Aurora Neural Headphones again raises its quantity from 1 to 2, on one single line.
    Add Product To Cart    1    Aurora Neural Headphones
    Go To Cart Page
    Cart Line Quantity Should Be    Aurora Neural Headphones    1
    Cart Should Have Lines    1
    Add Product To Cart    1    Aurora Neural Headphones
    Go To Cart Page
    Cart Line Quantity Should Be    Aurora Neural Headphones    2
    Cart Should Have Lines    1
