from flask import Flask, render_template, request, redirect, url_for, abort, flash
import flask
import requests
from config import *

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
params = {'q': 'Moscow', 'appid': API_KEY, 'units': 'metric'}


def get_weather(params):
    answ = requests.get(ENDPOINT, params=params)
    print(answ)
    if answ:
        data = answ.json()
        data['main']['temp'] = round(data['main']['temp'])
        data["weather"][0][
            'icon'] = f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
        return data

    flash('Bad request', 'error')
    abort(404)


@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == 'POST':
        params['q'] = request.form['city']  # для вызова след requests
        return redirect(url_for('index'))

    return render_template('index.html', data=get_weather(params))


@app.errorhandler(404)
def error_404(error):
    return render_template('page_404.html')


if __name__ == "__main__":
    app.run(debug=True, port=8080)
