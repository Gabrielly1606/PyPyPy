import os
import json
from flask import Flask, jsonify, request

app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), "database")

# Define the User class
class User:
    def __init__(self, id, name, exp):
        self.id = id
        self.name = name
        self.exp = exp
        self.level = 1

    def to_dict(self):
        return {"id": self.id, "name": self.name, "exp": self.exp, "level": self.level}

# Define a function to load users from the "database"
def load_users():
    try:
        with open(os.path.join(db_path, "users.json"), "r") as f:
            users = [User(**data) for data in json.load(f)]
    except FileNotFoundError:
        users = []
    return users

# Define a function to save users to the "database"
def save_users(users):
    with open(os.path.join(db_path, "users.json"), "w") as f:
        data = [u.to_dict() for u in users]
        json.dump(data, f)

# Define a route to return all users
@app.route("/api/users", methods=["GET"])
def get_users():
    users = load_users()
    for user in users:
        user.level = user.exp / 100 # simple formula to calculate level
    return jsonify([user.to_dict() for user in users])

# Define a route to create a new user
@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()
    users = load_users()
    user = User(len(users) + 1, data["name"], data["exp"])
    users.append(user)
    save_users(users)
    return jsonify(user.to_dict()), 201

if __name__ == "__main__":
    app.run(debug=True)
