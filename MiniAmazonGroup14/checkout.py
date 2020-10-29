
from flask import (
    Blueprint, render_template, request, redirect, url_for)
import MiniAmazonGroup14.db

bp = Blueprint('checkout', __name__, url_prefix='/checkout')

@bp.route('/checkout', methods=('GET', 'POST'))


@bp.route('/cartpage', methods=('GET', 'POST'))
def checkout(): 
    if request.method == 'POST':
        try: 
            sessionid = session['email']
        except:
            print('not logged in') 
        mydb = MiniAmazonGroup14.db.getdb()
        mycursor = mydb.cursor()
        mycursor.execute('SELECT cur_cart FROM users WHERE userid = %s' , (sessionid, ))
        cartid = mycursor.fetchone()[0]
        print(mycursor.fetchone())
        #logedin = "abc@abc.com"
        totalprice = request.form['total']
        #cartid = request.form['cartid']
        time = request.form['display']
        pnum = 3100
        print(cartid, time, pnum)
        mydb = MiniAmazonGroup14.db.getdb()
        mycursor = mydb.cursor()
        sql = "SELECT balance FROM users where userid = %s"
        val = (sessionid)
        mycursor.execute(sql, val)
        bal = mycursor.fetchall()
        if bal >= totalprice: 
            sql = "INSERT INTO purchase_history(cartid, purchase_num, date_brought) Values(%s, %s, %s)"
            val = (cartid, pnum, time )
            mycursor.execute(sql, val)
            sql = "UPDATE user SET balance = %s where userid = %s"
            newbal = bal - totalprice
            val = (newbal, sessionid)
            mycursor.execute(sql, val)
            mydb.commit()
            return render_template('checkout/checkoutpage.html')


            
        else: 

            return render_template('checkout/addbalance.html')

    return render_template('cart/cartpage.html')

@bp.route('/checkout', methods=('GET', 'POST'))
def sold():
    if request.method == 'POST':
        #logedin = "abc@abc.com"
        #totalprice = request.form['total']
        cartid = request.form['cartid']
        snum = 4000
      
        print(cartid, time, snum)
        mydb = MiniAmazonGroup14.db.getdb()
        mycursor = mydb.cursor()
        sql = "select ci.legoid, s.sellerid, ca.buyerid, c.date_bought, ci.quantity from checkout c, cart_item ci, sells s, cart ca where c.cartid = %s and c.cartid = c1.cartid and ci.legoid = s.legoid and ci.cartid = ca.cartid"
        val = (cartid)
        mycursor.execute(sql, val)
        items = mycursor.fetchall()
        print(items)
        for i in items:
            sql1  = "Insert into sold values(i[0]" 


        #add items from cart that checked out to sold 
        
      

