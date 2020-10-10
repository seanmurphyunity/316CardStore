from flask import Flask, render_template, request

import MiniAmazonGroup14.auth

import MiniAmazonGroup14.cards

import MiniAmazonGroup14.test

import MiniAmazonGroup14.db

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/cardlist')
def cardlist():
  return render_template('cardlist.html')

app.register_blueprint(MiniAmazonGroup14.auth.bp)
app.register_blueprint(MiniAmazonGroup14.cards.bp)
app.register_blueprint(MiniAmazonGroup14.test.bp)

#db.createtest()
#db.posttest()
#db.gettest()

#Once we are on a production server we will use something like this
#app.run(host='0.0.0.0', port=8080)