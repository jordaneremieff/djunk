from typing import Optional

from django.http import HttpRequest
from django.template.context import make_context
from django.template import loader

from djunk.apps.templating.templatetags.expr import ExpressionNode


def evaluate_template(
    template_name: str,
    context: Optional[object] = None,
    request: Optional[HttpRequest] = None,
    using=None,
) -> bool:
    """Load a template and evaluate all of the expressions to return a single boolean
    result.

    This is similar to the `django.template.loader.render_to_string` method except that
    it will only render the individual expression nodes instead of the entire template.
    """
    if isinstance(template_name, (list, tuple)):
        wrapper = loader.select_template(template_name, using=using)
    else:
        wrapper = loader.get_template(template_name, using=using)

    # The evaluation needs to bypass the render behaviour of the template wrapper, so
    # the context creation is done manually.
    context = make_context(
        context, request, autoescape=wrapper.backend.engine.autoescape
    )

    # Expressions are evaluated in order, so the first `False` result will end the
    # evaluation unless it represents a context variable assignment.
    for node in wrapper.template.nodelist.get_nodes_by_type(ExpressionNode):
        node.render(context, eval_only=True)
        if node.result is False and node.name not in context:
            return False

    return True
