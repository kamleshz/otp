from flask import Flask, request, jsonify
from email.message import EmailMessage
import smtplib
import random
import time

# CONFIGURATION
GMAIL_USER = "eprsyncaagarg@gmail.com"               
GMAIL_APP_PASSWORD = "phrmtxwvkmmsqpbv"      
RECIPIENT_EMAIL = "Kamlesh.zore@aagarg.in"
OTP_EXPIRY = 300                             

# OTP Store
otp_data = {"otp": None, "timestamp": 0}

app = Flask(__name__)

@app.route("/send-otp", methods=["GET"])
def send_otp():
    otp = str(random.randint(100000, 999999))
    otp_data["otp"] = otp
    otp_data["timestamp"] = time.time()

    msg = EmailMessage()
    msg.set_content(f"Your one-time password is: {otp}")
    msg["Subject"] = "Your Excel OTP"
    msg["From"] = GMAIL_USER
    msg["To"] = RECIPIENT_EMAIL

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            smtp.send_message(msg)
        return jsonify({"status": "sent"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/verify-otp", methods=["POST"])
def verify_otp():
    input_otp = request.json.get("otp")
    if not otp_data["otp"]:
        return "NO_OTP"

    if time.time() - otp_data["timestamp"] > OTP_EXPIRY:
        return "EXPIRED"

    if input_otp == otp_data["otp"]:
        return "VALID"
    return "INVALID"

if __name__ == "__main__":
    app.run(port=5000)
