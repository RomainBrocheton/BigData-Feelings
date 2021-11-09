from flask import Flask, render_template, request
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('home.html', sentiment = 0)

@app.route('/action', methods=["POST"])
def action():
    text = request.form.get("text")
    blob = TextBlob(text, analyzer=NaiveBayesAnalyzer())

    return render_template('home.html', sentiment = blob.sentiment)