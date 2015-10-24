
from flask.ext.mail import Message
from storaage import app, mail

def send_email(send_to, subject, template):
    msg = Message(subject, recipients=[send_to], html=template,
                    sender='human@storaage.io')
    mail.send(msg)

    #think this is DONE
