''' This file will start the server, for the server to start, we need to instnatiate an object of Flask'''
from dentyapp import app


if __name__=='__main__': 
    app.run(debug=True)   
    # app.run(debug=True,port=8082)   

