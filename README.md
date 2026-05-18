# 📱 QR Transfer - 二维码文件传输工具

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="version">
  <img src="https://img.shields.io/badge/python-3.8+-green.svg" alt="python">
  <img src="https://img.shields.io/badge/license-MIT-yellow.svg" alt="license">
</p>

<p align="center">
  <b>通过扫描二维码在电脑和手机之间快速传输文件</b>
</p>

<p align="center">
  <a href="#简体中文">简体中文</a> |
  <a href="#繁體中文">繁體中文</a> |
  <a href="#english">English</a>
</p>

---

## 🎉 项目介绍

**QR Transfer** 是一款轻量级的文件传输工具，让你无需数据线、无需安装App，仅通过扫描二维码就能在电脑和手机之间传输文件。

### 核心优势
- 🚀 **零配置** - 开箱即用，无需复杂设置
- 🔒 **安全可靠** - 本地传输，文件不经过第三方服务器
- 💻 **跨平台** - 支持 Windows、macOS、Linux
- 📱 **无需App** - 手机只需扫码即可使用浏览器传输
- 🎨 **双界面** - 提供图形界面和命令行两种使用方式

### 灵感来源
本项目灵感来源于 [qrcp](https://github.com/claudiodangelis/qrcp)，在其基础上增加了GUI界面、批量传输、剪贴板同步等增强功能。

---

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 📤 **发送文件** | 将电脑文件发送到手机，支持单文件、多文件、文件夹 |
| 📥 **接收文件** | 从手机接收文件到电脑，自动保存到指定目录 |
| 🔐 **安全传输** | 支持传输密码保护，防止未授权访问 |
| 📋 **剪贴板同步** | 快速同步文本内容到手机剪贴板 |
| 🖥️ **双模式** | 图形界面(GUI)和命令行(CLI)两种使用方式 |
| 🌐 **自动发现** | 自动获取本机IP，无需手动配置 |
| 📊 **传输记录** | 记录传输历史，方便追溯 |

---

## 🚀 快速开始

### 环境要求
- Python 3.8 或更高版本
- 支持的操作系统: Windows 10/11, macOS 10.15+, Linux

### 安装方式

#### 方式一：通过 pip 安装（推荐）
```bash
pip install qr-transfer
```

#### 方式二：从源码安装
```bash
git clone https://github.com/gitstq/qr-transfer.git
cd qr-transfer
pip install -e .
```

#### 方式三：下载可执行文件
从 [Releases](https://github.com/gitstq/qr-transfer/releases) 页面下载对应平台的可执行文件。

### 启动方式

#### 图形界面
```bash
qr-transfer-gui
# 或
python -m qr_transfer.gui
```

#### 命令行
```bash
# 接收模式（手机上传文件到电脑）
qr-transfer receive

# 发送模式（电脑发送文件到手机）
qr-transfer send /path/to/file

# 发送文件夹
qr-transfer send /path/to/folder
```

---

## 📖 详细使用指南

### 接收文件

1. 在电脑上启动接收模式：
```bash
qr-transfer receive
```

2. 终端会显示二维码，用手机扫码

3. 手机浏览器打开上传页面，选择文件上传

4. 文件自动保存到 `./received` 目录

**高级选项：**
```bash
# 指定端口
qr-transfer receive -p 9000

# 指定保存目录
qr-transfer receive -d ~/Downloads

# 保存二维码图片
qr-transfer receive --save-qr qr.png
```

### 发送文件

1. 在电脑上启动发送模式：
```bash
qr-transfer send ~/Documents/report.pdf
```

2. 终端显示二维码，手机扫码下载

3. 文件开始传输，完成后自动关闭

**高级选项：**
```bash
# 发送整个文件夹（自动压缩）
qr-transfer send ./my-project

# 指定端口
qr-transfer send file.txt -p 8080
```

### 图形界面使用

1. 启动 GUI：
```bash
qr-transfer-gui
```

2. 选择模式（接收/发送）

3. 如选择发送模式，点击"浏览"选择文件

4. 点击"启动服务"

5. 扫描二维码或复制链接到手机浏览器

---

## 💡 设计思路与迭代规划

### 技术选型
- **Python**: 跨平台、生态丰富、开发效率高
- **FastAPI**: 高性能异步Web框架
- **QRCode**: 成熟的二维码生成库
- **tkinter**: Python内置GUI库，无需额外依赖

### 架构设计
```
qr-transfer/
├── core/           # 核心功能模块
│   ├── server.py   # HTTP/WebSocket服务器
│   ├── transfer.py # 传输逻辑
│   └── qr_generator.py # 二维码生成
├── gui/            # 图形界面
├── cli/            # 命令行接口
└── utils/          # 工具函数
```

### 后续迭代计划

#### V1.1.0
- [ ] 传输历史记录
- [ ] 多文件同时传输
- [ ] 传输进度实时显示

#### V1.2.0
- [ ] 局域网设备自动发现
- [ ] 端到端加密传输
- [ ] 配套移动端App

#### V1.3.0
- [ ] 云同步功能
- [ ] 远程访问支持
- [ ] 插件系统

---

## 📦 打包与部署

### 打包为可执行文件

#### 安装打包工具
```bash
pip install pyinstaller
```

#### 打包命令
```bash
# Windows
pyinstaller --onefile --windowed --name qr-transfer-cli qr_transfer/cli/main.py
pyinstaller --onefile --windowed --name qr-transfer-gui qr_transfer/gui/app.py

# macOS/Linux
pyinstaller --onefile --name qr-transfer-cli qr_transfer/cli/main.py
pyinstaller --onefile --name qr-transfer-gui qr_transfer/gui/app.py
```

### Docker 部署
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install -e .

EXPOSE 8080

CMD ["qr-transfer", "receive", "-p", "8080"]
```

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 提交 Issue
- 使用清晰的标题描述问题
- 提供复现步骤和环境信息
- 如有错误日志，请一并提供

### 提交 Pull Request
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 代码规范
- 遵循 PEP 8 编码规范
- 添加必要的注释和文档
- 确保通过所有测试

---

## 📄 开源协议

本项目采用 [MIT](LICENSE) 协议开源。

---

<p align="center">
  Made with ❤️ by QR Transfer Team
</p>
