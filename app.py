# import flask 
from flask import *
import pymysql
import os

#  initialize the app 
app= Flask(__name__)

app.config["UPLOAD_FOLDER"]= "static/images"

# define  your route /endpoint
@app.route ("/api/signup" , methods = ["POST"])
# defne function to signout
def signup () :
    

     # get user inputs from the data 
     username = request.form ["username"] 
     email = request.form ["email"]
     password= request.form["password"]
     phone= request.form["phone"]

    #  estsblish connectoin to database 
     connection= pymysql.connect(user="root", host="localhost",password="", database="kifarusokogarden")
 
    #  define your cursor
     cursor = connection.cursor() 

    #  define sql to insert 
     sql= "insert into users (username, email, password, phone)  values ( %s, %s, %s ,%s)"


    #  define your data 
     data=(username,email, password, phone)

    #  axecute/run query
     cursor.execute(sql , data)

    #  commit/save changes
     connection.commit()


    #  return response to the user 
     return jsonify ({"message" : "signup successful"})


# signin/login
# define your route/ endpoint
@app.route("/api/signin", methods= ["POST"])

# define your function 
def signin():
     # get user inputs from the form 
     email= request.form["email"]
     password= request.form["password"]

     # connection to database
     connection=pymysql.connect(host="localhost", user="root", password="", database="kifarusokogarden")

     # define your cursor 
     cursor=connection.cursor(pymysql.cursors.DictCursor)
     #  define sql to select
     sql= "select* from users where email=%s and password=%s"
     # define your data 
     data=( email,password)
     # execute /run the query
     cursor.execute(sql,data)
     # check if user exists 
     if cursor.rowcount == 0:
          return jsonify({"message" :"login failed"})
     else:
          # fetch the user 
          user= cursor.fetchone()
          return  jsonify({"message" :"login succsess","user": user })


# add  product
# define you route/endpoint
@app.route("/api/add_product", methods =["POST"])
# define your function 
def add_products():
     # get products input 
     product_name= request.form["product_name"]
     product_description= request.form["product_description"]
     product_cost=request.form["product_cost"]
     product_photo=request.files["product_photo"]
     # get the filename
     filename= product_photo.filename
     # get the photopath
     photopath=os.path.join(app.config["UPLOAD_FOLDER"],filename)
     # save the photo 
     product_photo.save(photopath)
     # save the file to the upload folder
     product_photo.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
     # establish connection
     connection=pymysql.connect(user="root",host="localhost",password="",database="kifarusokogarden")
     # define your cursor 
     cursor= connection.cursor()
     # define sql to insert
     sql= "insert into product_details (product_name, product_description, product_cost, product_photo) values (%s,%s,%s,%s)"

     # define your data 
     data= (product_name, product_description,product_cost,filename)

     # execute your query
     cursor.execute(sql,data)

     # commit/save changes
     connection.commit()

     # return response to user 
     return jsonify ({ "message":"product added successfuly"})



# fetch/get products 
# define your route/endpoins
@app.route("/api/getproducts")
# defune your function 
def getproducts() :
     # connection to database
     connection=pymysql.connect(host="localhost", user="root", password="", database="kifarusokogarden")
     # define your cursor 
     cursor=connection.cursor(pymysql.cursors.DictCursor)
     # define sql to select 
     sql="select* from product_details"
     # execute your query
     cursor.execute(sql)
     # fetch all the products 
     products=cursor.fetchall()
     # return all the products 
     return jsonify(products) 




# Mpesa Payment Route/Endpoint 
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth
 
@app.route('/api/mpesa_payment', methods=['POST'])
def mpesa_payment():
    if request.method == 'POST':
        amount = request.form['amount']
        phone = request.form['phone']
        # GENERATING THE ACCESS TOKEN
        # create an account on safaricom daraja
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"
 
        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
 
        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']
 
        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379"
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')
 
        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://modcom.co.ke/api/confirmation.php",
            "AccountReference": "account",
            "TransactionDesc": "account"
        }
 
        # POPULAING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }
 
        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL
 
        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        return jsonify({"message": "Please Complete Payment in Your Phone and we will deliver in minutes"})








# Run the aplication
app.run(debug= True)