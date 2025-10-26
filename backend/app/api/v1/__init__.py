"""Router phiên bản 1 của API."""

from fastapi import APIRouter

from . import documents, health, sync

router = APIRouter()
router.include_router(health.router, tags=["health"])
router.include_router(documents.router, prefix="/documents", tags=["documents"])
router.include_router(sync.router, prefix="/sync", tags=["sync"])
