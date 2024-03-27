from flask import Flask, render_template, request
import flask
from config import *

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == 'POST':
        city = request.form['city']
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, port=8080)
