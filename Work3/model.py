from sqlite3 import IntegrityError
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound  # Добавляем импорт исключения

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    @classmethod
    def find_by_email(cls, email):
        try:
            return cls.query.filter_by(email=email).one()
        except NoResultFound:
            return None

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Пользователь с таким email уже зарегистрирован")