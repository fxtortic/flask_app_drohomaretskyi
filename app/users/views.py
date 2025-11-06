from flask import render_template, request, redirect, url_for, flash, session, make_response
from app.users import users_bp


@users_bp.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)
    return render_template("users/hi.html", name=name, age=age)


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if username == "admin" and password == "1234":
            session["user"] = username
            flash("Вхід виконано успішно!", "success")
            return redirect(url_for("users.profile"))
        else:
            flash("Невірний логін або пароль. Спробуйте ще раз!", "error")
            return redirect(url_for("users.login"))

    return render_template("users/login.html", page_title="Login")


@users_bp.route("/profile", methods=["GET", "POST"])
def profile():
    if "user" not in session:
        flash("Спочатку увійдіть у систему!", "error")
        return redirect(url_for("users.login"))

    username = session["user"]

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


@users_bp.route("/set-theme/<string:scheme>")
def set_theme(scheme):
    if "user" not in session:
        flash("Спочатку увійдіть у систему!", "error")
        return redirect(url_for("users.login"))

    allowed = {"light", "dark", "blue"}
    if scheme not in allowed:
        flash("Невідома кольорова схема.", "error")
        return redirect(url_for("users.profile"))

    resp = make_response(redirect(url_for("users.profile")))
    resp.set_cookie("profile_theme", scheme, max_age=30 * 24 * 60 * 60)
    flash(f"Кольорова схема змінена на '{scheme}'.", "info")
    return resp


@users_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("Ви вийшли із системи.", "info")
    return redirect(url_for("users.login"))
