#!/usr/bin/env python3
"""
QR Transfer - 二维码文件传输工具
安装脚本
"""
from setuptools import setup, find_packages
from pathlib import Path

# 读取README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="qr-transfer",
    version="1.0.0",
    author="QR Transfer Team",
    author_email="",
    description="通过二维码在电脑和手机之间传输文件",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/qr-transfer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0",
        "qrcode[pil]>=7.4.2",
        "websockets>=12.0",
        "aiofiles>=23.2.0",
        "python-multipart>=0.0.6",
        "jinja2>=3.1.2",
        "netifaces>=0.11.0",
    ],
    extras_require={
        "dev": [
            "pyinstaller>=6.2.0",
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "qr-transfer=qr_transfer.cli:run",
            "qr-transfer-gui=qr_transfer.gui:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
