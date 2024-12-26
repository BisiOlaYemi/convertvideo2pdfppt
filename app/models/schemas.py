from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

class ConversionStatus(BaseModel):
    id: str
    status: str = Field(..., pattern="^(processing|completed|failed)$")  
    output_format: str = Field(..., pattern="^(pdf|ppt)$")  
    created_at: datetime
    completed_at: Optional[datetime] = None
    file_path: Optional[str] = None

    @validator('output_format')
    def validate_output_format(cls, v):
        if v not in ['pdf', 'ppt']:
            raise ValueError('Output format must be either pdf or ppt')
        return v

class ConversionRequest(BaseModel):
    output_format: str = Field(..., pattern="^(pdf|ppt)$")