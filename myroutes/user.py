from flask import render_template,url_for,session,request,redirect,flash,abort,send_from_directory,jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import true
from sqlalchemy.sql import text
from email_validator import validate_email, EmailNotValidError
from sqlalchemy import func
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
from dentyapp.forms import Signup
from dentyapp import app,db,mail,Message
from dentyapp.mymodel import Recipients, Users, Posts, Donations, States




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

@app.route('/test')
def testmail():

    msg=Message(subject='Testing Mail', sender='debbiefelix2@gmail.com', recipients=['beepearl89@gmail.com'])
    f = open ('requirements.txt')
    msg.html = '<div><h1>Welcome on Board</h1</div>'
    
    msg.attach("requirements.txt", "application/text", f.read())
    mail.send(msg)
    return 'mail sent'

@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/blog/')
def blog():
    return render_template('blog.html')


@app.route('/recipient/recipient_account/', methods = ['POST', 'GET'])
def recipient_account():
    if request.method =='GET' and session.get('user') == None:
        return render_template('start_campaign.html')
    loggedin_user  = session.get('user')
    y = db.session.query(Recipients).get(session.get('userid'))
    total_donations_amount = func.sum(Donations.amount).label('total_donations')
    total_donations_count = func.count(Donations.id).label('number_of_donations')
    donations_stats = db.session.query(Donations, total_donations_amount, total_donations_count).filter_by(recipient_id=session.get('userid')).group_by(Donations.recipient_id).first()
    if loggedin_user:
        return render_template('/recipient/recipient_account.html',y=y,donations=donations_stats)
    else:
        return render_template('login.html')




@app.route('/recipient/recipient_profile/<id>')
def recipient_profile(id):
        
        rec_id = db.session.query(Recipients).get(id)
        total_donations_amount = func.sum(Donations.amount).label('total_donations')
        total_donations_count = func.count(Donations.id).label('number_of_donations')
        donations_stats = db.session.query(Donations, total_donations_amount, total_donations_count).filter_by(recipient_id=rec_id.rec_id).group_by(Donations.recipient_id).first()
        # set percentage raised value initially to 0
        percentage_raised = 0
        loggedin_user_id = session.get('userid')
        if donations_stats:
            percentage_raised = ((donations_stats.total_donations) / float(rec_id.amount) ) * 100
        
        percentage_raised = round(percentage_raised, 2)
        percentage_raised_css = "style=\"width: "+str(percentage_raised)+"%;\""
        return render_template('recipient/recipient_profile.html',loggedin_user_id=loggedin_user_id,rec_id=rec_id, donations_stats=donations_stats, percentage_raised=percentage_raised, percentage_raised_css=percentage_raised_css)



@app.route('/support/giver_account',methods = ['POST', 'GET'])
def giver_account():
    if request.method =='GET' and session.get('user') == None:
        return render_template('login.html')
    loggedin_user  = session.get('user')
    loggedin_user_id = session.get('userid')
    user = db.session.query(Users).get(session.get('userid'))
    rec = db.session.query(Recipients).get(session.get('userid'))
    total_donations_recipients = func.sum(Donations.recipient_id).label('total_donations_recipients')

    total_donations_amount = func.sum(Donations.amount).label('total_donations')
    total_donations_count = func.count(Donations.id).label('number_of_donations')
    donations_stats = db.session.query(Donations,total_donations_recipients, total_donations_amount, total_donations_count).filter_by(donor_id=session.get('userid')).group_by(Donations.donor_id).first()

    sqltext = text('SELECT SUM(amount) as total_donations, COUNT(id) as number_of_donations, recipient_id FROM donations WHERE donor_id=:did GROUP BY donor_id, recipient_id')
    donorstats = db.session.execute(sqltext, {'did':session.get('userid')}).fetchall()
    # for r in donorstats:
    #     print(r['total_donations']) # Access by positional index
    #     print(r['number_of_donations']) # Access by positional index
    #     print(r['recipient_id']) # Access by positional index
    if loggedin_user:
        return render_template('/support/giver_account.html',donorstats=donorstats,loggedin_user_id=loggedin_user_id,user=user,rec=rec,donations=donations_stats)
    else:
        return render_template('login.html')
    

    

