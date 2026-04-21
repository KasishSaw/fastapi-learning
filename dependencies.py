from fastapi import HTTPException, status, Depends

def verify_token(token: str):
    if token != "secret123":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return token

def verify_role(role: str):
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins only"
        )
    return role

def get_pagination(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}