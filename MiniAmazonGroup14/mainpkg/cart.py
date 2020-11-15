
from flask import (
    Blueprint, render_template, request, redirect, url_for, session)
from mainpkg import db

bp = Blueprint('cart', __name__, url_prefix='/cart')

@bp.route('/cart', methods=('GET', 'POST'))

@bp.route('/cartpage')
def cartpage():
    try: 
        sessionid = session['email']
    except:
        return render_template('auth/mustlogin.html')
    mydb = db.getdb()
    mycursor = mydb.cursor()
    sql = "SELECT * FROM users WHERE userid = '" + sessionid + "'"
    mycursor.execute(sql)
    test = mycursor.fetchall()
    print(test)

    #email = "kelly.george@yahoo.com"  
    #mycursor.execute("SELECT l.name, l.price, l.imageURL, l.id , ci.quantity FROM cart_item ci, Lego l, buyer b, users u WHERE b.userid =%s  and b.userid = u.userid and u.cur_cart  = ci.cartid and l.id = ci.legoid", (sessionid,))
    mycursor.execute("select l.name, l.price, l.imageURL, l.theme, l.year, l.minifigs, l.pieces, l.id, ci.quantity from sells s, cart_item ci, Lego l, users u where u.userid =%s and ci.cartid = u.cur_cart and l.id = ci.legoid and l.id = s.legoid", (sessionid, ))
    #val = 1
    #mycursor.execute(sql,val)
    #user needs to be one that is logged in 
    #cart needs to be current cart
    cart = mycursor.fetchall()
    print(cart)
    #full = mycursor.fetchone()
    totalprice = 0
    for i in cart: 
        totalprice = totalprice + (i[1]* i[8])
    print(totalprice)
    if len(cart) != 0: 
        return render_template('cart/cartpage.html', cart = cart, totalprice = totalprice)
        #return render_template('cart/cartpage.html', cart = cart)
    else: 
       return render_template('cart/emptycart.html')

@bp.route('/cartpage', methods=('GET', 'POST'))
def removefromcart(): 
    if request.method == 'POST':
        try: 
            sessionid = session['email']
        except:
            return render_template('auth/mustlogin.html')
        #cartid = request.form['id']
        #live variable 
        #cartid = 1003
        mydb = db.getdb()
        mycursor = mydb.cursor()
        mycursor.execute('SELECT cur_cart FROM users WHERE userid = %s' , (sessionid, ))
        cart = mycursor.fetchone()[0]
        print(mycursor.fetchone())
        legoid = request.form['legoid']
        quantity = request.form['quantity']
        #legoid = 30732
        #link from legopage
        print(cart, legoid)
        mydb = db.getdb()
        mycursor = mydb.cursor()
        if quantity == '0':
            mycursor.execute('DELETE FROM cart_item where cartid = %s and legoid = %s', (cart, legoid))
        #should delete 
            mydb.commit()
            return render_template('cart/removefromcart.html')
        else: 
            sql = "UPDATE cart_item SET quantity = %s where cartid = %s and legoid = %s"
            val = (quantity, cart, legoid)
            mycursor.execute(sql, val)
            mydb.commit()

             #return redirect(url_for('cart.cartpage'))
            return render_template('cart/updatedcart.html')



#create new cart when checkout 
#@bp.route('/cartpage')
#def cartpage():
    #return render_template('cart/cartpage.html')