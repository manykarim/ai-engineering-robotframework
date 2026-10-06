"""Assertion support shared by the ``Get`` keywords."""

from assertionengine import AssertionOperator

NUMBER_OPERATORS = frozenset(
    AssertionOperator[name] for name in ("==", "!=", "<", "<=", ">", ">=", "validate", "then")
)


def check_operator(operator: AssertionOperator | None) -> None:
    """Rejects the operators that AssertionEngine's ``int_str`` and ``float_str`` helpers do not allow.

    The helpers reject them only once the value has been fetched. Checking first keeps a keyword from contacting the
    shop for an assertion that cannot run. The message is the helpers' own.
    """
    if operator is not None and operator not in NUMBER_OPERATORS:
        raise ValueError(f"Operator '{operator.name}' is not allowed.")
