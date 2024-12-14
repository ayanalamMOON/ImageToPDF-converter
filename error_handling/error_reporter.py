import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def report_error(error_message, recipient_email):
    sender_email = "your_email@example.com"
    sender_password = "your_password"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Error Report"

    body = MIMEText(error_message, 'plain')
    msg.attach(body)

    try:
        server = smtplib.SMTP('smtp.example.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Failed to send error report: {e}")
