import random
from flask import Flask, jsonify, render_template

app = Flask(__name__)

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
  # Tạm thời trả về danh sách trống để web không bị xoay
  return jsonify([])


if __name__ == "__main__":
  app.run(debug=True, port=5000)
