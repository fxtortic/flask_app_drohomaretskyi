from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main():
    return 'Hello, world!'

@app.route('/resume')
def resume():
    return render_template('resume.html', page_title='Моє резюме')

@app.route("/contact")
def contact():
    return render_template("contact.html", page_title='Контакти')

@app.route("/form")
def form():
    return render_template("form.html", page_title='Форма')


if __name__ == '__main__':
    app.run(debug=True)
