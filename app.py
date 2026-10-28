import datetime
import random
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Biến lưu trữ trạng thái máy ảo VMOS hiện tại
vmos_session = {
    "status": "Chưa khởi động",  # Chưa khởi động / Đang chạy / Đã kết thúc
    "created_at": None,
    "expires_at": None,
    "instance_id": None,
}


@app.route("/")
def index():
  return render_template("index.html")


@app.route("/api/vmos/status", methods=["GET"])
def get_vmos_status():
  """Lấy trạng thái hiện tại của phiên VMOS và kiểm tra thời hạn 2 giờ"""
  global vmos_session
  if vmos_session["status"] == "Đang chạy" and vmos_session["expires_at"]:
    now = datetime.datetime.now()
    if now > vmos_session["expires_at"]:
      vmos_session["status"] = "Hết hạn (Quá 2 giờ)"

  return jsonify(vmos_session)


@app.route("/api/vmos/start", methods=["POST"])
def start_vmos():
  """Kích hoạt phiên máy ảo VMOS Cloud mới (Thời hạn 2 giờ)"""
  global vmos_session
  try:
    now = datetime.datetime.now()
    expires = now + datetime.timedelta(hours=2)

    # Giả lập khởi tạo phiên máy ảo thành công
    vmos_session = {
        "status": "Đang chạy",
        "created_at": now.strftime("%H:%M:%S - %d/%m/%Y"),
        "expires_at": expires,
        "expires_str": expires.strftime("%H:%M:%S - %d/%m/%Y"),
        "instance_id": f"VMOS-CLD-{random.randint(10000, 99999)}",
    }

    return jsonify({
        "status": "success",
        "message": "Đã tạo phiên máy ảo VMOS Cloud 2 giờ thành công!",
        "data": vmos_session,
    })
  except Exception as e:
    return jsonify(
        {"status": "error", "message": f"Lỗi tạo máy ảo: {str(e)}"}
    ), 500


@app.route("/api/vmos/stop", methods=["POST"])
def stop_vmos():
  """Dừng phiên máy ảo VMOS"""
  global vmos_session
  vmos_session = {
      "status": "Đã dừng thủ công",
      "created_at": None,
      "expires_at": None,
      "instance_id": None,
  }
  return jsonify({"status": "success", "message": "Đã dừng phiên máy ảo VMOS."})


if __name__ == "__main__":
  app.run(debug=True, port=5000)
