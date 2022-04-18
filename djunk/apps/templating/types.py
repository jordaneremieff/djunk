from typing import Protocol

from django.template import Context


class InfixTemplateLiteral(Protocol):
    """Refers to `django.template.smartif.infix` which creates an `Operator` instance
    to evaluate the condition in an expression.
    """

    def eval(self, context: Context) -> bool:
        ...
