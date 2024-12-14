import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def log_error(error_message, function_name=None, input_params=None, file_path=None):
    logging.basicConfig(filename='error_log.txt', level=logging.ERROR,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    log_message = error_message
    if function_name:
        log_message += f" | Function: {function_name}"
    if input_params:
        log_message += f" | Input Parameters: {input_params}"
    if file_path:
        log_message += f" | File Path: {file_path}"
    logging.error(log_message)

def send_error_log_to_centralized_system(error_message, recipient_email):
    sender_email = "your_email@example.com"
    sender_password = "your_password"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Error Log Report"

    body = MIMEText(error_message, 'plain')
    msg.attach(body)

    try:
        server = smtplib.SMTP('smtp.example.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Failed to send error log report: {e}")
