
from flask import (
    Blueprint, render_template, request, redirect, url_for)
import MiniAmazonGroup14.db

bp = Blueprint('checkout', __name__, url_prefix='/checkout')

@bp.route('/checkout', methods=('GET', 'POST'))


@bp.route('/checkout', methods=('GET', 'POST'))
def checkout(): 
    if request.method == 'POST':
        logedin = "abc@abc.com"
        totalprice = request.form['total']
        cartid = request.form['cartid']
        time = request.form['time']
        pnum = request.form['pnum']
        print(cartid, time, pnum)
        mydb = MiniAmazonGroup14.db.getdb()
        mycursor = mydb.cursor()
        sql = "SELECT balance FROM users where userid = %s"
        val = (logedin)
        mycursor.execute(sql, val)
        bal = mycursor.fetchall()
        if bal > totalprice: 
            date= 
            pnum 


        mydb.commit()
        return redirect(url_for('legos.addlegosuccess'))
    return render_template('checkout/checkoutpage.html')

