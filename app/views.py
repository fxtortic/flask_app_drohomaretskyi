import logging
from flask import render_template, request, redirect, url_for, flash

from . import app
from app.forms import ContactForm


@app.route("/")
def main():
    return render_template("resume.html", page_title="Моє резюме")


@app.route("/resume")
def resume():
    return render_template("resume.html", page_title="Моє резюме")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        logger = logging.getLogger("contact")
        if not logger.handlers:
            file_handler = logging.FileHandler("contact.log", encoding="utf-8")
            file_handler.setLevel(logging.INFO)
            logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)

        logger.info(
            "Contact form: name=%s, email=%s, phone=%s, topic=%s",
            form.name.data,
            form.email.data,
            form.phone.data,
            form.topic.data,
        )

        flash(
            f"Форму успішно відправлено. Дякуємо, {form.name.data} ({form.email.data})!",
            "success",
        )
        return redirect(url_for("contact"))

    if request.method == "POST" and not form.validate():
        flash("Форма містить помилки. Перевірте поля нижче.", "error")

    return render_template("contact.html", page_title="Контакти", form=form)

@app.route("/form")
def form():
    return render_template("form.html", page_title="Форма")
