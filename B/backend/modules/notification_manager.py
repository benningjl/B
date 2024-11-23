import smtplib
from email.message import EmailMessage

class NotificationManager:
    def __init__(self, smtp_server='smtp.example.com', port=587, username='your_email@example.com', password='your_password'):
        self.smtp_server = smtp_server
        self.port = port
        self.username = username
        self.password = password

    def send_email(self, to_email, subject, body):
        try:
            msg = EmailMessage()
            msg['From'] = self.username
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.set_content(body)

            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            print("Email sent successfully.")
        except Exception as e:
            print(f"Failed to send email: {e}")
