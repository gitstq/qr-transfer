"""
HTTP/WebSocket服务器模块
"""
import os
import asyncio
import shutil
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

from fastapi import FastAPI, File, UploadFile, HTTPException, Query, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from ..utils.network import get_local_ip, find_free_port
from ..utils.security import generate_token, hash_file
from .qr_generator import qr_to_base64


class TransferServer:
    """文件传输服务器"""
    
    def __init__(self, port: Optional[int] = None, upload_dir: str = "./received"):
        self.port = port or find_free_port()
        self.host = "0.0.0.0"
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(exist_ok=True)
        
        self.app = FastAPI(title="QR Transfer", version="1.0.0")
        self.setup_routes()
        self.setup_middleware()
        
        self.active_transfers: Dict[str, Any] = {}
        self.server_task = None
        
    def setup_middleware(self):
        """设置中间件"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def setup_routes(self):
        """设置路由"""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def index():
            """主页 - 上传界面"""
            return self._get_upload_html()
        
        @self.app.post("/upload")
        async def upload_file(
            file: UploadFile = File(...),
            token: Optional[str] = Query(None)
        ):
            """接收上传的文件"""
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_filename = f"{timestamp}_{file.filename}"
                file_path = self.upload_dir / safe_filename
                
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                
                return JSONResponse({
                    "success": True,
                    "filename": file.filename,
                    "saved_as": safe_filename,
                    "size": os.path.getsize(file_path)
                })
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/download/{filename}")
        async def download_file(filename: str):
            """下载文件"""
            file_path = self.upload_dir / filename
            if not file_path.exists():
                raise HTTPException(status_code=404, detail="File not found")
            return FileResponse(file_path, filename=filename)
        
        @self.app.get("/status")
        async def status():
            """服务器状态"""
            return {
                "status": "running",
                "port": self.port,
                "upload_dir": str(self.upload_dir)
            }
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket连接"""
            await websocket.accept()
            try:
                while True:
                    data = await websocket.receive_text()
                    await websocket.send_text(f"Echo: {data}")
            except WebSocketDisconnect:
                pass
    
    def _get_upload_html(self) -> str:
        """获取上传页面HTML"""
        return """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QR Transfer - 文件上传</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 500px;
            width: 100%;
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 10px;
            font-size: 28px;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 14px;
        }
        .upload-area {
            border: 3px dashed #667eea;
            border-radius: 15px;
            padding: 40px 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            background: #f8f9ff;
        }
        .upload-area:hover {
            background: #eef0ff;
            border-color: #764ba2;
        }
        .upload-area.dragover {
            background: #e0e4ff;
            border-color: #764ba2;
        }
        .upload-icon {
            font-size: 48px;
            margin-bottom: 15px;
        }
        .upload-text {
            color: #667eea;
            font-size: 16px;
            font-weight: 500;
        }
        .upload-hint {
            color: #999;
            font-size: 12px;
            margin-top: 10px;
        }
        #fileInput { display: none; }
        .progress-container {
            margin-top: 20px;
            display: none;
        }
        .progress-bar {
            width: 100%;
            height: 10px;
            background: #e0e0e0;
            border-radius: 5px;
            overflow: hidden;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            width: 0%;
            transition: width 0.3s ease;
        }
        .progress-text {
            text-align: center;
            margin-top: 10px;
            color: #667eea;
            font-weight: 500;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            border-radius: 10px;
            display: none;
        }
        .result.success {
            background: #d4edda;
            color: #155724;
            display: block;
        }
        .result.error {
            background: #f8d7da;
            color: #721c24;
            display: block;
        }
        .file-list {
            margin-top: 20px;
        }
        .file-item {
            display: flex;
            align-items: center;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 8px;
            margin-bottom: 8px;
        }
        .file-icon {
            font-size: 24px;
            margin-right: 10px;
        }
        .file-info {
            flex: 1;
        }
        .file-name {
            font-weight: 500;
            color: #333;
            font-size: 14px;
        }
        .file-size {
            color: #999;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📤 文件上传</h1>
        <p class="subtitle">选择文件上传到电脑</p>
        
        <div class="upload-area" id="uploadArea">
            <div class="upload-icon">📁</div>
            <div class="upload-text">点击或拖拽文件到此处</div>
            <div class="upload-hint">支持任意类型文件</div>
        </div>
        
        <input type="file" id="fileInput" multiple>
        
        <div class="progress-container" id="progressContainer">
            <div class="progress-bar">
                <div class="progress-fill" id="progressFill"></div>
            </div>
            <div class="progress-text" id="progressText">0%</div>
        </div>
        
        <div class="result" id="result"></div>
        
        <div class="file-list" id="fileList"></div>
    </div>

    <script>
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const progressContainer = document.getElementById('progressContainer');
        const progressFill = document.getElementById('progressFill');
        const progressText = document.getElementById('progressText');
        const result = document.getElementById('result');
        const fileList = document.getElementById('fileList');

        uploadArea.addEventListener('click', () => fileInput.click());
        
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            handleFiles(e.dataTransfer.files);
        });
        
        fileInput.addEventListener('change', (e) => {
            handleFiles(e.target.files);
        });

        function handleFiles(files) {
            if (files.length === 0) return;
            
            fileList.innerHTML = '';
            Array.from(files).forEach(file => {
                const item = document.createElement('div');
                item.className = 'file-item';
                item.innerHTML = `
                    <span class="file-icon">📄</span>
                    <div class="file-info">
                        <div class="file-name">${file.name}</div>
                        <div class="file-size">${formatSize(file.size)}</div>
                    </div>
                `;
                fileList.appendChild(item);
            });
            
            uploadFile(files[0]);
        }

        function formatSize(bytes) {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        }

        function uploadFile(file) {
            const formData = new FormData();
            formData.append('file', file);
            
            progressContainer.style.display = 'block';
            result.style.display = 'none';
            
            const xhr = new XMLHttpRequest();
            
            xhr.upload.addEventListener('progress', (e) => {
                if (e.lengthComputable) {
                    const percentComplete = (e.loaded / e.total) * 100;
                    progressFill.style.width = percentComplete + '%';
                    progressText.textContent = Math.round(percentComplete) + '%';
                }
            });
            
            xhr.addEventListener('load', () => {
                progressContainer.style.display = 'none';
                if (xhr.status === 200) {
                    const response = JSON.parse(xhr.responseText);
                    result.className = 'result success';
                    result.innerHTML = `✅ 上传成功！<br>文件名: ${response.filename}<br>大小: ${formatSize(response.size)}`;
                } else {
                    result.className = 'result error';
                    result.innerHTML = '❌ 上传失败，请重试';
                }
            });
            
            xhr.addEventListener('error', () => {
                progressContainer.style.display = 'none';
                result.className = 'result error';
                result.innerHTML = '❌ 网络错误，请重试';
            });
            
            xhr.open('POST', '/upload');
            xhr.send(formData);
        }
    </script>
</body>
</html>
        """
    
    async def start(self):
        """启动服务器"""
        config = uvicorn.Config(
            self.app,
            host=self.host,
            port=self.port,
            log_level="warning"
        )
        server = uvicorn.Server(config)
        await server.serve()
    
    def get_url(self) -> str:
        """获取服务器URL"""
        ip = get_local_ip()
        return f"http://{ip}:{self.port}"
    
    def get_qr_data(self) -> str:
        """获取二维码数据"""
        return self.get_url()
