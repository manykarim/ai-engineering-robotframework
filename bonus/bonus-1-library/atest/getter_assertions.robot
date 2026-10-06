*** Settings ***
Documentation       The assertion arguments shared by every Get keyword. Failing assertions are covered by the
...                 unit tests, because expecting a failure needs BuiltIn keywords.

Resource            resources/demoshop.resource
Library             demoshop_library.DemoShopLibrary    url=${SHOP_URL}    space=${WORKSHOP_SPACE}


*** Test Cases ***
Positional Assertion Arguments
    Get Product Price    1    ==    ${PRODUCT_1_PRICE}
    Get Cart Total    ==    0

Named Assertion Arguments
    Get Cart Total    assertion_operator=>=    assertion_expected=0
    Get Product Price    1    assertion_operator=equal    assertion_expected=${PRODUCT_1_PRICE}
    Get Product Count    assertion_operator=greater than    assertion_expected=0    message=The catalogue is empty

Whole-Number Expectation For A Price
    Get Product Price    5    ==    799

Alternative Operator Names
    Get Product Count    equal    ${PRODUCT_COUNT}
    Get Product Count    equals    ${PRODUCT_COUNT}
    Get Product Count    should be    ${PRODUCT_COUNT}
    Get Product Price    1    inequal    250
    Get Product Price    1    should not be    250
    Get Product Price    1    less than    250
    Get Product Count    greater than    0

Comparison Operators
    Get Product Count    !=    0
    Get Product Price    1    <    250
    Get Product Price    1    <=    ${PRODUCT_1_PRICE}
    Get Product Price    1    >    249
    Get Product Price    1    >=    ${PRODUCT_1_PRICE}
    Get Cart Item Count    <=    0

Validate
    Get Product Price    1    validate    100 < value < 300
    Get Cart Item Count    validate    value == 0

Value Returned Without Assertion
    ${count} =    Get Product Count
    Get Product Count    validate    value == $count and type($count) is int

Evaluate Returns Transformed Value
    ${double} =    Get Product Price    1    then    value * 2
    Get Product Price    1    validate    $double == 499.98
    ${half} =    Get Product Count    evaluate    value // 2
    Get Product Count    validate    $half == 6
