from tinydb import TinyDB, Query
import time
import smtplib, ssl
from datetime import datetime
import easyimap as imap


#probably only one of these is needed but i cant figure out which one and im sick of this so heres everything


db = TinyDB('usersdb.json')


def createTable():
    user1 = {"name": "Default", "tagId": "1A 1A 1A 1A", "temperature": 22, "light": 3000,
             "profile": "https://animesher.com/orig/0/3/32/328/animesher.com_hakase-sad-nichijou-32839.jpg"}
    user2 = {"name": "Deema", "tagId": "C3 6D D8 0B", "temperature": 22.5, "light": 3500,
             "profile": "https://d.newsweek.com/en/full/822411/pikachu-640x360-pokemon-anime.jpg?w=1600&h=1600&q=88&f=b65592079ef009b8b80897ddb8660b29"}
    user3 = {"name": "Christian", "tagId": "C3 5F 24 11", "temperature": 21, "light": 3500,
             "profile": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTxTaw9tHoCyvyEPdWHUtTHdPk203cmsBLSkRYyjLVoNg4XvbPWpChyY04gg5B45BNj_Hg&usqp=CAU"}
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
    if db.contains(authorizedUsers.tagId == inputTagId) == False:
        return False
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

def getDefaultUser():
    authorizedUsers = Query()
    currentUser = db.get(authorizedUsers.name == "Default")
    print(currentUser)
    return currentUser

createTable()