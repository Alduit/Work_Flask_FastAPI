from flask import Flask, flash, render_template, request, redirect, url_for, make_response


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login/')
def login():
    return render_template('login.html')


@app.route('/setcookie', methods=['POST'])
def setcookie():
    user = request.form['name']
    email = request.form['email']
    resp = make_response(redirect(url_for('user')))
    resp.set_cookie('userName', user)
    resp.set_cookie('userEmail', email)
    return resp


@app.route('/user')
def user():
    user = request.cookies.get('userName')
    email = request.cookies.get('userEmail')
    if not user or not email:
        user = 'NoName'
        email = 'NoData'
    return render_template('user.html', user=user)

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('userName', '', expires=0)
    resp.set_cookie('userEmail', '', expires=0)
    return resp

if __name__ == '__main__':
    app.run(debug=True)