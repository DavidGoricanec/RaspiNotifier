import requests
import telegram_send
import mysql.connector as mariadb

mariadb_connection = mariadb.connect(user='raspi', password='raspi', database='fachhochschule')
cursor = mariadb_connection.cursor(buffered=True)

cursor.execute("SELECT max(ip_adr) FROM myIP")
old_ip = cursor.fetchone()[0]
new_ip = requests.get('http://ip.42.pl/raw').text

print("Old_IP: ",old_ip," New_IP: ",new_ip)
if old_ip == new_ip:
    print("IPs are the same - do nothing")
else:
    cursor.execute("DELETE FROM myIP")
    cursor.execute("INSERT INTO myIP (ip_adr) VALUES (%s)",(new_ip,))
    mariadb_connection.commit()
    telegram_send.send(messages=["Neue IP: " + new_ip+":3389"])
    print("New IP added to DB and send to user")

mariadb_connection.close()