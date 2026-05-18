"""
命令行接口
"""
import argparse
import asyncio
import sys
from pathlib import Path

from ..core.transfer import FileTransfer
from ..core.qr_generator import save_qr_to_file
from ..__init__ import __version__


def create_parser() -> argparse.ArgumentParser:
    """创建命令行解析器"""
    parser = argparse.ArgumentParser(
        prog='qr-transfer',
        description='通过二维码在电脑和手机之间传输文件',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  qr-transfer receive              # 启动接收模式
  qr-transfer send file.txt        # 发送文件
  qr-transfer send ./folder        # 发送文件夹（自动压缩）
  qr-transfer receive -p 9000      # 指定端口
        """
    )
    
    parser.add_argument(
        '--version', 
        action='version', 
        version=f'%(prog)s {__version__}'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 接收命令
    receive_parser = subparsers.add_parser(
        'receive', 
        aliases=['r'],
        help='启动接收模式（手机上传文件到电脑）'
    )
    receive_parser.add_argument(
        '-p', '--port',
        type=int,
        default=None,
        help='指定服务器端口（默认自动分配）'
    )
    receive_parser.add_argument(
        '-d', '--directory',
        type=str,
        default='./received',
        help='指定接收文件保存目录（默认: ./received）'
    )
    receive_parser.add_argument(
        '--save-qr',
        type=str,
        metavar='PATH',
        help='保存二维码到指定路径'
    )
    
    # 发送命令
    send_parser = subparsers.add_parser(
        'send',
        aliases=['s'],
        help='启动发送模式（手机下载电脑文件）'
    )
    send_parser.add_argument(
        'path',
        type=str,
        help='要发送的文件或文件夹路径'
    )
    send_parser.add_argument(
        '-p', '--port',
        type=int,
        default=None,
        help='指定服务器端口（默认自动分配）'
    )
    send_parser.add_argument(
        '--save-qr',
        type=str,
        metavar='PATH',
        help='保存二维码到指定路径'
    )
    
    return parser


def print_banner():
    """打印欢迎信息"""
    print("""
╔═══════════════════════════════════════╗
║     📱 QR Transfer v{}              ║
║     二维码文件传输工具                ║
╚═══════════════════════════════════════╝
    """.format(__version__))


async def main():
    """主函数"""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    print_banner()
    
    try:
        if args.command in ['receive', 'r']:
            # 接收模式
            transfer = FileTransfer(
                port=args.port,
                receive_dir=args.directory
            )
            
            if args.save_qr:
                # 先启动服务器再保存二维码
                import threading
                import time
                
                # 延迟保存二维码，等待服务器启动
                def delayed_save():
                    time.sleep(1)
                    transfer.save_qr(args.save_qr)
                
                threading.Thread(target=delayed_save, daemon=True).start()
            
            await transfer.start_receive_mode()
            
        elif args.command in ['send', 's']:
            # 发送模式
            if not Path(args.path).exists():
                print(f"❌ 错误: 文件不存在: {args.path}")
                sys.exit(1)
            
            transfer = FileTransfer(port=args.port)
            
            if args.save_qr:
                import threading
                import time
                
                def delayed_save():
                    time.sleep(1)
                    transfer.save_qr(args.save_qr)
                
                threading.Thread(target=delayed_save, daemon=True).start()
            
            await transfer.start_send_mode(args.path)
            
    except KeyboardInterrupt:
        print("\n\n👋 再见！")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        sys.exit(1)


def run():
    """入口函数"""
    asyncio.run(main())


if __name__ == '__main__':
    run()
