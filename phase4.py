from tinydb import TinyDB, Query
import time
import smtplib, ssl
from datetime import datetime
import easyimap as imap


#probably only one of these is needed but i cant figure out which one and im sick of this so heres everything


db = TinyDB('usersdb.json')


def createTable():
    user1 = {"name": "Default", "tagId" : "1A 1A 1A 1A", "temperature" : 22, "light" : 3000}
    user2 = {"name": "Deema", "tagId" : "C3 6D D8 0B", "temperature" : 21.1, "light" : 3500}
    user3 = {"name": "Christian", "tagId" : "C3 5F 24 11", "temperature" : 24.5, "light" : 3500}
    db.truncate()
    db.insert(user1)
    db.insert(user2)
    db.insert(user3)
    print("Table has been created!")

# EMAIL
port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "iotPain2002@gmail.com"
receiver_email = "iotPain2002@gmail.com"
password = "IOT123testingclass"

def sendUserEmail(username, tagId):
    print("Sending email...")
    context = ssl.create_default_context()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    message = """Subject: User has entered\


    The user, {}, with tag ID {} has entered at {}
    """.format(username,tagId,current_time)
    #.format(sender_email, receiver_email, message)
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    print("Email sent successfully!")


def verifyUser(inputTagId):
    print("You are now being authenticated...")
    authorizedUsers = Query()
    currentUser = db.get(authorizedUsers.tagId == inputTagId)

    if currentUser:
        print("Authentication completed successfully.")
        name = currentUser['name']
        currTagId = currentUser['tagId']
        print("Welcome, " + name + "! Your Tag ID is: " + currTagId + ".")
        sendUserEmail(name, currTagId)
        return currentUser

    else:
        print("Authorization failed. You do not have access. gtfo")
        return False

def getDefaultUserjs():
    authorizedUsers = Query()
    currentUser = db.get(authorizedUsers.name == "Default")
    print(currentUser)
    return currentUser

#createTable()