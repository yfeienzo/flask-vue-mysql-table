import json
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/magickid'
db = SQLAlchemy(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    gender = db.Column(db.String(255))
    def __init__(self, id,name,gender):
        self.id = id
        self.name = name
        self.gender = gender
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

with app.app_context():
    db.create_all()

@app.route("/")
@cross_origin()
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/users", methods=['GET'])
@cross_origin()
def get_user_list():
    usersResult = db.session.query(User).all()
    users = []
    for userResult in usersResult:
        users.append(userResult.as_dict())
    return jsonify(users)

@app.route('/users', methods=['POST'])
@cross_origin()
def add_user():
    user = User(
            id=request.form["id"],
            name=request.form["name"],
            gender=request.form["gender"],
        )
    db.session.add(user)
    db.session.commit()
    return user.as_dict(), 201

@app.route('/users/<id>',methods=['PUT'])
@cross_origin()
def edit_user(id):
    user = User.query.filter_by(id=id).first()
    user.name = request.form["name"]
    user.gender = request.form["gender"]
    db.session.commit()
    return user.as_dict()

if __name__ == "__main__":
    app.run(port=8000, debug=True)