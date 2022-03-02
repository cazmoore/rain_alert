import config
import requests
from twilio.rest import Client

# OWM API details
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"

# Create parameter for OWM API
weather_params = {
    "lat": config.lat,
    "lon": config.lon,
    "appid": config.api_key,
    "units": "imperial",
    "exclude": "current,minutely,daily"
}

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:11]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]['id']

    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    client = Client(config.account_sid, config.auth_token)

    message = client.messages.create(
        body="It's going to rain today, bring an umbrella! ☔️",
        from_= config.from_num,
        to= config.to_num
    )

    print(message.status)
