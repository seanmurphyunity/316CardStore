from flask import (
    Blueprint, render_template
)

bp = Blueprint('cards', __name__, url_prefix='/cards')

@bp.route('/cardlistings')
def cardlistings():
    return render_template('cards/cardlistings.html')

