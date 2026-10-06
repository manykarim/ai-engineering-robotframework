*** Settings ***
Documentation       Variables shared by the acceptance suites: where the shop runs and its seed data.
...                 Override any of them with ``--variable``, for example ``--variable WORKSHOP_SPACE:team-7``.


*** Variables ***
${SHOP_URL}             http://localhost:9090
# Not ${SPACE}, which is Robot Framework's built-in variable holding a single space.
${WORKSHOP_SPACE}       ${NONE}

# The shop's seed catalogue.
${PRODUCT_COUNT}        12
${PRODUCT_1_PRICE}      249.99
${PRODUCT_2_PRICE}      39.5
${PRODUCT_5_PRICE}      799
