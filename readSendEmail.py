import easyimap as imap
import smtplib, ssl
from datetime import datetime

user = "iotPain2002@gmail.com"
pw = "IOT123testingclass"
port = 587  # For starttls
smtp_server = "smtp.gmail.com"

# Method to send Email to the user with the light status
def sendEmailLight():
    context = ssl.create_default_context()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    message = """Subject: Light\


    The light is ON at at {}
    """.format(current_time)
    #.format(sender_email, receiver_email, message)
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(user, pw)
        server.sendmail(user, user, message)

# Method to read the email and check if the user wants to turn on the fan
def readEmail():
    server = imap.connect("imap.gmail.com", user, pw)
    server.change_mailbox("Temperature")
    server.listids()
    email = server.mail(server.listids()[0])
    return email.body.strip()[0:3].lower() == 'yes'

# Method to send Email to the user with the temperature
def sendEmailTemperature(temperature):
    context = ssl.create_default_context()
    message = """Subject: Temperature\


    The temperature is {}. Do you want to turn on the fan?
    """.format(temperature)
    #.format(sender_email, receiver_email, message)
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(user, pw)
        server.sendmail(user, user, message)