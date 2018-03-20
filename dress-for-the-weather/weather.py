import codecs
import json
from requests import get
from datetime import datetime, timedelta
from pprint import pprint

KEY = 'ac990cac4b977951edfbf4e2aa0edfeb'
API_REQUEST = 'http://api.openweathermap.org/data/2.5/forecast?id={}&APPID={}'

def getCityId():
    #load data
    data = json.loads(open('city.list.json', encoding='utf-8').read())
    #pprint(data)

    #get city input from user
    city = input("Please input city: ")
    for item in data:
        if item['name'].lower().strip() == city.lower().strip():
            print('Is this the correct country (y/n): ', item['country'])
            answer = input()
            if answer.lower().strip() == 'y':
                return item['id']

def getWeatherData(cityId):
    weatherData = get(API_REQUEST . format(cityId, KEY))
    return weatherData.json()

def getArrival():
    today = datetime.now()
    maxDay = today + timedelta(days=4)

    #user choose day to arrive
    print("Choose day you will come your destination in this range:")
    print(today.strftime('%d'), ' - ', maxDay.strftime('%d'))
    day = input()

    #what is the arrive time
    print("What's time you get there?\n0-24")
    hour = int(input())
    #only have weather data 7 hours from now
    if day == today.strftime('%d'):
        today += timedelta(hours=7)
        hour = int(today.strftime('%H'))
    else:
        today += timedelta(days=(int(day) - int(today.strftime('%d'))))
        #only have data for every each 3 hours
    
    hour = hour - hour % 3
    arrival = "%s-%s-%s %02.0f:00:00" % (today.strftime('%Y'), today.strftime('%m'), today.strftime('%d'), float(hour))
    pprint(arrival)
    return arrival

def getForecast(weatherData, arrival):
    for item in weatherData['list']:
        if item['dt_txt'] == arrival:
            return item

def getReadableForecast(weatherData):
    weather = {}
    weather['cloudiness']    = weatherData['clouds']['all']
    weather['temperature']  = weatherData['main'] ['temp']
    weather['humidity']     = weatherData['main'] ['humidity']
    if '3h' in weatherData['rain']:
        weather['rain'] = float(weatherData['rain']['3h'])
    else:
        weather['rain'] = 0.0
    weather['description']  = weatherData['weather'] [0] ['description']
    weather['wind']         = weatherData['wind'] ['speed']

    return weather
    
def getClothes(weather):
    print('The overall description for the weather at that time is {}'.format(weather['description']))
    if weather['cloudiness'] < 10:
        print('It should be sunny, so a hat or sunglasses might be needed')
    if weather['rain'] == 0:
        print("It's not going to rain, so no umbrella is needed")
    elif weather['rain']/3 < 2.5:
        print("There'll be light rain, so consider a hood or umbrella")
    elif weather['rain']/3 < 7.6:
        print("There'll be moderate rain, so an umbrella is probably needed")
    elif weather['rain']/3 < 50:
        print("There'll be heavy rain, so you'll need an umbrella and a waterproof top")
    elif weather['rain']/3 > 50:
        print("There'll be violent rain, so wear a life-jacket")
    if weather['temperature'] < 273:
        print("It's going to be freezing, so take a heavy coat")
    elif weather['temperature'] < 283:
        print("It's going to be cold, so a coat or thick jumper might be sensible")
    elif weather['temperature'] < 293:
        print("It's not too cold, but you might consider taking a light jumper")
    elif weather['temperature'] < 303:
        print("Shorts and T-shirt weather :)")
    if weather['wind'] > 30:
        print("There'll be wind, so a jacket might be useful")
    elif weather['wind'] > 10:
        print("There'll be a light breeze, so maybe long sleeves might be useful")
    else:
        print("The air will be quite calm, so no need to worry about wind")

def main():
    cityId = getCityId()
    if not cityId:
        print('Can not find the weather in pur data. Please try again use difference input.')
    else:
        weatherData = getWeatherData(cityId)
        arrival = getArrival()
        forecast = getForecast(weatherData, arrival)
        weather = getReadableForecast(forecast)
        getClothes(weather)


main()
#pprint(getWeatherData(479687))
#print(getArrival())
#print(getForecast(getWeatherData(479687),getArrival()))