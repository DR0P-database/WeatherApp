from flask import Flask, render_template, request, redirect, url_for, abort, flash
import flask
import requests
from config import *

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
params = {'q': 'Los Angeles', 'appid': API_KEY, 'units': 'metric'}


def get_weather(params: dict) -> dict:
    """
    get_weather return weather info from API

    Args:
        params (dict): contains request parameters(API, region)

    Returns:
        dict: contains weather info
    """

    answ = requests.get(ENDPOINT, params=params)  # get response

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
    """index func to address main page"""

    if request.method == 'POST':
        params['q'] = request.form['city']  # для вызова след requests
        return redirect(url_for('index'))

    # Get weather info
    return render_template('index.html', data=get_weather(params))


@app.errorhandler(404)
def error_404(error):
    return render_template('page_404.html')


if __name__ == "__main__":
    app.run(debug=True, port=8080)
