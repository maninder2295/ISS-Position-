import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 32.755367
MY_LONG = 74.908215

def is_iss_overhead():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if (MY_LAT - 5) <= iss_latitude <= (MY_LAT + 5) and (MY_LONG - 5) <= iss_longitude <= (MY_LONG + 5):
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now().hour
    if time_now >= sunset or time_now <= sunrise:
        return True

time_date = datetime.now()
h = time_date.hour
m = time_date.minute
s = time_date.second
time_ = f"{h}:{m}:{s}"

def send_mail():
    my_email = "nitikabrixtechnology@gmail.com"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password="Manis@2295")
        connection.sendmail(from_addr=my_email,
                            to_addrs="manindersingh2295.10@gmail.com",
                            msg=f"Subject:Look ISS Is Moving Towards You\n\n"
                                f"ISS at your location at {time_}.See it!  ")

is_iss_up = False
while not is_iss_up:
    time.sleep(30)
    if is_night() and is_iss_overhead():
        send_mail()
        is_iss_up = True

