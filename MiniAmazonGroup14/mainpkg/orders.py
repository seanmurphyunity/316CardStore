
from flask import (
    Blueprint, render_template, request, redirect, url_for, session)

from mainpkg import db
import random

bp = Blueprint('orders', __name__, url_prefix='/orders')


@bp.route('/purchase_history', methods=('GET','POST'))
def purchase_history():
    mydb = db.getdb()
    mycursor = mydb.cursor()
    try: 
        sessionid = session['email']
    except:
        print('not logged in')
    sql = "SELECT * FROM users WHERE userid = '" + sessionid + "'"
    mycursor.execute(sql)
    test = mycursor.fetchall()
    mycursor.execute("SELECT bh.purchase_num, bh.date_bought FROM buyer b, buyer_history bh WHERE b.userid = %s and b.buyerid = bh.buyerid", (sessionid, ))
    #mycursor.execute("SELECT * FROM buyer_history")
    items = mycursor.fetchall()
    return render_template('orders/purchase_history.html', items = items)

@bp.route('/purchase', methods=('GET', 'POST'))
def purchase():
    mydb = db.getdb()
    pnum = request.form['pnum']
    mycursor = mydb.cursor()
    try: 
        sessionid = session['email']
    except:
        print('not logged in')
    sql = "SELECT * FROM users WHERE userid = '" + sessionid + "'"
    mycursor.execute(sql)
    test = mycursor.fetchall()
    mycursor.execute("SELECT bh.purchase_num, bh.date_bought, ci.quantity, l.name, l.price, l.id, se.userid,l.imageURL, l.theme, l.year, l.minifigs, l.pieces FROM Lego l, buyer_history bh, checkout c, cart_item ci, sells s, seller se WHERE c.purchase_num = %s and bh.purchase_num = c.purchase_num and c.cartid = ci.cartid and l.id = ci.legoid and s.legoid = ci.legoid and s.sellerid = se.sellerid", (pnum, ))
    # and b.userid = u.userid and b.userid = %s and b.buyerid = bh.buyerid and bh.purchase_num = c.purchase_num and ci.cartid = c.cartid and l.id = ci.legoid", (sessionid, ))
    #mycursor.execute("SELECT * FROM buyer_history")
    items = mycursor.fetchall()
    print(items)
    try:
        mydb = db.getdb()
        mycursor = mydb.cursor()
        star_input = request.form['stars']
        if star_input > 5:
            stars = 5
        if star_input < 1:
            stars = 1
        review_text = request.form['review_text']
        reviewid = genReviewId()
        purchase_num = items[0][0]
        date_bought = items[0][1]
        mycursor.execute("select buyerid from buyer where userid = '" + sessionid + "'")
        buyerid = mycursor.fetchone()[0]
        mycursor.execute("select sellerid from sold where buyerid ='" + str(buyerid) + '" and date_sold = "' + str(date_bought) + "'")
        sellerid = mycursor.fetchall()[0][0]
        mycursor.execute("select sales_num from sold where buyerid ='" + str(buyerid) + '" and date_sold = "' + str(date_bought) + "'")
        sales_num = mycursor.fetchall()[0][0]
        mycursor.execute("select legoid from sold where buyerid ='" + str(buyerid) + "' and date_sold = '" + str(date_bought) + "'")
        legoid = mycursor.fetchall()[0][0]
        if mycursor.execute("select * from Review where reviewid ='" + str(reviewid) + "' and sales_num = '" + str(sales_num) + "' buyerid ='" + str(buyerid) + "' and sellerid = '" + str(sellerid) + "' and legoid = '" + str(legoid) + "'stars ='").fetchall()[0][0] is None:
            sql = "INSERT INTO Review (reviewid, sales_num, buyerid, sellerid, legoid, stars, review_text) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (reviewid, sales_num, buyerid, sellerid, legoid, stars, review_text)
            mycursor.execute(sql, val)
            mydb.commit()
    except:
       print("Did not function properly")
    
    return render_template('orders/purchase.html', items = items)


@bp.route('/sales_history')
def sales_history():
    mydb = db.getdb()
    mycursor = mydb.cursor()
    try: 
        sessionid = session['email']
    except:
        print('not logged in')
    sql = "SELECT * FROM users WHERE userid = '" + sessionid + "'"
    mycursor.execute(sql)
    test = mycursor.fetchall()
    print(test)
    mycursor.execute("SELECT sh.sales_num, sh.date_bought FROM seller s, sales_history sh WHERE s.userid = %s and s.sellerid = sh.sellerid", (sessionid, ))
    #mycursor.execute("SELECT * FROM buyer_history")
    items = mycursor.fetchall()
    #print(items)
    return render_template('orders/sales_history.html', items =items)

@bp.route('/sale', methods=('GET', 'POST'))
def sale():
    mydb = db.getdb()
    snum = request.form['snum']
    print(snum)
    mycursor = mydb.cursor()
    try: 
        sessionid = session['email']
    except:
        print('not logged in')
    sql = "SELECT * FROM users WHERE userid = '" + sessionid + "'"
    mycursor.execute(sql)
    test = mycursor.fetchall()
    print(test)
    mycursor.execute("SELECT sh.sales_num, sh.date_bought, so.quantity, l.name, l.price, b.userid, l.id, l.imageURL, l.theme, l.year, l.minifigs, l.pieces FROM Lego l, sales_history sh, sold so, buyer b WHERE sh.sales_num = %s and sh.sales_num = so.sales_num and l.id = so.legoid and so.buyerid = b.buyerid", (snum, ))
    # and b.userid = u.userid and b.userid = %s and b.buyerid = bh.buyerid and bh.purchase_num = c.purchase_num and ci.cartid = c.cartid and l.id = ci.legoid", (sessionid, ))
    #mycursor.execute("SELECT * FROM buyer_history")
    items = mycursor.fetchall()
    print(items)
    return render_template('orders/sale.html', items =items)

def genReviewId():
    newReviewId = random.randrange(3000, 1000000, 1)
    mydb = db.getdb()
    mycursor = mydb.cursor()
    mycursor.execute("select reviewID from Review")
    nums = mycursor.fetchall()
    if newReviewId in nums: 
        genReviewId
    else: 
        return newReviewId