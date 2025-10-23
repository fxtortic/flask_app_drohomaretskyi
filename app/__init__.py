from flask import Flask, render_template

app = Flask(__name__)
app.config.from_pyfile("../config.py", silent=True)

from app import views