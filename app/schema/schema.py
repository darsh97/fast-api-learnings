from pydantic import BaseModel
from enum import Enum


class SpeechRateEnum(str, Enum):
    slow = "Slow"
    medium = "Medium"
    fast = "Fast"
    default = "Default"


class MetadataModel(BaseModel):
    title: str
    speech_rate: SpeechRateEnum


class UploadResponse(BaseModel):
    request_id: str
    file_name: str
    file_type: str

class FileResponse(BaseModel):
    pass