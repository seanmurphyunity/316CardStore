from flask import (
    Blueprint, render_template, request, redirect, url_for, session
)
from mainpkg import db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            session['email'] = email
            password = request.form['password']
            mydb = db.getdb()
            mycursor = mydb.cursor()
            mycursor.execute('SELECT * FROM users WHERE userid = %s', (email,))
            user = mycursor.fetchone()
            error=None
            if user is None:
                error = 'Incorrect username.'
            elif not (user[3], password):
                error = 'Incorrect password.'
            if error is None:
                return redirect(url_for('auth.loginsuccess'))
            return redirect(url_for('auth.authfail'))
        except:
            try:
                femail = request.form['femail']
                # security question = get sec q
                mydb = db.getdb()
                mycursor = mydb.cursor()
                mycursor.execute('SELECT question FROM passwordRecovery WHERE userid = %s', (femail,))
                securityquestion = mycursor.fetchone()
                mycursor.execute('SELECT userid FROM users WHERE userid = %s', (femail,))
                userid = mycursor.fetchone()
                return render_template('auth/forgotpassword.html', sq = securityquestion, userid = userid)
            except:
                answer = request.form['answer']
                userid = request.form['email']
                mydb = db.getdb()
                mycursor = mydb.cursor()
                mycursor.execute('SELECT * FROM passwordRecovery WHERE userid = %s', (userid,))    
                user = mycursor.fetchone()
                error=None
                if not (user[2], answer):
                    error = 'Incorrect Security Question.'
                if error is None:
                    return redirect(url_for('auth.profile')) #should redirect to account page
                return redirect(url_for('auth.authfail'))
    return render_template('auth/login.html')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        address = request.form['address']
        photo = request.form['photo']
        phonenumber = request.form['phonenumber']
        password = request.form['password']
        balance = 0
        mydb = db.getdb()
        mycursor = mydb.cursor()
        mycursor.execute('SELECT * FROM users WHERE userid = %s', (email,))
        user = mycursor.fetchone()
        error=None
        if user is not None:
            print(user)
            error = 'User already registered'
        if error is None:
            sql = "INSERT INTO users (userid, name, address, password, balance, photo_path, phone_numberr) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (email, name, address, password, balance, photo, phonenumber)
            mycursor.execute(sql, val)
            mydb.commit()
            try:
                if request.form['buyer'] == 'buyer':
                    buyerid = request.form['buyerid']
                    sql = "INSERT INTO buyer (buyerid, userid) VALUES (%s, %s)"
                    val = (buyerid, email)
                    mycursor.execute(sql, val)
                    mydb.commit()
            except:
                print('not buyer')
            try:
                if request.form['seller'] == 'seller':
                    sellerid = request.form['sellerid']
                    sql = "INSERT INTO seller (sellerid, userid) VALUES (%s, %s)"
                    val = (sellerid, email)
                    mycursor.execute(sql, val)
                    mydb.commit()
            except:
                print('not seller')
            return redirect(url_for('auth.registersuccess'))
        return redirect(url_for('auth.authfail'))
    return render_template('auth/register.html')

@bp.route('/account')
def account():
    return render_template('auth/account.html')

@bp.route('/registersuccess', methods=('GET', 'POST'))
def registersuccess():
    return render_template('auth/registersuccess.html')

@bp.route('/loginsuccess', methods=('GET', 'POST'))
def loginsuccess():
    return render_template('auth/loginsuccess.html')

@bp.route('/authfail', methods=('GET', 'POST'))
def authfail():
    return render_template('auth/authfail.html')

@bp.route('/profile', methods=('GET', 'POST'))
def profile():
    return render_template('auth/profile.html')

