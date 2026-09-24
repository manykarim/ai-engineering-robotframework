*** Settings ***
Documentation       The products page, /products (spec: shop/catalogue).

Resource            resources/shop.resource
Resource            resources/api.resource
Resource            resources/catalogue.resource
Resource            resources/legacy.resource

Suite Setup         Run Keywords    Open Shop Browser    AND    Open Shop API
Suite Teardown      Close Browser
Test Setup          Start Shop Test

Test Tags           WEB-002    ui


*** Test Cases ***
WEB-002_AC-1 Every Card Offers Add To Cart
    [Documentation]    Every card of the grid shows an "Add to Cart" button.
    Go To Catalogue
    ${cards}=    Get Grid Card Count
    Should Be Equal As Integers    ${cards}    12
    ${buttons}=    Get Add To Cart Button Count
    Should Be Equal As Integers    ${buttons}    ${cards}
    ...    msg=Every product card should offer "Add to cart".

WEB-002_AC-1 Card Prices Are The Product Prices
    [Documentation]    The price on every card is that product's price.
    @{catalogue}=    Get Catalogue From API
    &{prices}=    Evaluate    {product["name"]: product["price"] for product in $catalogue}
    Go To Catalogue
    @{names}=    Get Grid Card Names
    @{shown}=    Get Card Prices
    Length Should Be    ${shown}    12
    FOR    ${name}    ${price}    IN ZIP    ${names}    ${shown}
        ${expected}=    Format Price    ${prices}[${name}]
        Should Be Equal    ${price}    ${expected}    msg=${name} should cost ${expected}.
    END

WEB-002_AC-2 Categories Filter Group
    [Documentation]    A "Categories" group offers one unchecked checkbox per category.
    Go To Catalogue
    ${count}=    Get Category Checkbox Count
    Should Be Equal As Integers    ${count}    9
    Filter Checkboxes Should All Be Unchecked

WEB-002_AC-4 Rating Filter
    [Documentation]    A rating filter offers an unchecked minimum-rating checkbox.
    [Tags]    broken
    Go To Catalogue
    Checkbox Should Be Unchecked    4 stars and up

WEB-002_AC-7 Audio Filter Shows Only Audio
    [Documentation]    With only "Audio" checked, the grid shows only audio products.
    Go To Catalogue
    Check Category    Audio
    Apply Filters
    @{cards}=    Get Grid Cards
    Should Not Be Empty    ${cards}
    FOR    ${card}    IN    @{cards}
        ${category}=    Get Card Category    ${card}
        Should Be Equal    ${category}    audio
    END

WEB-002_AC-10 Reset Filters
    [Documentation]    "Reset" clears every filter and brings back all 12 products.
    Go To Catalogue
    Check Category    Audio
    Apply Filters
    Click    role=link[name="Reset"]
    Filter Checkboxes Should All Be Unchecked
    ${range}=    Get Price Range Values
    Should Be Equal    ${range}    ${{ ["39.50", "899.00"] }}
    ${cards}=    Get Grid Card Count
    Should Be Equal As Integers    ${cards}    12

WEB-002_AC-12 Handpicked Highlights
    [Documentation]    "Handpicked highlights" shows the three highest prices, highest first.
    [Tags]    broken
    @{catalogue}=    Get Catalogue From API
    ${expected}=    Evaluate    [str(p) for p in sorted((float(x["price"]) for x in $catalogue), reverse=True)[:3]]
    Go To Catalogue
    ${shown}=    Get Highlight Prices
    Should Be True    $shown == $expected
    ...    msg=The highlights should show the three highest prices, highest first.
