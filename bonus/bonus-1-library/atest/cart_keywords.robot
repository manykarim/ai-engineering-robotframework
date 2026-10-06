*** Settings ***
Documentation       Cart keywords. Every test starts with an empty cart of its own.

Resource            resources/demoshop.resource
Library             demoshop_library.DemoShopLibrary    url=${SHOP_URL}    space=${WORKSHOP_SPACE}


*** Test Cases ***
Empty Cart
    Get Cart Item Count    ==    0
    Get Cart Total    ==    0

Empty Cart Total Is A Float
    ${total} =    Get Cart Total
    Get Cart Total    validate    $total == 0.0 and type($total) is float

Default Quantity
    Add Product To Cart    1
    Get Cart Item Count    ==    1

Explicit Quantity
    Add Product To Cart    1    quantity=3
    Get Cart Item Count    ==    3

Same Product Added Twice
    Add Product To Cart    1    2
    Add Product To Cart    1
    Get Cart Item Count    ==    3
    Get Cart Total    ==    749.97

Quantities Summed Across Lines
    Add Product To Cart    1    2
    Add Product To Cart    2
    Get Cart Item Count    ==    3
    Get Cart Total    ==    539.48

Total After One Add
    Add Product To Cart    1    2
    Get Cart Total    ==    499.98
