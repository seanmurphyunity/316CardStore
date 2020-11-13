from flask import Flask, render_template, request

from mainpkg import auth 
from mainpkg import legos
from mainpkg import test
from mainpkg import cart 
from mainpkg import orders
from mainpkg import db 
from mainpkg import checkout



app = Flask(__name__)
app.config.from_mapping(SECRET_KEY='dev')

@app.route('/')
def index():
	return render_template('index.html')


app.register_blueprint(auth.bp)
app.register_blueprint(legos.bp)
app.register_blueprint(test.bp)
app.register_blueprint(cart.bp)
app.register_blueprint(orders.bp)
app.register_blueprint(checkout.bp)
#db.createtest()
#db.posttest()
#db.gettest()

#Once we are on a production server we will use something like this
#app.run(host='0.0.0.0')