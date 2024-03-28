from flask import Flask, render_template, request, redirect, url_for, abort, flash
import flask
import requests
from config import *

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
params = {'q': 'Moscow', 'appid': API_KEY, 'units': 'metric'}


def select_icon(clouds):
    match (clouds):
        case 'Clouds':
            return "static/img/clouds.png"
        case 'Clear':
            return "static/img/sun.png"
        case 'Rain':
            return "static/img/rainy.png"
        case 'Mist':
            return "static/img/mist.png"
        case 'Snow':
            return "static/img/snow.png"
        case 'Haze':
            return "static/img/haze.png"
        case _:
            return "static/img/sun.png"


def get_weather(params):
    answ = requests.get(ENDPOINT, params=params)
    if answ:
        data = answ.json()
        data["weather"][0]['icon'] = select_icon(data["weather"][0]['main'])
        return data

    flash('Bad request', 'error')
    abort(404)


@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == 'POST':
        params['q'] = request.form['city']  # для вызова след requests
        return redirect(url_for('index', data=get_weather(params)))

    return render_template('index.html', data=get_weather(params))


@app.errorhandler(404)
def error_404(error):
    return render_template('page_404.html')


if __name__ == "__main__":
    app.run(debug=True, port=8080)
