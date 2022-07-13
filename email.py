
from flask_mail import Message
from agri_app import mail


from flask import render_template


def send_email(to, subject, template):
    msg = Message(subject,
                  sender='americ474@gmail.com', recipients=[to])
    msg.body = render_template(template + '.txt')
    msg.html = render_template(template + '.html')
    mail.send(msg)


