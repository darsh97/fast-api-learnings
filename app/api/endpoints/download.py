from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter()


@router.get("download/{request_id}")
def download(request_id: str):
    # get the file from local
    # send streaming response back
    pass

