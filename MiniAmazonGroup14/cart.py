
from flask import (
    Blueprint, render_template, request, redirect, url_for)
import MiniAmazonGroup14.db

bp = Blueprint('cart', __name__, url_prefix='/cart')

@bp.route('/cart', methods=('GET', 'POST'))

@bp.route('/cartpage')
def cartpage():
    mydb = MiniAmazonGroup14.db.getdb()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT l.name, l.price, l.imageURL, l.id , ci.quantity FROM cart c, cart_item ci, Lego l WHERE c.buyerid = 3 and c.cartid = 1003 and c.cartid = ci.cartid and l.id = ci.legoid")
    #val = 1
    #mycursor.execute(sql,val)
    #user needs to be one that is logged in 
    #cart needs to be current cart
    cart = mycursor.fetchall()
    
    #full = mycursor.fetchone()
    totalprice = 0
    for i in cart: 
        totalprice = totalprice + (i[1]* i[4])
    print(totalprice)
    if len(cart) != 0: 
        return render_template('cart/cartpage.html', cart = cart, totalprice = totalprice)
    else: 
       return render_template('cart/emptycart.html')

@bp.route('/cartpage', methods=('GET', 'POST'))
def removefromcart(): 
    if request.method == 'POST':
        #cartid = request.form['id']
        #live variable 
        cartid = 1003
        legoid = request.form['legoid']
        quantity = request.form['quantity']
        #legoid = 30732
        #link from legopage
        print(cartid, legoid)
        mydb = MiniAmazonGroup14.db.getdb()
        mycursor = mydb.cursor()
        if quantity == '0':
            mycursor.execute('DELETE FROM cart_item where cartid = %s and legoid = %s', (cartid, legoid))
        #should delete 
            mydb.commit()
            return render_template('cart/removefromcart.html')
        else: 
            sql = "UPDATE cart_item SET quantity = %s where cartid = %s and legoid = %s"
            val = (quantity, cartid, legoid)
            mycursor.execute(sql, val)
            mydb.commit()

             #return redirect(url_for('cart.cartpage'))
            return render_template('cart/updatedcart.html')



#create new cart when checkout 
#@bp.route('/cartpage')
#def cartpage():
    #return render_template('cart/cartpage.html')