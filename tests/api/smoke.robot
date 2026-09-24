*** Settings ***
Documentation       API smoke tests: the shop answers, and the catalogue is complete.

Resource            resources/api.resource

Suite Setup         Open Shop API

Test Tags           smoke    api


*** Test Cases ***
Health Reports Ok
    ${health}=    Get Shop Health
    Should Be Equal    ${health}[status]    ok

Catalogue Lists Twelve Products
    @{products}=    Get Catalogue From API
    Length Should Be    ${products}    12
