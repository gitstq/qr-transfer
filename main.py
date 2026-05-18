#!/usr/bin/env python3
"""
QR Transfer - 二维码文件传输工具
主入口文件
"""
import sys
import argparse

def main():
    """主入口"""
    parser = argparse.ArgumentParser(
        description='QR Transfer - 二维码文件传输工具',
        add_help=False
    )
    parser.add_argument('--gui', action='store_true', help='启动图形界面')
    parser.add_argument('--cli', action='store_true', help='启动命令行界面')
    parser.add_argument('-h', '--help', action='store_true', help='显示帮助')
    
    args, remaining = parser.parse_known_args()
    
    if args.help or (not args.gui and not args.cli and len(sys.argv) == 1):
        print("""
╔═══════════════════════════════════════════════════════════╗
║              📱 QR Transfer v1.0.0                        ║
║         二维码文件传输工具                                ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  使用方式:                                                ║
║    python main.py --gui    启动图形界面                   ║
║    python main.py --cli    启动命令行界面                 ║
║                                                           ║
║  命令行示例:                                              ║
║    qr-transfer receive              接收模式              ║
║    qr-transfer send file.txt        发送文件              ║
║    qr-transfer send ./folder        发送文件夹            ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
        """)
        sys.exit(0)
    
    if args.gui:
        from qr_transfer.gui import main as gui_main
        gui_main()
    else:
        from qr_transfer.cli import run
        run()

if __name__ == '__main__':
    main()
