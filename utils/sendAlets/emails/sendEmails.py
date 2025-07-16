import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email details
sender_email = "raghunandan1016.in@gmail.com"
receiver_email = "contact.mrsuraj@gmail.com"
password = "pnag ptue ymoc wujh"

# Connect to the SMTP server
smtp_server = "smtp.gmail.com"
port = 587

def main():
    # Validate email addresses
    if not validate_email(sender_email):
        print("Invalid sender email address.")
        exit(1)

    if not validate_email(receiver_email):
        print("Invalid receiver email address.")
        exit(1)

    # Prompt the user for the email subject and body
    subject = input("Enter the email subject: ")
    body = input("Enter the email body: ")

    # Send the email
    send_email(subject, body, receiver_email)


def validate_email(email):
    # Simple regex to check if an email address is valid
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def send_email(subject, body, recipient):
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient
    msg.attach(MIMEText(body, "plain"))

    try:
        s = smtplib.SMTP(smtp_server, port)
        s.starttls()
        s.login(sender_email, password)
        s.sendmail(sender_email, recipient, msg.as_string())
        print("Email sent successfully!")
    except smtplib.SMTPAuthenticationError:
        print("Failed to authenticate. Check your email address and password.")
    except smtplib.SMTPRecipientsRefused:
        print("The recipient's email address was refused.")
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        s.quit()

if __name__ == "__main__":
    main()