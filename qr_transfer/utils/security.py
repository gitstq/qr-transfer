"""
安全工具模块
"""
import secrets
import hashlib
import base64
from typing import Optional


def generate_token(length: int = 16) -> str:
    """生成随机token"""
    return secrets.token_urlsafe(length)


def generate_short_code(length: int = 6) -> str:
    """生成短验证码"""
    return secrets.token_hex(length // 2).upper()


def hash_file(filepath: str) -> str:
    """计算文件SHA256哈希"""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def verify_password(stored_hash: str, provided_password: str) -> bool:
    """验证密码"""
    return secrets.compare_digest(stored_hash, hashlib.sha256(provided_password.encode()).hexdigest())


def hash_password(password: str) -> str:
    """哈希密码"""
    return hashlib.sha256(password.encode()).hexdigest()
