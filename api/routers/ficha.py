from flask import Blueprint, request, send_file
import os

ficha_bp = Blueprint('ficha', __name__)

@ficha_bp.route('/api/ficha/<int:id>', methods=['GET'])
def get_image(id):
    image_path = os.path.join('fichas', f'{id}.png')

    if os.path.isfile(image_path):
        return send_file(image_path, mimetype='image/png')
    else:
        return ({'error': 'Image not found'}), 404
