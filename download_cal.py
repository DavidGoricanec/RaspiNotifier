import urllib.request

print('Downloading calender file...')

# Contains download link of file
url = 'https://elearning.fh-joanneum.at/calendar/export_execute.php?userid=2629&authtoken=beb91d35194fc3177ed3b57ae34608829bf15b09&preset_what=all&preset_time=monthnow'

# Downloads file using download link as first parameter and destination as second paramter
urllib.request.urlretrieve(url, '/home/pi/Dokumente/RaspiNotifier/kalender.ics')

print('finished')