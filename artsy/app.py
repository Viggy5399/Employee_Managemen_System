from flask import Flask, render_template, request, jsonify, Response, json
from flask_pymongo import PyMongo, ObjectId

app = Flask(__name__)

app.config['MONGO_URI']="mongodb://localhost/newdatabase"
mongo = PyMongo(app)

db = mongo.db.users


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/users", methods=['GET'])
def getUsers():
    new_user = []
    for i in db.find():
        new_user.append(i)

    return render_template("register.html", newuser=new_user)


@app.route("/registration", methods=["POST"])
def createUsers():
    id = db.insert_one({
        'name': request.json['name'],
        'email': request.json['email']
    })
    print("=======================================")
    print(id.inserted_id)
    print("=======================================")

    #data = jsonify({'id':str(ObjectId(id.inserted_id)), 'msg':"User created successfully"})

    return Response(
        mimetype="application/json",
        status=201,
        response=json.dumps({"message": "User created successfully", "id":str(id.inserted_id)})
    )

if __name__ == "__main__":
    app.run(debug=True, port=2000)


# mongo -->   { 
#                  name: tom
#                  email: tom@gmail.com            
# }
