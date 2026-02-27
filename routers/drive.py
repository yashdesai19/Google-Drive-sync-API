from fastapi import APIRouter, UploadFile, File
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseUpload
import io

router = APIRouter()

# 🔹 Helper function to create credentials safely
def get_credentials(token: str):
    return Credentials(
        token=token,
        token_uri="https://oauth2.googleapis.com/token"
    )


# List Files
@router.get("/files")
def list_files(token: str):
    credentials = get_credentials(token)
    service = build("drive", "v3", credentials=credentials)

    results = service.files().list(
        pageSize=10,
        fields="files(id, name)"
    ).execute()

    return results.get("files", [])


#  Upload File
@router.post("/upload")
def upload_file(token: str, file: UploadFile = File(...)):
    credentials = get_credentials(token)
    service = build("drive", "v3", credentials=credentials)

    file_stream = io.BytesIO(file.file.read())

    media = MediaIoBaseUpload(
        file_stream,
        mimetype=file.content_type
    )

    file_metadata = {"name": file.filename}

    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()

    return uploaded_file


#  Delete File
@router.delete("/delete/{file_id}")
def delete_file(file_id: str, token: str):
    credentials = get_credentials(token)
    service = build("drive", "v3", credentials=credentials)

    service.files().delete(fileId=file_id).execute()

    return {"message": "File deleted successfully"}


#  Make File Public
@router.post("/make-public/{file_id}")
def make_public(file_id: str, token: str):
    credentials = get_credentials(token)
    service = build("drive", "v3", credentials=credentials)

    permission = {
        "type": "anyone",
        "role": "reader"
    }

    service.permissions().create(
        fileId=file_id,
        body=permission
    ).execute()

    return {"message": "File is now public"}