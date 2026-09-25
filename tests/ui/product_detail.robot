*** Settings ***
Documentation       A product's detail page, /products/{id} (spec: shop/product-detail).

Resource            resources/shop.resource
Resource            resources/api.resource
Resource            resources/product_detail.resource

Suite Setup         Run Keywords    Open Shop Browser    AND    Open Shop API
Suite Teardown      Close Browser
Test Setup          Start Shop Test

Test Tags           WEB-003    ui


*** Test Cases ***
WEB-003_AC-1 Detail Page Shows Product Information
    [Documentation]    /products/1 shows the product's image, name, category, rating, review count, price and description.
    VAR    ${name}    Aurora Neural Headphones
    ${product}=    Get Product From API    1
    Go To Product Page    1
    Product Detail Should Show    ${name}
    Product Image Should Be Shown    ${name}
    Category Badge Should Show    ${name}    ${product}[category]
    Star Rating Should Be Shown    ${name}
    Review Count Should Be Shown    ${name}
    Product Price Should Be    ${name}    ${product}[price]
    Product Description Should Be Shown    ${name}    ${product}[description]

WEB-003_AC-3 Add To Cart Posts The Product
    [Documentation]    The product's "Add to Cart" button sends a POST that adds product 1 to the cart.
    Go To Product Page    1
    Product Detail Should Show    Aurora Neural Headphones
    ${response}=    Click Add To Cart    Aurora Neural Headphones
    Cart Request Should Add Product    ${response}    1

WEB-003_AC-8 Back Button Returns To Catalogue
    [Documentation]    After a product is opened from /products, the browser's back button shows the products page.
    Go To Catalogue
    Open Product From Grid    Aurora Neural Headphones
    Product Detail Should Show    Aurora Neural Headphones
    Go Back
    Products Page Should Be Shown

WEB-003_AC-8 Navigation Link Returns To Catalogue
    [Documentation]    From a product's detail page, the header's navigation link leads to the products page.
    Go To Product Page    1
    Product Detail Should Show    Aurora Neural Headphones
    Follow Navigation Link To Products
    Products Page Should Be Shown

WEB-003_AC-9 Unknown Product ID Shows Not Found
    [Documentation]    /products/9999 shows a not-found message instead of a product detail page.
    Go To Product Page    9999
    Not Found Message Should Be Shown
    Product Actions Should Not Be Shown

WEB-003_AC-9 Non-Numeric Product ID Shows Not Found
    [Documentation]    /products/abc shows a not-found message instead of a product detail page.
    Go To Product Page    abc
    Not Found Message Should Be Shown
    Product Actions Should Not Be Shown
