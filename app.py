import os
from flask import Flask, render_template, jsonify, request
import time
import random

app = Flask(__name__)

virtual_machines = []

@app.route('/')
def index():
    return render_template('index.html', machines=virtual_machines)

@app.route('/api/auto-claim-vmos', methods=['POST'])
def auto_claim_vmos():
    try:
        # Giả lập quá trình tạo email và gọi API nhận máy tự động
        time.sleep(1.5)
        fake_email = f"user_{random.randint(10000, 99999)}@uberip.com"
        
        time.sleep(1)
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
            "message": "Tự động nhận máy thành công!",
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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
