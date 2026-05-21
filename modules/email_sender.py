import smtplib
import logging
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()

logger = logging.getLogger(__name__)

def send_report(recipient_email: str, subject : str, body:str, pdf_path: str) -> bool:
    """"
    Sends an email with PDF report attached
    
    Args:
        receipient email: Emaild addresss of the receiver
        subject : Email subject line
        body: Email body text
        pdf_path : Path of the pdf file to attach
    
    Returns:
        True if email sent successfully.
    """
    try:
        # Load credentials from .env
        sender_email = os.getenv("EMAIL_ADDRESS")
        sender_password = os.getenv("EMAIL_PASSWORD")

        if not sender_email or not sender_password:
            raise ValueError("Email address or Email password not found in .env file")
        
        # Create email object
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject

        # Attach email body as plain text
        msg.attach(MIMEText(body, "plain"))

        # Attach PDF file
        with open(pdf_path, "rb") as pdf_file:
            attachment = MIMEBase("application", "octet-stream")
            attachment.set_payload(pdf_file.read())
            encoders.encode_base64(attachment)
            attachment.add_header("Content-Disposition", f"attachment; filename ={os.path.basename(pdf_path)}")
            msg.attach(attachment)
        
        # Connect to Gmail SMTP and send
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        
        logger.info(f"Email sent to: {recipient_email}")
        return True
    
    except  Exception as e:
        logger.error(f" Failed to send email: {e}")
        raise