from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


app = Flask(__name__)
app.config.from_pyfile("../config.py")
app.config["SECRET_KEY"] = "super-secret-key"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app, model_class=Base)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

# ---------- Flask-Login ----------
login_manager = LoginManager(app)
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"

from app import views
from app.users import users_bp
from app.products import products_bp
from app.posts import posts_bp

app.register_blueprint(users_bp)
app.register_blueprint(products_bp)
app.register_blueprint(posts_bp)

from app.users.models import User


@login_manager.user_loader
def load_user(user_id: str):
    return User.query.get(int(user_id))
