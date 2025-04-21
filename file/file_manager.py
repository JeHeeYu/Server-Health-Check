import os
import threading
import paramiko
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn


class ProcessRequest(BaseModel):
    process_name: str
    ip: str

class FileManager:
    def __init__(self):
        self.app = FastAPI()
        self._setup_middleware()
        self._register_routes()

    def _setup_middleware(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _register_routes(self):
        @self.app.get("/download")
        async def download_file(
            path: str = Query(..., description="전체 파일 경로"),
            filename: str = Query(None, description="저장될 파일 이름 (선택)"),
        ):
            if not os.path.exists(path):
                raise HTTPException(status_code=404, detail="파일 경로가 존재하지 않습니다.")
            if not os.path.isfile(path):
                raise HTTPException(status_code=400, detail="유효한 파일이 아닙니다.")

            final_name = filename or os.path.basename(path)

            return FileResponse(
                path,
                media_type="application/octet-stream",
                filename=final_name,
            )

    def run(self):
        threading.Thread(
            target=lambda: uvicorn.run(self.app, host="0.0.0.0", port=14303, log_level="info"),
            daemon=True
        ).start()


def start_file_server():
    FileManager().run()
