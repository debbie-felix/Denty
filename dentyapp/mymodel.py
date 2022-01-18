import datetime
from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_user import user_manager
from sqlalchemy.orm import backref
from sqlalchemy.sql.schema import ForeignKey
from dentyapp import db


# denty = db.Table('users',
# db.Column('user_id',db.Integer(),db.ForeignKey('user.id')))
# db.Column('gift_id',db.Integer(),db.ForeignKey('gift.id')),
# db.Column('qty',db.Integer() ))

# recipients = db.Table('recipients',
# db.Column('recipients_id',db.Integer(),db.ForeignKey('recipients_id.id')))

class Users(db.Model):
    user_id=db.Column(db.Integer(),primary_key=True,autoincrement=True)
    fname=db.Column(db.String(100),nullable=False)
    lname=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(50),nullable=False)
    password=db.Column(db.String(255),nullable=False, server_default='')
    reg_date= db.Column(db.DateTime(), default= datetime.datetime.utcnow)




class Recipients(db.Model):
    rec_id=db.Column(db.Integer(),primary_key=True,autoincrement=True)
    fname=db.Column(db.String(100),nullable=False)
    lname=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(50),nullable=False)
    password=db.Column(db.String(255),nullable=False, server_default='')
    phone=db.Column(db.String(20),nullable=False)
    address=db.Column(db.String(100),nullable=False)
    city=db.Column(db.String(100),nullable=False)
    state=db.Column(db.String(100),nullable=False)
    post_title = db.Column(db.String(50), nullable=False)
    post_description = db.Column(db.String(255), nullable=True)
    amount = db.Column(db.String(30), nullable=True)
    post_image=db.Column(db.String(100),nullable=False)
    reg_date= db.Column(db.DateTime(), default= datetime.datetime.utcnow)

    # post=db.relationship("Posts")
    # status=db.relationship("Status")



class Posts(db.Model):
    
    post_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    post_date= db.Column(db.DateTime(), default= datetime.datetime.utcnow)
    post_title = db.Column(db.String(10), nullable=False)
    post_description = db.Column(db.String(1000), nullable=True)
    post_image=db.Column(db.String(100),nullable=False)
    # image2=db.Column(db.String(100),nullable=False)
    # image3=db.Column(db.String(100),nullable=False)
    # recipients=db.relationship("Recipients")
    # recipient_id = db.Column(db.Integer(),db.ForeignKey('recipients.id'))



class Donations(db.Model):
    id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
    amount = db.Column(db.Float(40), nullable=False)
    status = db.Column(db.String(40), nullable=False)
    donation_date= db.Column(db.DateTime(), default= datetime.datetime.utcnow)
    post_id = db.Column(db.Integer(),db.ForeignKey('posts.post_id'))
    recipient_id = db.Column(db.Integer(), db.ForeignKey('recipients.rec_id'))
    donor_id = db.Column(db.Integer(), db.ForeignKey('users.user_id'))


    
class States(db.Model):
    id=db.Column(db.Integer(),primary_key=True,autoincrement=True)
    name=db.Column(db.String(50),nullable=False)  

db.create_all()
db.session.commit()













# class Transactions(db.Model):
#     trans_id=db.Column(db.Integer(), primary_key=True, autoincrement=True)
#     customer_id=db.Column(db.Integer(), db. ForeignKey('customer.id'))
#     product_id = db.Column(db.Integer(), db.ForeignKet('product.id'))
#     qty = db.Column(db.integer())
#     trans_date= db.Column(db.DateTime(), default= datetime.datetime.utcnow)
#     #set up relationships
#     #when i want to see the customer who made the single transaction
#     dcustomer = db.relationship('customer', backref='cust_trans')
#     #when i want to see the product detauls of this single transaction
#     prod_details = db.relationship('Product', backref='prod_trans')














    # reg_date=db.Column(db.DateTime(),default=datetime.datetime.utcnow)
    # age=db.Column(db.String(100),nullable=False)
    # image=db.Column(db.String(100),nullable=False)

# def __init__(fname, lname, email, password, phone):
#         self.fname = fname
#         self.lname = lname
#         self.email = email
#         self.password = password
#         self.phone = phone
#         # self.reg_date = reg_date
#         # self.age = age







