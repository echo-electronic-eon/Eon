import smtplib
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import time

def check_internet():
    try:
        response = requests.get('http://www.google.com', timeout=5)
        return True
    except requests.ConnectionError:
        return False

def send_email():
    from_email = 'echo@echo-electronic-eon.ru'
    to_email = 'check@echo-electronic-eon.ru'
    password = '@Af7Z4tiqA#XEYeJDvJs'

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "Malina online"

    body = f"When: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.abcde.ru', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Имейл отправлен")
        return True
    except Exception as e:
        print(f"Имейл не отправлен: {e}")
        return False

def main():
    connection_lost = False
    while True:
        if check_internet():
            if connection_lost:
                if send_email():
                    connection_lost = False
        else:
            connection_lost = True
        time.sleep(60)

if __name__ == "__main__":
    main()


