*** Settings ***
Documentation       The cart as a shopper sees it: the cart badge in the site header, the
...                 navigation menu on small screens, and the cart page, /cart, with its
...                 lines and its summary. Through the shop's stable contract: roles,
...                 visible text, and the header's link to the cart page.

Library             Browser
Library             String
Resource            shop.resource
Resource            checkout.resource
Resource            product_detail.resource


*** Variables ***
# The whole number inside the header's link to the cart page. The spec quotes no text
# for that link or its badge, so the link is found by its target.
${CART BADGE}           role=banner >> a[href="/cart"] >> text=/^\\d+$/
# The menu button's only text is visually hidden: its accessible name, in the spec's
# words "navigation menu", finds it.
${MENU BUTTON}          role=banner >> role=button[name=/navigation|menu/i]
${CART LINES}           role=main >> role=article
# A dollar amount with cents, as a regex: "$539.48".
${AMOUNT PATTERN}       \\$[0-9,]+\\.[0-9]{2}


*** Keywords ***
Click Add To Cart And Confirm
    [Documentation]    Clicks the "Add to Cart" button on the open detail page and checks that the request succeeded.
    [Arguments]    ${product_id}    ${name}
    ${response}=    Click Add To Cart    ${name}
    Should Be True    ${response}[ok]
    ...    msg=Adding product ${product_id}, ${name}, should succeed, but the shop answered with status ${response}[status].

Add Product To Cart
    [Documentation]    Opens the product's detail page and adds the product to the cart ``times`` times.
    [Arguments]    ${product_id}    ${name}    ${times}=1
    Go To Product Page    ${product_id}
    Product Detail Should Show    ${name}
    FOR    ${_}    IN RANGE    ${times}
        Click Add To Cart And Confirm    ${product_id}    ${name}
    END

Use Small Screen
    [Documentation]    Resizes the test's page to a phone, 390 by 844 pixels. Call it before opening a page.
    Set Viewport Size    390    844

Open Navigation Menu
    [Documentation]    Opens the site header's navigation menu with its menu button, which small screens show.
    Click    ${MENU BUTTON}

Cart Badge Should Show
    [Documentation]    The cart badge in the site header is visible and shows ``count``.
    [Arguments]    ${count}
    Wait For Elements State    ${CART BADGE}    visible
    ...    message=The cart badge in the site header should be visible and show ${count}.
    Get Text    ${CART BADGE}    ==    ${count}
    ...    message=The cart badge in the site header should show ${count}, not {value}.

Cart Line
    [Documentation]    The locator of the cart page's line that shows the product ``name``, ignoring case.
    [Arguments]    ${name}
    RETURN    role=main >> article:has-text("${name}")

Cart Line Should Show
    [Documentation]    The line of ``name`` shows ``quantity``, and the amounts ``unit_price`` and ``line_total``,
    ...    written as ``$249.99``.
    [Arguments]    ${name}    ${quantity}    ${unit_price}    ${line_total}
    ${line}=    Cart Line    ${name}
    Wait For Elements State    ${line}    visible    message=The cart should list a line for "${name}".
    Get Text    ${line}    *=    ${unit_price}
    ...    message=The line of "${name}" should show the unit price ${unit_price}, but it reads: {value}
    Get Text    ${line}    *=    ${line_total}
    ...    message=The line of "${name}" should show the line total ${line_total}, but it reads: {value}
    Cart Line Quantity Should Be    ${name}    ${quantity}

Cart Line Quantity Should Be
    [Documentation]    Apart from the product's name and the dollar amounts, the only whole number in the line of
    ...    ``name`` is ``quantity``.
    [Arguments]    ${name}    ${quantity}
    ${line}=    Cart Line    ${name}
    Wait For Elements State    ${line}    visible    message=The cart should list a line for "${name}".
    ${text}=    Get Text    ${line}
    ${name pattern}=    Regexp Escape    ${name}
    ${rest}=    Replace String Using Regexp    ${text}    (?i)${name pattern}    ${SPACE}
    ${rest}=    Replace String Using Regexp    ${rest}    ${AMOUNT PATTERN}    ${SPACE}
    @{numbers}=    Get Regexp Matches    ${rest}    \\b\\d+\\b
    ${quantity}=    Convert To String    ${quantity}
    @{expected}=    Create List    ${quantity}
    Should Be Equal    ${numbers}    ${expected}    values=False
    ...    msg=The line of "${name}" should show the quantity ${quantity}, but its whole numbers are ${numbers}. It reads: ${text}

Cart Should Have Lines
    [Documentation]    The cart page lists exactly ``count`` lines.
    [Arguments]    ${count}
    Get Element Count    ${CART LINES}    ==    ${count}
    ...    message=The cart should list ${count} line(s), not {value}.

Summary Entry
    [Documentation]    The locator of the cart summary's entry that shows the whole word ``word``, then a value
    ...    matching the regex ``value``, ignoring case.
    [Arguments]    ${word}    ${value}
    RETURN    ${SUMMARY} >> text=/\\b${word}\\b[\\s\\S]*${value}/i

Get Cart Summary Amount
    [Documentation]    The amount of the cart summary's entry for ``word``, such as ``subtotal``, as a number.
    [Arguments]    ${word}
    ${entry}=    Summary Entry    ${word}    ${AMOUNT PATTERN}
    Wait For Elements State    ${entry}    visible
    ...    message=The cart summary should show the ${word} with an amount.
    ${text}=    Get Text    ${entry}
    ${amount}=    Amount From Text    ${text}
    RETURN    ${amount}

Cart Summary Amount Should Be
    [Documentation]    The cart summary's entry for ``word`` shows ``amount``, compared to the cent.
    [Arguments]    ${word}    ${amount}
    ${shown}=    Get Cart Summary Amount    ${word}
    Should Be Equal As Numbers    ${shown}    ${amount}    precision=2    values=False
    ...    msg=The cart summary's ${word} should be ${amount}, not ${shown}.

Cart Summary Should Show
    [Documentation]    The cart summary's entry for ``word`` shows ``text``, ignoring case.
    [Arguments]    ${word}    ${text}
    ${text pattern}=    Regexp Escape    ${text}
    ${entry}=    Summary Entry    ${word}    ${text pattern}
    Wait For Elements State    ${entry}    visible
    ...    message=The cart summary should show the ${word} as "${text}".
