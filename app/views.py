from flask import render_template
from . import app

@app.route('/')
def main():
    return render_template('resume.html', page_title='Моє резюме')

@app.route('/resume')
def resume():
    return render_template('resume.html', page_title='Моє резюме')

@app.route("/contact")
def contact():
    return render_template("contact.html", page_title='Контакти')

@app.route("/form")
def form():
    return render_template("form.html", page_title='Форма')
