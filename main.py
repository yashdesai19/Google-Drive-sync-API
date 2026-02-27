from fastapi import FastAPI
from routers import auth, drive   # 👈 import drive also
from fastapi.openapi.utils import get_openapi

# app = FastAPI(title="Google Drive Sync API")
app = FastAPI(
    title="Google Drive Sync API",
    swagger_ui_oauth2_redirect_url="/docs/oauth2-redirect",
    swagger_ui_init_oauth={
        "clientId": "YOUR_CLIENT_ID.apps.googleusercontent.com",
        "usePkceWithAuthorizationCodeGrant": True,
    },
)

@app.get("/")
def home():
    return {"message": "Drive Sync API Running"}

# Register Auth Router
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# ✅ Register Drive Router
app.include_router(drive.router, prefix="/drive", tags=["Drive"])




