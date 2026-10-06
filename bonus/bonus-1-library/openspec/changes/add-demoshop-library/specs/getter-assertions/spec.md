# Spec Delta

## Purpose

Defines the assertion contract shared by every `Get` keyword of the DemoShop library. With it, a value can be
fetched and checked in one step, the way Browser's `Get Text` and `Get Element Count` do, for example
`Get Product Price    1    ==    249.99`.

## ADDED Requirements

### Requirement: Assertion arguments
Every `Get` keyword SHALL accept three optional arguments, `assertion_operator`, `assertion_expected` and `message`, in
that order, after its own arguments. They SHALL be usable both positionally and by name.

#### Scenario: Positional assertion
- **WHEN** a test runs `Get Product Price    1    ==    249.99`
- **THEN** the keyword checks that product 1's price equals 249.99

#### Scenario: Named assertion
- **WHEN** a test runs `Get Cart Total    assertion_operator=>=    assertion_expected=0`
- **THEN** the keyword checks that the cart total is at least 0

### Requirement: Value returned without assertion
When `assertion_operator` is not given, a `Get` keyword SHALL return its value without checking it. Counts SHALL be
returned as integers and amounts of money as floating-point numbers.

#### Scenario: No operator
- **WHEN** a test runs `${count} =    Get Product Count`
- **THEN** `${count}` holds the product count as an integer, and the keyword does not fail

### Requirement: Numeric comparison
A `Get` keyword SHALL support the operators `==`, `!=`, `<`, `<=`, `>` and `>=`, together with their alternative names
(`equal`, `equals`, `should be`, `inequal`, `should not be`, `less than`, `greater than`). Before it compares, it SHALL
convert `assertion_expected` to the type of the value it returns, so that a number written in Robot data compares as a
number rather than as text. When the assertion passes, the keyword SHALL return the value.

#### Scenario: Text-written price compares as number
- **WHEN** a test runs `Get Product Price    1    ==    249.99`, and product 1 costs 249.99
- **THEN** the keyword passes and returns `249.99` as a float

#### Scenario: Whole-number expectation for a price
- **WHEN** a test runs `Get Product Price    5    ==    799`, and product 5 costs 799.0
- **THEN** the keyword passes

#### Scenario: Alternative operator name
- **WHEN** a test runs `Get Product Count    greater than    0`
- **THEN** the keyword passes while the catalogue is not empty

### Requirement: Assertion failure message
When an assertion fails, the keyword SHALL fail with a message of the form
`<subject> '<value>' (<value type>) <relation> '<expected>' (<expected type>)`. Here `<subject>` names what was
checked: `Product count`, `Product <id> price`, `Cart item count` or `Cart total`.

#### Scenario: Price mismatch
- **WHEN** a test runs `Get Product Price    1    ==    10`, and product 1 costs 249.99
- **THEN** the keyword fails with `Product 1 price '249.99' (float) should be '10.0' (float)`

#### Scenario: Count mismatch
- **WHEN** a test runs `Get Cart Item Count    >    0` on an empty cart
- **THEN** the keyword fails with `Cart item count '0' (int) should be greater than '0' (int)`

### Requirement: Custom failure message
When `message` is given, a failing assertion SHALL use it in place of the default message. The placeholders
`{value}`, `{value_type}`, `{expected}` and `{expected_type}` in `message` SHALL be replaced with the actual and
expected values and their types.

#### Scenario: Custom message with placeholders
- **WHEN** a test runs `Get Cart Total    ==    5    message=Total was {value}, wanted {expected}` on an empty cart
- **THEN** the keyword fails with `Total was 0.0, wanted 5.0`

### Requirement: Expression operators
A `Get` keyword SHALL support `validate`, which evaluates `assertion_expected` as a Python expression in which `value`
is the returned value and fails if the result is false. It SHALL also support `evaluate`, also written `then`, which
returns the result of evaluating `assertion_expected` with `value` in place of the value itself.

#### Scenario: Validate passes
- **WHEN** a test runs `Get Product Price    1    validate    100 < value < 300`, and product 1 costs 249.99
- **THEN** the keyword passes

#### Scenario: Validate fails
- **WHEN** a test runs `Get Product Price    1    validate    value < 100`, and product 1 costs 249.99
- **THEN** the keyword fails, and the message contains `should validate to true with`

#### Scenario: Evaluate returns transformed value
- **WHEN** a test runs `${double} =    Get Product Price    1    then    value * 2`, and product 1 costs 249.99
- **THEN** `${double}` is `499.98`

### Requirement: Text operators rejected
Because every `Get` keyword in this library returns a number, the keywords SHALL reject the text operators `*=` /
`contains`, `not contains`, `^=` / `starts` / `should start with`, `$=` / `ends` / `should end with` and `matches`.
They SHALL fail with an error that names the operator as not allowed.

#### Scenario: Contains on a price
- **WHEN** a test runs `Get Product Price    1    contains    249`
- **THEN** the keyword fails with an error stating that the operator `contains` is not allowed

### Requirement: Unknown operator rejected
An `assertion_operator` that is not a supported operator name SHALL fail the keyword before the shop is contacted.

#### Scenario: Misspelled operator
- **WHEN** a test runs `Get Product Count    ===    12`
- **THEN** the keyword fails with an argument conversion error for `assertion_operator`, and no request is sent
