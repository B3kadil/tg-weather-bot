from telebot import types

import config
import telebot
import requests

bot = telebot.TeleBot(config.token)


def ApiRequest(city_name):
    api_key = '735bb03774533f37710a31f65f3dda66'

    base_url = "https://api.openweathermap.org/data/2.5/weather?&units=metric"

    complete_url = base_url + "&appid=" + api_key + "&q=" + city_name

    response = requests.get(complete_url)

    date_weather = response.json()

    return date_weather


def GeoApiRequest(lat, long):
    api_key = '735bb03774533f37710a31f65f3dda66'

    base_url = "https://api.openweathermap.org/data/2.5/weather?&units=metric"

    complete_url = base_url + "&appid=" + api_key + "&lat=" + str(lat) + "&lon=" + str(long)
    print(f'{lat},{long}')
    print(complete_url)
    response = requests.get(complete_url)

    date_weather = response.json()

    return date_weather


@bot.message_handler(commands=["geo"])
def geo(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Send geolocation", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Hi can you send me your location)",
                     reply_markup=keyboard)


@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        long = message.location.longitude
        lat = message.location.latitude
        print(lat, long)
    date_weather = GeoApiRequest(lat, long)
    print(date_weather)
    try:
        if date_weather["cod"] != "404":

            y = date_weather["main"]

            current_temperature = round(y["temp"])

            feels_like = round(y["feels_like"])

            current_pressure = y["pressure"]

            current_humidity = y["humidity"]

            z = date_weather["weather"]

            photo = open(f'D:\python\project - 1\icons/{z[0]["icon"]}.png', 'rb')

            weather_description = z[0]["description"]

            text = f"Temperature (in celsius unit) = {str(current_temperature)}°C\nTemperature feels like (in celsius unit) = {str(feels_like)}°C\nAtmospheric pressure (in hPa unit) = {str(current_pressure)}\nHumidity (in percentage) = {str(current_humidity)}%\nDescription = {str(weather_description)}"
            print(text)
            bot.send_photo(message.chat.id, photo, caption=text)
        else:
            bot.send_message(message.chat.id, "City Not Found ")

    except:

        pass


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, "Enter the city name:")


@bot.message_handler()
def showWeather(message):
    city_name = message.text

    date_weather = ApiRequest(city_name)

    try:
        if date_weather["cod"] != "404":

            y = date_weather["main"]

            current_temperature = round(y["temp"])

            feels_like = round(y["feels_like"])

            current_pressure = y["pressure"]

            current_humidity = y["humidity"]

            z = date_weather["weather"]

            photo = open(f'D:\python\project - 1\icons/{z[0]["icon"]}.png', 'rb')

            weather_description = z[0]["description"]

            text = f"Temperature (in celsius unit) = {str(current_temperature)}°C\nTemperature feels like (in celsius unit) = {str(feels_like)}°C\nAtmospheric pressure (in hPa unit) = {str(current_pressure)}\nHumidity (in percentage) = {str(current_humidity)}%\nDescription = {str(weather_description)}"

            bot.send_photo(message.chat.id, photo, caption=text)
        else:
            bot.send_message(message.chat.id, "City Not Found ")

    except:

        pass


if __name__ == '__main__':
    bot.polling(none_stop=True)
