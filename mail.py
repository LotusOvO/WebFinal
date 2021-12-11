from flask_mail import Message, Mail
from app import app
from threading import Thread

# autgomifpcfwdgce imap

# uuwrxrlcgjymdfce pop3

app.config["MAIL_SERVER"] = "smtp.qq.com"
app.config["MAIL_PORT"] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config["MAIL_USERNAME"] = 'lotusovo@foxmail.com'
app.config["MAIL_PASSWORD"] = 'autgomifpcfwdgce'
mail = Mail(app)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def Sendmail(context, mailaddr):
    msg = Message("购买订单", sender='lotusovo@foxmail.com',
                  recipients=[mailaddr])
    msg.body = context
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return True

