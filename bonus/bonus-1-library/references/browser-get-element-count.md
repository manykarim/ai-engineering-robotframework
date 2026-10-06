### Get Element Count

#### Arguments

* `selector` (type: `str`)
* `assertion_operator` (type: `AssertionOperator | None`, default: `None`)
* `assertion_expected` (type: `int | str`, default: `0`)
* `message` (type: `str | None`, default: `None`)

#### Returns

* `int`

#### Tags

* `Assertion`
* `Getter`
* `PageContent`

#### Documentation

Returns the count of elements found with ``selector``.

| =Arguments= | =Description= |
| ``selector`` | Selector which shall be counted. See the `Finding elements` section for details about the selectors. |
| ``assertion_operator`` | See `Assertions` for further details. Defaults to None. |
| ``assertion_expected`` | Expected value for the assertion |
| ``message`` | overrides the default error message for assertion. |

Optionally asserts that the count matches the specified assertion. See
`Assertions` for further details for the assertion arguments. By default assertion
is not done.

Example:
| `Get Element Count`    label    >    1

[https://forum.robotframework.org/t//4270|Comment >>]

