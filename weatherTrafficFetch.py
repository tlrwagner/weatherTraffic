import pyowm, requests, json, time, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#getting weather data
def getTemp():
    owm_api_key = "18b01c0f7626ebed85f9449043085459"
    owm = pyowm.OWM(owm_api_key)
    observe = owm.weather_at_place('Manassas, us')
    w = observe.get_weather()
    temp = w.get_temperature()
    result = str(temp['temp_max']) + ", " + str(temp['temp']) + ", " + str(temp['temp_min']) + ", "
    return result

#getting traffic and travel data
def getDriveTime():
    r = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&departure_time=now&origins=Manassas,VA&destinations=Rockville,MD&key=AIzaSyBPJOSkCAxpp9p6hyzPkhmZ-A_jKUQgvRM')
    maps_parsed = json.loads(r.text)
    # print maps_parsed['rows'][0]['elements'][0]['duration_in_traffic']['text']
    return maps_parsed['rows'][0]['elements'][0]['duration_in_traffic']['value']

def writeData(data):
    f = open("/home/tlrwgnr/Documents/weatherTraffic/weather_traffic_data.csv","a")
    f.write(data)
    f.close()


def send():
	to = 'tlrwgnr@gmail.com'
	gmail_user = 'tlrwgnr@gmail.com'
	gmail_pwd = 'rglzgbazmkekkmdn'
	smtpserver = smtplib.SMTP("smtp.gmail.com",587)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo
	smtpserver.login(gmail_user, gmail_pwd)
	#header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:' + self.title + ' \n'
	#msg = header + '\n ' + self.body + '\n\n'

	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Weather Traffic error"
	msg['From'] = gmail_user
	msg['To'] = to

	html = "<html><head></head><body>"
	html += "There was an error recording the weather or traffic information"
	#html += e + "  "
	html += "</body></html>"

	# Record the MIME types of both parts - text/plain and text/html.
	#part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html.encode("ascii", "ignore"), 'html')

	# Attach parts into message container.
	# According to RFC 2046, the last part of a multipart message, in this case
	# the HTML message, is best and preferred.
	#msg.attach(part1)
	msg.attach(part2)

	smtpserver.sendmail(gmail_user, to, msg.as_string())
	#print 'done!'
	smtpserver.close()
if __name__ == "__main__":
    try:
        result = str(int(time.time())) + ", " + getTemp() + str(getDriveTime()) + "\n"
        writeData(result)
    except:
        send()

