from flask import Flask, render_template, request, redirect, url_for, abort, flash, session
import flask
import requests
from config import *

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
params = {'appid': API_KEY, 'units': 'metric'}
app.permanent_session_lifetime = 20

appHasRunBefore: bool = False


@app.before_request
def before_first_request():
    global appHasRunBefore
    global params

    session.permanent = True
    if not appHasRunBefore:
        if 'my_city' not in session:
            session['my_city'] = 'Los Angeles'
            session.modified = True

        params.update({'q': session['my_city']})
        appHasRunBefore = True
        print("[DECORATOR]", params['q'])


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
        # для вызова след requests as (params['q'] = request.form['city'])
        session['my_city'] = request.form['city']
        session.modified = True
        params.update({'q': session['my_city']})
        return redirect(url_for('index'))

    # Get weather info
    return render_template('index.html', data=get_weather(params))


@app.errorhandler(404)
def error_404(error):
    return render_template('page_404.html')


if __name__ == "__main__":
    app.run(debug=True, port=8080)
