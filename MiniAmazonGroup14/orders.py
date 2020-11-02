
from flask import (
    Blueprint, render_template, request, redirect, url_for, session)

import MiniAmazonGroup14.db

bp = Blueprint('orders', __name__, url_prefix='/orders')


@bp.route('/purchase_history')
def purchase_history():
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
    mycursor.execute("SELECT bh.purchase_num, bh.date_bought FROM buyer b, buyer_history bh WHERE b.userid = %s and b.buyerid = bh.buyerid", (sessionid, ))
    #mycursor.execute("SELECT * FROM buyer_history")
    items = mycursor.fetchall()
    print(items)
    return render_template('orders/purchase_history.html', items =items)

@bp.route('/purchase', methods=('GET', 'POST'))
def purchase():
    mydb = MiniAmazonGroup14.db.getdb()
    pnum = request.form['pnum']
    print(pnum)
    mycursor = mydb.cursor()
    try: 
        sessionid = session['email']
    except:
        print('not logged in')
    sql = "SELECT * FROM users WHERE userid = '" + sessionid + "'"
    mycursor.execute(sql)
    test = mycursor.fetchall()
    print(test)
    mycursor.execute("SELECT bh.purchase_num, bh.date_bought, ci.quantity, l.name, l.price FROM Lego l, buyer_history bh, checkout c, cart_item ci WHERE c.purchase_num = %s and bh.purchase_num = c.purchase_num and c.cartid = ci.cartid and l.id = ci.legoid", (pnum, ))
    # and b.userid = u.userid and b.userid = %s and b.buyerid = bh.buyerid and bh.purchase_num = c.purchase_num and ci.cartid = c.cartid and l.id = ci.legoid", (sessionid, ))
    #mycursor.execute("SELECT * FROM buyer_history")
    items = mycursor.fetchall()
    #print(items)
    return render_template('orders/purchase.html', items =items)


@bp.route('/sales_history')
def sales_history():
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
    mycursor.execute("SELECT sh.sales_num, sh.date_bought FROM buyer b, sales_history sh WHERE b.userid = %s and b.buyerid = bh.buyerid", (sessionid, ))
    #mycursor.execute("SELECT * FROM buyer_history")
    items = mycursor.fetchall()
    print(items)
    return render_template('orders/sales_history.html', items =items)