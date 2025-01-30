from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import random
from datetime import timedelta
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
app.permanent_session_lifetime = timedelta(days=1)

def init_session():
    if 'game_state' not in session:
        session['game_state'] = 'main_menu'
    if 'players' not in session:
        session['players'] = []
    if 'current_player_index' not in session:
        session['current_player_index'] = 0
    if 'selected_box' not in session:
        session['selected_box'] = None
    if 'themes' not in session:
        session['themes'] = []
    if 'progress_bars' not in session:
        session['progress_bars'] = [{
            'progress_value': 0,
            'validated_squares': [],
            'completed': False
        } for _ in range(len(session['themes']))]

@app.route('/api/add_theme', methods=['POST'])
def add_theme():
    data = request.get_json()
    theme = data.get('theme')
    if theme and theme not in session['themes']:
        themes = session['themes']
        themes.append(theme)
        session['themes'] = themes
        
        return jsonify({
            'success': True, 
            'themes': session['themes']
        })
    return jsonify({'success': False, 'message': 'Invalid theme'})

@app.route('/api/remove_theme', methods=['POST'])
def remove_theme():
    data = request.get_json()
    theme = data.get('theme')
    if theme in session['themes']:
        themes = session['themes']
        themes.remove(theme)
        session['themes'] = themes

        return jsonify({
            'success': True, 
            'themes': session['themes']
        })
    return jsonify({'success': False, 'message': 'Theme not found'})

@app.route('/api/start_theme_input', methods=['POST'])
def start_theme_input():
    session['game_state'] = 'theme_input'
    return jsonify({'success': True, 'game_state': 'theme_input'})

def get_level_points(square_number):
    if square_number <= 3:
        return 1
    elif square_number <= 6:
        return 2
    elif square_number <= 9:
        return 3
    else:
        return 5

@app.route('/')
def index():
    init_session()
    return render_template('index.html', 
                         game_state=session['game_state'],
                         players=session['players'],
                         themes=session['themes'])

@app.route('/api/game_state')
def get_game_state():
    return jsonify({
        'game_state': session['game_state'],
        'players': session['players'],
        'current_player_index': session['current_player_index'],
        'selected_box': session['selected_box'],
        'progress_bars': session['progress_bars'],
        'themes': session['themes']
    })

@app.route('/api/add_player', methods=['POST'])
def add_player():
    data = request.get_json()
    player_name = data.get('player_name')
    if player_name and player_name not in [p['name'] for p in session['players']]:
        players = session['players']
        players.append({
            'name': player_name,
            'points': 0
        })
        session['players'] = players
    return jsonify({'success': True, 'players': session['players']})

@app.route('/api/remove_player', methods=['POST'])
def remove_player():
    data = request.get_json()
    player_name = data.get('player_name')
    players = session['players']
    new_players = []
    for player in players:
        if player['name'] != player_name:
            print(player['name'])
            print(player_name)
            new_players.append(player)
    session['players'] = new_players
    return jsonify({'success': True, 'players': session['players']})

@app.route('/api/init_game', methods=['POST'])
def init_game():
    if not session or session['progress_bars'] == []:
        session['progress_bars'] = [{
        'progress_value': 0,
        'validated_squares': [],
        'completed': False
        } for _ in range(len(session['themes']))]
    session['current_player_index'] = random.randint(0, len(session['players']) - 1)
    session['game_state'] = 'box_selection'
    return jsonify({'success': True, 'game_state': session['game_state']})

@app.route('/api/select_box', methods=['POST'])
def select_box():
    data = request.get_json()
    box_index = data.get('box_index')
    session['selected_box'] = box_index
    session['game_state'] = 'progress_bar'
    return jsonify({'success': True, 'game_state': session['game_state']})

@app.route('/api/update_progress', methods=['POST'])
def update_progress():
    data = request.get_json()
    action = data.get('action')
    progress_bars = session['progress_bars']
    selected_box = session['selected_box']
    current_bar = progress_bars[selected_box]
    
    if action == 'next':
        if current_bar['progress_value'] < 10:
            current_bar['progress_value'] += 1
    elif action == 'lock':
        points_gained = 0
        for i in range(1, current_bar['progress_value'] + 1):
            if i not in current_bar['validated_squares']:
                points_gained += get_level_points(i)
                current_bar['validated_squares'].append(i)
        players = session['players']
        players[session['current_player_index']]['points'] += points_gained
        session['players'] = players
        if len(current_bar['validated_squares']) == 10:
            current_bar['completed'] = True
        session['current_player_index'] = (session['current_player_index'] + 1) % len(session['players'])
        session['game_state'] = 'box_selection'
    elif action == 'pass':
        session['current_player_index'] = (session['current_player_index'] + 1) % len(session['players'])
    elif action == 'remove':
        if current_bar['progress_value'] > 0:
            if current_bar['progress_value'] in current_bar['validated_squares']:
                current_bar['validated_squares'].remove(current_bar['progress_value'])
            current_bar['progress_value'] -= 1
    elif action == 'back':
        session['current_player_index'] = (session['current_player_index'] + 1) % len(session['players'])
        session['game_state'] = 'box_selection'
    
    session['progress_bars'] = progress_bars
    return jsonify({
        'success': True,
        'progress_bars': session['progress_bars'],
        'players': session['players'],
        'current_player_index': session['current_player_index']
    })

@app.route('/api/reset_game', methods=['POST'])
def reset_game():
    session['players'] = [{
        'name': player['name'],
        'points': 0
    } for player in session['players']]
    session['progress_bars'] = [{
        'progress_value': 0,
        'validated_squares': [],
        'completed': False
    } for _ in range(len(session['themes']))]
    return jsonify({'success': True})

@app.route('/api/go_main_menu', methods=['POST'])
def go_main_menu():
    session['game_state'] = 'main_menu'
    return jsonify({'success': True, 'game_state': session['game_state']})

if __name__ == '__main__':
    app.run(debug=True)