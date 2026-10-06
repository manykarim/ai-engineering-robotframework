### Get Text

#### Arguments

* `selector` (type: `str`)
* `assertion_operator` (type: `AssertionOperator | None`, default: `None`)
* `assertion_expected` (type: `Any | None`, default: `None`)
* `message` (type: `str | None`, default: `None`)
* `text_type` (type: `TextType | None`, default: `None`, named-only)

#### Returns

* `str | list[str] | dict | tuple`

#### Tags

* `Assertion`
* `Getter`
* `PageContent`

#### Documentation

Returns text attribute of the element found by ``selector``.

Keyword can also return the value property text of ``input`` or ``textarea`` elements.
See the `Finding elements` section for details about the selectors.

| =Arguments= | =Description= |
| ``selector`` | Selector from which the text is to be retrieved. See the `Finding elements` section for details about the selectors. |
| ``assertion_operator`` | See `Assertions` for further details. Defaults to None. |
| ``assertion_expected`` | Expected value for the state |
| ``message`` | overrides the default error message for assertion. |
| ``text_type`` | How text is returned. Possible values are ``allInnerTexts``, ``allTextContents``, ``innerText``, ``inputValue``, and ``innerHTML``. Defaults to ``None``, which returns the value of ``input`` and ``textarea`` elements and the inner text of all other elements. |

Keyword uses strict mode, see `Finding elements` for more details about strict mode.
The ``text_type`` argument determines how text is returned. The ``allInnerTexts`` and
``allTextContents`` will return a list of strings, while other types return a single
string.

Optionally asserts that the text matches the specified assertion. See `Assertions`
for further details for the assertion arguments. By default, assertion is not done.

Example:
| ${text} =    `Get Text`    id=important                                # Returns element text without assertion.
| ${text} =    `Get Text`    id=important    ==    Important text        # Returns element text with assertion.
| ${text} =    `Get Text`    //input         ==    root                  # Returns input element text with assertion.
| ${text} =    `Get Text`    id=important    text_type=innerHTML         # Returns element inner HTML.
| ${text} =    `Get Text`    id=important    text_type=allInnerTexts     # Returns element inner text as list of strings.

[https://forum.robotframework.org/t//4285|Comment >>]

