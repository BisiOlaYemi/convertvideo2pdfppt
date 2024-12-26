from fastapi import APIRouter, UploadFile, File, HTTPException
from ..models.schemas import ConversionStatus
from ..database.mongodb import conversions
from ..services.video_service import extract_frames
from ..services.converter_service import create_pdf, create_ppt
from ..config import settings
from datetime import datetime
import os
import asyncio
from bson import ObjectId

router = APIRouter()

@router.post("/convert/", response_model=ConversionStatus)
async def convert_video(
    file: UploadFile = File(...),
    output_format: str = "pdf"
):
    if output_format not in ["pdf", "ppt"]:
        raise HTTPException(400, "Output format must be 'pdf' or 'ppt'")
    
    os.makedirs(settings.TEMP_DIR, exist_ok=True)
    os.makedirs(settings.FRAMES_DIR, exist_ok=True)
    
    video_path = os.path.join(settings.TEMP_DIR, file.filename)
    with open(video_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    conversion_id = ObjectId()
    conversion = {
        "_id": conversion_id,
        "status": "processing",
        "output_format": output_format,
        "created_at": datetime.utcnow(),
        "completed_at": None,
        "file_path": None
    }
    await conversions.insert_one(conversion)
    
    asyncio.create_task(process_video(
        conversion_id,
        video_path,
        output_format
    ))
    
    return ConversionStatus(
        id=str(conversion_id),
        status="processing",
        output_format=output_format,
        created_at=conversion["created_at"]
    )

async def process_video(
    conversion_id: ObjectId,
    video_path: str,
    output_format: str
):
    try:
        frames = await extract_frames(video_path)
        
        output_filename = f"output.{output_format}"
        output_path = os.path.join(settings.TEMP_DIR, output_filename)
        
        if output_format == "pdf":
            await create_pdf(frames, output_path)
        else:
            await create_ppt(frames, output_path)
        
        await conversions.update_one(
            {"_id": conversion_id},
            {
                "$set": {
                    "status": "completed",
                    "completed_at": datetime.utcnow(),
                    "file_path": output_path
                }
            }
        )
        
        for frame in frames:
            os.remove(frame)
        
    except Exception as e:
        await conversions.update_one(
            {"_id": conversion_id},
            {
                "$set": {
                    "status": "failed",
                    "completed_at": datetime.utcnow(),
                    "error": str(e)
                }
            }
        )

@router.get("/status/{conversion_id}", response_model=ConversionStatus)
async def get_conversion_status(conversion_id: str):
    conversion = await conversions.find_one({"_id": ObjectId(conversion_id)})
    if not conversion:
        raise HTTPException(404, "Conversion not found")
    
    return ConversionStatus(
        id=str(conversion["_id"]),
        status=conversion["status"],
        output_format=conversion["output_format"],
        created_at=conversion["created_at"],
        completed_at=conversion.get("completed_at"),
        file_path=conversion.get("file_path")
    )