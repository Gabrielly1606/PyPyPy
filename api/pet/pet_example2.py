import os
import json
import time
from flask import Blueprint, request, jsonify

pet_bp = Blueprint('pet', __name__)
PETS_FILE_PATH = 'pets.json'

def get_current_time():
    return int(time.time())

def get_pets():
    if os.path.exists(PETS_FILE_PATH):
        with open(PETS_FILE_PATH, 'r') as f:
            pets = json.load(f)
    else:
        pets = {}
    return pets

def save_pets(pets):
    with open(PETS_FILE_PATH, 'w') as f:
        json.dump(pets, f, indent=2)

def get_pet(pet_id, owner=1):
    pets = get_pets()
    if (pets[str(pet_id)]):
        pet = pets[str(pet_id)]
        pet = update_pet_stats(pet)
    else:
        pet = None
        #pet = create_pet(owner, pet_id)
    return pet

def create_pet(owner_id, pet_id):
    pet = {
        'name': f'Pet {owner_id}',
        'pet_id': pet_id,
        'owner_id': owner_id,
        'health': 100,
        'hunger': 0,
        'attention': 0,
        'hygiene': 0,
        'last_updated': get_current_time()
    }
    pets = get_pets()
    pets[pet['pet_id']] = pet
    save_pets(pets)
    return pet

def update_pet_stats(pet):
    current_time = get_current_time()
    elapsed_time = current_time - pet['last_updated']
    pet['hunger'] += elapsed_time // 10
    pet['attention'] += elapsed_time // 20
    pet['hygiene'] += elapsed_time // 30
    if pet['hunger'] > 100:
        pet['hunger'] = 100
        pet['health'] -= 10
    if pet['attention'] > 100:
        pet['attention'] = 100
        pet['health'] -= 5
    if pet['hygiene'] > 100:
        pet['hygiene'] = 100
        pet['health'] -= 5
    if pet['health'] < 0:
        pet['health'] = 0
    elif pet['health'] > 100:
        pet['health'] = 100
    pet['last_updated'] = current_time
    return pet

def feed_pet(pet_id):
    pet = get_pet(pet_id)
    if pet is not None:
        pet['hunger'] -= 20
        if pet['hunger'] < 0:
            pet['hunger'] = 0
        pet = update_pet_stats(pet)
        pets = get_pets()
        pets[pet_id] = pet
        save_pets(pets)
        return jsonify(pet)
    else:
        return jsonify({'error': f'Pet with id {pet_id} not found'})

def pet_pet(pet_id):
    pet = get_pet(pet_id)
    if pet is not None:
        pet['attention'] -= 20
        if pet['attention'] < 0:
            pet['attention'] = 0
        pet = update_pet_stats(pet)
        pets = get_pets()
        pets[pet_id] = pet
        save_pets(pets)
        return jsonify(pet)
    else:
        return jsonify({'error': f'Pet with id {pet_id} not found'})

def bath_pet(pet_id):
    pet = get_pet(pet_id)
    if pet is not None:
        pet['hygiene'] -= 20
        if pet['hygiene'] < 0:
            pet['hygiene'] = 0
        pet = update_pet_stats(pet)
        pets = get_pets()
        pets[pet_id] = pet
        save_pets(pets)
        return jsonify(pet)
    else:
        return jsonify({'error': f'Pet with id {pet_id} not found'})
@pet_bp.route('/api/pet/<int:id>', methods=['GET'])
def get_pet_info(id):
    pet_info = get_pet(id)
    return jsonify(pet_info)

# route to give food to pet
@pet_bp.route('/api/pet/<int:id>/food', methods=['GET','POST'])
def give_food(id):
    feed_pet(id)
    return jsonify({"message": "Deu comida para o pet."})

# route to pet the pet
@pet_bp.route('/api/pet/<int:id>/pet', methods=['GET','POST'])
def pet_the_pet(id):
    pet_pet(id)
    return jsonify({"message": "Deu carinho no pet."})

# route to give bath to pet
@pet_bp.route('/api/pet/<int:id>/bath', methods=['GET','POST'])
def give_bath(id):
    bath_pet(id)
    return jsonify({"message": "Deu banho no pet."})