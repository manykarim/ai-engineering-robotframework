*** Settings ***
Documentation       Product search on the home page and the products page (spec: shop/search).

Resource            resources/shop.resource
Resource            resources/api.resource
Resource            resources/search.resource

Suite Setup         Run Keywords    Open Shop Browser    AND    Open Shop API
Suite Teardown      Close Browser
Test Setup          Start Shop Test

Test Tags           WEB-004    ui


*** Test Cases ***
WEB-004_AC-1 Home Page Hero Shows Search Input
    [Documentation]    The first screen of / shows the main heading and a search input whose placeholder or label says "search".
    Go To Home Page
    Hero Search Input Should Be Shown
    Search Input Should Indicate Its Purpose

WEB-004_AC-3 Enter Shows Matching Results
    [Documentation]    Searching "headphones" with Enter lists Aurora Neural Headphones with its name, image and price.
    ${product}=    Get Product From API    1
    Go To Home Page
    Submit Search With Enter    headphones
    Search Results Should List    Aurora Neural Headphones
    Search Result Card Should Show    Aurora Neural Headphones    ${product}[price]

WEB-004_AC-3 Search Button Shows Matching Results
    [Documentation]    Searching "headphones" with the search button lists Aurora Neural Headphones with its name, image and price.
    ${product}=    Get Product From API    1
    Go To Home Page
    Submit Search With Button    headphones
    Search Results Should List    Aurora Neural Headphones
    Search Result Card Should Show    Aurora Neural Headphones    ${product}[price]

WEB-004_AC-6 Clear Results On Home Page
    [Documentation]    On /, clearing the results hides them, shows the hero again and empties the search input.
    Go To Home Page
    Submit Search With Enter    headphones
    Search Results Should List    Aurora Neural Headphones
    Clear Search Results
    Search Results Should Be Hidden
    Hero Section Should Be Shown
    Search Input Should Be Empty

WEB-004_AC-6 Clear Search On Products Page
    [Documentation]    On /products, clearing the search hides the results, shows the grid again and empties the search input.
    Go To Catalogue
    Submit Search With Enter    headphones
    Search Results Should List    Aurora Neural Headphones
    Clear Search Results
    Search Results Should Be Hidden
    Product Grid Should Be Shown
    Search Input Should Be Empty

WEB-004_AC-7 Unmatched Query Shows Empty State
    [Documentation]    Searching "xyz123" shows a "no products" message in the search results, and no card.
    Go To Home Page
    Submit Search With Enter    xyz123
    Search Results Should Be Shown
    Empty Search Message Should Be Shown
    Search Results Should Hold No Cards
