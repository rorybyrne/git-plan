import pytest

from git_plan.exceptions import ConfigurationError
from git_plan.model.plan import Plan, PlanId, PlanMessage
from git_plan.service.providers.provider import Provider


def test_provider_should_generate_valid_id():
    provider = Provider("TST")
    id_ = provider.generate_id()

    assert id_.label == "TST"
    assert id_.number == 1

def test_provider_should_increment_from_last_plan():
    provider = Provider("TST")
    plan_id = PlanId("TST", 1)
    plan = Plan(None, plan_id, None, None, None)

    new_id = provider.generate_id(plan)

    assert new_id.label == "TST"
    assert new_id.number == 2

def test_provider_should_raise_if_labels_dont_match():
    provider = Provider("FOO")
    plan_id = PlanId("TST", 1)
    plan = Plan(None, plan_id, None, None, None)

    msg = "Configured label 'FOO' does not match plan's label: TST"
    with pytest.raises(ConfigurationError, match=msg):
        provider.generate_id(plan)
