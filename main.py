import requests
import smtplib
import pytz
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 디스코드 초대 코드 (예: https://discord.gg/abcd1234 → abcd1234)
INVITE_CODE = os.environ.get("DISCORD_INVITE_CODE")

# 이메일 설정
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")   # Gmail 앱 비밀번호
TO_EMAIL = "jasuil@daum.net"

def check_invite():
    url = f"https://discord.com/api/v10/invites/{INVITE_CODE}?with_counts=true&with_expiration=true"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get("expires_at") is None:
            print("만료일 없음")
            return True
        dt = datetime.fromisoformat(data.get("expires_at"))
        kst = pytz.timezone("Asia/Seoul")
        dt = dt.astimezone(kst)
        if dt > datetime.now(kst):
            print("초대링크는 만료되지 않았습니다.")
            return False
        else:
            print("초대링크가 만료되었습니다.")
            print(data.get("expires_at"))
            return True
    else:
        print("초대링크가 유효하지 않습니다 (이미 만료됨).")
        return True

def send_email():
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL
    msg["Subject"] = "디스코드 초대링크 만료 알림"

    body = "디스코드 초대링크가 만료되었습니다. 새로운 링크를 생성하세요."
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

if __name__ == "__main__":
    if check_invite():
        send_email()
