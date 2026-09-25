*** Settings ***
Documentation       A product's detail page, /products/{id}, and the page shown for an unknown
...                 ID, through the shop's stable contract: roles, accessible names and visible
...                 text. Keywords that look inside the product's own section take the
...                 product's name, because that section is found by its main heading.

Library             Browser
Library             String
Resource            shop.resource
Resource            catalogue.resource


*** Variables ***
# The detail page's two actions, by their visible text as the spec quotes it.
${ADD TO CART}      button:has-text("Add to Cart")
${BUY NOW}          :is(a, button):has-text("Buy Now")
${STAR RATING}      role=group[name=/star/i]
# A review count in either form the spec quotes: "214 reviews" or "(214)".
${REVIEW COUNT}     text=/\\d+\\s+reviews?\\b|\\(\\d+\\)/i
${NOT FOUND}        role=main >> text=/not[\\s-]+found/i
# The header's link to the products page, by its target: the spec quotes no text for it.
${NAV PRODUCTS}     role=banner >> role=navigation >> a[href="/products"]


*** Keywords ***
Product Section
    [Documentation]    The locator of the product's own section: the one whose main heading shows ``name``.
    [Arguments]    ${name}
    RETURN    role=main >> section:has(h1:has-text("${name}"))

Go To Product Page
    [Documentation]    Opens ``/products/{product_id}``.
    [Arguments]    ${product_id}
    Go To Shop Page    /products/${product_id}

Product Detail Should Show
    [Documentation]    The page shows the product's section, whose main heading shows ``name``, ignoring case.
    [Arguments]    ${name}
    ${section}=    Product Section    ${name}
    Wait For Elements State    ${section} >> role=heading[level=1]    visible
    ...    message=The page should show "${name}" as its main heading.

Product Image Should Be Shown
    [Documentation]    The product's section shows a loaded image whose alternative text names the product.
    [Arguments]    ${name}
    ${section}=    Product Section    ${name}
    ${pattern}=    Regexp Escape    ${name}
    ${image}=    Set Variable    ${section} >> role=img[name=/${pattern}/i]
    Wait For Elements State    ${image}    visible
    ...    message=The product's section should show an image of "${name}".
    Get Property    ${image}    naturalWidth    >    ${0}
    ...    message=The image of "${name}" should have loaded.

Category Badge Should Show
    [Documentation]    The product's section shows one badge whose whole visible text is ``category``, ignoring case.
    [Arguments]    ${name}    ${category}
    ${section}=    Product Section    ${name}
    ${pattern}=    Regexp Escape    ${category}
    ${badge}=    Set Variable    ${section} >> text=/^${pattern}$/i
    Get Element Count    ${badge}    ==    1
    ...    message=The product's section should show one "${category}" category badge, not {value}.
    Wait For Elements State    ${badge}    visible
    ...    message=The "${category}" category badge should be visible.

Star Rating Should Be Shown
    [Arguments]    ${name}
    ${section}=    Product Section    ${name}
    Wait For Elements State    ${section} >> ${STAR RATING}    visible
    ...    message=The product's section should show a star rating.

Review Count Should Be Shown
    [Documentation]    The product's section shows a review count, "<n> reviews" or "(<n>)".
    [Arguments]    ${name}
    ${section}=    Product Section    ${name}
    Wait For Elements State    ${section} >> ${REVIEW COUNT} >> nth=0    visible
    ...    message=The product's section should show a review count.

Product Price Should Be
    [Documentation]    The product's section shows exactly one price, and it is ``amount``, written as ``$249.99``.
    [Arguments]    ${name}    ${amount}
    ${section}=    Product Section    ${name}
    ${expected}=    Format Price    ${amount}
    Get Element Count    ${section} >> ${CARD PRICE}    ==    1
    ...    message=The product's section should show exactly one price, not {value}.
    Get Text    ${section} >> ${CARD PRICE}    ==    ${expected}
    ...    message=The product's price should be ${expected}, not {value}.

Product Description Should Be Shown
    [Documentation]    The product's section shows ``description`` as visible text, ignoring case.
    [Arguments]    ${name}    ${description}
    ${section}=    Product Section    ${name}
    Wait For Elements State    ${section} >> text=${description}    visible
    ...    message=The product's section should show its description.

Click Add To Cart
    [Documentation]    Clicks the product's "Add to Cart" button and returns the response to the cart request
    ...    it sends.
    [Arguments]    ${name}
    ${section}=    Product Section    ${name}
    Wait For Elements State    ${section} >> ${ADD TO CART}    visible
    ...    message=The product's section should show an "Add to Cart" button.
    ${promise}=    Promise To    Wait For Response    matcher=**/api/cart/items
    Click    ${section} >> ${ADD TO CART}
    ${response}=    Wait For    ${promise}
    RETURN    ${response}

Cart Request Should Add Product
    [Documentation]    The cart request was a POST carrying ``product_id``, it succeeded, and the cart it
    ...    returned holds that product.
    [Arguments]    ${response}    ${product_id}
    Should Be Equal    ${response}[request][method]    POST
    ...    msg=The cart request should be a POST, not ${response}[request][method].
    ${body}=    Set Variable    ${response}[request][postData]
    Should Be True    isinstance($body, dict)    msg=The cart request should send a JSON body, not ${body}.
    ${expected}=    Convert To Integer    ${product_id}
    ${sent}=    Evaluate    $body.get("product_id")
    Should Be Equal    ${sent}    ${expected}
    ...    msg=The cart request should carry the product ID ${expected}, not ${sent}.
    Should Be True    ${response}[ok]
    ...    msg=The cart request should succeed, but it answered with status ${response}[status].
    ${held}=    Evaluate    [item.get("product_id") for item in $response["body"].get("items", [])]
    Should Contain    ${held}    ${expected}
    ...    msg=The cart the request returned should hold product ${expected}, but it holds ${held}.

Open Product From Grid
    [Documentation]    Follows the name link of the product ``name`` in the products page's grid.
    [Arguments]    ${name}
    Click    ${GRID} >> role=heading >> a:has-text("${name}")

Follow Navigation Link To Products
    [Documentation]    Follows the site header's navigation link to the products page.
    Click    ${NAV PRODUCTS}

Products Page Should Be Shown
    [Documentation]    The browser is on ``/products``, and the product grid is visible.
    Get Url    $=    /products    message=The browser should be on /products, not {value}.
    Wait For Elements State    ${GRID}    visible
    ...    message=The products page's grid should be visible.

Not Found Message Should Be Shown
    [Documentation]    The main content shows a visible message saying "not found", with a space or a hyphen.
    Wait For Elements State    ${NOT FOUND} >> nth=0    visible
    ...    message=The page's main content should show a not-found message.

Product Actions Should Not Be Shown
    [Documentation]    The main content holds no "Add to Cart" button and no "Buy Now" link or button.
    Get Element Count    role=main >> ${ADD TO CART}    ==    0
    ...    message=The main content should hold no "Add to Cart" button, but it holds {value}.
    Get Element Count    role=main >> ${BUY NOW}    ==    0
    ...    message=The main content should hold no "Buy Now" link or button, but it holds {value}.
