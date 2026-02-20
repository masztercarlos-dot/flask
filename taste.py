# import flask
from flask import *

# initialize the app
app= Flask(__name__)

# define your rout/endpoint
@app.route ("/api/home")
# define your function
def home():
    return "welcome home"




















# run the app
app.run(debug=True)