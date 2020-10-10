from flask import (
    Blueprint, render_template
)
import MiniAmazonGroup14.db

bp = Blueprint('test', __name__, url_prefix='/test')

@bp.route('/')
def test():
    mydb = MiniAmazonGroup14.db.getdb()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM tutorials_tbl")
    tests = mycursor.fetchall()
    print(tests)
    return render_template('test.html', tests=tests)