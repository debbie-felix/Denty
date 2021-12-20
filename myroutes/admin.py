from flask import render_template,url_for,session,redirect,flash

from dentyapp import app,db
from dentyapp.mymodel import Users


@app.route('/admin/delete/<int:guestid>')
def delete(user_id):
    x = db.session.query(Users).get(user_id)
    db.session.delete(x)
    db.commit()
    flash ('user deleted')
    return redirect(url_for('allguests'))

 
@app.route('/admin/dashboard/')
def dashboard():
    users = db.session.query(Users).count()
    return render_template('admin/dashboard.html', users=users)


@app.route('/admin')
def adminhome(): 
    return "Welcome to Admin Home Page"


