from fastapi import Depends, HTTPException, status

from app.core.oauth2 import get_current_user


def admin_required(current_user=Depends(get_current_user)):

    if current_user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user


def support_agent_required(current_user=Depends(get_current_user)):

    if current_user.role != "Support Agent":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Support Agent access required"
        )

    return current_user


def customer_required(current_user=Depends(get_current_user)):

    if current_user.role != "Customer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Customer access required"
        )

    return current_user