import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def main():
    email = "siyagour105@gmail.com"
    subject = "BOT FOUND SAT TEST CENTER AVAILABLE"
    body = "This is a test email sent from Python using smtplib."
    sender = "diamondjetzrule@gmail.com"
    password = "rzaoypgdnrdumtvi"
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = email
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    # Convert message to string
    text = message.as_string()
    try: 
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, email, text)

        server.sendmail(sender, email, text)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        server.quit()

if __name__ == "__main__":
    main()