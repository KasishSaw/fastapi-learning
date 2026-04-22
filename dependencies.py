from fastapi import HTTPException, status, Depends

# ─── Level 1 — Token Verification ────────────────────────
def verify_token(token: str):
    if token != "secret123":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return token

# ─── Level 2 — Get Current User (depends on verify_token)
def get_current_user(token: str = Depends(verify_token)):
    # in real app → look up user from DB using token
    user = {"id": 1, "name": "Kasish", "role": "admin"}
    return user

# ─── Level 3 — Admin Only (depends on get_current_user)
def get_admin_user(user: dict = Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins only!"
        )
    return user

# ─── Pagination ───────────────────────────────────────────
def get_pagination(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}