# routers/__init__.py

from .excel_router import router as excel_router
from .image_router import router as image_router
from .pdf_router import router as pdf_router

__all__ = ["excel_router", "image_router", "pdf_router"]