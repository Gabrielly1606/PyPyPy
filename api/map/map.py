from flask import Blueprint, request, send_file, abort
import os
from PIL import Image, ImageDraw

map_bp = Blueprint('map', __name__)
MAP_FOLDER = 'map'
PLAYER_FOLDER = os.path.join(MAP_FOLDER, 'players')
MAP_IMAGE = os.path.join(MAP_FOLDER, 'map.jpg')

# Define the endpoint
@map_bp.route('/api/map', methods=['GET'])
def get_map():
    # Get player token and coordinates
    player_count = 5
    players = []
    for i in range(player_count):
        player_token = request.args.get(f'player{i+1}')
        if player_token is not None:
            x_coord = request.args.get(f'x{i+1}')
            y_coord = request.args.get(f'y{i+1}')
            players.append((player_token, int(x_coord), int(y_coord)))
    print(players)
    # Load the map image
    try:
        map_img = Image.open(MAP_IMAGE).convert('RGBA')
    except FileNotFoundError:
        abort(404)
    
    # Draw player tokens on the map image
    draw = ImageDraw.Draw(map_img)
    for player in players:
        player_img_path = os.path.join(PLAYER_FOLDER, f'{player[0]}.png')
        try:
            player_img = Image.open(player_img_path).convert('RGBA')
            player_img = player_img.resize((50, 50))
            map_img.alpha_composite(player_img, (player[1], player[2]))
        except FileNotFoundError:
            pass

    # Save the resulting image to a temporary file and return it
    temp_file = 'temp.png'
    map_img.save(temp_file, format='PNG')
    return send_file(temp_file, mimetype='image/png')
