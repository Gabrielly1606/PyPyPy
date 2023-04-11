from flask import Blueprint, request, jsonify

template_bp = Blueprint('template', __name__)

@template_bp.route('/api/template', methods=['GET', 'POST'])
def roll_dice():
    hello = request.args.get('text', 'Hello World!') 
    return hello
