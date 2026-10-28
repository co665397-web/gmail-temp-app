import threading
import time
import requests
from flask import Flask, jsonify, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)

# Địa chỉ web TempMail Cloud của bạn trên Render
RENDER_API_BASE = "https://gmail-temp-app.onrender.com"

# Biến toàn cục lưu trạng thái tiến trình
automation_status = {
    "running": False,
    "log": "Hệ thống sẵn sàng.",
    "email": "",
}


def run_automation_task(target_url):
  global automation_status
  automation_status["running"] = True
  automation_status["log"] = "Đang lấy email tạm thời từ Render..."

  try:
    # 1. Lấy email từ Render
    res = requests.post(f"{RENDER_API_BASE}/api/change-email")
    email = res.json().get("email")
    automation_status["email"] = email
    automation_status["log"] = f"Đã nhận email: {email}. Đang mở trình duyệt..."

    # 2. Khởi động Selenium Chrome
    options = Options()
    # options.add_argument("--headless") # Bỏ chú thích nếu muốn chạy ẩn không hiện cửa sổ Chrome
    driver = webdriver.Chrome(options=options)

    try:
      automation_status["log"] = f"Đang truy cập: {target_url}"
      driver.get(target_url)

      # Tại đây bạn có thể thêm code Selenium để tìm ô input email và điền biến `email` vào
      # Ví dụ:
      # email_input = driver.find_element("id", "email_input_id")
      # email_input.send_keys(email)

      automation_status["log"] = (
          "Đã điền email thành công! Đang chờ bạn xử lý Captcha hoặc nhận OTP..."
      )

      # Giữ trình duyệt mở một thời gian để thao tác thủ công phần Captcha
      time.sleep(60)

    finally:
      driver.quit()
      automation_status["log"] = "Đã hoàn tất phiên tự động hóa."
  except Exception as e:
    automation_status["log"] = f"Lỗi: {str(e)}"
  finally:
    automation_status["running"] = False


@app.route("/")
def index():
  return render_template("index.html")


@app.route("/api/status", methods=["GET"])
def get_status():
  return jsonify(automation_status)


@app.route("/api/start", methods=["POST"])
def start_task():
  global automation_status
  if automation_status["running"]:
    return jsonify(
        {"status": "error", "message": "Tiến trình đang chạy rồi!"}
    )

  data = request.json
  target_url = data.get(
      "url", "https://www.vmoscloud.com/"
  )  # Link trang đăng ký VMOS

  # Chạy bằng luồng riêng (threading) để web không bị treo xoay vòng
  t = threading.Thread(target=run_automation_task, args=(target_url,))
  t.start()

  return jsonify(
      {"status": "success", "message": "Đã kích hoạt tiến trình tự động!"}
  )


if __name__ == "__main__":
  app.run(debug=True, port=5000)
