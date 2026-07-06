from fastapi import Depends, HTTPException, status

from app.core.oauth2 import get_current_user


class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user=Depends(get_current_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action."
            )

        return current_user


# Predefined Role Dependencies
admin_only = RoleChecker(["Admin"])

support_agent_only = RoleChecker(["Support Agent"])

customer_only = RoleChecker(["Customer"])

admin_or_support = RoleChecker([
    "Admin",
    "Support Agent"
])

admin_or_customer = RoleChecker([
    "Admin",
    "Customer"
])

all_roles = RoleChecker([
    "Admin",
    "Support Agent",
    "Customer"
])