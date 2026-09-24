## Purpose

Describes a product's detail page, `/products/{id}`, as a shopper experiences it: the product's information, its actions, the recommendations around it, and the page shown for a product that does not exist.

## ADDED Requirements

### Requirement: Product core information (WEB-003_AC-1)
When a shopper opens a product's detail page and it finishes loading, the page SHALL display the product's image, name, a category badge, a visual star rating, a numeric review count, the price and the product description.

#### Scenario: Opening a product
- **WHEN** a shopper opens `/products/1`
- **THEN** the page shows the product image, the name "Aurora Neural Headphones", a category badge, a star rating, a review count, the price and a description

### Requirement: Star rating accuracy (WEB-003_AC-2)
For a product rated 4.8 stars with 214 reviews, the detail page SHALL show a rating of 4.8 stars, or an equivalent visual, and a review count text of "214 reviews" or "(214)".

#### Scenario: Aurora Neural Headphones
- **WHEN** a shopper opens `/products/1`, the seeded product Aurora Neural Headphones rated 4.8 with 214 reviews
- **THEN** the rating shows 4.8 stars and the review count reads "214 reviews" or "(214)"

### Requirement: Add to Cart button (WEB-003_AC-3)
The detail page's action area SHALL display an "Add to Cart" button that identifies the product it adds. Clicking it SHALL send a POST request that adds that product to the cart.

#### Scenario: Adding from the detail page
- **WHEN** a shopper clicks "Add to Cart" on `/products/1`
- **THEN** a POST request adds Aurora Neural Headphones to the shopper's cart

### Requirement: Buy Now link (WEB-003_AC-4)
The detail page's action area SHALL display a "Buy Now" link or button, and clicking it SHALL navigate to the checkout page, `/checkout`.

#### Scenario: Buying now
- **WHEN** a shopper clicks "Buy Now" on a product's detail page
- **THEN** the browser is on `/checkout`

### Requirement: You might also like (WEB-003_AC-5)
The detail page SHALL display a "You might also like" section with up to 4 related products. Products from the same category SHALL be listed first, and each related product card SHALL link to that product's own detail page.

#### Scenario: Related products
- **WHEN** the shopper scrolls to "You might also like" on a product's detail page
- **THEN** at most 4 products are shown, those in the same category as the viewed product come first, and each card links to its product's detail page

### Requirement: Trending in the studio (WEB-003_AC-6)
The detail page SHALL display a "Trending in the studio" section with further product recommendations, each card showing the product's name, price and image.

#### Scenario: Trending products
- **WHEN** the shopper scrolls to "Trending in the studio"
- **THEN** product cards are shown, each with a name, a price and an image

### Requirement: Product highlights (WEB-003_AC-7)
The detail page SHALL display a product highlights section with warranty information, compatibility details, and impact or sustainability information.

#### Scenario: Highlights
- **WHEN** the shopper scrolls to the product highlights
- **THEN** warranty, compatibility and impact or sustainability information are visible

### Requirement: Navigation back to the catalogue (WEB-003_AC-8)
From a product's detail page, the shopper SHALL be able to return to the products page, `/products`, with the browser's back button or a navigation link.

#### Scenario: Back to the catalogue
- **WHEN** a shopper who opened a detail page from `/products` goes back, or follows a navigation link to the products
- **THEN** the products page is shown

### Requirement: Invalid product ID (WEB-003_AC-9)
When a visitor opens `/products/{id}` for an ID that does not exist, the page SHALL show an appropriate error state or not-found message, and SHALL NOT show a broken or empty product detail page.

#### Scenario: Unknown numeric ID
- **WHEN** a visitor opens `/products/9999`
- **THEN** a not-found message is shown instead of a product detail page

#### Scenario: Non-numeric ID
- **WHEN** a visitor opens `/products/abc`
- **THEN** a not-found message is shown instead of a product detail page
