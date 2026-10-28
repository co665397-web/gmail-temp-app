import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Địa chỉ trang web TempMail Cloud của bạn trên Render
RENDER_API_BASE = "https://gmail-temp-app.onrender.com"


def get_new_temp_email():
  """Lấy một địa chỉ email tạm thời mới từ web Render của bạn"""
  try:
    response = requests.post(f"{RENDER_API_BASE}/api/change-email")
    data = response.json()
    email = data.get("email")
    print(f"[+] Đã tạo và lấy email thành công: {email}")
    return email
  except Exception as e:
    print(f"[-] Lỗi khi gọi API lấy email: {e}")
    return None


def get_latest_otp_or_content():
  """Quét hộp thư trên Render để lấy nội dung mã OTP"""
  try:
    response = requests.get(f"{RENDER_API_BASE}/api/messages")
    messages = response.json()
    if messages and len(messages) > 0:
      latest_msg = messages[0]
      msg_id = latest_msg["id"]
      subject = latest_msg["subject"]
      print(f"[+] Tìm thấy thư mới: {subject}")

      # Đọc nội dung chi tiết thư
      detail_res = requests.get(f"{RENDER_API_BASE}/api/read?id={msg_id}")
      content = detail_res.json().get("rawText", "")
      return content
  except Exception as e:
    print(f"[-] Lỗi quét hộp thư: {e}")
  return None


def run_vmos_automation():
  # 1. Lấy email tạm thời từ hệ thống Render
  email = get_new_temp_email()
  if not email:
    return

  # 2. Khởi động trình duyệt tự động trên máy tính
  options = webdriver.ChromeOptions()
  # Bỏ dòng dưới đây nếu bạn muốn nhìn thấy trình duyệt thao tác trực tiếp trên màn hình
  # options.add_argument("--headless")

  driver = webdriver.Chrome(options=options)

  try:
    print("[*] Đang truy cập trang đăng ký VMOS...")
    driver.get(
        "https://www.vmoscloud.com/"
    )  # Thay thế bằng đường dẫn trang đăng ký thực tế của VMOS

    # --- KHU VỰC ĐIỀN THÔNG TIN TỰ ĐỘNG ---
    # Ví dụ: Chờ ô nhập email xuất hiện và điền email tạm thời vào
    # wait = WebDriverWait(driver, 15)
    # email_input = wait.until(EC.presence_of_element_located((By.ID, "email-input-field-id")))
    # email_input.send_keys(email)

    print(
        "[*] Đã điền email. Đang chờ bạn xử lý captcha kéo trượt (nếu có) hoặc"
        " chờ mã OTP gửi tới..."
    )

    # 3. Vòng lặp chờ mã OTP từ hộp thư Render
    otp_code = None
    for i in range(30):  # Chờ tối đa 3 phút (30 lần * 6 giây)
      time.sleep(6)
      content = get_latest_otp_or_content()
      if content:
        print(f"[*] Nội dung thư nhận được:\n{content}")
        # Tại đây bạn có thể dùng Regex để lọc lấy mã OTP số (ví dụ 6 chữ số)
        break

    print("[*] Hoàn thành quy trình tự động!")

  except Exception as e:
    print(f"[-] Lỗi trong quá trình chạy automation: {e}")
  finally:
    # Giữ trình duyệt mở một lúc để quan sát
    time.sleep(10)
    driver.quit()


if __name__ == "__main__":
  run_vmos_automation()
