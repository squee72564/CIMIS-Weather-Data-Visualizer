from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('welcome.html')

@app.route('/<name>')
def hello_world(name):
    return render_template('hello.html', person=name)
