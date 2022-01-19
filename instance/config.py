import os

class AppConfig:
    SECRET_KEY='O7hPqKchcAdlmbo'

class LiveConfig(AppConfig):
    SECRET_KEY='Hz_Vq0XyJUJ6rbo'
 
PASSWORD=os.getenv('MYSQL_PASSWORD', '1236')
SQLALCHEMY_DATABASE_URI=os.getenv('MYSQL_CONSTRING', 'mysql+mysqlconnector://debbie2@127.0.0.1:8889/denty')
#mysql://co082kx8umns1i88:pkr09xi1kjegx4xy@i0rgccmrx3at3wv3.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/sywrz74qh5uxv10i
#mysql+mysqlconnector://co082kx8umns1i88:pkr09xi1kjegx4xy@i0rgccmrx3at3wv3.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/sywrz74qh5uxv10i