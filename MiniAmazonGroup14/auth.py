from flask import (
    Blueprint, render_template, request, redirect, url_for, session
)
import MiniAmazonGroup14.db
import random

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            session['email'] = email
            password = request.form['password']
            mydb = MiniAmazonGroup14.db.getdb()
            mycursor = mydb.cursor()
            mycursor.execute('SELECT * FROM users WHERE userid = %s', (email,))
            user = mycursor.fetchone()
            error=None
            if user is None:
                error = 'Incorrect username.'
            elif not user[3] == password:
                error = 'Incorrect password.'
            if error is None:
                return redirect(url_for('auth.loginsuccess'))
            return redirect(url_for('auth.authfail'))
        except:
            try:
                femail = request.form['femail']
                # security question = get sec q
                mydb = MiniAmazonGroup14.db.getdb()
                mycursor = mydb.cursor()
                mycursor.execute('SELECT * FROM passwordRecovery WHERE userid = %s', (femail,))    
                user = mycursor.fetchone()
                error=None
                if user is None:
                    error = 'incorrect username'
                mycursor.execute('SELECT question FROM passwordRecovery WHERE userid = %s', (femail,))
                if error is None:
                    return render_template('auth/forgotpassword.html', sq = mycursor.fetchone()[0], userid = user[0])
                return redirect(url_for('auth.authfail'))
            except:
                answer = request.form['answer']
                userid = request.form['email']
                mydb = MiniAmazonGroup14.db.getdb()
                mycursor = mydb.cursor()
                mycursor.execute('SELECT * FROM passwordRecovery WHERE userid = %s', (userid,))    
                user = mycursor.fetchone()
                print(user)
                error=None
                if user is not None:
                    if not user[2] == answer:
                        error = 'Incorrect Security Question.'
                else:
                    error = "Incorrect Username"
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
        securityQuestion = request.form['question']
        securityAnswer = request.form['answer']
        initialCart = rangenartnum()
        balance = 0
        mydb = MiniAmazonGroup14.db.getdb()
        mycursor = mydb.cursor()
        mycursor.execute('SELECT * FROM users WHERE userid = %s', (email,))
        user = mycursor.fetchone()
        error=None
        if user is not None:
            print(user)
            error = 'User already registered'
        if error is None:
            sql = "INSERT INTO users (userid, name, address, password, balance, photo_path, phone_numberr, cur_cart) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (email, name, address, password, balance, photo, phonenumber, initialCart)
            mycursor.execute(sql, val)
            mydb.commit()
            sql = "INSERT INTO passwordRecovery (userid, question, answer) VALUES (%s, %s, %s)"
            val = (email, securityQuestion, securityAnswer)
            mycursor.execute(sql, val)
            mydb.commit()
            session['email'] = email
            
            try:
                if request.form['buyer'] == 'buyer':
                    buyerid = genBuyerNum()
                    sql = "INSERT INTO buyer (buyerid, userid) VALUES (%s, %s)"
                    val = (buyerid, email)
                    mycursor.execute(sql, val)
                    mydb.commit()
            except:
                print("Not a buyer")
            
            try:
                if request.form['seller'] == 'seller':
                    sellerid = genSellerNum()
                    sql = "INSERT INTO seller (sellerid, userid) VALUES (%s, %s)"
                    val = (sellerid, email)
                    mycursor.execute(sql, val)
                    mydb.commit()
            except:
                print("Not a seller")
            
            return redirect(url_for('auth.registersuccess'))
        return redirect(url_for('auth.authfail'))
    return render_template('auth/register.html')

