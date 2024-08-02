from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from werkzeug.security import generate_password_hash

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f6c810cd79289a26fa921298ffd7f9a9a006b3206924c0bd81e4b8c262126185'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

"""
>>> import secrets
>>> secrets.token_hex()
"""


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


class RegistrationForm(FlaskForm):
    first_name = StringField('Имя', validators=[DataRequired(), Length(min=2, max=150)])
    last_name = StringField('Фамилия', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Подтвердите Пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')


@app.before_request
def create_tables():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        existing_user = User.find_by_email(form.email.data)
        if existing_user:
            flash('Пользователь с таким email уже зарегистрирован', 'danger')
        else:
            new_user = User(first_name=form.first_name.data, last_name=form.last_name.data,
                            email=form.email.data, password=hashed_password)
            try:
                new_user.save_to_db()
                flash('Вы успешно зарегистрированы!', 'success')
            except IntegrityError:
                flash('Что-то пошло не так. Пожалуйста, попробуйте еще раз.', 'danger')

        return redirect(url_for('index'))

    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)