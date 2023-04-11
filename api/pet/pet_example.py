from flask import Blueprint, request, jsonify
import random
import time

pet_bp = Blueprint('pet', __name__)

# dictionary to store pet data
pet = {
    "name": "Fluffy",
    "pet_id": 1,
    "owner_id": 1,
    "health": 100,
    "hunger": 100,
    "attention": 100,
    "hygiene": 100,
    "last_updated": time.time()
}

# calculate the updated value for each pet stat based on elapsed time
def update_stats():
    global pet
    elapsed_time = time.time() - pet['last_updated']
    pet['hunger'] -= int(elapsed_time / 10)
    pet['attention'] -= int(elapsed_time / 20)
    pet['hygiene'] -= int(elapsed_time / 30)
    if pet['hunger'] < 0:
        pet['hunger'] = 0
    if pet['attention'] < 0:
        pet['attention'] = 0
    if pet['hygiene'] < 0:
        pet['hygiene'] = 0
    pet['last_updated'] = time.time()

# route to get pet info
@pet_bp.route('/api/pet', methods=['GET'])
def get_pet_info():
    update_stats()
    pet_info = {
        "name": pet['name'],
        "pet_id": pet['pet_id'],
        "owner_id": pet['owner_id'],
        "health": pet['health'],
        "hunger": pet['hunger'],
        "attention": pet['attention'],
        "hygiene": pet['hygiene']
    }
    return jsonify(pet_info)

# route to give food to pet
@pet_bp.route('/api/pet/food', methods=['POST'])
def give_food():
    update_stats()
    pet['hunger'] += int(request.json['amount'])
    if pet['hunger'] > 100:
        pet['hunger'] = 100
    pet['health'] += int(request.json['amount'] / 2)
    if pet['health'] > 100:
        pet['health'] = 100
    return jsonify({"message": "Food given to pet."})

# route to pet the pet
@pet_bp.route('/api/pet/pet', methods=['POST'])
def pet_pet():
    update_stats()
    pet['attention'] += int(request.json['amount'])
    if pet['attention'] > 100:
        pet['attention'] = 100
    pet['health'] += int(request.json['amount'] / 2)
    if pet['health'] > 100:
        pet['health'] = 100
    return jsonify({"message": "Petted the pet."})

# route to give bath to pet
@pet_bp.route('/api/pet/bath', methods=['POST'])
def give_bath():
    update_stats()
    pet['hygiene'] += int(request.json['amount'])
    if pet['hygiene'] > 100:
        pet['hygiene'] = 100
    pet['health'] += int(request.json['amount'] / 2)
    if pet['health'] > 100:
        pet['health'] = 100
    return jsonify({"message": "Bathed the pet."})
