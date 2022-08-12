"""Base Provider"""

from abc import ABC
from typing import Optional

from git_plan.exceptions import ConfigurationError
from git_plan.model.plan import Plan, PlanId


class Provider(ABC):
    """Base class for plan providers"""

    def __init__(self, label: str):
        self._label = label

    def from_id(self, id_: str) -> Plan:
        """Create a new plan from the contents of the issue with a given ID"""
        raise NotImplementedError()

    def generate_id(self, latest_plan: Optional[Plan] = None) -> PlanId:
        """Generate a new ID"""
        if latest_plan and self._label != latest_plan.id.label:
            msg = f"Configured label '{self._label}' does not match plan's label: {latest_plan.id.label}"
            raise ConfigurationError(msg)

        number = (latest_plan.id.number + 1) if latest_plan else 1

        return PlanId(self._label, number)
