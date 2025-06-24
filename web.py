from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "TweetBot está rodando no Heroku!"
