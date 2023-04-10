import random
import string
import time
import os
import json
from flask import Blueprint, render_template, request, redirect, url_for

vip_bp = Blueprint('vip', __name__)


DATABASE_DIR = "database"
DATABASE_FILENAME = "vip_codes.json"
DATABASE_PATH = os.path.join(os.getcwd(), DATABASE_DIR, DATABASE_FILENAME)


class VipCode:
    def __init__(self, serial_code=None, user_id=None, used_at=None, duration=2592000, reusable=False):
        self.serial_code = serial_code or self.generate_serial_code()
        self.user_id = user_id
        self.used_at = used_at
        self.duration = duration
        self.reusable = reusable
    
    @staticmethod
    def generate_serial_code(size=8, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
    
    def to_dict(self):
        return {
            "serial_code": self.serial_code,
            "user_id": self.user_id,
            "used_at": self.used_at,
            "duration": self.duration,
            "reusable": self.reusable
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            serial_code=data.get("serial_code"),
            user_id=data.get("user_id"),
            used_at=data.get("used_at"),
            duration=data.get("duration", 2592000),
            reusable=data.get("reusable", False)
        )
    
    def authenticate(user_id, serial_code):
        database_path = os.path.join(os.getcwd(), DATABASE_DIR, DATABASE_FILENAME)
        with open(database_path, "r") as f:
            data = json.load(f)
        
        code_data = next((code for code in data if code["serial_code"] == serial_code), None)
        if code_data is None:
            return  "Codigo VIP invalido"
        
        if code_data["used_at"] is not None:
            return  "Esse código VIP já foi usado"
        
        if not code_data["reusable"] and code_data["user_id"] is not None and code_data["user_id"] != user_id:
            return  "Esse codigo VIP já foi usado por outro usuário"
        
        #if time.time() > code_data["duration"] + code_data["created_at"]:
        #    return  "This VIP code has expired"
        
        code_data["user_id"] = user_id
        code_data["used_at"] = time.time()
        
        with open(database_path, "w") as f:
            json.dump(data, f, indent=4)
        
        return "Authentication successful"
    
    @staticmethod
    def read_codes():
        codes = []
        database_path = os.path.join(os.getcwd(), DATABASE_DIR, DATABASE_FILENAME)
        if os.path.isfile(database_path):
            with open(database_path, "r") as f:
                data = json.load(f)
                for code_data in data:
                    code = VipCode.from_dict(code_data)
                    codes.append(code)
        return codes
    
    @staticmethod
    def write_codes(codes):
        database_path = os.path.join(os.getcwd(), DATABASE_DIR, DATABASE_FILENAME)
        if os.path.isfile(database_path):
            with open(database_path, "r") as f:
                data = json.load(f)
        else:
            data = []
        data.extend(code.to_dict() for code in codes)
        with open(database_path, "w") as f:
            json.dump(data, f, indent=4)

    
    def update_serial_file(self):
        with open(self.serial_file_path, 'r') as f:
            serials_data = json.load(f)
        
        for serial_data in serials_data:
            if serial_data["serial_code"] == self.serial_code:
                serial_data.update(self.to_dict())
                break
        
        with open(self.serial_file_path, 'w') as f:
            json.dump(serials_data, f, indent=4)
            
    @staticmethod
    def generate_code(serial_code=None, user_id=None, duration=2592000, reusable=False):
        code = VipCode(serial_code=serial_code, user_id=user_id, duration=duration, reusable=reusable)
        codes = VipCode.read_codes()
        codes.append(code)
        VipCode.write_codes(codes)
        return code.serial_code
    
    def read_vip_codes():
        with open(DATABASE_PATH, "r") as f:
            return json.load(f)

    # Define a helper function to write the VIP codes to the JSON file
    def write_vip_codes(vip_codes):
        with open(DATABASE_PATH, "w") as f:
            json.dump(vip_codes, f, indent=4)

    
@vip_bp.route("/api/vip_code", methods=["GET"])
def generate_vip_code():
    serial_code = request.args.get("serial_code")
    user_id = request.args.get("user_id")
    reusable = request.args.get("reusable")
    duration = request.args.get("duration", type=int, default=2592000)
    
    if not serial_code:
        serial_code = VipCode.generate_serial_code()
    
    vip_code = VipCode(serial_code=serial_code, user_id=user_id, duration=duration, reusable=reusable)
    VipCode.write_codes([vip_code])  # Pass the VipCode object in a list
    return vip_code.to_dict()

@vip_bp.route("/api/vip", methods=["GET"])
def authenticate_vip_code():
    serial_code = request.args.get("serial_code")
    user_id = request.args.get("user_id")
    reusable = request.args.get("reusable")
    duration = request.args.get("duration", type=int, default=2592000)
    response = VipCode.authenticate(user_id=user_id, serial_code=serial_code)
    return response


# Define a route to list all the VIP codes
@vip_bp.route("/vip_codes", methods=["GET"])
def vip_list():
    vip_codes = VipCode.read_vip_codes()
    return render_template("vip_list.html", vip_codes=vip_codes)

# Define a route to create a new VIP code
@vip_bp.route("/vip_codes/new", methods=["GET", "POST"])
def vip_create():
    if request.method == "POST":
        vip_code = {
            "code": request.form["code"],
            "duration": int(request.form["duration"]),
            "reusable": request.form.get("reusable") is not None,
            "created_at": int(time.time()),
            "used_at": None,
            "user_id": None
        }
        vip_codes = VipCode.read_vip_codes()
        vip_codes.append(vip_code)
        VipCode.write_vip_codes(vip_codes)
        return redirect(url_for("vip_list"))
    else:
        return render_template("vip_create.html")

    
# Define a route to edit a VIP code
@vip_bp.route("/vip_codes/<string:serial_code>/edit", methods=["GET", "POST"])
def vip_edit(serial_code):
    vip_codes = VipCode.read_vip_codes()
    vip_code = None
    for code in vip_codes:
        if code["serial_code"] == serial_code:
            vip_code = code
            break
    if vip_code is None:
        return "404"

    if request.method == "POST":
        vip_code["code"] = request.form["code"]
        vip_code["duration"] = int(request.form["duration"])
        vip_code["reusable"] = request.form.get("reusable") is not None
        VipCode.write_vip_codes(vip_codes)
        return redirect(url_for("vip_list"))
    else:
        return render_template("vip_edit.html", code=vip_code)

# Define a route to delete a VIP code
@vip_bp.route("/vip_codes/<int:index>/delete")
def vip_delete(index):
    vip_codes = VipCode.read_vip_codes()
    vip_codes.pop(index)
    VipCode.write_vip_codes(vip_codes)
    return redirect(url_for("vip_list"))