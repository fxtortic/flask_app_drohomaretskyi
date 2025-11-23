import os

from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import config_map, INSTANCE_DIR
from app.forms import ContactForm

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name: str | None = None) -> Flask:


    if config_name is None:
        config_name = os.environ.get("FLASK_CONFIG", "development").lower()

    app = Flask(__name__, instance_relative_config=True)


    os.makedirs(INSTANCE_DIR, exist_ok=True)

    config_class = config_map.get(config_name, config_map["development"])
    app.config.from_object(config_class)

    db.init_app(app)

    from app.posts.models import Post

    migrate.init_app(app, db)

    from app.users import users_bp
    from app.products import products_bp
    from app.posts import posts_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(posts_bp)

    @app.route("/")
    def main():
        return redirect(url_for("users.login"))

    @app.route("/contact", methods=["GET", "POST"])
    def contact():
        form = ContactForm()

        if form.validate_on_submit():
            with open("contact.log", "a", encoding="utf-8") as f:
                f.write(
                    f"{form.name.data} <{form.email.data}>: "
                    f"{form.subject.data} - {form.message.data}\n"
                )
            flash("Ваше повідомлення надіслано.", "success")
            return redirect(url_for("contact"))

        return render_template("contact.html", form=form)

    @app.route("/resume")
    def resume():
        return render_template("resume.html")

    @app.route("/form", methods=["GET", "POST"])
    def form():
        form_obj = ContactForm()

        if form_obj.validate_on_submit():
            flash("Дані форми успішно надіслано (демо).", "info")
            return redirect(url_for("form"))

        return render_template("form.html", form=form_obj)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404

    return app
