from flask import (
    Blueprint, render_template, request, redirect, url_for, session
)
import MiniAmazonGroup14.db

bp = Blueprint('legos', __name__, url_prefix='/legos')

@bp.route('/legolistings',  methods=('GET', 'POST'))
def legolistings():
    mydb = MiniAmazonGroup14.db.getdb()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Lego")
    lego = mycursor.fetchall()
    print(lego)
    return render_template('legos/legolistings.html', legos = lego)

@bp.route('/legopage/<legoid>',  methods=('GET', 'POST'))
def legopage(legoid):

        #setid = request.form['legoid']
    mydb = MiniAmazonGroup14.db.getdb()
    mycursor = mydb.cursor()
        #sql = "SELECT * FROM Lego WHERE id = %s" 
        #val = (setid)
    mycursor.execute('SELECT * FROM Lego WHERE id = %s', (legoid, ))
    lego = mycursor.fetchall()
    print(lego)
        #return redirect(url_for('legos.legopage', legoid =legoid))
    return render_template('legos/legopage.html', legoid =legoid, onelego = lego)

@bp.route('/search',  methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        searchterm = request.form['search']
        mydb = MiniAmazonGroup14.db.getdb()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM Lego WHERE name LIKE '%" + searchterm + "%'")
        search = mycursor.fetchall()
        print(search)
        return render_template('legos/searchresults.html', search = search)
    return render_template('legos/searchpage.html')

@bp.route('/categoryselect',  methods=('GET', 'POST'))
def categoryselect():
    if request.method == 'POST':
        mydb = MiniAmazonGroup14.db.getdb()
        mycursor = mydb.cursor()
        
        try:
            searchterm = request.form['theme']
            mycursor.execute("SELECT * FROM Lego WHERE theme LIKE '%" + searchterm + "%'")
            category = mycursor.fetchall()
            title = "Theme Search Results"
            return render_template('legos/categoryresults.html', category = category, title = title)
        except:
            try:
                minpieces = request.form['minpieces']
                maxpieces = request.form['maxpieces']
                sql = "SELECT * FROM Lego WHERE pieces >= " + minpieces + " AND pieces <= " + maxpieces
                mycursor.execute(sql)
                category = mycursor.fetchall()
                title = str(minpieces) + " to " + str(maxpieces) + " Pieces"
                return render_template('legos/categoryresults.html', category = category, title = title)
            except:
                try:
                    minminifigs = request.form['minminifigs']
                    maxminifigs = request.form['maxminifigs']
                    sql = "SELECT * FROM Lego WHERE minifigs >= " + str(minminifigs) + " AND minifigs <= " + str(maxminifigs)
                    mycursor.execute(sql)
                    category = mycursor.fetchall()
                    title = str(minminifigs) + " to " + str(maxminifigs) + " Minifigs"
                    return render_template('legos/categoryresults.html', category = category, title = title)
                except:
                    try:
                        minprice = request.form['minprice']
                        maxprice = request.form['maxprice']
                        sql = "SELECT * FROM Lego WHERE price >= " + minprice + " AND price <= " + maxprice
                        mycursor.execute(sql)
                        category = mycursor.fetchall()
                        title = "$" + str(minprice) + " to " + "$" + str(maxprice)
                        return render_template('legos/categoryresults.html', category = category, title = title)
                    except: 
                        try:
                            minyear = request.form['minyear']
                            maxyear = request.form['maxyear']
                            sql = "SELECT * FROM Lego WHERE year >= " + minyear + " AND year <= " + maxyear
                            mycursor.execute(sql)
                            category = mycursor.fetchall()
                            title = str(minyear) + " to " + str(maxyear)
                            return render_template('legos/categoryresults.html', category = category, title = title)
                        except:
                            return render_template('legos/categoryselect.html')

    return render_template('legos/categoryselect.html')

@bp.route('/category/<categoryid>',  methods=('GET', 'POST'))
def category(categoryid):
    mydb = MiniAmazonGroup14.db.getdb()
    mycursor = mydb.cursor()

    #themes
    if categoryid == 'starwars':
        sql = "SELECT * FROM Lego WHERE theme = 'Star Wars'"
        title = "Star Wars"
        mycursor.execute(sql)
        category = mycursor.fetchall()
        return render_template('legos/categoryresults.html', category = category, title = title)
    elif categoryid == 'duplo':
        sql = "SELECT * FROM Lego WHERE theme = 'Duplo'"
        title = "Duplo"
        mycursor.execute(sql)
        category = mycursor.fetchall()
        return render_template('legos/categoryresults.html', category = category, title = title)
    elif categoryid == 'harrypotter':
        sql = "SELECT * FROM Lego WHERE theme = 'Harry Potter'"
        title = "Harry Potter"
        mycursor.execute(sql)
        category = mycursor.fetchall()
        return render_template('legos/categoryresults.html', category = category, title = title)
    elif categoryid == 'creatorexpert':
        sql = "SELECT * FROM Lego WHERE theme = 'Creator Expert'"
        title = "Creator Expert"
        mycursor.execute(sql)
        category = mycursor.fetchall()
        return render_template('legos/categoryresults.html', category = category, title = title)

    #pieces
    elif categoryid == 'pieces0':
        sql = "SELECT * FROM Lego WHERE pieces >= 0 AND pieces <= 100"
        title = "0 - 100 Pieces"
        mycursor.execute(sql)
        category = mycursor.fetchall()
        return render_template('legos/categoryresults.html', category = category, title = title)
    elif categoryid == 'pieces1':
        sql = "SELECT * FROM Lego WHERE pieces >= 100 AND pieces <= 250"
        title = "100 - 250 Pieces"
        mycursor.execute(sql)
        category = mycursor.fetchall()
        return render_template('legos/categoryresults.html', category = category, title = title)
    if categoryid == 'pieces2':
        sql = "SELECT * FROM Lego WHERE pieces >= 250 AND pieces <= 500"
        title = "250 - 500 Pieces"
        mycursor.execute(sql)
        category = mycursor.fetchall()
        return render_template('legos/categoryresults.html', category = category, title = title)
    if categoryid == 'pieces3':
        sql = "SELECT * FROM Lego WHERE pieces >= 500 AND pieces <= 1000"
        title = "500 - 1,000 Pieces"
        mycursor.execute(sql)
        category = mycursor.fetchall()
        return render_template('legos/categoryresults.html', category = category, title = title)
    if categoryid == 'pieces4':
        sql = "SELECT * FROM Lego WHERE pieces >= 1000 AND pieces <= 2000"
        title = "1,000 - 2,000 Pieces"
        mycursor.execute(sql)
        category = mycursor.fetchall()
        return render_template('legos/categoryresults.html', category = category, title = title)
    if categoryid == 'pieces5':
        sql = "SELECT * FROM Lego WHERE pieces >= 2000 AND pieces <= 3500"
        title = "2,000 - 3,500 Pieces"
        mycursor.execute(sql)
        category = mycursor.fetchall()
        return render_template('legos/categoryresults.html', category = category, title = title)
    if categoryid == 'pieces6':
        sql = "SELECT * FROM Lego WHERE pieces >= 3500 AND pieces <= 5000"
        title = "3,500 - 5,000 Pieces"
        mycursor.execute(sql)
        category = mycursor.fetchall()
        return render_template('legos/categoryresults.html', category = category, title = title)
    if categoryid == 'pieces7':
        sql = "SELECT * FROM Lego WHERE pieces >= 5000 AND pieces <= 10000"
        title = "5,000 - 10,000 Pieces"
        mycursor.execute(sql)
        category = mycursor.fetchall()
        return render_template('legos/categoryresults.html', category = category, title = title)
    if categoryid == 'pieces8':
        sql = "SELECT * FROM Lego WHERE pieces >= 10000"
        title = "10,000+ Pieces"
        mycursor.execute(sql)
        category = mycursor.fetchall()
        return render_template('legos/categoryresults.html', category = category, title = title)

    #minifigs
    if categoryid == 'minifigs0':
        sql = "SELECT * FROM Lego WHERE minifigs >= 0 AND minifigs <= 2"
        title = "0-2 Minifigs"
        mycursor.execute(sql)
        category = mycursor.fetchall()
        return render_template('legos/categoryresults.html', category = category, title = title)
    if categoryid == 'minifigs1':
        sql = "SELECT * FROM Lego WHERE minifigs >= 3 AND minifigs <= 5"
        title = "3-5 Minifigs"
        mycursor.execute(sql)
        category = mycursor.fetchall()
        return render_template('legos/categoryresults.html', category = category, title = title)
    if categoryid == 'minifigs2':
        sql = "SELECT * FROM Lego WHERE minifigs >= 6 AND minifigs <= 9"
        title = "6-9 Minifigs"
        mycursor.execute(sql)
        category = mycursor.fetchall()
        return render_template('legos/categoryresults.html', category = category, title = title)
    if categoryid == 'minifigs3':
        sql = "SELECT * FROM Lego WHERE minifigs >= 10"
        title = "10+ Minifigs"
        mycursor.execute(sql)
        category = mycursor.fetchall()
        return render_template('legos/categoryresults.html', category = category, title = title)

    #year
    elif categoryid == 'year2018':
        sql = "SELECT * FROM Lego WHERE year = 2018"
        title = "2018 Sets"
        mycursor.execute(sql)
        category = mycursor.fetchall()
        return render_template('legos/categoryresults.html', category = category, title = title)
    elif categoryid == 'year2019':
        sql = "SELECT * FROM Lego WHERE year = 2019"
        title = "2019 Sets"
        mycursor.execute(sql)
        category = mycursor.fetchall()
        return render_template('legos/categoryresults.html', category = category, title = title)
    elif categoryid == 'year2020':
        sql = "SELECT * FROM Lego WHERE year = 2020"
        title = "2020 Sets"
        mycursor.execute(sql)
        category = mycursor.fetchall()
        return render_template('legos/categoryresults.html', category = category, title = title)

    #price
    if categoryid == 'price0':
        sql = "SELECT * FROM Lego WHERE price >= 0 AND price <= 25"
        title = "$0 - $25"
        mycursor.execute(sql)
        category = mycursor.fetchall()
        return render_template('legos/categoryresults.html', category = category, title = title)
    if categoryid == 'price1':
        sql = "SELECT * FROM Lego WHERE price >= 25 AND price <= 50"
        title = "$25 - $50"
        mycursor.execute(sql)
        category = mycursor.fetchall()
        return render_template('legos/categoryresults.html', category = category, title = title)
    if categoryid == 'price2':
        sql = "SELECT * FROM Lego WHERE price >= 50 AND price <= 100"
        title = "$50 - $100"
    if categoryid == 'price3':
        sql = "SELECT * FROM Lego WHERE price >= 100 AND price <= 200"
        title = "$100 - $200"
        mycursor.execute(sql)
        category = mycursor.fetchall()
        return render_template('legos/categoryresults.html', category = category, title = title)
    if categoryid == 'price4':
        sql = "SELECT * FROM Lego WHERE price >= 200 AND price <= 500"
        title = "$200 - $500"
        mycursor.execute(sql)
        category = mycursor.fetchall()
        return render_template('legos/categoryresults.html', category = category, title = title)
    if categoryid == 'price5':
        sql = "SELECT * FROM Lego WHERE price >= 500"
        title = "500+"
        mycursor.execute(sql)
        category = mycursor.fetchall()
        return render_template('legos/categoryresults.html', category = category, title = title)

    return render_template('legos/categoryselect.html')

   

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

@bp.route('/addtocart', methods=('GET', 'POST'))
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
