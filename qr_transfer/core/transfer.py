"""
文件传输核心逻辑
"""
import os
import asyncio
import shutil
from pathlib import Path
from typing import Optional, Callable, List
from dataclasses import dataclass
from datetime import datetime

from .server import TransferServer
from .qr_generator import qr_to_terminal, qr_to_base64, save_qr_to_file
from ..utils.network import get_local_ip


@dataclass
class TransferInfo:
    """传输信息"""
    filename: str
    filesize: int
    source: str
    timestamp: datetime
    status: str  # pending, transferring, completed, failed


class FileTransfer:
    """文件传输管理器"""
    
    def __init__(self, port: Optional[int] = None, receive_dir: str = "./received"):
        self.server = TransferServer(port=port, upload_dir=receive_dir)
        self.receive_dir = Path(receive_dir)
        self.receive_dir.mkdir(exist_ok=True)
        self.transfer_history: List[TransferInfo] = []
        self.on_transfer_complete: Optional[Callable] = None
        
    async def start_receive_mode(self):
        """启动接收模式（等待上传）"""
        print(f"\n📥 接收模式已启动")
        print(f"🌐 访问地址: {self.server.get_url()}")
        print(f"📁 保存目录: {self.receive_dir.absolute()}")
        
        # 显示二维码
        self._show_qr()
        
        # 启动服务器
        await self.server.start()
    
    async def start_send_mode(self, filepath: str):
        """启动发送模式（等待下载）"""
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {filepath}")
        
        # 复制文件到上传目录
        dest = self.receive_dir / path.name
        if path.is_file():
            shutil.copy2(path, dest)
        elif path.is_dir():
            shutil.make_archive(str(dest), 'zip', path)
            dest = Path(str(dest) + '.zip')
        
        print(f"\n📤 发送模式已启动")
        print(f"📄 文件: {path.name}")
        print(f"📦 大小: {self._format_size(dest.stat().st_size)}")
        print(f"🌐 下载地址: {self.server.get_url()}/download/{dest.name}")
        
        # 显示二维码
        self._show_qr(f"/download/{dest.name}")
        
        # 启动服务器
        await self.server.start()
    
    def _show_qr(self, path: str = ""):
        """显示二维码"""
        url = self.server.get_url() + path
        print(f"\n📱 请扫描二维码访问:")
        print(qr_to_terminal(url))
        print(f"🔗 或直接访问: {url}\n")
    
    def save_qr(self, filepath: str = "qr_code.png"):
        """保存二维码到文件"""
        url = self.server.get_url()
        save_qr_to_file(url, filepath, size=10)
        print(f"✅ 二维码已保存: {filepath}")
    
    def get_qr_base64(self) -> str:
        """获取Base64二维码"""
        return qr_to_base64(self.server.get_url())
    
    def _format_size(self, size: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
    
    def stop(self):
        """停止传输服务"""
        # 实现停止逻辑
        pass


class TransferSession:
    """传输会话管理"""
    
    def __init__(self):
        self.sessions = {}
    
    def create_session(self, files: List[str]) -> str:
        """创建新的传输会话"""
        import uuid
        session_id = str(uuid.uuid4())[:8]
        self.sessions[session_id] = {
            'files': files,
            'created_at': datetime.now(),
            'downloads': 0
        }
        return session_id
    
    def get_session(self, session_id: str) -> Optional[dict]:
        """获取会话信息"""
        return self.sessions.get(session_id)
    
    def cleanup_expired(self, max_age_minutes: int = 30):
        """清理过期会话"""
        now = datetime.now()
        expired = []
        for sid, session in self.sessions.items():
            age = (now - session['created_at']).total_seconds() / 60
            if age > max_age_minutes:
                expired.append(sid)
        for sid in expired:
            del self.sessions[sid]
