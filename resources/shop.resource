*** Settings ***
Documentation       The browser and the shop's pages.
...
...                 One browser per suite and one context per test, so every test starts
...                 with its own cookies and an empty cart. When ${SHOP_SPACE} is set,
...                 every request the context sends - pages, assets and API calls - carries
...                 that workshop space.

Library             Browser


*** Variables ***
${HEADLESS}     ${True}


*** Keywords ***
Open Shop Browser
    [Documentation]    Starts the browser once for the suite.
    New Browser    chromium    headless=${HEADLESS}

Start Shop Test
    [Documentation]    Opens a fresh context and page for one test.
    IF    "${SHOP_SPACE}"
        &{headers}=    Create Dictionary    X-Workshop-Space=${SHOP_SPACE}
        New Context    baseURL=${SHOP_URL}    extraHTTPHeaders=${headers}
    ELSE
        New Context    baseURL=${SHOP_URL}
    END
    New Page

Go To Shop Page
    [Documentation]    Opens a path of the shop, for example ``/products``.
    [Arguments]    ${path}
    Go To    ${SHOP_URL}${path}
