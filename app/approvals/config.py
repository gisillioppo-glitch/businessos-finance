from types import MappingProxyType


BUSINESSOS_APPROVAL_CONFIG = MappingProxyType({
    "branch_id": "businessos",
    "statuses": frozenset({"pending", "approved", "rejected", "cancelled"}),
    "priorities": frozenset({"low", "medium", "high", "critical"}),
    "active_statuses": frozenset({"pending"}),
    "protected_source_modules": frozenset({"pilot_expansion"}),
    "approval_types": frozenset(
        {"decision", "access", "budget", "policy", "incident"}
    ),
})


def get_approval_config():
    return BUSINESSOS_APPROVAL_CONFIG


def get_valid_approval_types():
    return get_approval_config()["approval_types"]


def get_valid_priorities():
    return get_approval_config()["priorities"]


def get_active_statuses():
    return get_approval_config()["active_statuses"]


def get_valid_approval_statuses():
    return get_approval_config()["statuses"]


def get_demo_protected_source_modules():
    return get_approval_config()["protected_source_modules"]
