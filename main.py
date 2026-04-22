from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from routers import users, products
from dependencies import verify_token, get_current_user, get_admin_user, get_pagination


app = FastAPI(
    title="FastAPI Learning Project",
    description="Learning FastAPI from scratch with Kasish",
    version="1.0.0"
)

# ─── Exception Handlers ───────────────────────────────────
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=404,
        content={"status": "error", "code": 404, "message": "Resource not found"}
    )

@app.exception_handler(401)
async def unauthorized_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=401,
        content={"status": "error", "code": 401, "message": "Unauthorized access"}
    )

@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"status": "error", "code": 422, "message": "Validation failed", "details": exc.errors()}
    )

# ─── Routers ──────────────────────────────────────────────
app.include_router(users.router)
app.include_router(products.router)

# ─── Root ─────────────────────────────────────────────────
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/me", tags=["Auth"])
async def get_me(user: dict = Depends(get_current_user)):
    return {"message": f"Hello {user['name']}!", "user": user}

@app.get("/admin", tags=["Auth"])
async def get_admin(user: dict = Depends(get_admin_user)):
    return {"message": f"Welcome admin {user['name']}!"}