import os,json,random,re
import urllib.request
from flask import render_template,url_for,session,request,redirect,flash,abort,send_from_directory,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask.wrappers import Response
import mysql.connector
from werkzeug.utils import secure_filename
from dentyapp.forms import Signup
from dentyapp import app,db
from dentyapp.mymodel import Recipients, Users, Posts, Donations



@app.errorhandler(404)
def my404(error):
    return render_template('error.html'),404
    
@app.route('/')
def home():
    loggedin_user  = session.get('user')
    y = db.session.query(Recipients).limit(4).all()
    data = db.session.query(Users).get(loggedin_user)
    if loggedin_user:
        #y= db.session.query(Recipients).get(loggedin_user)
        return render_template('index.html',recipients=y,user=data)
    else:
        return render_template('index.html', recipients=y)






@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/blog/')
def blog():
    return render_template('blog.html')

@app.route('/donor_user/giver')
def giver():
    return render_template('/donor_user/giver.html')

    
@app.route('/receive_user/recipient')
def recipient():
    return render_template('/receive_user/recipient.html')




@app.route('/recipient/recipient_account/', methods = ['POST', 'GET'])
def recipient_account():
    loggedin_user  = session.get('user')
    if loggedin_user:
        y= db.session.query(Recipients).get(loggedin_user)

        return render_template('/recipient/recipient_account.html',y=y)
    else:
        # return render_template('/recipient/recipient_account.html',y=y)

        return redirect(url_for('login'))






@app.route('/recipient/recipient_profile/<id>')
def recipient_profile(id):
        rec_id = db.session.query(Recipients).get(id)

        total_donations_amount = func.sum(Donations.amount).label('total_donations')
        total_donations_count = func.count(Donations.id).label('number_of_donations')
        donations_stats = db.session.query(Donations, total_donations_amount, total_donations_count).filter_by(recipient_id=rec_id.rec_id).group_by(Donations.recipient_id).first()

        # set percentage raised value initially to 0
        percentage_raised = 0
        
        if donations_stats:
          percentage_raised = ((donations_stats.total_donations) / float(rec_id.amount) ) * 100
        
        percentage_raised = round(percentage_raised, 2)
        percentage_raised_css = "width:"+str(percentage_raised)+"%;"


        return render_template('recipient/recipient_profile.html',rec_id=rec_id, donations_stats=donations_stats, percentage_raised=percentage_raised, percentage_raised_css=percentage_raised_css)




@app.route('/support/giver_account',methods = ['POST', 'GET'])
def giver_account():
    loggedin_user = session.get('user')
    if loggedin_user:
        user= db.session.query(Users).get(loggedin_user)

        return render_template('/support/giver_account.html',user=user)
    else:
        return redirect(url_for('login'))

    
    
    # if loggedin :
    #     return render_template('/support/giver_account.html')

    # if session.get('user') !=None: 
    #     if request.method=='GET':
    #         return render_template('login.html')
    # #     email = session.get('user')
    # #     password = session.get('password')
    #     else:
    #         return redirect(url_for('giver_account'))

            
    # else:
    #     return redirect(url_for('login'))


    

@app.route('/signup', methods = ['GET','POST'])
def signup():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        password = request.form.get('password')
        # phone = request.form.get('phone')
        # age = request.form['age']
        
        my_data = Users(fname=fname, lname=lname, email=email, password=password)
        db.session.add(my_data)
        db.session.commit()

        flash("Thank you for signing up")
        return render_template('index.html')
    else:
        return render_template('signup.html')



@app.route('/recipient_signup', methods = ['GET','POST'])
def recipient_signup():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        address = request.form.get('address')
        # image = request.form.get('image')  
        post_title = request.form.get('post_title')
        post_description = request.form.get('post_desc')
        amount = request.form.get('amount')
        post_image = request.form.get('post_image')    
        my_data = Recipients(fname=fname, lname=lname, email=email, password=password, phone=phone, address=address,post_title=post_title,post_description=post_description,amount=amount, post_image=post_image)
        db.session.add(my_data)
        db.session.commit()

        flash("Thank you for signing up")
        return render_template('index.html')
    else:  
        return render_template('recipient_signup.html')



@app.route('/signup_successful',methods = ['POST', 'GET'])
def signup_successful():
    if request.method =='GET':
        return render_template('signup.html')
    else:
        return render_template('signup_successful.html')



