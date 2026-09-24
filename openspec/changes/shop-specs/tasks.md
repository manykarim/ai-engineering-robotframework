## 1. Verify the derivation

- [ ] 1.1 Check criterion coverage. List the `### AC-<n>` headings of the seven in-scope stories at demo-webshop tag `v0.3.0` (WEB-002 to WEB-007 and API-005) and the criterion named by each behaviour requirement under `specs/shop/`. Verify: 71 active criteria and 71 requirements; no criterion missing, duplicated or inactive; and none of `WEB-004_AC-4`, `WEB-005_AC-8` or `WEB-006_AC-9` in any behaviour spec (design D1).
- [ ] 1.2 Scan for neutrality. Verify: a case-insensitive search of `specs/shop/` for `BUG_`, `LOCATOR_`, `stage`, `planted`, `drift`, `data-`, `css`, `xpath` and `flag` finds nothing (design D5).
- [ ] 1.3 Check every concrete value used in a scenario against the image built from the tagged commit (`sha-6342d4b`, identical in source to `0.3.0`), run locally. Verify at API level:
  - 12 products, 9 categories and prices from $39.50 to $899.00;
  - product 1 is Aurora Neural Headphones at $249.99, rated 4.8 with 214 reviews;
  - `GET /api/search/?query=headphones` and `?query=aurora` list it, and `?query=xyz123` lists nothing;
  - `/products/9999` and `/products/abc` show the not-found page;
  - a cart API request carrying only a `session_id` cookie is handled in session `workshop-demo`.

  Verify in a browser:
  - searching "headphones", "aurora" and "xyz123" behaves as the search scenarios say;
  - `/products/1` shows "214 reviews" or "(214)";
  - the badge reads 1 after one add, and two adds show $249.99 and $499.98 on `/cart`;
  - "notanemail", "A" and "123" at checkout produce three field errors and keep the shopper on `/checkout`;
  - Alex's name appears after signing in with the Alex credentials.

  A failing instance is corrected in the spec, never explained away.
- [ ] 1.4 Check the interpretation rules against the same image. Verify: a product card's button with visible text "Add to cart" satisfies the quoted "Add to Cart", and its accessible name is more specific. The checkout form's full name field is found by the label "Full name". Its email field is labelled "Email", so no scenario may cite "Email address" as a label.

## 2. Validate and archive

- [ ] 2.1 Confirm the rule reaches agents. Once `workshop-foundation` has added the namespaces and the neutrality rule to `openspec/config.yaml`, verify: `openspec instructions specs --change shop-specs --json` returns both, and `openspec validate shop-specs --strict` passes.
- [ ] 2.2 Archive the change. Verify: `openspec archive shop-specs -y` creates `openspec/specs/shop/{interpretation-rules,catalogue,product-detail,search,cart,checkout,authentication}/spec.md`, each with its Purpose, and 77 requirements in total.
