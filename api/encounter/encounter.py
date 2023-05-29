import random
from flask import Blueprint, request, jsonify

encounter_bp = Blueprint('encounter', __name__)

def read_words(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [word.strip() for word in f]

person_types = read_words('encounter/text/person_types.txt')
weapons = read_words('encounter/text/weapons.txt')
encounters = read_words('encounter/text/encounters.txt')
actions = read_words('encounter/text/actions.txt')

@encounter_bp.route('/api/encounter', methods=['GET', 'POST'])
def generate_encounter():
    random.seed() # initialize the random seed
    amount = random.randint(1, 5) # generate a random number of people
    person_type = random.choice(person_types) # choose a random person type
    encounter = random.choice(encounters) # choose a random encounter
    weapons_list = random.sample(weapons, random.randint(1, 3)) # choose a random number of weapons
    action = random.choice(actions)
    # choose a random action based on the seed

    text = f"Você se depara com {amount} {person_type}, {encounter}. Esses {person_type} estão armados com {', '.join(weapons_list)}, eles não vão o incomodar se você {action}."
    return jsonify({'text': text})
