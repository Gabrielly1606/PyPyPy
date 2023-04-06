import os
import json
from flask import Flask, jsonify, request

app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), "database")

# Define the User class
class User:
    def __init__(self, id, name, exp, level = 1):
        self.id = id
        self.name = name
        self.exp = exp
        self.level = level

    def to_dict(self):
        level = self.exp // 100
        return {"id": self.id, "name": self.name, "exp": self.exp, "level": level}

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
        json.dump(data, f, indent=2)

# Define a route to return all users
@app.route("/api/users", methods=["GET"])
def get_users():
    name = request.args.get("name")
    user_id = request.args.get("id")
    exp = request.args.get("exp")

    # Load all users from the database
    users = load_users()

    # Filter users based on the parameters
    if name:
        users = [user for user in users if user.name.lower() == name.lower()]
    if user_id:
        users = [user for user in users if user.id == int(user_id)]
    if exp:
        users = [user for user in users if user.exp == int(exp)]

    # Calculate the level for each user
    for user in users:
        user.level = user.exp // 100  # simple formula to calculate level

    # Return the filtered users as JSON
    return jsonify([user.to_dict() for user in users])
@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    # Load the user from the database
    user = load_user_by_id(user_id)

    if user:
        # Calculate the level for the user
        user.level = user.exp // 100  # simple formula to calculate level

        # Return the user details as JSON
        return jsonify(user.to_dict())
    else:
        # Return a 404 error if the user does not exist
        return jsonify({"error": "User not found"}), 404

def load_user_by_id(user_id):
    with open("database/users.json", "r") as f:
        users = json.load(f)
    
    for user in users:
        if user["id"] == user_id:
            return User(user["id"], user["name"], user["exp"])

    # Return None if the user with the specified ID does not exist
    return None

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
