from argparse import Action
from flask import Flask, render_template, request, redirect,url_for,jsonify,make_response,flash,session
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_session import Session
import random

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/Employee_Management_System"
app.config['SECRET_KEY'] = '@#$%^&*('
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
app.config["SESSION_PERMANENT"] = False

app.config["SESSION_TYPE"] = "filesystem"
sessionv = Session(app)
app.secret_key = "ems"


db = mongo.db.registered_users
db1 = mongo.db.addemployee

@app.route("/homepage", methods= ["GET"])
def homepage():
    return render_template("homepage.html")
    
    


@app.route("/login", methods =["POST","GET"])
def login():
    if request.method == "POST":
        # user = db.registered_users.find_one({"Employee_id":request.form.get("id")})
        # Name = request.form.get("name")
        password = request.form.get("password")
        id = request.form.get("id")
        res = db.registered_users.find({"Employee_id":request.form.get("id")},{"Password":1})
        l = list(res)



        if len(l) != 0 and bcrypt.check_password_hash(l[0]["Password"],password):
            session["id"] = id
            return redirect(url_for('employeelistuser', id=id))
        else:
            return make_response(jsonify({'error': 'Unauthorized access'}), 403)
        
    return render_template("login.html")

@app.route('/employeelistuser/<id>', methods =["POST","GET"] )
def employeelistuser(id):
    headings =("NAME","ID","Phone_number","Job_designation","Date_of_joining","Address","Job_Location")
    allusers=[]
    for i in db1.addemployee.find({},{'_id':0}):
        allusers.append(list(i.values()))
    print(allusers)
    return render_template ("employeelistuser.html",id=id,headings=headings,data=allusers)


@app.route("/adminlogin", methods =["GET","POST"])
def adminlogin():
    if request.method == "POST":
        ID = request.form.get("id")
        if ID == "Admin":
            return redirect(url_for('employeelist'))
        else:
            return make_response(jsonify({'error': 'Unauthorized access'}), 403)



    return render_template("login.html")

@app.route("/register" , methods =["GET","POST"])
def register():
    if request.method == "POST":
       Employee_name = request.form["name"]
       Employee_id = request.form["id"]
       Password = request.form["password"]
       haspassword=bcrypt.generate_password_hash(Password)
       
       db.registered_users.insert_one({"Employee_name" : Employee_name,"Employee_id":Employee_id,"Password":haspassword})
       flash(f'User is succesfully created','success')


       return redirect(url_for('homepage'))
    return render_template("register1.html")

@app.route("/addemployee" , methods=["GET","POST"])
def addemployee():
    if request.method =="POST":
        Name = request.form["name"]
        ID = request.form["employee_id"]
        Phone_number = request.form["phone"]
        Job_designation = request.form["job"]
        Date =request.form["dateemployed"]
        Address = request.form["resaddress"]
        Location = request.form["reslocation"]
        db1.addemployee.insert_one({"Employee_name" : Name,"Employee_id":ID,"Phone_Number":Phone_number,
        "Designation":Job_designation,"Date_of_Joining":Date,"Address":Address,"Location":Location})
    return render_template ("add_employee.html")


@app.route("/employeelist", methods=["GET","POST"])
def employeelist():
    headings =("NAME","ID","Phone_number","Job_designation","Date_of_joining","Address","Job_Location")
    allusers=[]
    for i in db1.addemployee.find({},{'_id':0}):
        allusers.append(list(i.values()))
    print(allusers)
    

    return render_template("employee_list.html",headings= headings, data=allusers)

@app.route("/update/<id>", methods=["GET","POST"])
def update(id):
    if request.method=='GET':
        emp=[]
        empdata=db1.addemployee.find({'Employee_id':id},{'_id':0})
        for i in empdata:
            emp.append(i)
            print(emp)
    
    if request.method=="POST":
        N = request.form.get("name")
        i = request.form.get("employee_id")
        p = request.form.get("phone")
        jd = request.form.get("job")
        d = request.form.get("dateemployed")
        ad = request.form.get("resaddress")
        jl = request.form.get("reslocation")
        db1.addemployee.update_one({"Employee_id": i},{"$set":{'Employee_name':N,'Employee_id':i,'Phone_Number':p,'Designation':jd,'Date_of_Joining':d,'Address':ad,'Location':jl}})
        return redirect(url_for('employeelist'))

    return render_template ("Update.html",emps=emp)

@app.route("/update_id", methods=["GET","POST"])
def update_id():
    if request.method == "POST":
        ID = request.form.get("ID")
        return redirect(url_for('update',id=ID))
    return render_template("Update_id.html")

@app.route("/delete/<id>", methods=["GET"])
def delete(id):
    db1.addemployee.delete_one({"Employee_id":id})
    db.registered_users.delete_one({"Employee_id":id})
    return redirect(url_for("homepage"))

@app.route("/forgotpassword",methods=["GET","POST"])
def forgotpassword():
    if request.method == "POST":
        Phone = request.form.get("phone")
        ID = request.form.get("id")
        idcheck =db.registered_users.find_one({"Employee_id":ID})
        print (idcheck)
        phonecheck =db1.addemployee.find({'Phone_number':Phone})
        print(phonecheck)
        if idcheck and phonecheck :
            return redirect(url_for("showpassword",id=ID))  

    return render_template("forgotpassword.html") 

@app.route("/showpassword/<id>",methods=["GET","POST"]) 
def showpassword(id):
    if request.method=="POST":
        password = request.form.get("newpassword")
        print(password)
        repassword = request.form.get("confirmpassword")
        if (password==repassword):
            haspassword=bcrypt.generate_password_hash(password)
            db.registered_users.update_one({"Employee_id": id},{"$set":{'Password':haspassword}})
            return redirect(url_for("homepage"))

    return render_template("showpassword.html")

@app.route("/tasks", methods=["GET","POST"])
def tasks():
    Heading = ["Completed tasks","Tasks Yet to complete","Timeline"]
    task1=["Python Flask","Java", "DBMS","Operating System"]
    task2=["Mongo DB","SQL","Angular","Networking"]
    timeline=["Monday","Tuesday","Wednesday","Thursday"]
    return render_template("Tasks.html",headings=Heading,task1=task1,task2=task2,timeline=timeline)

@app.route("/signout", methods=["GET","POST"])
def signout():
    if request.method=="POST":
        session[id]=None
        
    return render_template("homepage.html")


    

if __name__ == "__main__":
    app.run(debug=True)

