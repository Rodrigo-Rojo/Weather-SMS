import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

proxy_client = TwilioHttpClient(proxy={'http': os.environ['http_proxy'], 'https': os.environ['https_proxy']})
OWM_url = "https://api.openweathermap.org/data/2.5/onecall"
api_key = "YourAPIKEY"
account_sid = "ACc29ff39a8eae3f42d28edf662f8fc91a"
auth_token = "YourAPIKEY"

weather_params = {
    "lat": 43.51957599608531,
    "lon": -111.9638428711688,
    "exclude": "current,minutely,daily",
    "units": "imperial",
    "appid": api_key
}
temp_list = []
response = requests.get(OWM_url, params=weather_params)
response.raise_for_status()
weather_data = response.json()
hourly_weather_data = weather_data["hourly"]
description_list = []
main_list = []
main_string = ""
description_string = ""

for i in range(12):
    temp = int(weather_data["hourly"][i]["temp"])
    main = weather_data["hourly"][i]["weather"][0]["main"]
    description = weather_data["hourly"][i]["weather"][0]["description"]
    icon = weather_data["hourly"][i]["weather"][0]["icon"]
    temp_list.append(temp)
    description_list.append(description)
    main_list.append(main)

description_list = list(set(description_list))
main_list = list(set(main_list))
if len(main_list) > 0:
    for index in main_list:
        main_string += f"{index}, "
else:
    main_string = main_list[0]

if len(description_list) > 0:
    for index in description_list:
        description_string += f"{index}, "
else:
    description_string = description_list[0]
print(description_string)
client = Client(account_sid, auth_token, http_client=proxy_client)

message = client.messages.create(
    body=f"Today the lowest temp: {min(temp_list)}°F and the Highest: {max(temp_list)}°F\n"
         f", Today is going to be: {main_string} and {description_string}",
    from_="+16692383298",
    to="2082274011"
)

print(message.status)
