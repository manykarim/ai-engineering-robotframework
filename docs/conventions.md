# Test conventions

How the tests in this repository are written. The shipped suite follows these rules, and so should every test you or
an agent add. They are specified in `openspec/specs/workshop/test-conventions/spec.md`.

## 1. The criterion ID comes first

A test that verifies a story criterion starts its name with the criterion's ID, `<STORY>_<AC>`:

```robotframework
WEB-006_AC-1 Order Total Adds Up
```

When one criterion needs several tests, they share the prefix: `WEB-002_AC-1 Every Card Offers Add To Cart` and
`WEB-002_AC-1 Card Prices Are The Product Prices`. A test that verifies no criterion carries the `smoke` tag instead.

*Why:* a failing test names the requirement it protects, and results trace back to `openspec/specs/shop/`.

## 2. Locators live in resources

Test files call keywords. Every locator is written inside a keyword under `resources/`.

*Why:* when the page changes, there is exactly one place to fix, and a test reads as behaviour rather than markup.

## 3. The stable contract first

Build locators from what a person or an assistive technology perceives. That doesn't change when the markup is
restyled:

| Use | Example |
|---|---|
| a role and its accessible name | `role=button[name="Apply filters"]` |
| a form field by its label, inside its form | `form[action="/checkout"] >> role=textbox[name="Email"]` |
| visible text | `button:has-text("Add to cart")` |
| a link target | `a[href="/cart"]` |

Element ids, CSS classes and `data-test` hooks are implementation details. Pages rename and remove them.

*Known deviation:* `resources/legacy.resource` still finds some elements by id, class or `data-test` hook. It is kept
deliberately: Module 8 heals exactly these locators. Never add a new keyword to it.

## 4. Quoted text means visible text

When a specification quotes UI text, match it against the element's visible text, ignoring case, as a phrase
contained in that text. Use the accessible name only where the specification speaks of a label or a name.
`openspec/specs/shop/interpretation-rules/spec.md` has the full rules, with examples.

*Example:* the quoted "Add to Cart" is a button whose visible text reads "Add to cart". Its accessible name is the
longer "Add Aurora Neural Headphones to cart", so a lookup by the exact name "Add to Cart" finds nothing.

## 5. Scope form fields to their form

Always locate a field inside its form: `form[action="/checkout"] >> role=textbox[name="Email"]`, not
`[name="email"]`.

*Why:* the same field name can appear in more than one form on a page. The checkout page also contains the sign-in
dialog, which has its own email field.

## 6. Every test is isolated

Every UI test runs in its own browser context, and therefore with its own cookies and its own empty cart. A test never
applies a preset or resets a space. It creates the state it needs through the shop's pages or API, inside its own
session.

*Why:* tests can run in any order, alone or together, locally or on the shared instance.

## 7. Tags

| Tag | On |
|---|---|
| the story ID, for example `WEB-002` | every test that verifies a criterion |
| `smoke` | every test that verifies no criterion |
| `ui` or `api` | every test, exactly one of the two |
| `broken` | the two tests that are broken on purpose, and no other |
