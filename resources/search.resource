*** Settings ***
Documentation       Product search on the home page, /, and the products page, /products, through
...                 the shop's stable contract: roles, labels and visible text. The hero section has
...                 no role, label or text of its own, so it is recognised as a shopper sees it: the
...                 first screen of the page, which opens with the page's main heading.

Library             Browser
Library             String
Resource            shop.resource
Resource            catalogue.resource


*** Variables ***
${MAIN HEADING}     role=main >> role=heading[level=1]
${SEARCH FORM}      role=main >> role=search
${SEARCH INPUT}     role=main >> role=searchbox
# The search form's button, by the spec's word in "the search button".
${SEARCH BUTTON}    ${SEARCH FORM} >> button:has-text("Search")
${RESULTS}          role=region[name=/search results/i]
# Either label the spec quotes: "Clear results" on /, "Clear search" on /products.
${CLEAR BUTTON}     ${RESULTS} >> :is(button:has-text("Clear search"), button:has-text("Clear results"))
# The spec's words "no products". The suggestions' own "No results" lies outside ${RESULTS}.
${EMPTY MESSAGE}    ${RESULTS} >> text=/no products/i
# The shop runs the typed search again by itself, 300 ms after the last keystroke. A click on
# Clear before that search has returned lets it show the results again.
${SEARCH SETTLE}    1s


*** Keywords ***
Go To Home Page
    Go To Shop Page    /

Hero Search Input Should Be Shown
    [Documentation]    The main content holds one visible search input, and it lies with the page's main
    ...    heading within the first screen. Call it before anything scrolls.
    Get Element Count    ${SEARCH INPUT}    ==    1
    ...    message=The main content should hold one search input, not {value}.
    Wait For Elements State    ${SEARCH INPUT}    visible
    ...    message=The search input should be visible.
    Wait For Elements State    ${MAIN HEADING}    visible
    ...    message=The page should show its main heading.
    Element Should Lie Within First Screen    ${MAIN HEADING}    main heading
    Element Should Lie Within First Screen    ${SEARCH INPUT}    search input

Element Should Lie Within First Screen
    [Documentation]    The element lies entirely within the browser window, as the page is scrolled now.
    [Arguments]    ${locator}    ${what}
    ${window}=    Get Viewport Size
    ${box}=    Get BoundingBox    ${locator}
    ${top}=    Evaluate    round($box["y"])
    ${bottom}=    Evaluate    round($box["y"] + $box["height"])
    Should Be True    $box["y"] >= 0 and $box["y"] + $box["height"] <= $window["height"]
    ...    msg=The ${what} should lie within the first screen, 0 to ${window}[height] px, but it spans ${top} to ${bottom} px.

Search Input Should Indicate Its Purpose
    [Documentation]    The search input's placeholder or its label contains "search", ignoring case.
    ${placeholder}=    Get Property    ${SEARCH INPUT}    placeholder
    ${labelled}=    Get Element Count    role=main >> role=searchbox[name=/search/i]
    Should Be True    "search" in $placeholder.lower() or ${labelled} > 0
    ...    msg=The search input's placeholder or label should say "search", but its placeholder is "${placeholder}" and no label names a search.

Submit Search With Enter
    [Documentation]    Enters ``query`` in the search input and presses Enter in it.
    [Arguments]    ${query}
    Fill Text    ${SEARCH INPUT}    ${query}
    Press Keys    ${SEARCH INPUT}    Enter

Submit Search With Button
    [Documentation]    Enters ``query`` in the search input and clicks the search button.
    [Arguments]    ${query}
    Fill Text    ${SEARCH INPUT}    ${query}
    Click    ${SEARCH BUTTON}

Search Results Should Be Shown
    Wait For Elements State    ${RESULTS}    visible
    ...    message=The page should show a search results section.

Search Result Card
    [Documentation]    The locator of the result card that shows ``name``, ignoring case.
    [Arguments]    ${name}
    RETURN    ${RESULTS} >> article:has-text("${name}")

Search Results Should List
    [Documentation]    The search results section is shown, with a card for ``name``.
    [Arguments]    ${name}
    Search Results Should Be Shown
    ${card}=    Search Result Card    ${name}
    Wait For Elements State    ${card}    visible
    ...    message=The search results should list a card for "${name}".

Search Result Card Should Show
    [Documentation]    The card of ``name`` shows the name, a loaded image of the product and exactly one
    ...    price, ``amount`` written as ``$249.99``.
    [Arguments]    ${name}    ${amount}
    ${card}=    Search Result Card    ${name}
    ${heading}=    Get Text    ${card} >> role=heading
    Should Contain    ${heading}    ${name}    ignore_case=True
    ...    msg=The card's heading should show "${name}", not "${heading}".
    ${pattern}=    Regexp Escape    ${name}
    ${image}=    Set Variable    ${card} >> role=img[name=/${pattern}/i]
    Wait For Elements State    ${image}    visible
    ...    message=The card of "${name}" should show an image of it.
    Get Property    ${image}    naturalWidth    >    ${0}
    ...    message=The image of "${name}" should have loaded.
    ${expected}=    Format Price    ${amount}
    Get Element Count    ${card} >> ${CARD PRICE}    ==    1
    ...    message=The card of "${name}" should show exactly one price, not {value}.
    Get Text    ${card} >> ${CARD PRICE}    ==    ${expected}
    ...    message=The card of "${name}" should show the price ${expected}, not {value}.

Clear Search Results
    [Documentation]    Lets the search that the typing started settle, then clicks "Clear search" or
    ...    "Clear results" in the search results section.
    Sleep    ${SEARCH SETTLE}    reason=The shop runs the typed search again 300 ms after the last keystroke.
    Click    ${CLEAR BUTTON}

Search Results Should Be Hidden
    Wait For Elements State    ${RESULTS}    hidden
    ...    message=The search results section should be hidden, but it is still shown.

Hero Section Should Be Shown
    [Documentation]    The hero is shown: the page's main heading is visible.
    Wait For Elements State    ${MAIN HEADING}    visible
    ...    message=The hero section, with the page's main heading, should be shown.

Product Grid Should Be Shown
    Wait For Elements State    ${GRID}    visible
    ...    message=The products page's grid should be shown.

Search Input Should Be Empty
    Get Property    ${SEARCH INPUT}    value    ==    ${EMPTY}
    ...    message=The search input should be empty, not "{value}".

Empty Search Message Should Be Shown
    [Documentation]    The search results section shows a visible message saying "no products", ignoring case.
    Wait For Elements State    ${EMPTY MESSAGE} >> nth=0    visible
    ...    message=The search results should show a message saying "no products".

Search Results Should Hold No Cards
    Get Element Count    ${RESULTS} >> role=article    ==    0
    ...    message=The search results should hold no product card, but they hold {value}.