@app.route('/signup', methods = ['GET','POST'])
def signup():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        # if email:
        existing_user = Users.query.filter(Users.email == email).first()
        if existing_user:
            flash(f'{email} already exists! Please try again.')    
            return render_template('signup.html')
        try:
            emailIsValid = validate_email(email)
            email = emailIsValid.email
        except EmailNotValidError as e:
            invalidEmail = true
            flash('Invalid Email. Please Try Again')
            return render_template('signup.html', invalidEmail=invalidEmail)

        password = request.form.get('password')
        formated = generate_password_hash(password)
        if not len(password) >= 8 and '[a-z A-Z 0-9 ~`!@#$%^&*()-_+=[]|\;:"<>,./?]' not in password:
            flash('Password must be at least 8 characters long, and must contain at least one uppercase character, one lowercase character, one special character, and one number.')
            return render_template('signup.html')

        my_data = Users(fname=fname, lname=lname, email=email, password=formated)
        db.session.add(my_data)
        db.session.commit()

        return render_template('index.html',signupsuccessful=1)
    else:
        flash('Please Sign Up')
        return render_template('signup.html')



@app.route('/start_campaign/', methods = ['GET','POST'])
def start_campaign():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        existing_user = Recipients.query.filter(Recipients.email == email).first()
        if existing_user:
            flash(f'{email} already exists! Please try again.')   
            return render_template ('start_campaign.html')
        try:
            emailIsValid = validate_email(email)
            email = emailIsValid.email
        except EmailNotValidError as e:
            invalidEmail = true
            flash(f'Invalid {email}! Please try again.')   
            return render_template('start_campaign.html', invalidEmail=invalidEmail)

        password = request.form.get('password')
        
        if (len(password)<8) and '[a-z A-Z 0-9 ~`!@#$%^&*()-_+=[]|\;:"<>,./?]' not in password:
            flash('Password must be at least 8 characters long, and must contain at least one uppercase character, one lowercase character, one special character, and one number.')
            return redirect (url_for('start_campaign'))

        formated = generate_password_hash(password)
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        phone = request.form.get('phone')
        post_title = request.form.get('post_title')
        post_description = request.form.get('post_desc')
        amount = request.form.get('amount')
        post_image = request.form.get('post_image')    
        my_data = Recipients(fname=fname, lname=lname, email=email, password=formated, phone=phone, address=address,city=city,state=state,post_title=post_title,post_description=post_description,amount=amount, post_image=post_image)
        db.session.add(my_data)
        db.session.commit()

        return render_template('index.html', signupsuccessful=1)
    else:  
        return render_template('start_campaign.html')



@app.route('/signup_successful',methods = ['POST', 'GET'])
def signup_successful():
    if request.method =='GET':
        return render_template('signup.html')
    else:
        return render_template('signup_successful.html')



@app.route('/payment_successful/',methods = ['POST', 'GET'])
def payment_successful():
    if request.method =='GET':
        return render_template('index.html')
    loggedin_user  = session.get('user')
    if loggedin_user:
        return render_template('payment_successful.html')
    else:
        return render_template('index.html')

       

       
       
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method =='GET':
        flash('login')
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
                session['userid'] = x.user_id
                session['usertype'] = usertype
                
            return redirect(url_for('giver_account'))
        elif usertype =='receive':
            x = db.session.query(Recipients).filter(Recipients.email==email).filter(Recipients.password==password).first()       
            if x:
                # session['user'] = email
                loggedin_user = x.fname
                # session['image'] = x.user_id
                session['userid'] = x.rec_id
                session['user'] = loggedin_user
            return redirect(url_for('recipient_account'))
        else:
            flash('Email/password is incorrect. Please try again.')
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
    user = request.form.get('user') 
    amt = Donations(amount=amount, status=status, recipient_id=recipient,donor_id=user)
    
    db.session.add(amt)
    db.session.commit()
    return jsonify(saved=1,id=amt.id)
    #return render_template('donate.html',amt=amt)





@app.route('/start_campaign/',methods=['GET','POST'])
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




