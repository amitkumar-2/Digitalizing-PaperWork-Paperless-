from flask import Flask
from Database import init_and_conf

# Create a flask Instance
app=Flask(__name__)


#Add database
app.config['SQLALCHEMY_DATABASE_URI']=''
# Secret Key
app.config['SECRET_KEY'] = ''
# Initializing Database
init_and_conf.db.init_app(app)




@app.route("/")
def home():
    return "Hello World!"

if __name__=="__main__":
    app.run(debug=True)