#!flask/bin/python

#all the imports
import pdb
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

#configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECREATE_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


#create out little application :)
app = Flask(__name__)
app.config.from_object(__name__)

def connnect_db():
	return sqlite3.connect(app.config['DATABASE'])


@app.before_request
def before_request():
	g.db = connnect_db() 

@app.teardown_request
def teardown_request(exception):
	db = getattr(g,'db',None)
	if db is not None:
		db.close() 

@app.route('/')
def show_entires():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0],text=row[1]) for row in cur.fetchall()]
    pdb.set_trace()
    rdt = render_template('show_entries.html', entires=entries)
    return rdt 

@app.route('/add',methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	g.db.execute('insert into entries (title,text) values (?,?)', [request.form['title'],request.form['text']])
	g.db.commit()
	flash('New entry was successfuly posted')
	redirect(url_for('show_entries'))

@app.route('/login',methods=['GET','POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('show_entries'))
	return render_template('login.html',error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in',None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))
	

if __name__ == '__main__':
	app.run() 
