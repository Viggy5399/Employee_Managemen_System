from flask import Flask, render_template, request, redirect,url_for,jsonify,make_response
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/Employee_Management_System"

mongo = PyMongo(app)



db = mongo.db.registered_users

@app.route("/homepage", methods= ["GET"])
def homepage():
    return render_template("homepage.html")
    
    


@app.route("/login", methods =["POST","GET"])
def login():
    if request.method == "POST":
        user = db.registered_users.find_one({"Employee_id":request.form.get("id")})
        if user and (request.form.get("password")==user["Password"]):
            return redirect(url_for('addemployee'))
        else:
            return make_response(jsonify({'error': 'Unauthorized access'}), 403)
        
    return render_template("login.html")

@app.route("/register" , methods =["GET","POST"])
def register():
    if request.method == "POST":
       Employee_name = request.form["name"]
       Employee_id = request.form["id"]
       Password = request.form["password"]
       #Gender = request.form["gender"]
       Email = request.form["email"]
       Contact_Number   = request.form["phonenumber"]
       Postal = request.form["postal"]
       db.registered_users.insert_one({"Employee_name" : Employee_name,"Employee_id":Employee_id,"Password":Password,
       "Email":Email,"Contact_Number":Contact_Number,"Postal":Postal})
       return redirect(url_for('homepage'))
    return render_template("register.html")

#@app.route("/dashboard" , methods=["GET","POST"])

@app.route("/addemployee" , methods=["GET","POST"])
def addemployee():
    return render_template ("add_employee.html")


if __name__ == "__main__":
    app.run(debug=True)

