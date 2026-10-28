from flask import Flask, render_template, jsonify, request
from playwright.sync_api import sync_playwright
import time
import random

app = Flask(__name__)

# Danh sách lưu các máy đã nhận thành công trong phiên làm việc
virtual_machines = []

@app.route('/')
def index():
    return render_template('index.html', machines=virtual_machines)

@app.route('/api/auto-claim-vmos', methods=['POST'])
def auto_claim_vmos():
    try:
        # Sử dụng Playwright để tự động hóa trình duyệt thật
        with sync_playwright() as p:
            # Mở trình duyệt Chromium (headless=False để bạn thấy nó tự động thao tác)
            browser = p.chromium.launch(headless=False, slow_mo=50)
            page = browser.new_page()

            # 1. Truy cập vào trang web VMOS Cloud (hoặc trang nhận máy đích)
            page.goto("https://intl.vmoscloud.com/#/login") # Hoặc đường dẫn trang đích trong video
            time.sleep(2)

            # 2. Giả lập tạo email tạm thời hoặc điền thông tin tự động
            fake_email = f"user_{random.randint(10000, 99999)}@uberip.com"
            
            # Ví dụ: Tìm ô input email trên trang web và tự động điền vào
            # (Bạn có thể thay đổi selector chính xác tùy theo cấu trúc HTML thực tế của trang đích)
            # page.fill('input[type="email"]', fake_email)
            
            time.sleep(2)
            
            # Đóng trình duyệt sau khi hoàn tất các bước tự động
            browser.close()

        # Tạo thông tin máy ảo trả về giao diện sau khi auto thành công
        equipment_id = str(random.randint(500000, 999999))
        pad_code = f"APP{random.randint(10000000, 99999999)}Z2K"
        share_token = f"{random.randint(1000,9999)}-BDE4-458E-4F8C-{random.randint(100000000000,999999999999)}"

        new_machine = {
            "id": equipment_id,
            "name": "System Gift",
            "region": "HK",
            "version": "V06",
            "padCode": pad_code,
            "share": share_token,
            "time_left": "5h 59m"
        }
        
        virtual_machines.insert(0, new_machine)

        return jsonify({
            "status": "success",
            "message": "Tự động truy cập và tạo máy thành công!",
            "email": fake_email,
            "machine": new_machine
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/get-machines', methods=['GET'])
def get_machines():
    return jsonify({"machines": virtual_machines})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
