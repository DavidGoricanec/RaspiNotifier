#!/bin/bash
echo start script RaspiNotifierShell

echo start download_cal.py
python3 /home/pi/Dokumente/RaspiNotifier/download_cal.py

echo start Kalender_ins_upd_DB
python3 /home/pi/Dokumente/RaspiNotifier/Kalender_ins_upd_DB.py

echo start user_benachrichtigen
python3 /home/pi/Dokumente/RaspiNotifier/user_benachrichtigen.py

echo end script RaspiNotifier
