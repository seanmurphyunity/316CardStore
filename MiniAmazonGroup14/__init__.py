from flask import Flask, render_template, request

import MiniAmazonGroup14.auth

import MiniAmazonGroup14.legos

import MiniAmazonGroup14.test

import MiniAmazonGroup14.cart

import MiniAmazonGroup14.orders

import MiniAmazonGroup14.db

import MiniAmazonGroup14.checkout

app = Flask(__name__)
app.config.from_mapping(SECRET_KEY='dev')

@app.route('/')
def index():
	return render_template('index.html')


app.register_blueprint(MiniAmazonGroup14.auth.bp)
app.register_blueprint(MiniAmazonGroup14.legos.bp)
app.register_blueprint(MiniAmazonGroup14.test.bp)
app.register_blueprint(MiniAmazonGroup14.cart.bp)
app.register_blueprint(MiniAmazonGroup14.orders.bp)
app.register_blueprint(MiniAmazonGroup14.checkout.bp)
#db.createtest()
#db.posttest()
#db.gettest()

#Once we are on a production server we will use something like this
#app.run(host='0.0.0.0')