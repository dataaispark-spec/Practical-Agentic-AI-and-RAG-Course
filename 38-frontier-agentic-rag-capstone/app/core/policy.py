"""Small deterministic policy engine used before tool execution."""

from dataclasses import dataclass

from .contracts import ActionClass, ActionRequest, TaskContract


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    approval_required: bool
    reason: str


class PolicyEngine:
    """Enforce task scope before an agent can cause side effects."""

    def evaluate(self, task: TaskContract, action: ActionRequest) -> PolicyDecision:
        if action.task_id != task.task_id:
            return PolicyDecision(False, False, "action belongs to a different task")

        if task.allowed_systems and action.tool not in task.allowed_systems:
            return PolicyDecision(False, False, "tool is outside the task allowlist")

        if action.action_class in task.required_approvals:
            return PolicyDecision(True, True, "explicit approval is required")

        if action.action_class in {
            ActionClass.FINANCIAL,
            ActionClass.DESTRUCTIVE,
        }:
            return PolicyDecision(True, True, "high-impact action requires approval")

        return PolicyDecision(True, False, "action is within task policy")
