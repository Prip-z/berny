import asyncio
from contextlib import asynccontextmanager

from app.channels.api.router import channel_router
from app.identify.api.routers import identify_router
from app.identify.domain.exception import (
    InvalidToken,
    TokenExpired,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.messaging.api.dependencies import connection_manager, message_broker, scylla_db
from app.messaging.api.http import message_router
from app.messaging.api.websocket import router as websocket_router
from app.shared.exception import AccessDenied
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    scylla_db.connect()
    broker_task = asyncio.create_task(
        message_broker.subscribe("chat_events", connection_manager.handle_broker_message)
    )

    yield

    broker_task.cancel()
    try:
        await broker_task
    except asyncio.CancelledError:
        pass

    scylla_db.close()


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(websocket_router)
app.include_router(identify_router)
app.include_router(channel_router)
app.include_router(message_router)


@app.exception_handler(UserAlreadyExistsError)
async def user_already_exists_handler(request: Request, exc: UserAlreadyExistsError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(InvalidToken)
async def invalid_tokenr(request: Request, exc: InvalidToken):
    return JSONResponse(status_code=401, content={"detail": str(exc)})


@app.exception_handler(TokenExpired)
async def token_expired(request: Request, exc: TokenExpired):
    return JSONResponse(status_code=401, content={"detail": str(exc)})


@app.exception_handler(AccessDenied)
async def access_denied(request: Request, exc: AccessDenied):
    return JSONResponse(status_code=403, content={"detail": str(exc)})