@app.route('/payment_successful',methods = ['POST', 'GET'])
def payment_successful():
    if request.method =='GET':
        return render_template('index.html')
    else:
        return render_template('payment_successful.html')

       

       
       
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method =='GET':
        return render_template('login.html')
    else:  
        email = request.form.get('email')
        password = request.form.get('password')
        usertype = request.form.get('usertype','') 
        if usertype =='give':
            x = db.session.query(Users).filter(Users.email==email).filter(Users.password==password).first()
            if x:
                # session['user'] = email
                loggedin_user = x.fname
                session['user'] = loggedin_user 
                
            return redirect(url_for('giver_account'))
        elif usertype =='receive':
            x = db.session.query(Recipients).filter(Recipients.email==email).filter(Recipients.password==password).first()       
            if x:
                # session['user'] = email
                loggedin_user = x.fname
                # session['image'] = x.user_id
                session['user'] = loggedin_user
            return redirect(url_for('recipient_account')) 
        else:
            flash('The username/password is incorrect')
            return render_template('login.html')





@app.route('/logout')
def logout():
    session.pop('user',None)
    # flash('You have logged out', 'info')
    return redirect(url_for('home'))



@app.route('/donate/')
def donate():
    loggedin_user  = session.get('user')
    y = db.session.query(Recipients).all()
    if loggedin_user:
        #y= db.session.query(Recipients).get(loggedin_user)
        return render_template('donate.html',recipients=y)
    else:
        return render_template('donate.html', recipients=y)




@app.route('/donations', methods=['POST'])
def donations():
    amount = request.form.get('amount') 
    status = request.form.get('status')
    recipient = request.form.get('recipient')   
    amt = Donations(amount=amount, status=status, recipient_id=recipient)
    db.session.add(amt)
    db.session.commit()
    return jsonify(saved=1,id=amt.id)
    #return render_template('donate.html',amt=amt)







@app.route('/start_campaign/')
def start_campaign():
    return render_template('start_campaign.html')



@app.route('/user/submitajax',methods=['GET','POST'])
def submitajax():
    loggedin=session.get('user')
    if loggedin != None:
        quest=request.form.get('quest')
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
      
        v = Users(user_id=loggedin,quest=quest)
        db.session.add(v)
        db.session.commit()
        return f'Thank you, {fname} {lname}, form submitted'
    else:
        return "You need to login to ask a question"








# @app.route('/recipient/recipient_posts/', methods = ['POST', 'GET'])
# def recipient_posts():
#     loggedin_user  = session.get('user')
#     if loggedin_user:
#         # y = db.session.query(Posts).get(loggedin_user)
#         post_title = request.form.get('post_title')
#         post_description = request.form.get('post_desc')
#         image1 = request.form.get('image1')    
#             # all=db.session.query(Posts).all()
#             # data = db.session.query(Posts,Recipients).join(Recipients).all()
#         x = Posts(post_title=post_title,post_description=post_description,image1=image1,recipient_id=loggedin_user)
#         flash(f'Description added!', category='success')

#         db.session.add(x)
#         db.session.commit()
#         return render_template('/recipient/recipient_account.html')














# @app.route('/recipient/retrieve/')
# def retrieve():
#     loggedin = session.get('user')
#     if loggedin != None:
#         all = db.session.query(Posts,).all()
    
    
    
    
    # data = db.session.query(Recipients,Posts).join(Recipients).all()

    # cur = mysql.connection.cursor()
    # cur.exexcute('SELECT * FROM posts where id =%s""',(id,))
    # data = cur.fetchall()
    # cur.close()
    # return render_template('/recipient/recipient_profile.html',data=data,all=all)
    
    
    
    
    # loggedin_user =session.get('user')
    # if loggedin_user != None:
    #     data =db.session.query(Posts).get(loggedin_user)
    #     return render_template('/recipient/recipient_profile.html',data=data)  
    # else:
    #     return 'Display'  

    
        
        
        
        
        
        
        #  retrieve=x.fetchall()
     
#      x = Posts(post_description=post_description, image1=image1)
# #         if x:
# #             loggedin_user = x
# #             session['user'] = loggedin_user 
# #             session['image1'] = image1       
# #             db.session.add(x)
# #             db.session.commit()
# #             return render_template('/recipient/recipient_account.html')

