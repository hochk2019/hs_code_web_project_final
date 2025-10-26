"""Khai báo router chính cho API."""

from fastapi import APIRouter

from . import v1

api_router = APIRouter()
api_router.include_router(v1.router, prefix="/api/v1")
