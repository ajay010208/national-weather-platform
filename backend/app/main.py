from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger
import os

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    os.makedirs("data", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    os.makedirs("models", exist_ok=True)
    logger.info(f"Starting {settings.APP_NAME} in {settings.APP_ENV} mode")
    yield
    logger.info("Shutting down...")

app = FastAPI(
    title=settings.APP_NAME,
    description="National Weather Big Data Analytics Platform – SIH 2026 Problem 69 MVP",
    version="1.0.0-mvp",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS + ["*"] if settings.DEBUG else settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix=settings.API_PREFIX)

@app.get("/")
async def root():
    return {
        "message": "National Weather Analytics Platform API",
        "version": "1.0.0-mvp",
        "docs": "/docs",
        "health": f"{settings.API_PREFIX}/health"
    }
