## Purpose

Describes signing in and out as a returning customer experiences it: the sign-in dialog, the demo accounts, the account dropdown with its order documents, and how the signed-in state behaves across pages.

## ADDED Requirements

### Requirement: Log in button in the header (WEB-007_AC-1)
On any page of the shop, a visitor who is not signed in SHALL see a "Log in" button in the header.

#### Scenario: Signed-out header
- **WHEN** a signed-out visitor opens `/`, `/products` or `/cart`
- **THEN** a "Log in" button is visible in the header

### Requirement: Sign-in dialog opens (WEB-007_AC-2)
When a visitor who is not signed in clicks the "Log in" button, a sign-in dialog SHALL open that overlays the page content, with the background dimmed or visually de-emphasised.

#### Scenario: Opening the dialog
- **WHEN** a signed-out visitor clicks "Log in"
- **THEN** a dialog opens over the page and the content behind it is dimmed

### Requirement: The dialog contains the sign-in form (WEB-007_AC-3)
The open sign-in dialog SHALL contain an email input, a password input, a submit button and a close button that dismisses the dialog.

#### Scenario: Dialog contents
- **WHEN** the sign-in dialog is open
- **THEN** it offers an email field, a password field, a submit button and a close button

### Requirement: Successful sign-in (WEB-007_AC-4)
When a visitor submits valid credentials in the sign-in dialog, the dialog SHALL close and the "Log in" button SHALL be replaced by an account dropdown or indicator showing the signed-in user's name. The shop's demo accounts are:

| User | Email | Password |
|---|---|---|
| Jamie | `jamie@flowlinesupply.com` | `demo123` |
| Alex | `alex.productlead@example.com` | `flowline` |

#### Scenario: Jamie signs in
- **WHEN** a visitor signs in as `jamie@flowlinesupply.com` with `demo123`
- **THEN** the dialog closes and the header shows an account dropdown with Jamie's name instead of "Log in"

#### Scenario: Alex signs in
- **WHEN** a visitor signs in as `alex.productlead@example.com` with `flowline`
- **THEN** the dialog closes and the header shows an account dropdown with Alex's name

### Requirement: Account dropdown contents (WEB-007_AC-5)
When a signed-in user opens the account dropdown, it SHALL display the user's name and a saved addresses section, a payment methods section and a recent orders section, and the order entries SHALL include links to invoice and summary PDF documents.

#### Scenario: Opening the dropdown
- **WHEN** a signed-in user opens the account dropdown
- **THEN** it shows the user's name and the saved addresses, payment methods and recent orders sections, with document links on the order entries

### Requirement: Order documents in the dropdown (WEB-007_AC-6)
For a signed-in user with past orders, every entry in the dropdown's recent orders SHALL link to a downloadable invoice PDF and a downloadable order summary PDF.

#### Scenario: Past orders
- **WHEN** a signed-in user with past orders views the recent orders in the dropdown
- **THEN** each order entry links to an invoice PDF and an order summary PDF

### Requirement: Log out (WEB-007_AC-7)
When a signed-in user clicks the "Log out" button in the account dropdown, the user's session SHALL be cleared, the account dropdown SHALL be replaced by the "Log in" button, and the user SHALL be back in the signed-out state.

#### Scenario: Signing out
- **WHEN** a signed-in user clicks "Log out" in the account dropdown
- **THEN** the header shows "Log in" again and the user is signed out

### Requirement: Invalid credentials (WEB-007_AC-8)
When a visitor submits invalid credentials - a wrong email or a wrong password - an error alert SHALL be displayed within the dialog, indicating invalid credentials, and the dialog SHALL remain open for another attempt.

#### Scenario: Wrong password
- **WHEN** a visitor submits `jamie@flowlinesupply.com` with `wrongpass`
- **THEN** an error alert inside the still-open dialog reports invalid credentials

#### Scenario: Unknown user
- **WHEN** a visitor submits `nobody@example.com` with `anypass`
- **THEN** an error alert inside the still-open dialog reports invalid credentials

### Requirement: Close the dialog (WEB-007_AC-9)
When the visitor clicks the dialog's close button, the dialog SHALL close, the visitor SHALL remain on the current page, and no sign-in attempt SHALL be made.

#### Scenario: Closing without signing in
- **WHEN** a visitor opens the sign-in dialog on `/products` and clicks its close button
- **THEN** the dialog is gone, the visitor is still on `/products`, and no sign-in request was sent

### Requirement: Signed-in state persists across pages (WEB-007_AC-10)
After a successful sign-in, the user SHALL remain signed in while navigating between the shop's pages, with the account dropdown staying visible and the session maintained.

#### Scenario: Navigating while signed in
- **WHEN** a user signs in on `/` and then opens `/products` and `/cart`
- **THEN** the account dropdown is shown on every page
