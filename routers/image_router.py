import io
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from PIL import Image

router = APIRouter()

@router.post("/resize")
async def resize_image(
    file: UploadFile = File(...),
    width: int = Form(...),
    height: int = Form(...),
    output_format: str = Form("PNG")
):
    try:
        image_bytes = await file.read()
        img = Image.open(io.BytesIO(image_bytes))
        
        resized_img = img.resize((width, height), Image.Resampling.LANCZOS)
        
        output_stream = io.BytesIO()
        fmt = output_format.upper()
        if fmt == "JPG": 
            fmt = "JPEG"
        if fmt == "JPEG" and resized_img.mode in ("RGBA", "P"):
            resized_img = resized_img.convert("RGB")
            
        resized_img.save(output_stream, format=fmt)
        output_stream.seek(0)
        
        ext = "jpg" if fmt == "JPEG" else "png"
        return StreamingResponse(
            output_stream,
            media_type=f"image/{ext}",
            headers={"Content-Disposition": f'attachment; filename="resized.{ext}"'}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))