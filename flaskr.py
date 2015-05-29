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



if __name__ == '__main__':
	app.run() 
