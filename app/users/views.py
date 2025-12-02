from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    make_response,
)
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user,
)

from app.users import users_bp
from app.forms import LoginForm, RegistrationForm
from app.users.models import User
from app import db


@users_bp.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)
    return render_template("users/hi.html", name=name, age=age)


# ---------- РЕЄСТРАЦІЯ ----------
@users_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("users.profile"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash="",
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash(f"Обліковий запис для {user.username} створено успішно!", "success")
        return redirect(url_for("users.login"))

    if request.method == "POST" and not form.validate():
        flash("Форма містить помилки. Перевірте поля нижче.", "error")

    return render_template("users/register.html", page_title="Register", form=form)


# ---------- ВХІД ----------
@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("users.profile"))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash("Вхід виконано успішно.", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("users.profile"))
        else:
            flash("Невірний логін або пароль!", "error")
            return redirect(url_for("users.login"))

    if request.method == "POST" and not form.validate():
        flash("Перевірте правильність заповнення форми.", "error")

    return render_template("users/login.html", page_title="Login", form=form)


# ---------- ПРОФІЛЬ (ЗАХИЩЕНИЙ @login_required) ----------
@users_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    username = current_user.username

    if request.method == "POST":
        action = request.form.get("action")

        if action == "add":
            key = request.form.get("cookie_key", "").strip()
            value = request.form.get("cookie_value", "").strip()
            max_age = request.form.get("cookie_max_age", "").strip()

            if not key or not value:
                flash("Ключ і значення кукі обовʼязкові.", "error")
                return redirect(url_for("users.profile"))

            resp = make_response(redirect(url_for("users.profile")))
            if max_age.isdigit():
                resp.set_cookie(key, value, max_age=int(max_age))
            else:
                resp.set_cookie(key, value)

            flash(f"Кука '{key}' додана.", "success")
            return resp

        if action == "delete_one":
            key = request.form.get("cookie_delete_key", "").strip()
            if not key:
                flash("Вкажіть ключ кукі для видалення.", "error")
                return redirect(url_for("users.profile"))

            resp = make_response(redirect(url_for("users.profile")))
            resp.delete_cookie(key)
            flash(f"Кука '{key}' видалена (якщо вона існувала).", "info")
            return resp

        if action == "delete_all":
            resp = make_response(redirect(url_for("users.profile")))
            for ckey in request.cookies.keys():
                if ckey == "session":
                    continue
                resp.delete_cookie(ckey)
            flash("Усі кукі (крім сесійної) видалені.", "info")
            return resp

    cookies_dict = request.cookies
    current_theme = request.cookies.get("profile_theme", "light")

    return render_template(
        "users/profile.html",
        page_title="Profile",
        user=username,
        cookies=cookies_dict,
        theme=current_theme,
    )


# ---------- ВИХІД ----------
@users_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Ви вийшли із системи.", "info")
    return redirect(url_for("users.login"))


# ---------- ЗМІНА КОЛЬОРОВОЇ СХЕМИ ----------
@users_bp.route("/set-theme/<string:scheme>")
@login_required
def set_theme(scheme: str):
    allowed = {"light", "dark", "blue"}
    if scheme not in allowed:
        flash("Невідома кольорова схема.", "error")
        return redirect(url_for("users.profile"))

    resp = make_response(redirect(url_for("users.profile")))
    resp.set_cookie("profile_theme", scheme, max_age=30 * 24 * 60 * 60)

    flash(f"Кольорова схема змінена на '{scheme}'.", "info")
    return resp

@users_bp.route("/users-list")
@login_required
def users_list():
    users = User.query.order_by(User.id).all()
    total = len(users)
    return render_template(
        "users/users_list.html",
        page_title="Усі користувачі",
        users=users,
        total=total,
    )