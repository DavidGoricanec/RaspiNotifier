#!/usr/bin/python
import mysql.connector as mariadb
from icalendar import Calendar, Event

mariadb_connection = mariadb.connect(user='raspi', password='raspi', database='fachhochschule')
cursor = mariadb_connection.cursor(buffered=True)

#selecting
#for kal_id,event_typ,bezeichnung,beschreibung,startzeit,endzeit in cursor:
#    print(("Kal_id: {}, event_typ: {}").format(kal_id,event_typ))

#read ics file
g = open('/home/pi/Dokumente/RaspiNotifier/kalender.ics','rb')
gcal = Calendar.from_ical(g.read())
for component in gcal.walk():
    if component.name == "VEVENT":
        bezeichnung = component.get('summary')
        startzeit = component.get('dtstart').dt
        endzeit = component.get('dtend').dt
        uid = component.get('uid')
        beschreibung = component.get('description')

        #testausgabe um zu sehen ob die Daten passen
        #print("Bezeichnung: " + bezeichnung + " | startzeit: " + startzeit.strftime("%m/%d/%Y, %H:%M:%S") + " | endzeit: " + endzeit.strftime("%m/%d/%Y, %H:%M:%S"))
        print("uid: " + uid)
        #print("beschreibung: " + beschreibung)

        #check if data exists
        cursor.execute("SELECT kal_id FROM kalender WHERE uid = %s", (str(uid),))
        if cursor.rowcount == 0:
            #insert
            print("inserting uid: " + uid)
        else:
            #update
            kal_id = cursor.fetchone()
            print("updateing uid: " + uid + " | kal_id: " + kal_id)
g.close()