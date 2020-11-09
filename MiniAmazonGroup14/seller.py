from flask import (
    Blueprint, render_template, request, redirect, url_for, session)
import MiniAmazonGroup14.db

bp = Blueprint('seller', __name__, url_prefix='/seller')

@bp.route('/seller', methods=('GET', 'POST'))

@bp.route('/mylegos')
def mylegos():
    mydb = MiniAmazonGroup14.db.getdb()
    mycursor = mydb.cursor()
    try: 
        sessionid = session['email']
    except:
        print('not logged in')
    sql = "SELECT * FROM users WHERE userid = '" + sessionid + "'"
    mycursor.execute(sql)
    test = mycursor.fetchall()
    print(test)
    #email = "kelly.george@yahoo.com"  
    mycursor.execute("SELECT l.name, l.price, l.imageURL, l.id , s.quantity FROM Seller s, Lego l WHERE s.userid =%s and l.sellerid  = s.userid", (sessionid,))
    #val = 1
    #mycursor.execute(sql,val)
    #user needs to be one that is logged in 
    seller = mycursor.fetchall()
    print(seller)
    #full = mycursor.fetchone()
    if len(seller) != 0: 
        return render_template('seller/mylegos.html', seller = seller)
    else: 
       return render_template('seller/nolegos.html')