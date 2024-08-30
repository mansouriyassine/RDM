# app.py
from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/surprise')
def surprise():
    phrases = [
        "hajjoura",
        "9ahbouna",
        "bo7da 3anda tabbouna",
        "za3kouna",
        "bangola",
        "mangola"
    ]
    return jsonify({'phrase': random.choice(phrases)})

if __name__ == '__main__':
    app.run(debug=True)