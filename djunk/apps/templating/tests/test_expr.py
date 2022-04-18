import pytest

from django.utils.html import strip_tags
from django.template import loader

from djunk.apps.templating.utils import evaluate_template


@pytest.mark.parametrize(
    "context_data,expected_result",
    [
        ({"not_item": {}}, False),
        ({"item": None}, False),
        ({"item": {"name": "thing"}}, False),
        ({"item": {"amount": 1}}, False),
        ({"item": {"amount": 2, "name": "thing"}}, False),
        ({"item": {"amount": 2, "name": "something"}}, False),
        ({"item": {"amount": 1, "name": "something_else"}}, False),
        ({"item": {"amount": 2, "name": "something_else", "other_data": 1}}, True),
    ],
)
def test_evaluate_misc_example(context_data, expected_result):
    result = evaluate_template("templating/misc.html", context_data)
    assert result == expected_result


@pytest.mark.parametrize(
    "eligible_for_points,total,membership_type,membership_points,expected",
    [
        (
            True,
            100,
            "gold",
            100,
            "ProductTotalPromosPointsP112YesP2YesP334NoShippingEstimate:",
        ),
        (
            True,
            10,
            "silver",
            0,
            "ProductTotalPromosP112P2P334ShippingEstimate:",
        ),
        (
            False,
            100,
            "bronze",
            99,
            "ProductTotalP1P2P3Signuptoday!ShippingEstimate:",
        ),
        (
            True,
            100,
            "bronze",
            0,
            "ProductTotalP1P2P3Signuptoday!ShippingEstimate:",
        ),
    ],
)
def test_render_template_to_string(
    order_factory,
    eligible_for_points,
    total,
    membership_type,
    membership_points,
    expected,
):
    context = order_factory(
        eligible_for_points, total, membership_type, membership_points
    )
    result = loader.render_to_string("templating/cart.html", context)
    s = "".join(strip_tags(result).splitlines()).replace(" ", "")
    assert s == expected
