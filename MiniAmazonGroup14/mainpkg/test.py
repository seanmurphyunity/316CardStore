from flask import (
    Blueprint, render_template
)
from mainpkg import db

bp = Blueprint('test', __name__, url_prefix='/test')

@bp.route('/')
def test():
    mydb = db.getdb()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM tutorials_tbl")
    tests = mycursor.fetchall()
    print(tests)
    return render_template('test.html', tests=tests)