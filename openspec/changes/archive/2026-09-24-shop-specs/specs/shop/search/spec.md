## Purpose

Describes product search as a shopper and an API consumer experience it: the search forms, suggestions while typing, results, clearing, the empty state, and the search API.

## ADDED Requirements

### Requirement: Search form on the home page (WEB-004_AC-1)
The home page, `/`, SHALL show a search form or input in its hero section, with a placeholder or label indicating its purpose.

#### Scenario: Home page search
- **WHEN** a shopper opens `/`
- **THEN** a search input with a placeholder or label is visible in the hero section

### Requirement: Search form on the products page (WEB-004_AC-2)
The products page, `/products`, SHALL show a search form or input.

#### Scenario: Products page search
- **WHEN** a shopper opens `/products`
- **THEN** a search input is visible

### Requirement: Search submission shows results (WEB-004_AC-3)
When the shopper has entered a query and submits the search form, either by pressing Enter or by clicking the search button, a search results section SHALL be displayed with the products matching the query, as a grid of product cards with name, image and price.

#### Scenario: Searching for headphones
- **WHEN** a shopper enters "headphones" and presses Enter
- **THEN** a search results section lists Aurora Neural Headphones as a card with its name, image and price

### Requirement: Autocomplete suggestions (WEB-004_AC-5)
While the shopper types in the search input, autocomplete suggestions SHALL appear through a call to `/api/search/suggest`, and SHALL be displayed in a dropdown or list below the input.

#### Scenario: Typing a query
- **WHEN** a shopper types characters into the search input
- **THEN** a request to `/api/search/suggest` is made and suggestions appear below the input

### Requirement: Clear search results (WEB-004_AC-6)
When search results are displayed and the shopper clicks the "Clear search" or "Clear results" button, the results section SHALL be hidden, the normal page content (the product grid or the hero section) SHALL be shown again, and the search input SHALL be cleared.

#### Scenario: Clearing results
- **WHEN** results are displayed and the shopper clicks "Clear search" or "Clear results"
- **THEN** the results are hidden, the page's normal content is back, and the search input is empty

### Requirement: Empty state for no results (WEB-004_AC-7)
When a submitted query matches no product, a visible, user-friendly empty-state message SHALL be shown, for example "No products found".

#### Scenario: A query without matches
- **WHEN** a shopper searches for "xyz123"
- **THEN** a visible message states that no products were found

### Requirement: Results are product cards (WEB-004_AC-8)
When a query returns matching products, each result SHALL be displayed as a product card that includes the product's name, price and image, has an "Add to Cart" button, and links to the product's detail page.

#### Scenario: A result card
- **WHEN** a search for "aurora" returns Aurora Neural Headphones
- **THEN** its card shows the name, price and image, offers "Add to Cart", and links to `/products/1`

### Requirement: Search via the API (WEB-004_AC-9)
When an API consumer sends `GET /api/search/` with the search text in the `query` parameter, the response SHALL be successful and SHALL list the products that match the search text.

#### Scenario: Searching through the API
- **WHEN** an API consumer sends `GET /api/search/?query=headphones`
- **THEN** the response is successful and lists Aurora Neural Headphones
