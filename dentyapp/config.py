PASSWORD='1236'
SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://debbie2@127.0.0.1:8889/denty' 

MERCHANT_ID='UUFHFIUHF34567'
DEBUG=True
ADMIN_EMAIL='debbiefelix2@gmail.com'
FLASK_RUN_PORT = 8080 
SECRET_KEY = 'admin12345'

class AppConfig:
    SECRET_KEY='O7hPqKchcAdlmbo'

class LiveConfig(AppConfig):
    SECRET_KEY='Hz_Vq0XyJUJ6rbo'
 

