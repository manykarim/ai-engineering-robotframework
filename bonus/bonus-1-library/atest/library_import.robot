*** Settings ***
Documentation       Importing the library: URL, workshop space, one cart per instance and the TEST scope.
...                 The library is imported twice, so every keyword is called with its instance's alias.

Resource            resources/demoshop.resource
Library             demoshop_library.DemoShopLibrary    url=${SHOP_URL}    AS    ShopA
Library             demoshop_library.DemoShopLibrary    url=${SHOP_URL}/    space=atest    AS    ShopB

Suite Setup         ShopA.Add Product To Cart    1


*** Test Cases ***
Trailing Slash URL And Space
    ShopB.Get Product Count    ==    ${PRODUCT_COUNT}
    ShopB.Get Product Price    1    ==    ${PRODUCT_1_PRICE}
    ShopB.Add Product To Cart    1
    ShopB.Get Cart Item Count    ==    1

Two Instances Have Separate Carts
    ShopA.Add Product To Cart    1
    ShopB.Get Cart Item Count    ==    0
    ShopA.Get Cart Item Count    ==    1

Test Adds Products
    ShopA.Add Product To Cart    1    3
    ShopA.Get Cart Item Count    ==    3

Cart Does Not Carry Over To The Next Test
    ShopA.Get Cart Item Count    ==    0

Test Setup Shares The Test's Cart
    [Setup]    ShopA.Add Product To Cart    1
    ShopA.Get Cart Item Count    ==    1

Suite Setup Cart Is Not Visible To Tests
    ShopA.Get Cart Item Count    ==    0
