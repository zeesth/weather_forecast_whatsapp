from twilio.rest import Client
import requests

twilio_sid = ""
twilio_auth = ""
weather_endpoint = "http://api.openweathermap.org/data/2.5/forecast"
weather_key = ""

#   Stores API parameters
weather_parameters = {
    "lat": -23.5475,
    "lon": -46.6361,
    "appid": weather_key,
    "units": "metric",
}

#   Calling Open Weather Map API
weather_response = requests.get(weather_endpoint, params=weather_parameters)
weather_response.raise_for_status()
weather_data = weather_response.json()

#   Getting the forecast from 6 a.m to 9 p.m
weather_slice = weather_data["list"][3:8]

#   Calculating the median temperature
forecast_temp = [int(weather_slice[i]["main"]["temp"]) for  i in range(5)]
forecast_temp = sorted(forecast_temp)
median_temp = forecast_temp[2]

#   Analysing if it's going to rain and getting the weather description
will_rain = False
for i in range(5):
    forecast = weather_slice[i]["weather"][0]
    if i == 0:
        forecast_id = forecast["id"]
        description = forecast["description"]
    if int(forecast["id"]) < 700:
        will_rain = True

#   Sending a message to warn user of today's forecast
if will_rain:
    client = Client(twilio_sid, twilio_auth)

    message = client.messages.create(
    from_="whatsapp:+",
    body=f"Today's forecast: {description}\nMedium temperature: {median_temp}ºC\nYou should probably take the umbrella.",
    to="whatsapp:+"
    )
else:
    client = Client(twilio_sid, twilio_auth)

    message = client.messages.create(
    from_="whatsapp:+",
    body=f"Today's forecast: {description}\nMedium temperature: {median_temp}ºC\nNo need for the umbrella.",
    to="whatsapp:+"
    )

#   Checking if the message was sent
print(message.status)