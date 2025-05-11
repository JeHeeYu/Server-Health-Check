import os
import threading
import paramiko
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.background import BackgroundTask
import uvicorn

from config import (
    DEVICE_ID,
    DEVICE_PASSWORD,
    CONFIG_FILENAME,
    DSMC_BASE_PATH,
    DSMC_BASE_PORT,
    DSSNR_BASE_PATH,
    DSSNR_BASE_PORT,
    FEED_BASE_PATH,
    FEED_BASE_PORT,
)


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

        @self.app.post("/download/config")
        def fetch_config(req: ProcessRequest):
            process_name = req.process_name.upper()

            if "DSMC" in process_name:
                base_path = DSMC_BASE_PATH
                base_port = int(DSMC_BASE_PORT)
            elif "DSSNR" in process_name:
                base_path = DSSNR_BASE_PATH
                base_port = int(DSSNR_BASE_PORT)
            elif "FEED" in process_name:
                base_path = FEED_BASE_PATH
                base_port = int(FEED_BASE_PORT)
            else:
                raise HTTPException(status_code=400, detail="지원하지 않는 프로세스 유형입니다.")

            try:
                index = int(process_name.split("-")[-1])
            except ValueError:
                raise HTTPException(status_code=400, detail="프로세스 번호 파싱 실패")

            port = base_port + index
            remote_path = f"{base_path}/{CONFIG_FILENAME}"
            filename = f"{process_name}_config.js"
            local_path = os.path.join(os.getcwd(), filename)

            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(req.ip, port=port, username=DEVICE_ID, password=DEVICE_PASSWORD)

                sftp = ssh.open_sftp()
                sftp.get(remote_path, local_path)
                sftp.close()
                ssh.close()

            except Exception as e:
                raise HTTPException(status_code=500, detail=f"SFTP 에러: {str(e)}")

            if not os.path.isfile(local_path):
                raise HTTPException(status_code=404, detail="파일 저장 실패")

            return FileResponse(
                local_path,
                media_type="application/octet-stream",
                filename=filename,
                background=BackgroundTask(lambda: os.remove(local_path))
            )

    def run(self):
        threading.Thread(
            target=lambda: uvicorn.run(self.app, host="0.0.0.0", port=14303, log_level="info"),
            daemon=True
        ).start()


def start_file_server():
    FileManager().run()
