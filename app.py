from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
import io
import datetime

app = Flask(__name__)

@app.route('/sig.png')
def sig():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ua = request.headers.get('User-Agent', 'Unknown')
    date = datetime.datetime.now().strftime("%Y年%m月%d日 %A")

    def get_os(ua):
        if 'Android' in ua: return 'Android'
        if 'iPhone' in ua: return 'iOS'
        if 'Windows' in ua: return 'Windows'
        if 'Mac' in ua: return 'macOS'
        return '未知'

    def get_browser(ua):
        if 'Chrome' in ua: return 'Chrome'
        if 'Firefox' in ua: return 'Firefox'
        if 'Safari' in ua and 'Chrome' not in ua: return 'Safari'
        return '未知'

    os_name = get_os(ua)
    browser = get_browser(ua)

    img = Image.new('RGB', (480, 150), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("font.ttf", 20)

    draw.text((10, 20), f"IP: {ip}", fill="black", font=font)
    draw.text((10, 50), f"日期: {date}", fill="black", font=font)
    draw.text((10, 80), f"系统: {os_name}", fill="black", font=font)
    draw.text((10, 110), f"浏览器: {browser}", fill="black", font=font)

    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')