from flask import Blueprint, request, jsonify

talya_bp = Blueprint('talya', __name__)

@talya_bp.route('/api/talya', methods=['GET', 'POST'])
def roll_dice():
    hello = request.args.get('text', 'Hello World!') 
    return hello
