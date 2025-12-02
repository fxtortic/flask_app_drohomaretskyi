from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
)
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user,
)

from app.users import users_bp
from app.forms import LoginForm, RegistrationForm, UpdateAccountForm, ChangePasswordForm
from app.users.models import User
from app.users.utils import save_profile_picture
from app import db


@users_bp.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)
    return render_template("users/hi.html", name=name, age=age)


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


@users_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_profile_picture(form.picture.data)
            current_user.image = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data

        db.session.commit()
        flash("Ваш профіль оновлено!", "success")
        return redirect(url_for("users.profile"))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me

    image_file = url_for(
        "static",
        filename="profile_pics/" + (current_user.image or "profile_default.jpg"),
    )

    return render_template(
        "users/profile.html",
        page_title="Профіль",
        user=current_user,
        form=form,
        image_file=image_file,
    )

@users_bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash("Поточний пароль вказано неправильно.", "error")
        else:
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash("Пароль успішно змінено.", "success")
            return redirect(url_for("users.profile"))

    return render_template(
        "users/change_password.html",
        page_title="Change Password",
        form=form,
    )


@users_bp.route("/users-list")
@login_required
def users_list():
    users = User.query.order_by(User.id).all()
    total = len(users)
    return render_template(
        "users/list.html",
        page_title="Усі користувачі",
        users=users,
        total=total,
    )


@users_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Ви вийшли із системи.", "info")
    return redirect(url_for("users.login"))
