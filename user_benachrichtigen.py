#!/usr/bin/python
import smtplib, ssl
import mysql.connector as mariadb
import telegram_send

#print("user benachrichtigung start")

#Variablen
mariadb_connection = mariadb.connect(user='raspi', password='raspi', database='fachhochschule')
cursor = mariadb_connection.cursor(buffered=True)

port = 465  # For SSL
sender_email = "GoricanecRasPi@gmail.com"
receiver_emails = ["GoricanecRasPi@gmail.com", "ownifty@gmail.com"]
text= "Das steht in deinem Kalender:"
emailmessage = ("""\
Subject: RaspberryPi-Kalender

""")


cursor.execute("""SELECT endzeit, bezeichnung, beschreibung FROM kalender
                  WHERE (prioritaet = 'H' AND endzeit > NOW()- INTERVAL 1 DAY AND endzeit <= (NOW() + INTERVAL 10 DAY))
                     OR (prioritaet = 'M' AND endzeit > NOW()- INTERVAL 1 DAY AND endzeit <= (NOW() + INTERVAL 7 DAY))
                     OR (prioritaet = 'L' AND endzeit > NOW()- INTERVAL 1 DAY AND endzeit <= (NOW() + INTERVAL 3 DAY))
                     OR (prioritaet = 'C' AND endzeit > NOW()- INTERVAL 1 DAY AND endzeit <= (NOW() + INTERVAL 1 DAY))
                  ORDER BY endzeit;""")
if cursor.rowcount == 0:
    print("Done: Keine Daten zu senden")
else:
    for endzeit,bezeichnung,beschreibung, in cursor:
        text = text + "\nAm: " + endzeit.strftime("%Y-%m-%d") + "\n" + bezeichnung + "\n" + beschreibung + "\n"

    text = text + "\nGesendet mit ❤ von deinem Raspberry Pi"

    #EMail
    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("GoricanecRasPi@gmail.com", "GoricanecRasPiDevelopment")
        #new and empty google account. If you're comming from github and you wanna see my account, do it. It only has development-testmails

        emailmessage = emailmessage + text
        emailmessage = emailmessage.encode('utf-8')
        #print(emailmessage)

        for rec in receiver_emails:
            server.sendmail(sender_email, rec, emailmessage)
        server.close()
    print("Done: Email(s) gesendet")

    #Telegram
    telegram_send.send(messages=[text])
    print("Nachricht(en) gesendet")