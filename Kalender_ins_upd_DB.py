#!/usr/bin/python
import mysql.connector as mariadb
from icalendar import Calendar, Event
import re

def get_prioritaet(bez, besch):
    x = re.search("[C,c]ancel|[A,a]bgesagt", bez)
    if x:
        return "C"

    txt = str(bez) + " " + str(besch) #full text
    x = re.search("[P,p]r[ü,u]e?fung|[K,k]lausur|[T,t]est|[A,a]bschlu[ss,ß]arbeit", txt)

    if x:
        return "H"
    x = re.search("[A,a]bgabe|[P,p]r[ä,a]e?sentation|ist *f[ä,a]e?llig", txt)
    if x:
        return "M"
    return "L"

#print("Kalender_ins_upd_DB start")

mariadb_connection = mariadb.connect(user='raspi', password='raspi', database='fachhochschule')
cursor = mariadb_connection.cursor(buffered=True)

#some stats for logging
inserted = 0
updated = 0

#read ics file
g = open('/home/pi/Dokumente/RaspiNotifier/kalender.ics','rb')
gcal = Calendar.from_ical(g.read())
for component in gcal.walk():
    if component.name == "VEVENT":
        #um vtext zu string umzuwandeln verwenden wir str
        #mit dt und strftime bekommen wir das datum in einem string welches das richtig format hat

        bezeichnung = str(component.get('summary'))
        startzeit = component.get('dtstart').dt.strftime("%Y-%m-%d")
        endzeit = component.get('dtend').dt.strftime("%Y-%m-%d")
        uid = str(component.get('uid'))
        beschreibung = str(component.get('description'))

        #testausgabe um zu sehen ob die Daten passen
        #print("Bezeichnung: " + bezeichnung + " | startzeit: " + startzeit + " | endzeit: " + endzeit)
        #print("uid: " + uid)
        #print("beschreibung: " + beschreibung)

        #check if data exists
        cursor.execute("SELECT kal_id FROM kalender WHERE uid = %s", (uid,))
        if cursor.rowcount == 0:
            #insert - data doesn't exists
            #print("inserting uid: " + uid)
            cursor.execute("INSERT INTO kalender (event_typ,bezeichnung,beschreibung,startzeit,endzeit,uid,prioritaet) VALUES ('FH',%s,%s,%s,%s,%s,%s)", (bezeichnung,beschreibung,startzeit,endzeit,uid,get_prioritaet(bezeichnung,beschreibung)))
            inserted = inserted + 1
        else:
            #update
            kal_id = cursor.fetchone()[0]
            #print("updateing uid: " + uid + " | kal_id: " + str(kal_id))
            cursor.execute("UPDATE kalender SET event_typ = 'FH',bezeichnung = %s, beschreibung = %s, startzeit = %s, endzeit = %s , prioritaet = %s WHERE kal_id = %s", (bezeichnung,beschreibung,startzeit,endzeit,get_prioritaet(bezeichnung,beschreibung),kal_id))
            updated = updated + 1
#festschreiben der änderungen
mariadb_connection.commit()
print("Data commited; Inserted: "+ str(inserted) + " | updated: " + str(updated))
g.close()
mariadb_connection.close()