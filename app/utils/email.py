from app import mail

from flask_mail import Message

# Function to send an email
def send_email(to, subject, template):
    msg = Message( subject, recipients=[to], html=template, sender="noreply@chowforex.com")
    mail.send(msg)