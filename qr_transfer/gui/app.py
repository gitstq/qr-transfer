"""
图形界面模块
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import asyncio
import threading
from pathlib import Path

from ..core.transfer import FileTransfer
from ..core.qr_generator import qr_to_base64
from ..__init__ import __version__


class QRTransferGUI:
    """QR Transfer 图形界面"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"QR Transfer v{__version__}")
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        
        self.transfer = None
        self.server_thread = None
        self.loop = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI界面"""
        # 样式配置
        self.style = ttk.Style()
        self.style.configure('Title.TLabel', font=('Helvetica', 24, 'bold'))
        self.style.configure('Subtitle.TLabel', font=('Helvetica', 12), foreground='gray')
        self.style.configure('Action.TButton', font=('Helvetica', 14), padding=10)
        
        # 主容器
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 标题
        ttk.Label(main_frame, text="📱 QR Transfer", style='Title.TLabel').grid(row=0, column=0, pady=(0, 5))
        ttk.Label(main_frame, text="二维码文件传输工具", style='Subtitle.TLabel').grid(row=1, column=0, pady=(0, 20))
        
        # 模式选择
        mode_frame = ttk.LabelFrame(main_frame, text="选择模式", padding="15")
        mode_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.mode_var = tk.StringVar(value="receive")
        ttk.Radiobutton(mode_frame, text="📥 接收模式（手机→电脑）", variable=self.mode_var, 
                       value="receive").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Radiobutton(mode_frame, text="📤 发送模式（电脑→手机）", variable=self.mode_var,
                       value="send").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        # 文件选择（发送模式）
        self.file_frame = ttk.LabelFrame(main_frame, text="文件选择", padding="15")
        self.file_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.file_path_var = tk.StringVar()
        ttk.Entry(self.file_frame, textvariable=self.file_path_var, state='readonly').grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        ttk.Button(self.file_frame, text="浏览...", command=self.browse_file).grid(row=0, column=1)
        
        # 设置
        settings_frame = ttk.LabelFrame(main_frame, text="设置", padding="15")
        settings_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Label(settings_frame, text="端口:").grid(row=0, column=0, sticky=tk.W)
        self.port_var = tk.StringVar(value="自动")
        ttk.Entry(settings_frame, textvariable=self.port_var, width=10).grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        ttk.Label(settings_frame, text="(留空自动分配)").grid(row=0, column=2, sticky=tk.W, padx=(5, 0))
        
        ttk.Label(settings_frame, text="保存目录:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.save_dir_var = tk.StringVar(value="./received")
        ttk.Entry(settings_frame, textvariable=self.save_dir_var).grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=(10, 0), pady=(10, 0))
        
        # 启动按钮
        self.start_btn = ttk.Button(main_frame, text="🚀 启动服务", command=self.start_service, style='Action.TButton')
        self.start_btn.grid(row=5, column=0, pady=(0, 15))
        
        # 状态显示
        self.status_frame = ttk.LabelFrame(main_frame, text="状态", padding="15")
        self.status_frame.grid(row=6, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        
        self.status_var = tk.StringVar(value="就绪")
        ttk.Label(self.status_frame, textvariable=self.status_var, wraplength=400).grid(row=0, column=0, sticky=tk.W)
        
        self.url_var = tk.StringVar(value="")
        url_label = ttk.Label(self.status_frame, textvariable=self.url_var, foreground="blue", cursor="hand2")
        url_label.grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        url_label.bind("<Button-1>", self.copy_url)
        
        # 二维码显示
        self.qr_label = ttk.Label(self.status_frame)
        self.qr_label.grid(row=2, column=0, pady=(10, 0))
        
        # 停止按钮
        self.stop_btn = ttk.Button(main_frame, text="⏹ 停止服务", command=self.stop_service, state='disabled')
        self.stop_btn.grid(row=7, column=0, pady=(0, 15))
        
        # 日志
        log_frame = ttk.LabelFrame(main_frame, text="日志", padding="10")
        log_frame.grid(row=8, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.log_text = tk.Text(log_frame, height=8, wrap=tk.WORD, state='disabled')
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text['yscrollcommand'] = scrollbar.set
        
        # 配置grid权重
        main_frame.columnconfigure(0, weight=1)
        self.file_frame.columnconfigure(0, weight=1)
        settings_frame.columnconfigure(1, weight=1)
        self.status_frame.columnconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
    def browse_file(self):
        """浏览文件"""
        path = filedialog.askopenfilename() or filedialog.askdirectory()
        if path:
            self.file_path_var.set(path)
            
    def copy_url(self, event=None):
        """复制URL到剪贴板"""
        url = self.url_var.get()
        if url and url.startswith("http"):
            self.root.clipboard_clear()
            self.root.clipboard_append(url)
            messagebox.showinfo("提示", "URL已复制到剪贴板！")
            
    def log(self, message: str):
        """添加日志"""
        self.log_text['state'] = 'normal'
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text['state'] = 'disabled'
        
    def start_service(self):
        """启动服务"""
        mode = self.mode_var.get()
        
        if mode == "send" and not self.file_path_var.get():
            messagebox.showerror("错误", "请先选择要发送的文件！")
            return
        
        # 获取端口
        port_str = self.port_var.get()
        port = None if port_str == "自动" else int(port_str)
        
        # 创建传输对象
        self.transfer = FileTransfer(
            port=port,
            receive_dir=self.save_dir_var.get()
        )
        
        # 启动服务器线程
        self.server_thread = threading.Thread(target=self.run_server, args=(mode,), daemon=True)
        self.server_thread.start()
        
        # 更新UI
        self.start_btn['state'] = 'disabled'
        self.stop_btn['state'] = 'normal'
        self.status_var.set("服务运行中...")
        self.log(f"服务已启动 - 模式: {mode}")
        
        # 显示二维码
        self.root.after(1000, self.show_qr)
        
    def run_server(self, mode: str):
        """运行服务器"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        try:
            if mode == "receive":
                self.loop.run_until_complete(self.transfer.start_receive_mode())
            else:
                self.loop.run_until_complete(self.transfer.start_send_mode(self.file_path_var.get()))
        except Exception as e:
            self.log(f"错误: {e}")
            
    def show_qr(self):
        """显示二维码"""
        if self.transfer:
            try:
                qr_base64 = self.transfer.get_qr_base64()
                # 这里简化处理，实际应该显示图片
                url = self.transfer.server.get_url()
                self.url_var.set(f"🔗 {url}")
                self.log(f"访问地址: {url}")
            except Exception as e:
                self.log(f"生成二维码失败: {e}")
                
    def stop_service(self):
        """停止服务"""
        if self.transfer:
            self.transfer.stop()
            
        self.start_btn['state'] = 'normal'
        self.stop_btn['state'] = 'disabled'
        self.status_var.set("已停止")
        self.url_var.set("")
        self.log("服务已停止")
        
    def run(self):
        """运行应用"""
        self.root.mainloop()


def main():
    """GUI入口"""
    app = QRTransferGUI()
    app.run()


if __name__ == '__main__':
    main()
