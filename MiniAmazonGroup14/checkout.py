
from flask import (
    Blueprint, render_template, request, redirect, url_for, session)
import random
import MiniAmazonGroup14.db

bp = Blueprint('checkout', __name__, url_prefix='/checkout')




@bp.route('/checkout', methods=('GET', 'POST'))
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
        pnum = rangenpnum()
        print(time)
        print(cartid, time, pnum)
        mydb = MiniAmazonGroup14.db.getdb()
        mycursor = mydb.cursor()
        sql = "SELECT balance FROM users where userid = %s"
        val = (sessionid)
        mycursor.execute(sql, val)
        bal = mycursor.fetchall()
        if bal >= totalprice: 
            sql = "INSERT INTO purchase_history(cartid, purchase_num, date_brought) Values(%s, %s, %s)"
            val = (cartid, pnum, time)
            mycursor.execute(sql, val)
            sql = "UPDATE user SET balance = %s where userid = %s"
            newbal = bal - totalprice
            val = (newbal, sessionid)
            mycursor.execute(sql, val)
            mydb.commit()
            #sold(cartid)
            return render_template('checkout/checkoutpage.html')


            
        else: 

            return render_template('checkout/addbalance.html')

    return render_template('cart/cartpage.html')

@bp.route('/checkoutpage', methods=('GET', 'POST'))
def sold(cartid):
    if request.method == 'POST':
        #logedin = "abc@abc.com"
        #totalprice = request.form['total']
        
        #snum = rangensnum()
      
        print(cartid)
        mydb = MiniAmazonGroup14.db.getdb()
        mycursor = mydb.cursor()
        sql = "select ci.legoid, s.sellerid, ca.buyerid, c.date_bought, ci.quantity, s.quantity, l.price from checkout c, cart_item ci, sells s, cart ca, Legos l where c.cartid = %s and l.legoid = ci.legoid and c.cartid = c1.cartid and ci.legoid = s.legoid and ci.cartid = ca.cartid"
        val = (cartid)
        mycursor.execute(sql, val)
        items = mycursor.fetchall()
        
        print(items)
        for i in items:
            snum = rangensnum()
            #inserts sold items 
            sql1  = "Insert into sold values(%s, %s, %s,%s, %s, %s)" 
            val1 = (i[1], i[0],i[2],i[3], snum, i[4])
            mycursor.execute(sql1, val1)
            newq = i[4] - i[5]
            #updates q available 
            sql2  = "update sells set quantity = %s where sellerid = %s and legoid  = %s" 
            val2 = (newq, i[1], i[0])
            mycursor.execute(sql2, val2)
            # puts sale into sales history 
            sql3 = "insert into sales_history values(%s, %s, %s)"
            val3 = (snum, i[1],i[3])
            mycursor.execute(sql3, val3) 
            sql4 = ""
            #p = 
            val4 = (p)
            return
        

@bp.route('/balancepage', methods=('GET', 'POST'))
def balancepage():
    return render_template('checkout/addbalance.html')    

@bp.route('/addbalance', methods=('GET', 'POST'))
def addbalance():
    if request.method == 'POST':
        #need to add balance 
        try: 
            sessionid = session['email']
        except:
            print('not logged in') 
        mydb = MiniAmazonGroup14.db.getdb()
        mycursor = mydb.cursor()
        addamt = request.form['amt']
        mycursor.execute('select balance FROM users WHERE userid = %s' , (sessionid, ))
        curbal = mycursor.fetchone()[0]
        newb = float(curbal) + float(addamt) 
        print(newb)
        mycursor.execute('UPDATE users SET balance = %s WHERE userid = %s' , (newb, sessionid, ))
        mydb.commit()
        return render_template('checkout/newbalance.html', newb = newb)

       


def rangensnum(): 
    s = random.randrange(10000)  
    mydb = MiniAmazonGroup14.db.getdb()
    mycursor = mydb.cursor()
    sql = "select sale_num from sales_history"
    mycursor.execute(sql)
    nums = mycursor.fetchall()
    if s in nums: 
        rangensnum
    else: 
        return s  
    
def rangenpnum(): 
    p = random.randrange(10000)  
    mydb = MiniAmazonGroup14.db.getdb()
    mycursor = mydb.cursor()
    sql = "select purchase_num from buyer_history"
    mycursor.execute(sql)
    nums = mycursor.fetchall()
    if p in nums: 
        rangenpnum
    else: 
        return p
