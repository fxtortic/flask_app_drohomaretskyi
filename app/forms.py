from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    SelectField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Email, Length, Regexp


class ContactForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            DataRequired(message="Ім'я є обов'язковим"),
            Length(min=4, max=10, message="Ім'я має бути від 4 до 10 символів"),
        ],
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Email є обов'язковим"),
            Email(message="Введіть коректну адресу email"),
        ],
    )

    phone = StringField(
        "Phone",
        validators=[
            DataRequired(message="Телефон є обов'язковим"),
            Regexp(r"^\+380\d{9}$", message="Формат телефону: +380XXXXXXXXX"),
        ],
    )

    subject = SelectField(
        "Subject",
        choices=[
            ("support", "Підтримка"),
            ("question", "Запитання"),
            ("job", "Співпраця / робота"),
            ("other", "Інше"),
        ],
        validators=[DataRequired(message="Оберіть тему звернення")],
    )

    message = TextAreaField(
        "Message",
        validators=[
            DataRequired(message="Повідомлення є обов'язковим"),
            Length(
                max=500,
                message="Повідомлення не повинно перевищувати 500 символів",
            ),
        ],
    )

    submit = SubmitField("Send")


class LoginForm(FlaskForm):
    username = StringField(
        "Username / Email",
        validators=[
            DataRequired(message="Поле обов'язкове"),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Поле обов'язкове"),
            Length(
                min=4,
                max=10,
                message="Пароль має бути від 4 до 10 символів",
            ),
        ],
    )
    remember = BooleanField("Запам'ятати мене")
    submit = SubmitField("Sign in")


class PostForm(FlaskForm):
    title = StringField(
        "Заголовок",
        validators=[
            DataRequired(message="Заголовок є обов'язковим"),
            Length(max=150, message="Максимальна довжина заголовка — 150 символів"),
        ],
    )

    content = TextAreaField(
        "Текст",
        validators=[
            DataRequired(message="Текст є обов'язковим"),
        ],
    )

    category = SelectField(
        "Категорія",
        choices=[
            ("news", "Новина"),
            ("publication", "Публікація"),
            ("tech", "Технічна"),
            ("other", "Інше"),
        ],
        validators=[DataRequired(message="Оберіть категорію")],
    )

    is_active = BooleanField("Публікувати зараз", default=True)

    author = StringField(
        "Автор",
        validators=[
            DataRequired(message="Автор є обов'язковим"),
            Length(
                max=20,
                message="Ім'я автора не повинно перевищувати 20 символів",
            ),
        ],
        default="Anonymous",
    )

    submit = SubmitField("Зберегти")
