from flask import (
    Blueprint, render_template, request, redirect, url_for
)
import MiniAmazonGroup14.db

bp = Blueprint('example', __name__, url_prefix='/example')

@bp.route('/exampleget')
def legolistings():
    mydb = MiniAmazonGroup14.db.getdb()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Example")
    example = mycursor.fetchall()
    #example in this case is what your html will be getting

    return render_template('samplecode/example.html', examples = example)

@bp.route('/examplepost', methods=('GET', 'POST'))
def examplepost():
    if request.method == 'POST':
        exampleformfield = request.form['exampleformfield']
        exformfield = request.form['exformfield']
        mydb = MiniAmazonGroup14.db.getdb()
        mycursor = mydb.cursor()
        sql = "INSERT INTO Example (exampleformfield, exformfield) VALUES (%s, %s)"
        val = (exampleformfield, exformfield)
        mycursor.execute(sql, val)
        mydb.commit()
        return redirect(url_for('samplecode.whateverblueprint'))
    return render_template('samplecode/example.html')


