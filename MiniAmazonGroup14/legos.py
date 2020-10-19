from flask import (
    Blueprint, render_template, request, redirect, url_for
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


@bp.route('/addlegosuccess', methods=('GET', 'POST'))
def addlegosuccess():
    return render_template('legos/addlegosuccess.html')
