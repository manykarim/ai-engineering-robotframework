*** Settings ***
Documentation       The cart and checkout pages through the shop's stable contract.
...                 Form fields are always scoped to the checkout form: the sign-in dialog
...                 has an email field too.

Library             Browser
Library             Collections
Library             String
Resource            shop.resource


*** Variables ***
${CHECKOUT FORM}    form[action="/checkout"]
${SUMMARY}          role=complementary
${CART LINK}        role=banner >> role=link[name=/^Cart/]


*** Keywords ***
Add Product To Cart From Its Page
    [Documentation]    Adds one unit from the product's own page and waits until the cart counts it.
    [Arguments]    ${product_id}    ${product_name}
    Go To Shop Page    /products/${product_id}
    Click    role=button[name="Add ${product_name} to cart"]
    Get Text    ${CART LINK}    matches    \\d

Go To Checkout
    Go To Shop Page    /checkout
    Wait For Elements State    ${CHECKOUT FORM}    visible

Fill Checkout Form
    [Documentation]    Fills the required fields, found by their labels.
    [Arguments]    ${email}    ${full_name}    ${address}
    Fill Text    ${CHECKOUT FORM} >> role=textbox[name="Email"]    ${email}
    Fill Text    ${CHECKOUT FORM} >> role=textbox[name="Full name"]    ${full_name}
    Fill Text    ${CHECKOUT FORM} >> role=textbox[name="Address"]    ${address}

Place Order
    Click    ${CHECKOUT FORM} >> role=button[name="Place order"]

Get Order Confirmation
    [Documentation]    The text of the confirmation that appears after an order is placed.
    ${text}=    Get Text    role=main >> role=alert    *=    confirmed
    RETURN    ${text}

Get Summary Amount
    [Documentation]    The amount on the order summary's line labelled ``label``, with "Complimentary" as 0.
    [Arguments]    ${label}
    ${text}=    Get Text    ${SUMMARY} >> dt:text-is("${label}") + dd
    IF    "${text.strip().lower()}" == "complimentary"    RETURN    ${0}
    ${amount}=    Amount From Text    ${text}
    RETURN    ${amount}

Amount From Text
    [Documentation]    The amount in a text, ``$1,234.50`` as the number 1234.5.
    ...                A label around it is ignored; with several amounts, the last one counts.
    [Arguments]    ${text}
    @{amounts}=    Get Regexp Matches    ${text}    \\$([0-9,]+\\.[0-9]{2})    1
    Should Not Be Empty    ${amounts}    msg=No amount in "${text}".
    ${amount}=    Evaluate    float($amounts[-1].replace(",", ""))
    RETURN    ${amount}

Get Field Messages
    [Documentation]    The messages attached to a field through ``aria-describedby``, as id -> text.
    ...                Read through the relation, so the drifting ids are never written down.
    [Arguments]    ${label}
    &{messages}=    Evaluate JavaScript    ${CHECKOUT FORM} >> role=textbox[name="${label}"]
    ...    (field) => Object.fromEntries((field.getAttribute("aria-describedby") || "").split(/\\s+/)
    ...        .filter(Boolean).map((id) => [id, (document.getElementById(id)?.innerText || "").trim()]))
    RETURN    ${messages}

Get New Field Message
    [Documentation]    The text of the messages a field gained since ``before`` - the ones that
    ...                appeared because of the last action, not help text that was already there.
    [Arguments]    ${label}    ${before}
    &{now}=    Get Field Messages    ${label}
    @{texts}=    Create List
    FOR    ${id}    ${text}    IN    &{now}
        IF    $id not in $before    Append To List    ${texts}    ${text}
    END
    ${message}=    Catenate    @{texts}
    RETURN    ${message}

Go To Cart Page
    Go To Shop Page    /cart

Cart Should Say It Is Empty
    Get Text    role=main    *=    Your cart is still empty

Get Cart Link Text
    [Documentation]    The visible text of the cart link in the site header.
    ${text}=    Get Text    ${CART LINK}
    RETURN    ${text.strip()}
