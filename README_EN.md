# 📱 QR Transfer - QR Code File Transfer Tool

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="version">
  <img src="https://img.shields.io/badge/python-3.8+-green.svg" alt="python">
  <img src="https://img.shields.io/badge/license-MIT-yellow.svg" alt="license">
</p>

<p align="center">
  <b>Transfer files between computer and phone by scanning QR codes</b>
</p>

<p align="center">
  <a href="#简体中文">简体中文</a> |
  <a href="#繁體中文">繁體中文</a> |
  <a href="#english">English</a>
</p>

---

## 🎉 Project Introduction

**QR Transfer** is a lightweight file transfer tool that allows you to transfer files between your computer and phone without data cables or installing apps - just scan a QR code!

### Key Advantages
- 🚀 **Zero Configuration** - Works out of the box, no complex setup needed
- 🔒 **Secure & Private** - Local transfer, files never go through third-party servers
- 💻 **Cross-Platform** - Supports Windows, macOS, and Linux
- 📱 **No App Required** - Phone only needs a browser to scan and transfer
- 🎨 **Dual Interface** - Both GUI and CLI interfaces available

### Inspiration
This project is inspired by [qrcp](https://github.com/claudiodangelis/qrcp), with enhancements including a GUI interface, batch transfers, and clipboard sync.

---

## ✨ Core Features

| Feature | Description |
|---------|-------------|
| 📤 **Send Files** | Send files from computer to phone, supports single/multiple files and folders |
| 📥 **Receive Files** | Receive files from phone to computer, auto-saved to specified directory |
| 🔐 **Secure Transfer** | Password protection to prevent unauthorized access |
| 📋 **Clipboard Sync** | Quickly sync text content to phone clipboard |
| 🖥️ **Dual Mode** - Both GUI and CLI interfaces |
| 🌐 **Auto Discovery** - Automatically detects local IP, no manual configuration |
| 📊 **Transfer History** - Records transfer history for easy tracking |

---

## 🚀 Quick Start

### Requirements
- Python 3.8 or higher
- Supported OS: Windows 10/11, macOS 10.15+, Linux

### Installation

#### Option 1: Install via pip (Recommended)
```bash
pip install qr-transfer
```

#### Option 2: Install from Source
```bash
git clone https://github.com/gitstq/qr-transfer.git
cd qr-transfer
pip install -e .
```

#### Option 3: Download Executable
Download the executable for your platform from the [Releases](https://github.com/gitstq/qr-transfer/releases) page.

### Usage

#### GUI Mode
```bash
qr-transfer-gui
# or
python -m qr_transfer.gui
```

#### CLI Mode
```bash
# Receive mode (phone uploads to computer)
qr-transfer receive

# Send mode (computer sends to phone)
qr-transfer send /path/to/file

# Send folder
qr-transfer send /path/to/folder
```

---

## 📖 Detailed Usage Guide

### Receiving Files

1. Start receive mode on computer:
```bash
qr-transfer receive
```

2. Terminal displays QR code, scan with phone

3. Phone browser opens upload page, select files to upload

4. Files automatically saved to `./received` directory

**Advanced Options:**
```bash
# Specify port
qr-transfer receive -p 9000

# Specify save directory
qr-transfer receive -d ~/Downloads

# Save QR code image
qr-transfer receive --save-qr qr.png
```

### Sending Files

1. Start send mode on computer:
```bash
qr-transfer send ~/Documents/report.pdf
```

2. Terminal displays QR code, phone scans to download

3. File transfers, auto-closes when complete

**Advanced Options:**
```bash
# Send entire folder (auto-compressed)
qr-transfer send ./my-project

# Specify port
qr-transfer send file.txt -p 8080
```

### GUI Usage

1. Launch GUI:
```bash
qr-transfer-gui
```

2. Select mode (Receive/Send)

3. If sending, click "Browse" to select file

4. Click "Start Service"

5. Scan QR code or copy link to phone browser

---

## 💡 Design Philosophy & Roadmap

### Tech Stack
- **Python**: Cross-platform, rich ecosystem, high development efficiency
- **FastAPI**: High-performance async web framework
- **QRCode**: Mature QR code generation library
- **tkinter**: Built-in Python GUI library, no extra dependencies

### Architecture
```
qr-transfer/
├── core/           # Core functionality
│   ├── server.py   # HTTP/WebSocket server
│   ├── transfer.py # Transfer logic
│   └── qr_generator.py # QR code generation
├── gui/            # GUI interface
├── cli/            # CLI interface
└── utils/          # Utility functions
```

### Roadmap

#### V1.1.0
- [ ] Transfer history records
- [ ] Multiple file simultaneous transfer
- [ ] Real-time transfer progress display

#### V1.2.0
- [ ] LAN device auto-discovery
- [ ] End-to-end encryption
- [ ] Companion mobile app

#### V1.3.0
- [ ] Cloud sync functionality
- [ ] Remote access support
- [ ] Plugin system

---

## 📦 Packaging & Deployment

### Build Executable

#### Install PyInstaller
```bash
pip install pyinstaller
```

#### Build Commands
```bash
# Windows
pyinstaller --onefile --windowed --name qr-transfer-cli qr_transfer/cli/main.py
pyinstaller --onefile --windowed --name qr-transfer-gui qr_transfer/gui/app.py

# macOS/Linux
pyinstaller --onefile --name qr-transfer-cli qr_transfer/cli/main.py
pyinstaller --onefile --name qr-transfer-gui qr_transfer/gui/app.py
```

### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install -e .

EXPOSE 8080

CMD ["qr-transfer", "receive", "-p", "8080"]
```

---

## 🤝 Contributing

We welcome all forms of contributions!

### Submitting Issues
- Use clear titles to describe the problem
- Provide reproduction steps and environment info
- Include error logs if available

### Submitting Pull Requests
1. Fork this repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push branch (`git push origin feature/AmazingFeature`)
5. Create Pull Request

### Code Standards
- Follow PEP 8 coding standards
- Add necessary comments and documentation
- Ensure all tests pass

---

## 📄 License

This project is licensed under the [MIT](LICENSE) License.

---

<p align="center">
  Made with ❤️ by QR Transfer Team
</p>
