# routers/pdf_router.py

import io
import zipfile
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse

router = APIRouter()

@router.post("/convert-page")
async def convert_pdf_page(
    file: UploadFile = File(...),
    page_number: int = Form(1),
    output_format: str = Form("png"),  # "png" or "jpeg"
    dpi: int = Form(150)
):
    """Converts a specific page of a PDF document into an image."""
    try:
        import fitz  # PyMuPDF

        pdf_bytes = await file.read()
        if not pdf_bytes:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        if doc.page_count == 0:
            raise HTTPException(status_code=400, detail="PDF contains no pages.")

        # Ensure page index is within bounds (1-based index from frontend)
        target_page_idx = page_number - 1
        if target_page_idx < 0 or target_page_idx >= doc.page_count:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid page number. Document has {doc.page_count} pages."
            )

        page = doc.load_page(target_page_idx)
        
        # Calculate rendering scale based on requested DPI (default 72 DPI)
        zoom = dpi / 72.0
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)

        fmt = output_format.lower()
        if fmt not in ["png", "jpeg", "jpg"]:
            fmt = "png"
        
        img_format = "jpeg" if fmt in ["jpg", "jpeg"] else "png"
        img_bytes = pix.tobytes(img_format)
        
        output_stream = io.BytesIO(img_bytes)
        output_stream.seek(0)

        media_type = f"image/{img_format}"
        filename = f"page_{page_number}.{img_format}"

        return StreamingResponse(
            output_stream,
            media_type=media_type,
            headers={"Content-Disposition": f'attachment; filename="{filename}"'}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")


@router.post("/convert-all")
async def convert_all_pdf_pages(
    file: UploadFile = File(...),
    output_format: str = Form("png"),
    dpi: int = Form(150)
):
    """Converts all pages of a PDF document into images and returns them in a ZIP archive."""
    try:
        import fitz  # PyMuPDF

        pdf_bytes = await file.read()
        if not pdf_bytes:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        if doc.page_count == 0:
            raise HTTPException(status_code=400, detail="PDF contains no pages.")

        fmt = output_format.lower()
        img_format = "jpeg" if fmt in ["jpg", "jpeg"] else "png"
        zoom = dpi / 72.0
        mat = fitz.Matrix(zoom, zoom)

        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for page_idx in range(doc.page_count):
                page = doc.load_page(page_idx)
                pix = page.get_pixmap(matrix=mat)
                img_bytes = pix.tobytes(img_format)
                
                image_filename = f"page_{page_idx + 1}.{img_format}"
                zip_file.writestr(image_filename, img_bytes)

        zip_buffer.seek(0)

        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={"Content-Disposition": 'attachment; filename="pdf_pages.zip"'}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF zip export: {str(e)}")