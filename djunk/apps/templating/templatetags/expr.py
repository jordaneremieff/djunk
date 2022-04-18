from typing import Optional, cast

from django.template import (
    Library,
    Context,
    NodeList,
    Node,
    VariableDoesNotExist,
    TemplateSyntaxError,
)
from django.template.base import Parser, Token
from django.template.defaulttags import TemplateIfParser

from djunk.apps.templating.types import InfixTemplateLiteral


register = Library()


class ExpressionNode(Node):
    """A template node returned by the `{% expr %}` tag to evaluate expressions and
    optionally store the result.

    This is based on the `django.template.defaulttags.IfNode` class, but stripped down
    to handle only a single condition and nodelist and support variable assignments.

    Essentially `{% expr condition %}` is a shortcut for `{% if condition %}{% endif %}`
    that also supports assignments.
    """

    def __init__(
        self,
        condition: InfixTemplateLiteral,
        nodelist: NodeList,
        name: Optional[str] = None,
    ) -> None:
        self.condition = condition
        self.nodelist = nodelist
        self.name = name
        self.result: Optional[bool] = None

    def render(self, context: Context, eval_only: bool = False) -> str:
        try:
            result = self.condition.eval(context)
        except VariableDoesNotExist:
            pass
        else:
            self.result = bool(result)

        # Update the context with the expression result for variable assignments.
        if self.name:
            context[self.name] = self.result

        # Either the variable is missing or only the evaluation result is required, so
        # return an empty string without rendering.
        if eval_only or self.result is None:
            return ""

        return self.nodelist.render(context)


@register.tag()
def expr(parser: Parser, token: Token) -> ExpressionNode:
    """Evaluate an expression and optionally store the result. This will support any
    condition that is valid for use with the builtin `{% if %}` tag.

    Usage:
        {% expr condition %}
        {% expr condition as name %}
    """
    args = token.split_contents()[1:]

    # Extract the variable name for assignment expressions.
    try:
        idx = args.index("as")
        name = args[idx + 1]
    except KeyError:
        raise TemplateSyntaxError("Variable name must follow `as` operator.")
    except ValueError:
        name = None
    else:
        del args[idx:]

    condition = TemplateIfParser(parser, args).parse()
    nodelist = parser.parse()

    return ExpressionNode(cast(InfixTemplateLiteral, condition), nodelist, name=name)
