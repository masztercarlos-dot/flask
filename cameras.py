# add products 
# define your route/endpoint
from flask import jsonify, request

import app


@app.route("api/cameras",methods=["POST"]) 
# define your function 
def add_camera():
    # get products input
    camera_name=request.form["camera_name"]
    camera_brand=request.form["camera_brand"]   
    camera_resolution=request.form["camera_resolution"]
    lens_type=request.form["lens_type"]
    camera_connectivity=request.form["camera_connectivity"]
    camera_price=request.form["camera_price"] 
    stock=request.form["stock"]
    camera_photo=request.files["camera_photo"]
    # get  the file name 
    filename=camera_photo.filename
    # get the photopath
    photopath=os.path.join(app.config["UPLOAD_FOLDER"])
    # save the photo 
    camera_photo.save(photopath)
    # save the file to upload the folder 
    camera_photo.save(os.path.join(app.config["UPLOAD_FOLDER"],filename))
    # establish connection 
    connection=pymysql.connect(user="root",host="localhost", password="",database="kifarusokogarden")
    # define your cursor 
    cursor=connection.cursor()
    # define sql to insert
    sql="insert into camera details (camera_name,camera_brand,camera_resolution,lens_type,camera_connectivity,camera_price,stock,camera_photo) values (%s,%s,%s,%s,%s,%s,%s,%s)"
    # define your data 
    data=(camera_name, camera_brand, camera_resolution, lens_type, camera_connectivity, camera_price, stock, filename)
    # execute your query 
    cursor.execute(sql,data)
    # commit/save changes
    connection.commit()
    # return response to user
    return jsonify({"message":"camera added successfully"})


# run the application
app.run(debug=True)