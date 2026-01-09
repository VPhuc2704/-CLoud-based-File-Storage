from typing import List
from ninja import Router

from ..security import AuthBearer

from ..schemas.auth_schemas import MessageResponse
from ..schemas.files_schemas import (
    UploadInitIn,
    UploadInitOut,
    UploadCompleteIn,
    RenameIn,
    FileOut,
    PresignedUrl
)
from ..services.files_service import FilesService

router = Router(tags=["Files"])




@router.post("/upload/init", auth=AuthBearer(), response=UploadInitOut)
def upload_files(request, payload: UploadInitIn):
    account = request.auth
    
    file, upload_url = FilesService.init_upload(
        owner=account,
        data=payload
    )
    
    return {
        "file_id": file.id,
        "upload_url": upload_url,
    }


@router.post("/upload-complete",  auth=AuthBearer(), response=MessageResponse)
def upload_complete(request, payload: UploadCompleteIn):
    account = request.auth
    
    FilesService.upload_complete(owner=account, data=payload)

    return {"success": True, "message": "Upload thành công"}


@router.patch("/rename/{file_id}",  auth=AuthBearer(), response=FileOut)
def rename(request, file_id: str, payload: RenameIn):
    account = request.auth
    file = FilesService.rename(
        owner=account,
        file_id=file_id,
        data=payload
    )

    return file


@router.get("/list",auth=AuthBearer(), response=List[FileOut])
def list_files(request):
    account = request.auth

    files = FilesService.list_files(owner=account)
        
    return  [
        {
            "id": str(f.id),
            "file_name": f.file_name,
            "mime_type": f.mime_type,
            "file_size": f.file_size,
            "created_at": f.created_at,
            "updated_at": f.updated_at
        }
        for f in files
    ]

@router.get("/view/{file_id}", auth=AuthBearer(), response=PresignedUrl)
def download(request, file_id: str):
    account = request.auth
    
    url = FilesService.view_file(owner=account, file_id=file_id)
    
    return {
        "presigned_url": url
    } 

@router.get("/download/{file_id}", auth=AuthBearer(), response=PresignedUrl)
def download(request, file_id: str):
    account = request.auth
    
    url = FilesService.download_file(owner=account, file_id=file_id)
    
    return {
        "presigned_url": url
    } 


@router.get("/trash", auth=AuthBearer(), response=List[FileOut])
def list_trash(request):
    account = request.auth
    
    files = FilesService.list_trashed_files(owner=account)
    
    return  [
        {
            "id": str(f.id),
            "file_name": f.file_name,
            "mime_type": f.mime_type,
            "file_size": f.file_size,
            "created_at": f.created_at,
            "updated_at": f.updated_at,
        }
        for f in files
    ]

@router.delete("/{file_id}", auth=AuthBearer(), response=MessageResponse)
def soft_delete_file(request, file_id: str):
    account = request.auth
    
    FilesService.soft_delete_file(owner=account, file_id=file_id)
    
    return {
        "success": True,
        "message": "Đã đưa vào thùng rác"
    }

@router.patch("/restore/{file_id}", auth=AuthBearer(), response=MessageResponse)
def restore_file(request, file_id: str):
    account = request.auth
    
    FilesService.restore_temporary_file(owner=account, file_id=file_id)

    return {
        "success": True,
        "message": "Đã Khôi phục thành công"
    }


@router.delete("/permanent/{file_id}", auth=AuthBearer(), response=MessageResponse)
def hard_delete_file(request, file_id: str):
    account = request.auth
    
    FilesService.hard_delete_file(owner=account, file_id=file_id)
    
    return {
        "success": True,
        "message": "Đã xóa thành công"
    }


