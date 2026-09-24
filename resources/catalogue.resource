*** Settings ***
Documentation       The products page, /products, through the shop's stable contract:
...                 roles, accessible names, visible text and labels.

Library             Browser
Library             Collections
Library             String
Resource            shop.resource


*** Variables ***
# The innermost section headed "All products": the product grid, without the
# category previews further down the page.
${GRID}             section:has(h2:text-is("All products")):not(:has(section))
${FILTERS}          role=complementary
${HIGHLIGHTS}       section:has(h2:text-is("Handpicked highlights"))


*** Keywords ***
Go To Catalogue
    Go To Shop Page    /products
    Wait For Elements State    ${GRID}    visible

Get Grid Card Count
    [Documentation]    The number of product cards in the grid.
    ${count}=    Get Element Count    ${GRID} >> article
    RETURN    ${count}

Get Add To Cart Button Count
    [Documentation]    The number of grid cards whose button reads "Add to cart".
    ${count}=    Get Element Count    ${GRID} >> article >> button:has-text("Add to cart")
    RETURN    ${count}

Get Grid Card Names
    [Documentation]    The product names of the grid cards, in page order.
    @{names}=    Get Texts    ${GRID} >> article >> role=heading[level=3]
    RETURN    ${names}

Get Texts
    [Documentation]    The visible text of every element the locator matches.
    [Arguments]    ${locator}
    @{elements}=    Get Elements    ${locator}
    @{texts}=    Create List
    FOR    ${element}    IN    @{elements}
        ${text}=    Get Text    ${element}
        Append To List    ${texts}    ${text.strip()}
    END
    RETURN    ${texts}

Get Card Category
    [Documentation]    The category a card shows, from its ``data-category`` content attribute.
    [Arguments]    ${card}
    ${category}=    Get Attribute    ${card} >> [data-category]    data-category
    RETURN    ${category}

Check Category
    [Arguments]    ${category}
    Check Checkbox    ${FILTERS} >> role=checkbox[name="${category}"]

Apply Filters
    Click    ${FILTERS} >> role=button[name="Apply filters"]
    Wait For Elements State    ${GRID}    visible

Get Category Checkbox Count
    ${count}=    Get Element Count    ${FILTERS} >> role=group[name="Categories"] >> role=checkbox
    RETURN    ${count}

Filter Checkboxes Should All Be Unchecked
    [Documentation]    Every checkbox of the filter sidebar is unchecked.
    @{boxes}=    Get Elements    ${FILTERS} >> role=checkbox
    Should Not Be Empty    ${boxes}
    FOR    ${box}    IN    @{boxes}
        Get Checkbox State    ${box}    ==    unchecked
    END

Checkbox Should Be Unchecked
    [Documentation]    The filter checkbox labelled ``label`` exists and is unchecked.
    [Arguments]    ${label}
    Get Checkbox State    ${FILTERS} >> role=checkbox[name="${label}"]    ==    unchecked

Get Price Range Values
    [Documentation]    The minimum and maximum the price range shows.
    @{values}=    Get Texts    ${FILTERS} >> role=group[name="Price range"] >> role=status
    RETURN    ${values}

Get Highlight Prices
    [Documentation]    The prices shown in "Handpicked highlights", in page order.
    @{links}=    Get Texts    ${HIGHLIGHTS} >> role=link
    @{prices}=    Create List
    FOR    ${text}    IN    @{links}
        ${price}=    Get Regexp Matches    ${text}    \\$[0-9,]+\\.[0-9]{2}
        Append To List    ${prices}    ${price}[0]
    END
    RETURN    ${prices}

Format Price
    [Documentation]    ``249.99`` as the shop shows it: ``$249.99``.
    [Arguments]    ${amount}
    ${text}=    Evaluate    "$" + format(float($amount), ",.2f")
    RETURN    ${text}
