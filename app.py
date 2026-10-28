import os
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
        # Trên môi trường Render (Linux server), bắt buộc phải chạy headless=True
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
            page = browser.new_page()

            # Truy cập vào trang web VMOS Cloud
            page.goto("https://intl.vmoscloud.com/#/login")
            time.sleep(2)

            fake_email = f"user_{random.randint(10000, 99999)}@uberip.com"
            
            # Tại đây bạn có thể bổ sung thêm các lệnh thao tác tự động trên trang (ví dụ: page.fill(...))
            time.sleep(1)
            
            browser.close()

        # Giả lập kết quả trả về thông tin máy ảo sau khi auto thành công
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
        }, 500)

@app.route('/api/get-machines', methods=['GET'])
def get_machines():
    return jsonify({"machines": virtual_machines})

if __name__ == '__main__':
    # Lấy cổng PORT do Render cung cấp tự động, mặc định là 5000 khi chạy local
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
