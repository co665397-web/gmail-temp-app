from flask import Flask, render_template, jsonify, request
import time
import random

app = Flask(__name__)

# Lưu danh sách máy ảo đã nhận giả lập trong phiên làm việc
virtual_machines = []

@app.route('/')
def index():
    return render_template('index.html', machines=virtual_machines)

@app.route('/api/get-free-machine', methods=['POST'])
def get_free_machine():
    data = request.json
    cloud_type = data.get('type', 'vmos')

    # 1. Giả lập bước tạo email tạm thời (Temp Mail API)
    time.sleep(1)
    random_email = f"user_{random.randint(10000, 99999)}@uberip.com"

    # 2. Giả lập gửi mã xác thực và vượt Captcha
    time.sleep(1.5)

    # 3. Giả lập gọi API tạo máy thành công từ hệ thống đích
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
        "code": 200,
        "email": random_email,
        "machine": new_machine
    })

@app.route('/api/get-machines', methods=['GET'])
def get_machines():
    return jsonify({"machines": virtual_machines})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
