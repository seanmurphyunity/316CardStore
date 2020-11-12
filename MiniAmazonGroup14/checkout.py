
from flask import (
    Blueprint, render_template, request, redirect, url_for, session)
import random
from datetime import  datetime
import MiniAmazonGroup14.db

bp = Blueprint('checkout', __name__, url_prefix='/checkout')




@bp.route('/checkout', methods=('GET', 'POST'))
def checkout():
    try: 
        sessionid = session['email']
    except:
        return render_template('auth/mustlogin.html') 
    if request.method == 'POST':
        mydb = MiniAmazonGroup14.db.getdb()
        mycursor = mydb.cursor()
        mycursor.execute('SELECT cur_cart FROM users WHERE userid = %s' , (sessionid, ))
        cartid = mycursor.fetchone()[0]
        mycursor.execute('SELECT buyerid FROM buyer WHERE userid = %s' , (sessionid, ))
        buyerid = mycursor.fetchone()[0]
        print(mycursor.fetchone())
        #logedin = "abc@abc.com"
        totalprice = float(request.form['total'])
        #cartid = request.form['cartid']
        #time = request.form['display']
        date = datetime.now() 
        #print(date)
        time =  date.strftime("%Y-%m-%d %H:%M:%S" )
        pnum = rangenpnum()
        print(time)
        print(cartid, time, pnum)
        mydb = MiniAmazonGroup14.db.getdb()
        mycursor = mydb.cursor()
        sql = "SELECT balance FROM users where userid = %s"
        val = (sessionid,)
        mycursor.execute(sql, val)
        
        bal = mycursor.fetchall()[0][0]
        print(bal)
        print(totalprice)
        if bal >= totalprice: 
            mycursor.execute("INSERT INTO buyer_history(buyerid, purchase_num, date_bought) Values(%s, %s, %s)",(buyerid, pnum, time ))
            mydb.commit()
            mycursor.execute("INSERT INTO checkout(cartid, purchase_num, date_bought) Values(%s, %s, %s)",(cartid, pnum, time ))
            mydb.commit()
            sql = "UPDATE users SET balance = %s where userid = %s"
            newbal = bal - totalprice
            val = (newbal, sessionid)
            mycursor.execute(sql, val)
            mydb.commit()
            createnewcart(sessionid)
            sold(cartid, sessionid)
            return render_template('checkout/checkoutpage.html')
        else: 

            return render_template('checkout/addbalance.html')

    return render_template('cart/cartpage.html')

def createnewcart(sessionid): 
    newcart = rangencartnum()
    mydb = MiniAmazonGroup14.db.getdb()
    mycursor = mydb.cursor()
    mycursor.execute("select buyerid from buyer where userid = %s", (sessionid, ))
    buyerid = mycursor.fetchall()[0][0]
    print(buyerid)
    mycursor.execute("INSERT INTO cart(cartid, buyerid) VALUES(%s, %s)", (newcart, buyerid))
    mydb.commit()
    mycursor.execute("UPDATE users SET cur_cart = %s where userid = %s", (newcart, sessionid))
    mydb.commit()
    return 

@bp.route('/checkoutpage', methods=('GET', 'POST'))
def sold(cartid, sessionid):
    try: 
        sessionid = session['email']
    except:
        return render_template('auth/mustlogin.html')
    if request.method == 'POST':
        #logedin = "abc@abc.com"
        #totalprice = request.form['total']
        
        #snum = rangensnum()
      
        print(cartid)
        mydb = MiniAmazonGroup14.db.getdb()
        mycursor = mydb.cursor()
        sql = "select ci.legoid, s.sellerid, ca.buyerid, c.date_bought, ci.quantity, s.quantity, l.price from checkout c, cart_item ci, sells s, cart ca, Lego l where c.cartid = %s and l.id = ci.legoid and c.cartid = ci.cartid and ci.legoid = s.legoid and ci.cartid = ca.cartid"
        val = (cartid, )
        mycursor.execute(sql, val)
        items = mycursor.fetchall()
        
        print(items)
        for i in items:
            snum = rangensnum()
            #inserts sold items 
            sql1  = "Insert into sold values(%s, %s, %s,%s, %s, %s)" 
            val1 = (i[1], i[0],i[2],i[3], snum, i[4])
            mycursor.execute(sql1, val1)
            mydb.commit()
            newq = i[4] - i[5]
            #updates q available 
            sql2  = "update sells set quantity = %s where sellerid = %s and legoid  = %s" 
            val2 = (newq, i[1], i[0])
            mycursor.execute(sql2, val2)
            mydb.commit()
            # puts sale into sales history 
            sql3 = "insert into sales_history values(%s, %s, %s)"
            val3 = (snum, i[1],i[3])
            mycursor.execute(sql3, val3) 
            mydb.commit()
            #adds money to seller
            mycursor.execute("Select userid from seller where sellerid = %s", (i[1],))
            user = mycursor.fetchall()[0][0]
            sql4 = "Update users set balance = %s where userid = %s"
            p = i[6] * i[5]
            val4 = (p, user)
            mycursor.execute(sql4, val4) 
            mydb.commit()
            return
        

@bp.route('/balancepage', methods=('GET', 'POST'))
def balancepage():
    try: 
        sessionid = session['email']
    except:
        return render_template('auth/mustlogin.html')
    mydb = MiniAmazonGroup14.db.getdb()
    mycursor = mydb.cursor()
    
    mycursor.execute('select balance FROM users WHERE userid = %s' , (sessionid, ))
    curbal = mycursor.fetchone()[0]
    return render_template('checkout/addbalance.html', curbal = curbal)    

@bp.route('/addbalance', methods=('GET', 'POST'))
def addbalance():
    try: 
        sessionid = session['email']
    except:
        return render_template('auth/mustlogin.html')
    if request.method == 'POST':
        #need to add balance 
        mydb = MiniAmazonGroup14.db.getdb()
        mycursor = mydb.cursor()
        addamt = request.form['amt']
        mycursor.execute('select balance FROM users WHERE userid = %s' , (sessionid, ))
        curbal = mycursor.fetchone()[0]
        if float(addamt) < 0: 
            return render_template('checkout/badbalance.html')
        else: 
            newb = float(curbal) + float(addamt) 
            print(newb)
            mycursor.execute('UPDATE users SET balance = %s WHERE userid = %s' , (newb, sessionid, ))
            mydb.commit()
            return render_template('checkout/newbalance.html', newb = newb)

       


def rangensnum(): 
    s = random.randrange(10000)  
    mydb = MiniAmazonGroup14.db.getdb()
    mycursor = mydb.cursor()
    sql = "select sales_num from sales_history"
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

def rangencartnum(): 
    cart = random.randrange(10000)  
    mydb = MiniAmazonGroup14.db.getdb()
    mycursor = mydb.cursor()
    sql = "select cartid from cart"
    mycursor.execute(sql)
    nums = mycursor.fetchall()
    if cart in nums: 
        rangencartnum
    else: 
        return cart
