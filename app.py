import streamlit as st
from email.message import EmailMessage
import smtplib
import random
import time

# CONFIGURATION
GMAIL_USER = "eprsyncaagarg@gmail.com"
GMAIL_APP_PASSWORD = "phrmtxwvkmmsqpbv"
RECIPIENT_EMAIL = "Kamlesh.zore@aagarg.in"
OTP_EXPIRY = 300  # seconds

# OTP Store
otp_data = {"otp": None, "timestamp": 0}

st.set_page_config(page_title="OTP Verification", page_icon="🔒")

st.title("🔒 Excel OTP Verification")
st.write("Send OTP to Email and Verify")

# --- Send OTP Section ---
if st.button("Send OTP to Email"):
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
        st.success("✅ OTP has been sent to your email.")
    except Exception as e:
        st.error(f"❌ Failed to send OTP: {str(e)}")

# --- Verify OTP Section ---
st.subheader("Enter OTP to Verify")
input_otp = st.text_input("OTP", max_chars=6)

if st.button("Verify OTP"):
    if not otp_data["otp"]:
        st.warning("⚠️ No OTP sent yet. Please send OTP first.")
    elif time.time() - otp_data["timestamp"] > OTP_EXPIRY:
        st.error("⏰ OTP has expired. Please request a new one.")
    elif input_otp == otp_data["otp"]:
        st.success("✅ OTP Verified Successfully!")
    else:
        st.error("❌ Invalid OTP. Please try again.")

