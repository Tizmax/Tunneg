import random
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

# Global variables to store state
themes_list = ["États des états-unis", "Les fruits", "L'art du spectacle", "Les zones de Jeux-vidéos", "Les youtubers/streamers", "thème mystère", "Les sports d'hiver"]
players = []
current_player_index = 0
tunnels = [{'last_q': 5, 'lock_q': 2, 'completed': False} for _ in range(len(themes_list))]
questions = [['q1','q2','q3','q4','q5','q6','q7','q8','q9','q10'] for _ in range(len(themes_list))]

@app.route('/')
def index():
    return render_template('playerSelection.html', players=players)

@app.route('/themes', methods=['POST'])
def themes():
    return render_template('themeSelection.html', themes=themes_list, players=players, tunnels=tunnels)

@app.route('/tunnel', methods=['POST'])
def tunnel():
    tunnel = themes.query.get(themes)
    return render_template('tunnel.html', themes=themes_list,  players=players)


if __name__ == '__main__':
    app.run(debug=True)