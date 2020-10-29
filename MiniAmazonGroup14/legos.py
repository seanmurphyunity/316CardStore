from flask import (
    Blueprint, render_template, request, redirect, url_for, session
)
import MiniAmazonGroup14.db

bp = Blueprint('legos', __name__, url_prefix='/legos')

@bp.route('/legolistings')
def legolistings():
    mydb = MiniAmazonGroup14.db.getdb()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Lego")
    lego = mycursor.fetchall()
    print(lego)
    return render_template('legos/legolistings.html', legos = lego)

@bp.route('/legolistings',  methods=('GET', 'POST'))
def legopage():
    if request.method == 'POST':
        setid = request.form['legoid']
        mydb = MiniAmazonGroup14.db.getdb()
        mycursor = mydb.cursor()
        #sql = "SELECT * FROM Lego WHERE id = %s" 
        #val = (setid)
        mycursor.execute('SELECT * FROM Lego WHERE id = %s', (setid, ))
        olego = mycursor.fetchall()
        print(olego)
        #return redirect(url_for('legos.legopage'))
    return render_template('legos/legopage.html', onelego =olego)

   

@bp.route('/addlego', methods=('GET', 'POST'))
def addlego():
    if request.method == 'POST':
        setid = request.form['id']
        name = request.form['name']
        price = request.form['price']
        theme = request.form['theme']
        year = request.form['year']
        minifigs = request.form['minifigs']
        pieces = request.form['pieces']
        image = request.form['image']
        print(setid, theme, year, name, minifigs, pieces, price, image)
        mydb = MiniAmazonGroup14.db.getdb()
        mycursor = mydb.cursor()
        sql = "INSERT INTO Lego (id, theme, year, name, minifigs, pieces, price, imageURL) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (setid, theme, year, name, minifigs, pieces, price, image)
        mycursor.execute(sql, val)
        mydb.commit()
        return redirect(url_for('legos.addlegosuccess'))
    return render_template('legos/addlego.html')

@bp.route('/legopage', methods=('GET', 'POST'))
def addtocart():
    #needs to link to added to cartpage 
    if request.method == 'POST':
        #cartid = request.form['id']
        #live variable
        try: 
            sessionid = session['email']
        except:
            print('not logged in') 
        mydb = MiniAmazonGroup14.db.getdb()
        mycursor = mydb.cursor()
        mycursor.execute('SELECT cur_cart FROM users WHERE userid = %s' , (sessionid, ))
        cart = mycursor.fetchone()[0]
        print(mycursor.fetchone())
        legoid = request.form['legoid']
        quantity = int(request.form['quantity'])
        #link from legopage
        print(quantity)
        
        mycursor.execute('SELECT * FROM cart_item WHERE cartid = %s and legoid =%s' , (cart, legoid))
        item = mycursor.fetchone()
        sql1 = "SELECT sum(quantity) FROM sells where legoid = %s"
        val2 = (legoid,)
        mycursor.execute(sql1,val2)
        forsale = mycursor.fetchone()
        print(forsale)
        error=None
        if forsale[0] is not None and forsale[0] >= quantity: 
            if item is not None:
                #print(user)
                #error = 'User already registered'
                sql = "UPDATE cart_item SET quantity = %s where cartid = %s and legoid = %s"
                val = (quantity, cart, legoid)
                mycursor.execute(sql, val)
                mydb.commit()
                error = "updated quanity"
                return render_template('cart/addedtocart.html')
            if error is None:
                sql = "INSERT INTO cart_item(cartid, legoid, quantity) VALUES (%s, %s, %s)"
                val = (cart, legoid, quantity)
                mycursor.execute(sql, val)
                mydb.commit()
            
        #return redirect(url_for('legos.addtocart'))
                return render_template('cart/addedtocart.html')
        else: 
            return render_template('cart/quantitylow.html')

@bp.route('/addlegosuccess', methods=('GET', 'POST'))
def addlegosuccess():
    return render_template('legos/addlegosuccess.html')
