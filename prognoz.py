appid = "1d0fb1e1e0aea22c8338225b779044be"
city_id = 627904
from flask import Flask, render_template

app = Flask(__name__, template_folder='render_template')

import requests

def get_wind_direction(deg):
    l = ['С ','СВ',' В','ЮВ','Ю ','ЮЗ',' З','СЗ']
    for i in range(0,8):
        step = 45.
        min = i*step - 45/2.
        max = i*step + 45/2.
        if i == 0 and deg > 360-45/2.:
            deg = deg - 360
        if deg >= min and deg <= max:
            res = l[i]
            break
    return res
# Запрос текущей погоды
def request_current_weather(city_id):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                     params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        print("В городе Гродно:")
        print("Условия:", data['weather'][0]['description'])
        print("Температура:", data['main']['temp'])
        print("Минимальная температура :", data['main']['temp_min'])
        print("Максимальная температура:", data['main']['temp_max'])
        print("Влажность:", data['main']['humidity'])
    except Exception as e:
        print("Exception (weather):", e)
        pass
    return data
# Прогноз
def request_forecast(city_id):
    result = []
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                      params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        #print('city:', data['city']['name'], data['city']['country'])
        for i in data['list']:
            forecast_line = "{} {} {}".format((i['dt_txt'])[:16], '{0:+3.0f}'.format(i['main']['temp']), i['weather'][0]['description'])
            result.append(forecast_line)
            print(forecast_line)
    except Exception as e:
        print("Exception (forecast):", e)
        pass
    return result

#request_current_weather(city_id)
#request_forecast(city_id)

@app.route('/', methods = ['POST','GET'])
def route():
    return render_template('my_form.html', current_weather=request_current_weather(city_id), forecast=request_forecast(city_id))
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)