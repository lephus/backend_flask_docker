from flask_mail import Message
from app import mail
from flask_mail import Mail
from flask import Flask

app = Flask(__name__)
msg = Message('test subject', 'gr3atcode@gmail.com',
recipients=['phulealali@gmail.com'])
msg.body = 'text body'
msg.html = '<h1>HTML body</h1>'
mail.send(msg)