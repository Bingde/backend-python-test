from alayatodo import app
from flask import Blueprint

from flask_paginate import Pagination, get_page_parameter, get_page_args
from flask import (
	Flask,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
    session,
    )
from alayatodo import models
from alayatodo.models import Todo
from alayatodo.models import User

@app.route("/auto")
def logincheck():
  		if not session.get('logged_in'):
  			return redirect('/login')

@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l.decode('utf-8') for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')
#     user = session.query(users).filter_by(username == '%s' %username ).filter_by(password == '%s' %password ).one()
#     print(user)
    sql = "SELECT * FROM users WHERE username = '%s' AND password = '%s'";
    cur = g.db.execute(sql % (username, password))
    user = cur.fetchone()
    print(dict(user))
    if user:
        session['user'] = dict(user)
        session['logged_in'] = True
        flash('You were successfully logged in')	
        return redirect('/todo')
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    flash('You were successfully logged out')
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
		todo=Todo.query.filter_by(id='%s' % id)
		return render_template('todo.html', todo=todo)
    
# allow to view in JSON format
@app.route('/todo/<id>/json', methods=['GET'])
def todojson(id):
# 	change to ORM way
		todo=Todo.query.filter_by(id='%s' % id)
		print(id)
		return render_template('json.html',todo=todo)

@app.route('/todo',defaults={'page': 1} ,methods=['GET'])
@app.route('/todo/',defaults={'page': 1},methods=['GET'])
@app.route('/todo/page/<int:page>/',methods=['GET'])
@app.route('/todo/page/<int:page>',methods=['GET'])
def todos(page):
	
	total = Todo.query.count()
	page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
	todos = Todo.query.filter_by(user_id='%s' % session['user']['id']).slice(offset, per_page).limit(per_page)
	pagination = Pagination(page=page,
                                per_page=per_page,
                                total=total,
                                record_name='todos',
                                format_total=True,
                                format_number=True,
                                )
	return render_template('todos.html', todos=todos,
                           page=page,
                           per_page=per_page,
                           pagination=pagination
                           )

@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')
        
#    if form description is empty, then not insert into DB
    elif request.form.get('description') == "":
    	flash('You can not add todo list without description')
    	redirect('/todo')
    else:
    	flash('You were successfully add one todo list')
    	g.db.execute(
        "INSERT INTO todos (user_id, description,completed) VALUES ('%s', '%s','%s')"
        % (session['user']['id'], request.form.get('description'), 0)
    )
#     g.db.commit()
    
    return redirect('/todo')

@app.route('/todo/complete/<id>', methods=['POST'])

def todo_completed(id):
    logincheck()
#     g.db.execute("UPDATE todos SET completed = 1 WHERE id ='%s'" % id)
#     g.db.commit()
    to_complete=Todo.query.filter_by(id='%s' % id).update({Todo.completed:1},synchronize_session=False)
    flash('You were successfully completed one todo list')
    return redirect('/todo')
    
@app.route('/todo/not_complete/<id>', methods=['POST'])
   
def todo_not_completed(id):
    logincheck()
    not_complete=Todo.query.filter_by(id='%s' % id).update({Todo.completed:0},synchronize_session=False)
    flash('You have put one todo list into incomplete')
    return redirect('/todo')


@app.route('/todo/<id>', methods=['POST'])

def todo_delete(id):
    logincheck()
    to_delete=Todo.query.filter_by(id='%s' % id).delete()
    flash('You were successfully delete one todo list')
    return redirect('/todo')

