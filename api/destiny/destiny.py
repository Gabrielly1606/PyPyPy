import random
from flask import Blueprint, request, jsonify

destiny_bp = Blueprint('template', __name__)

def read_words(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [word.strip() for word in f]
   
names = read_words('destiny/names.txt')
titles = read_words('destiny/titles.txt')
aspects = read_words('destiny/aspect.txt')
Classes = read_words('destiny/class.txt')
destinies = read_words('destiny/destinies.txt')
destinations = read_words('destiny/destinations.txt')

@destiny_bp.route('/api/destiny', methods=['GET', 'POST'])
def generate_text():
    name = random.choice(names)
    title = random.choice(titles)
    aspect = random.choice(aspects)
    Class = random.choice(Classes)
    destiny = random.choice(destinies)
    destination = random.choice(destinations)

    text = f"Você é {title} {name}, O {Class} {aspect}, destinado a {destiny} {destination}!"
    return jsonify({'text': text})
