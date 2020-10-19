from flask import (
    Blueprint, render_template
)
import MiniAmazonGroup14.db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login')
def login():
    return render_template('auth/login.html')

@bp.route('/register')
def register():
    return render_template('auth/register.html')

@bp.route('/account')
def account():
    return render_template('auth/account.html')