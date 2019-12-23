#!/usr/bin/python
import mysql.connector as mariadb

mariadb_connection = mariadb.connect(user='raspi', password='raspi', database='fachhochschule')
cursor = mariadb_connection.cursor()

bezeichnung = "TEST"
cursor.execute("SELECT kal_id,event_typ,lehrveranstaltung,bezeichnung,beschreibung,startzeit,endzeit FROM kalender WHERE bezeichnung=%s", (bezeichnung,))

#selecting
for kal_id,event_typ,lehrveranstaltung,bezeichnung,beschreibung,startzeit,endzeit in cursor:
    print(("Kal_id: {}, event_typ: {}").format(kal_id,event_typ))