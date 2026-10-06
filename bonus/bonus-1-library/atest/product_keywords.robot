*** Settings ***
Documentation       Product keywords against the shop's seed catalogue.

Resource            resources/demoshop.resource
Library             demoshop_library.DemoShopLibrary    url=${SHOP_URL}    space=${WORKSHOP_SPACE}


*** Test Cases ***
Count Of The Seed Catalogue
    ${count} =    Get Product Count
    Get Product Count    validate    value == $count and type($count) is int

Count With Assertion
    Get Product Count    ==    ${PRODUCT_COUNT}

Price Of A Product
    ${price} =    Get Product Price    1
    Get Product Price    1    validate    value == $price and type($price) is float

Price With Assertion
    Get Product Price    1    ==    ${PRODUCT_1_PRICE}
    Get Product Price    2    ==    ${PRODUCT_2_PRICE}

Whole-Number Price Is A Float
    Get Product Price    5    ==    ${PRODUCT_5_PRICE}
    Get Product Price    5    validate    value == 799.0 and type(value) is float