@bp.route('/account')
def account():
    try:
        sessionid = session['email']
        return render_template('auth/account.html')
    except:
        return render_template('auth/mustlogin.html')


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
    try: 
        sessionid = session['email']
    except:
        return render_template('auth/mustlogin.html')
    mydb = MiniAmazonGroup14.db.getdb()
    mycursor = mydb.cursor()
    userData = ["userid", "name", "address", "password", "balance", "photo_path", "phone_numberr", "cur_cart"]
    i = 0
    user = ["", "", "", "", "", "", "", ""]
    for word in userData:
        sql = "SELECT " + word +  " FROM users WHERE userid = '" + sessionid + "'"
        mycursor.execute(sql)
        user[i] = mycursor.fetchone()[0]
        i = i + 1
    userid = user[0]
    name = user[1]
    address = user[2]
    password = user[3]
    photo_path = user[5]
    phone_number = user[6]

    j = 0
    recovery = ["question", "answer"]
    recoveryData = ["", ""]
    for word in recovery:
        sql = "SELECT " + word + " FROM passwordRecovery WHERE userid = '" + userid + "'"
        mycursor.execute(sql)
        recoveryData[j] = mycursor.fetchone()[0]
        j = j + 1
    securityQuestion = recoveryData[0]
    securityAnswer = recoveryData[1]

    sql = "SELECT * FROM seller WHERE userid = '" + userid + "'"
    mycursor.execute(sql)
    if mycursor.fetchone() is None:
        sellerStatus = "Not Currently a seller"
    else:
        sellerStatus = "Currently a seller"

    sql = "SELECT * FROM buyer WHERE userid = '" + userid + "'"
    mycursor.execute(sql)
    if mycursor.fetchone() is None:
        buyerStatus = "Not Currently a buyer"
    else:
        buyerStatus = "Currently a buyer"

    if request.method == 'POST':
        mydb = MiniAmazonGroup14.db.getdb()
        mycursor = mydb.cursor()
        try: 
            address = request.form['newaddress']
            sql = "UPDATE users SET address = " + address + "WHERE userid = "+ userid + ""
            mycursor.execute(sql)
            mydb.commit()
        except:
            try:
                photo = request.form['photo']
                sql = "UPDATE users SET photo_path = " + photo + "WHERE userid = " + userid + ""
                mycursor.execute(sql)
                mydb.commit()
            except:
                try:
                    phonenumber = request.form['newphonenumber']
                    sql = "UPDATE users SET phone_numberr = " + phonenumber + "WHERE userid = " + userid + ""
                    mycursor.execute(sql)
                    mydb.commit()
                except:
                    try:
                        password = request.form['newpassword']
                        sql = "UPDATE users SET password = " + password + "WHERE userid = " + userid + ""
                        mycursor.execute(sql)
                        mydb.commit()
                    except:
                        try:
                            securityQuestion = request.form['question']
                            securityAnswer = request.form['answer']
                            sql = "UPDATE users SET question = " + question + ", answer = " + answer +  "WHERE userid = " + userid + ""
                            mycursor.execute(sql)
                            mydb.commit()
                        except:
                            try:
                                if request.form['buyer'] == 'buyer' and buyerStatus == "Not Currently a buyer":
                                    buyerid = genBuyerNum()
                                    sql = "INSERT INTO buyer (buyerid, userid) VALUES (%s, %s)"
                                    val = (buyerid, userid)
                                    mycursor.execute(sql, val)
                                    mydb.commit()
                            except:
                                try:
                                    if request.form['seller'] == 'seller' and sellerStatus == "Not Currently a seller":
                                        sellerid = genSellerNum()
                                        sql = "INSERT INTO seller (sellerid, userid) VALUES (%s, %s)"
                                        val = (sellerid, userid)
                                        mycursor.execute(sql, val)
                                        mydb.commit()
                                except:
                                    print("hello")  
    return render_template('auth/profile.html', email = userid, name = name, address = address, 
    password = password, photopath = photo_path, phonenumber = phone_number, securityquestion = securityQuestion, 
    securityanswer = securityAnswer, buyerstatus = buyerStatus, sellerstatus = sellerStatus)
    
    
@bp.route('/logout')
def logout():
    try: 
        sessionid = session['email']
    except:
        return render_template('auth/mustlogin.html')
    session.clear()
    return redirect(url_for('index'))


def genBuyerNum(): 
    newBuyerId = random.randrange(1, 10000, 1)  
    mydb = MiniAmazonGroup14.db.getdb()
    mycursor = mydb.cursor()
    sql = "select buyerid from buyer"
    mycursor.execute(sql)
    nums = mycursor.fetchall()
    if newBuyerId in nums: 
        getBuyerNum()
    else: 
        return newBuyerId

def genSellerNum():
    newSellerId = random.randrange(1, 10000, 1)
    mydb = MiniAmazonGroup14.db.getdb()
    mycursor = mydb.cursor()
    sql = "select sellerid from seller"
    mycursor.execute(sql)
    nums = mycursor.fetchall()
    if newSellerId in nums: 
        getSellerNum()
    else: 
        return newSellerId

def rangencartnum(): 
    cart = random.randrange(10000)  
    mydb = MiniAmazonGroup14.db.getdb()
    mycursor = mydb.cursor()
    sql = "select cartid from cart"
    mycursor.execute(sql)
    nums = mycursor.fetchall()
    if cart in nums: 
        rangencartnum()
    else: 
        return cart