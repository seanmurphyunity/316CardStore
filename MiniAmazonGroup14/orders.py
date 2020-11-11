
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
    mycursor.execute("SELECT bh.purchase_num, bh.date_bought, ci.quantity, l.name, l.price, l.id, se.userid,l.imageURL FROM Lego l, buyer_history bh, checkout c, cart_item ci, sold s, seller se WHERE c.purchase_num = %s and bh.purchase_num = c.purchase_num and c.cartid = ci.cartid and l.id = ci.legoid and s.date_sold = bh.date_bought and s.legoid = ci.legoid and s.sellerid = se.sellerid", (pnum, ))
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
    mycursor.execute("SELECT sh.sales_num, sh.date_bought FROM seller s, sales_history sh WHERE s.userid = %s and s.sellerid = sh.sellerid", (sessionid, ))
    #mycursor.execute("SELECT * FROM buyer_history")
    items = mycursor.fetchall()
    print(items)
    return render_template('orders/sales_history.html', items =items)

@bp.route('/sale', methods=('GET', 'POST'))
def sale():
    mydb = MiniAmazonGroup14.db.getdb()
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
    mycursor.execute("SELECT sh.sales_num, sh.date_bought, so.quantity, l.name, l.price, b.userid, l.id, l.imageURL FROM Lego l, sales_history sh, sold so, buyer b WHERE sh.sales_num = %s and sh.sales_num = so.sales_num and  l.id = so.legoid and so.buyerid = b.buyerid", (snum, ))
    # and b.userid = u.userid and b.userid = %s and b.buyerid = bh.buyerid and bh.purchase_num = c.purchase_num and ci.cartid = c.cartid and l.id = ci.legoid", (sessionid, ))
    #mycursor.execute("SELECT * FROM buyer_history")
    items = mycursor.fetchall()
    #print(items)
    return render_template('orders/sale.html', items =items)