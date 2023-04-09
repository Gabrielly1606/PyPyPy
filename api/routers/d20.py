from flask import Blueprint, request, jsonify
import d20

d20_bp = Blueprint('d20', __name__)

@d20_bp.route('/api/d20', methods=['GET', 'POST'])
def roll_dice():
    dice = request.args.get('dice', '1d20')  # default to rolling a 6-sided die once
    bonus = int(request.args.get('bonus', 0))  # default to no bonus

    try:
        result = d20.roll(dice)
        return jsonify({
            'result': result.total + bonus,
            'dice': dice,
            'bonus': bonus
        })
    except d20.errors.RollError as e:
        return jsonify({'error': str(e)}), 400
