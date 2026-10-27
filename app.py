import email
import imaplib
import random
import re
from email.header import decode_header
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

GMAIL_USER = "vinhvuive12312@gmail.com"
GMAIL_APP_PASSWORD = "lujk radr dihe tyuc"
IMAP_SERVER = "imap.gmail.com"

# Khởi tạo alias ngẫu nhiên ngay khi chạy
current_alias_prefix = f"vinhvuive12312+vmos{random.randint(100000, 999999)}"


@app.route("/")
def index():
  return render_template("index.html")


@app.route("/api/get-email", methods=["GET"])
def get_email():
  return jsonify({"email": f"{current_alias_prefix}@gmail.com"})


@app.route("/api/change-email", methods=["POST"])
def change_email():
  global current_alias_prefix
  current_alias_prefix = f"vinhvuive12312+vmos{random.randint(100000, 999999)}"
  return jsonify({"email": f"{current_alias_prefix}@gmail.com"})


@app.route("/api/messages", methods=["GET"])
def get_messages():
  try:
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(GMAIL_USER, GMAIL_APP_PASSWORD.replace(" ", ""))
    mail.select("inbox")

    status, messages = mail.search(None, "ALL")
    if status != "OK":
      mail.logout()
      return jsonify([])

    mail_ids = messages[0].split()
    recent_ids = mail_ids[-5:][::-1]

    message_list = []
    for num in recent_ids:
      status, msg_data = mail.fetch(
          num, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])"
      )
      if status != "OK":
        continue

      for response_part in msg_data:
        if isinstance(response_part, tuple):
          msg = email.message_from_bytes(response_part[1])
          subject, encoding = decode_header(msg["Subject"])[0]
          if isinstance(subject, bytes):
            subject = subject.decode(
                encoding if encoding else "utf-8", errors="ignore"
            )

          message_list.append({
              "id": num.decode("utf-8"),
              "from": msg.get("From"),
              "subject": subject or "(Không có tiêu đề)",
              "date": msg.get("Date"),
          })

    mail.logout()
    return jsonify(message_list)
  except Exception as e:
    print(f"Lỗi IMAP: {e}")
    return jsonify([])


@app.route("/api/read", methods=["GET"])
def read_message():
  msg_id = request.args.get("id")
  if not msg_id:
    return jsonify({"error": "Thiếu ID thư"}), 400

  try:
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(GMAIL_USER, GMAIL_APP_PASSWORD.replace(" ", ""))
    mail.select("inbox")

    status, msg_data = mail.fetch(msg_id.encode(), "(RFC822)")
    if status != "OK":
      mail.logout()
      return jsonify({"error": "Không tìm thấy thư"}), 404

    raw_html_or_text = ""
    for response_part in msg_data:
      if isinstance(response_part, tuple):
        msg = email.message_from_bytes(response_part[1])
        if msg.is_multipart():
          for part in msg.walk():
            if part.get_content_type() in ["text/plain", "text/html"]:
              payload = part.get_payload(decode=True)
              if payload:
                charset = part.get_content_charset() or "utf-8"
                try:
                  raw_html_or_text += (
                      payload.decode(charset, errors="ignore") + "\n"
                  )
                except:
                  raw_html_or_text += (
                      payload.decode("latin-1", errors="ignore") + "\n"
                  )
        else:
          payload = msg.get_payload(decode=True)
          if payload:
            charset = msg.get_content_charset() or "utf-8"
            try:
              raw_html_or_text = payload.decode(charset, errors="ignore")
            except:
              raw_html_or_text = payload.decode("latin-1", errors="ignore")
          else:
            raw_html_or_text = str(msg.get_payload())

    mail.logout()

    clean_text = re.sub(
        r"<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>",
        "",
        raw_html_or_text,
        flags=re.IGNORECASE,
    )
    clean_text = re.sub(
        r"<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>",
        "",
        clean_text,
        flags=re.IGNORECASE,
    )
    clean_text = re.sub(r"<[^>]+>", "", clean_text)
    clean_text = re.sub(r"[ \t]+", " ", clean_text)
    clean_text = re.sub(r"\n\s*\n", "\n\n", clean_text).strip()

    return jsonify({"rawText": clean_text or "Thư trống."})
  except Exception as e:
    return jsonify({"rawText": f"Lỗi đọc nội dung thư: {e}"})


if __name__ == "__main__":
  app.run(debug=True, port=5000)
