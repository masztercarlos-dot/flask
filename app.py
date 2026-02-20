# import flask 
from flask import *
import pymysql

#  initialize the app 
app= Flask(__name__)

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
     cursor=connection.cursor()
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
@app.route("/api/add_products", methods =["POST"])
# define your function 
def add_products():
     # get products input 
     product_name= request.form["product_name"]
     product_description= request.form["product_description"]
     product_cost=request.form["product_cost"]
     product_image=request.files["product_image"]

     # establish connection
     connection=pymysql.connect(user="root",host="localhost",password="",database="kifarusokogarden")
     # define your cursor
     cursor= connection.cursor()
     # define sql to insert
     sql= "insert into products_details (product_name, product_description, product_cost, product_image) values (%s,%s,%s,%s)"

     # define your data 
     data= (product_name, product_description,product_cost, product_image)

     # execute your query
     cursor.execute(sql,data)

     # commit/save changes
     connection.commit()

     # return response to user 
     return jsonify ({ "message":"product added successfuly"})













# Run the aplication
app.run(debug= True)