#     # q = db.session.query(Survey, Person, Question, Answer).filter(Person.survey_id == Survey.survey_id,Question.survey_id == Survey.survey_id,Answer.question_id == Question.question_id).all()
#     print(ans)
#     return 'OK'

    
    
  
   

   
   
   
   
   
   
     



#         # db.session.query(Recipients, Posts, Status).join(Buyer, Buyer.buyer_id == Company.id).all()
#         # db.session.query(Recipients, Posts, Status).join(Recipients, Posts.post_id == Recipients.id).all()

#         x = Posts(post_description=post_description, image1=image1)
#         if x:
#             loggedin_user = x
#             session['user'] = loggedin_user 
#             session['image1'] = image1       
#             db.session.add(x)
#             db.session.commit()
#             return render_template('/recipient/recipient_account.html')

        
#     else:
#         return render_template('signup.html')


    
# @app.route('/available/',methods=['GET','POST'])
# def available():
#     if request.method=='GET':
#         records = db.session.query(Tbl_state).all()
#         return render_template('available.html', records=records)
#     else:
#         user = request.form.get('user')
#         deets = db.session.query(Users).filter(Users.email==user).all()
#         if deets:
#             rsp = {"msg":"you have registered with this email","status":"failed"}
#             return json.dumps(rsp)
#         else:
#             rsp = {"msg":"username available","status":"success"}
#             return json.dumps(rsp)




    
# @app.route('/lga/',methods=['GET','POST'])
# def lga():
#     state = request.args.get('state_id')
#     data = db.session.query(Lga).filter(Lga.state_id==state).all()

#     tosend = "<select class='form-control' name=''>"
#     for t in data:
#         tosend = tosend + f'<option>{t.lga_name}</option>'
#     tosend =tosend+'</select>'

#     return tosend





# @app.route('/login',methods=['GET','POST'])
# def login():
#     if request.method =='GET':
#         return render_template('login.html')
#     else:    
#         email = request.form.get('email')
#         password = request.form.get('password')
#         x = db.session.query(Users).filter(Users.email==email).filter(Users.password==password).first()

#         if x:
#             session['user'] = email
#             loggedin_user = x.fname
#             session['user'] = loggedin_user
#             session['image'] = x.image
#             usertype = request.form.get ('usertype','')
#             if usertype =='give':
#                     return redirect(url_for('giver_account'))
#             elif usertype == 'receive':
#                     return redirect(url_for('recipient_account')) 
#         else:
#             flash('The username/password is incorrect')
#             return render_template('login.html')







            
    
    
    # newfile = Recipients(image=file.filename, data=file.read())
    # db.session.add(newfile)
    # db.session.commit()
    # flash('successful')
 
    # return redirect(url_for('uploads')) 



# @app.route('/<int:id>')
# def get_img():
#     img = image.query.filter_by(id=id).first()
#     if not img:
#         return 'No img with that id'
#     else:
#         return Response(img.img,imgtype=img.imgtype)



# @app.route("/update", methods =['GET', 'POST'])
# def update():
#     msg = ''
#     if 'user' in session:
#         if request.method == 'POST' and 'fname' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form:
#             fname = request.form['username']
#             password = request.form['password']
#             email = request.form['email']
#             address = request.form['address']
#             city = request.form['city']
#             state = request.form['state']
#             country = request.form['country']    
#             postalcode = request.form['postalcode'] 
#             cursor = db.session.query(Recipients).all()
#             cursor.execute('SELECT * FROM recipients WHERE fname = % s', (fname ))
#             account = cursor.fetchone()
#             if account:
#                 msg = 'Account already exists !'
#             elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
#                 msg = 'Invalid email address !'
#             elif not re.match(r'[A-Za-z0-9]+', username):
#                 msg = 'name must contain only characters and numbers !'
#             else:
#                 cursor.execute('UPDATE accounts SET  username =% s, password =% s, email =% s, organisation =% s, address =% s, city =% s, state =% s, country =% s, postalcode =% s WHERE id =% s', (username, password, email, organisation, address, city, state, country, postalcode, (session['id'], ), ))
#                 mysql.connection.commit()
#                 msg = 'You have successfully updated !'
#         elif request.method == 'POST':
#             msg = 'Please fill out the form !'
#         return render_template("update.html", msg = msg)
#     return redirect(url_for('login'))