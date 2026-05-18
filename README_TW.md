# 📱 QR Transfer - 二維碼檔案傳輸工具

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="version">
  <img src="https://img.shields.io/badge/python-3.8+-green.svg" alt="python">
  <img src="https://img.shields.io/badge/license-MIT-yellow.svg" alt="license">
</p>

<p align="center">
  <b>透過掃描二維碼在電腦和手機之間快速傳輸檔案</b>
</p>

<p align="center">
  <a href="#简体中文">简体中文</a> |
  <a href="#繁體中文">繁體中文</a> |
  <a href="#english">English</a>
</p>

---

## 🎉 專案介紹

**QR Transfer** 是一款輕量級的檔案傳輸工具，讓您無需數據線、無需安裝App，僅透過掃描二維碼就能在電腦和手機之間傳輸檔案。

### 核心優勢
- 🚀 **零配置** - 開箱即用，無需複雜設定
- 🔒 **安全可靠** - 本地傳輸，檔案不經過第三方伺服器
- 💻 **跨平台** - 支援 Windows、macOS、Linux
- 📱 **無需App** - 手機只需掃碼即可使用瀏覽器傳輸
- 🎨 **雙介面** - 提供圖形介面和命令列兩種使用方式

### 靈感來源
本專案靈感來源於 [qrcp](https://github.com/claudiodangelis/qrcp)，在其基礎上增加了GUI介面、批次傳輸、剪貼簿同步等增強功能。

---

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 📤 **傳送檔案** | 將電腦檔案傳送到手機，支援單檔案、多檔案、資料夾 |
| 📥 **接收檔案** | 從手機接收檔案到電腦，自動儲存到指定目錄 |
| 🔐 **安全傳輸** | 支援傳輸密碼保護，防止未授權存取 |
| 📋 **剪貼簿同步** | 快速同步文字內容到手機剪貼簿 |
| 🖥️ **雙模式** | 圖形介面(GUI)和命令列(CLI)兩種使用方式 |
| 🌐 **自動發現** | 自動取得本機IP，無需手動配置 |
| 📊 **傳輸記錄** | 記錄傳輸歷史，方便追溯 |

---

## 🚀 快速開始

### 環境要求
- Python 3.8 或更高版本
- 支援的作業系統: Windows 10/11, macOS 10.15+, Linux

### 安裝方式

#### 方式一：透過 pip 安裝（推薦）
```bash
pip install qr-transfer
```

#### 方式二：從原始碼安裝
```bash
git clone https://github.com/gitstq/qr-transfer.git
cd qr-transfer
pip install -e .
```

#### 方式三：下載可執行檔案
從 [Releases](https://github.com/gitstq/qr-transfer/releases) 頁面下載對應平台的可執行檔案。

### 啟動方式

#### 圖形介面
```bash
qr-transfer-gui
# 或
python -m qr_transfer.gui
```

#### 命令列
```bash
# 接收模式（手機上傳檔案到電腦）
qr-transfer receive

# 傳送模式（電腦傳送檔案到手機）
qr-transfer send /path/to/file

# 傳送資料夾
qr-transfer send /path/to/folder
```

---

## 📖 詳細使用指南

### 接收檔案

1. 在電腦上啟動接收模式：
```bash
qr-transfer receive
```

2. 終端機會顯示二維碼，用手機掃碼

3. 手機瀏覽器開啟上傳頁面，選擇檔案上傳

4. 檔案自動儲存到 `./received` 目錄

**進階選項：**
```bash
# 指定連接埠
qr-transfer receive -p 9000

# 指定儲存目錄
qr-transfer receive -d ~/Downloads

# 儲存二維碼圖片
qr-transfer receive --save-qr qr.png
```

### 傳送檔案

1. 在電腦上啟動傳送模式：
```bash
qr-transfer send ~/Documents/report.pdf
```

2. 終端機顯示二維碼，手機掃碼下載

3. 檔案開始傳輸，完成後自動關閉

**進階選項：**
```bash
# 傳送整個資料夾（自動壓縮）
qr-transfer send ./my-project

# 指定連接埠
qr-transfer send file.txt -p 8080
```

### 圖形介面使用

1. 啟動 GUI：
```bash
qr-transfer-gui
```

2. 選擇模式（接收/傳送）

3. 如選擇傳送模式，點選「瀏覽」選擇檔案

4. 點選「啟動服務」

5. 掃描二維碼或複製連結到手機瀏覽器

---

## 💡 設計思路與迭代規劃

### 技術選型
- **Python**: 跨平台、生態豐富、開發效率高
- **FastAPI**: 高效能非同步Web框架
- **QRCode**: 成熟的二維碼生成函式庫
- **tkinter**: Python內建GUI函式庫，無需額外依賴

### 架構設計
```
qr-transfer/
├── core/           # 核心功能模組
│   ├── server.py   # HTTP/WebSocket伺服器
│   ├── transfer.py # 傳輸邏輯
│   └── qr_generator.py # 二維碼生成
├── gui/            # 圖形介面
├── cli/            # 命令列介面
└── utils/          # 工具函式
```

### 後續迭代計劃

#### V1.1.0
- [ ] 傳輸歷史記錄
- [ ] 多檔案同時傳輸
- [ ] 傳輸進度即時顯示

#### V1.2.0
- [ ] 區域網路裝置自動發現
- [ ] 端到端加密傳輸
- [ ] 配套行動端App

#### V1.3.0
- [ ] 雲端同步功能
- [ ] 遠端存取支援
- [ ] 外掛系統

---

## 📦 打包與部署

### 打包為可執行檔案

#### 安裝打包工具
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

## 🤝 貢獻指南

我們歡迎所有形式的貢獻！

### 提交 Issue
- 使用清晰的標題描述問題
- 提供復現步驟和環境資訊
- 如有錯誤日誌，請一併提供

### 提交 Pull Request
1. Fork 本倉庫
2. 建立特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 建立 Pull Request

### 程式碼規範
- 遵循 PEP 8 編碼規範
- 新增必要的註釋和文件
- 確保通過所有測試

---

## 📄 開源協議

本專案採用 [MIT](LICENSE) 協議開源。

---

<p align="center">
  Made with ❤️ by QR Transfer Team
</p>
