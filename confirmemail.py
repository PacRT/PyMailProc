__author__ = 'chiradip'
#Import smtplib for the actual sending function
import smtplib, redis, json, sys, logging

# Import the email modules we'll need
from email.mime.text import MIMEText

logging.basicConfig(filename='/var/log/confirmmemail.log',level=logging.DEBUG)

logging.debug("Starting up....")

s = smtplib.SMTP('192.168.1.2')

r = redis.Redis()
p = r.pubsub()

p.subscribe("RegReqConfEmail")

def sendmail(json_msg):
    try:
        name = json_msg['name']
    except:
        name = "There"

    msg = MIMEText("Hello " + name + "!!! Thanks for the registration request. Check your email for further actions. It may take longer due to system load and verification.")
    msg['Subject'] = "Paperless CLub registration request confirmation message"
    msg['To'] = json_msg['email']
    msg['Bcc'] = "chiradip@chiradip.com"
    msg['From'] = "registrar@paperlessclub.org"
    s.send_message(msg)

def sendconfemail(msg):
    logging.debug(str(msg))
    try:
        j_son = msg.decode('utf-8')
        vj_son = json.loads(j_son)
        logging.debug(vj_son)
        sendmail(vj_son)
    except AttributeError:
        logging.debug(msg, " :: Possibly the literal is not string and cannot be treated as JSON")
    except ValueError:
        logging.debug("Possible illegal JSON structure")
    except:
        logging.debug("something wrong", sys.exc_info())


for message in p.listen():
    sendconfemail(message['data'])

# while True:
#     msg = p.get_message()
#     if msg:
#         sendconfemail(msg['data'])
#     time.sleep(0.001)

p.close()

s.quit()

