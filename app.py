
from flask import Flask, send_file, request
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import io
import platform
import re

app = Flask(__name__)

def get_browser(user_agent):
    browsers = {
        "Edge": "Edge", "Edg": "Edge", "OPR": "Opera", "Chrome": "Chrome",
        "Safari": "Safari", "Firefox": "Firefox", "MSIE": "Internet Explorer", "Trident": "Internet Explorer"
    }
    for key, name in browsers.items():
        if key in user_agent:
            return name
    return "Unknown"

def get_os(user_agent):
    if "Windows" in user_agent:
        return "Windows"
    elif "Mac" in user_agent:
        return "macOS"
    elif "Linux" in user_agent:
        return "Linux"
    elif "Android" in user_agent:
        return "Android"
    elif "iPhone" in user_agent or "iPad" in user_agent:
        return "iOS"
    else:
        return "Unknown"

@app.route('/sig.png')
def signature():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    date = datetime.now().strftime("%Y年%m月%d日 %A")
    user_agent = request.headers.get('User-Agent', '')
    os_name = get_os(user_agent)
    browser = get_browser(user_agent)

    width, height = 480, 150
    image = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("font.ttf", 20)
    except:
        font = ImageFont.load_default()

    draw.text((10, 20), f"IP: {ip}", font=font, fill=(0, 0, 0))
    draw.text((10, 50), f"日期: {date}", font=font, fill=(0, 0, 0))
    draw.text((10, 80), f"系统: {os_name}", font=font, fill=(0, 0, 0))
    draw.text((10, 110), f"浏览器: {browser}", font=font, fill=(0, 0, 0))

    img_io = io.BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')
