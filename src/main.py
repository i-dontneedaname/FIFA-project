from fastapi import FastAPI

from src.auth.schemas import UserRead, UserCreate, UserUpdate
from src.auth.base_config import fastapi_users, auth_backend
from src.auth.routers import router as router_users
from src.players.routers import router as router_players
from src.matches.routers import router as router_matches

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

# app.include_router(
#     fastapi_users.get_users_router(UserRead, UserUpdate),
#     prefix="/users",
#     tags=["users"],
# )

app.include_router(router_users)
app.include_router(router_players)
app.include_router(router_matches)
