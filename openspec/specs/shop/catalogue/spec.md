# shop/catalogue Specification

## Purpose
Describes the products page, `/products`, as a shopper experiences it: the product grid, its filters, the collection previews and the highlights.

## Requirements

### Requirement: Full product grid (WEB-002_AC-1)
When a shopper opens `/products` and the page finishes loading, the page SHALL display all 12 seeded products in a grid. Each product card SHALL show the product's name, its image, its price - the product's own price - and an "Add to Cart" button.

#### Scenario: Opening the products page
- **WHEN** a shopper opens `/products`
- **THEN** 12 product cards are displayed, and each shows the product's name, image and price and an "Add to Cart" button

### Requirement: Category filter group (WEB-002_AC-2)
The products page SHALL display a "Categories" filter group with one checkbox for each of the 9 categories in the seeded catalogue, and no category checkbox SHALL be selected by default.

#### Scenario: Default category filters
- **WHEN** the products page has loaded
- **THEN** a "Categories" group offers 9 category checkboxes, none of them checked

### Requirement: Price range filter (WEB-002_AC-3)
The products page SHALL display a "Price range" filter with a dual slider that has a minimum and a maximum handle. Its minimum SHALL be the lowest product price, $39.50, and its maximum the highest product price, $899.00. Slider labels or input fields SHALL show the current minimum and maximum values.

#### Scenario: Default price range
- **WHEN** the products page has loaded
- **THEN** the price range runs from $39.50 to $899.00, and both current values are shown

### Requirement: Rating filter (WEB-002_AC-4)
The products page SHALL display a rating filter with a "4 stars & up" checkbox, unchecked by default.

#### Scenario: Default rating filter
- **WHEN** the products page has loaded
- **THEN** a "4 stars & up" checkbox is shown unchecked

### Requirement: Availability filter (WEB-002_AC-5)
The products page SHALL display an availability filter with a "Show in-stock only" checkbox, unchecked by default.

#### Scenario: Default availability filter
- **WHEN** the products page has loaded
- **THEN** a "Show in-stock only" checkbox is shown unchecked

### Requirement: Apply filters (WEB-002_AC-6)
When the shopper has selected one or more filter criteria and clicks "Apply filters", the product grid SHALL show only the products that match all selected criteria, and the product count SHALL reflect the filtered results.

#### Scenario: Several criteria selected
- **WHEN** the shopper selects a category, "4 stars & up" and "Show in-stock only", and clicks "Apply filters"
- **THEN** the grid shows only products that satisfy all three criteria, and the displayed product count equals the number of those products

### Requirement: Category filter application (WEB-002_AC-7)
When the shopper checks the "Audio" category and clicks "Apply filters", only products in the "Audio" category SHALL be displayed in the grid.

#### Scenario: Audio only
- **WHEN** the shopper checks "Audio" and clicks "Apply filters"
- **THEN** every product in the grid belongs to the "Audio" category

### Requirement: Price range filter application (WEB-002_AC-8)
When the shopper sets the price range to $100-$300 and clicks "Apply filters", only products priced between $100.00 and $300.00 inclusive SHALL be displayed.

#### Scenario: $100 to $300
- **WHEN** the shopper sets the price range to $100-$300 and clicks "Apply filters"
- **THEN** every product in the grid is priced from $100.00 to $300.00 inclusive

### Requirement: Combined filters (WEB-002_AC-9)
When the shopper selects a category filter and a price range and clicks "Apply filters", only products matching all selected criteria SHALL be displayed, and products outside the intersection of the filters SHALL be hidden.

#### Scenario: Category and price range
- **WHEN** the shopper selects a category and a price range and clicks "Apply filters"
- **THEN** the grid shows exactly the products in that category whose prices lie in that range

### Requirement: Reset filters (WEB-002_AC-10)
When the shopper has applied one or more filters and clicks the "Reset" link, all filter checkboxes SHALL be unchecked, the price range sliders SHALL return to their default minimum and maximum, and the grid SHALL show all 12 products again.

#### Scenario: Resetting applied filters
- **WHEN** filters have been applied and the shopper clicks "Reset"
- **THEN** no filter checkbox is checked, the price range is back at $39.50 to $899.00, and 12 products are shown

### Requirement: Collections to explore (WEB-002_AC-11)
The products page SHALL display a "Collections to explore" section with category previews, each showing up to 3 products from its category.

#### Scenario: Category previews
- **WHEN** the shopper scrolls to "Collections to explore"
- **THEN** category previews are shown, and none shows more than 3 products, all from its own category

### Requirement: Handpicked highlights (WEB-002_AC-12)
The products page SHALL display a "Handpicked highlights" section showing the 3 highest-priced products, sorted by price with the highest first.

#### Scenario: Top three by price
- **WHEN** the shopper views "Handpicked highlights"
- **THEN** it shows the three most expensive products of the catalogue in descending order of price

### Requirement: Empty state for no results (WEB-002_AC-13)
When the shopper applies filters that match no product, a message SHALL indicate that no products match the current filters, and SHALL suggest adjusting the filters or resetting them.

#### Scenario: A combination nothing satisfies
- **WHEN** the shopper applies a combination of filters that no product satisfies
- **THEN** a message says that no products match and suggests adjusting or resetting the filters
