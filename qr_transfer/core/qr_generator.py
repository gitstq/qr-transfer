"""
二维码生成模块
"""
import qrcode
import io
import base64
from typing import Optional
from qrcode.constants import ERROR_CORRECT_M


def generate_qr_code(data: str, size: int = 10) -> qrcode.QRCode:
    """生成二维码对象"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=ERROR_CORRECT_M,
        box_size=size,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)
    return qr


def qr_to_base64(data: str, size: int = 10) -> str:
    """生成Base64编码的二维码图片"""
    qr = generate_qr_code(data, size)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"


def qr_to_terminal(data: str) -> str:
    """生成终端可显示的二维码（ASCII艺术）"""
    qr = generate_qr_code(data, size=1)
    
    # 使用Unicode块字符生成更清晰的二维码
    img = qr.make_image(fill_color="black", back_color="white")
    
    # 转换为ASCII
    lines = []
    pixels = img.load()
    width, height = img.size
    
    for y in range(0, height, 2):
        line = ""
        for x in range(width):
            top = pixels[x, y] == 0 if y < height else False
            bottom = pixels[x, y + 1] == 0 if y + 1 < height else False
            
            if top and bottom:
                line += "█"
            elif top:
                line += "▀"
            elif bottom:
                line += "▄"
            else:
                line += " "
        lines.append(line)
    
    return "\n".join(lines)


def save_qr_to_file(data: str, filepath: str, size: int = 10) -> None:
    """保存二维码到文件"""
    qr = generate_qr_code(data, size)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filepath)
