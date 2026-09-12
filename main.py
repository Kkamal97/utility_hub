import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

# Import routers from the package
from routers import excel_router, image_router, pdf_router

app = FastAPI(title="Production Utility Suite")

# Path resolving for production server compatibility
BASE_DIR = Path(__file__).resolve().parent

# CORS setup for frontend-backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Register API Endpoints
app.include_router(excel_router, prefix="/api/excel", tags=["Excel Tools"])
app.include_router(image_router, prefix="/api/image", tags=["Image Tools"])
app.include_router(pdf_router, prefix="/api/pdf", tags=["PDF Tools"])

# 2. Mount Static Files & Frontend Modules
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.mount("/pages", StaticFiles(directory=BASE_DIR / "pages"), name="pages")

# 3. Serving HTML Page Routes
@app.get("/", response_class=FileResponse)
async def serve_home():
    return FileResponse(BASE_DIR / "pages" / "index.html")

@app.get("/excel", response_class=FileResponse)
async def serve_excel_page():
    return FileResponse(BASE_DIR / "pages" / "excel" / "index.html")

@app.get("/image", response_class=FileResponse)
async def serve_image_page():
    return FileResponse(BASE_DIR / "pages" / "image" / "index.html")

@app.get("/pdf", response_class=FileResponse)
async def serve_pdf_page():
    return FileResponse(BASE_DIR / "pages" / "pdf" / "index.html")

# Health check route required by cloud providers
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    # Read environment PORT provided by cloud environments (defaults to 8000 for local dev)
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)