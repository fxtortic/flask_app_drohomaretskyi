from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    TextAreaField,
    SelectField,
    SelectMultipleField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
)


# ---------- ContactForm ----------
class ContactForm(FlaskForm):
    name = StringField(
        "Імʼя",
        validators=[DataRequired(), Length(min=2, max=50)],
    )
    email = StringField(
        "E-mail",
        validators=[DataRequired(), Email(), Length(max=120)],
    )
    phone = StringField(
        "Телефон",
        validators=[Length(max=20)],
    )
    topic = SelectField(
        "Тема",
        choices=[
            ("question", "Запитання"),
            ("order", "Замовлення"),
            ("other", "Інше"),
        ],
    )
    message = TextAreaField(
        "Повідомлення",
        validators=[DataRequired(), Length(min=5)],
    )
    submit = SubmitField("Надіслати")


# ---------- LoginForm ----------
class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=50)],
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=3, max=100)],
    )
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")


# ---------- RegistrationForm ----------
class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=50)],
    )
    email = StringField(
        "E-mail",
        validators=[DataRequired(), Email(), Length(max=120)],
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=3, max=100)],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Паролі мають збігатися."),
        ],
    )
    submit = SubmitField("Sign up")

    def validate_username(self, field: StringField) -> None:
        from app.users.models import User

        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError("Користувач з таким username вже існує.")

    def validate_email(self, field: StringField) -> None:
        from app.users.models import User

        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError("Користувач з таким email вже існує.")


# ---------- PostForm (для постів / тегів) ----------
class PostForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[DataRequired(), Length(min=3, max=200)],
    )
    body = TextAreaField(
        "Content",
        validators=[DataRequired(), Length(min=3)],
    )
    author_id = SelectField("Author", coerce=int, validators=[DataRequired()])
    tags = SelectMultipleField("Tags", coerce=int)
    submit = SubmitField("Add Post")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        from app.users.models import User
        from app.posts.models import Tag

        self.author_id.choices = [
            (u.id, u.username) for u in User.query.order_by(User.id)
        ]
        self.tags.choices = [
            (t.id, t.name) for t in Tag.query.order_by(Tag.name)
        ]
