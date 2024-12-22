import streamlit as st
import random

# Initialize session state
if 'liste_themes' not in st.session_state:
    st.session_state.liste_themes = ["États des états-unis", "Les fruits", "L'art du spectacle", "Les zones de Jeux-vidéos", "Les youtubers/streamers", "thème mystère", "Les sports d'hiver"]

if 'game_state' not in st.session_state:
    st.session_state.game_state = 'main_menu'  # states: main_menu, box_selection, progress_bar
if 'players' not in st.session_state:
    st.session_state.players = []
if 'current_player_index' not in st.session_state:
    st.session_state.current_player_index = 0
if 'selected_box' not in st.session_state:
    st.session_state.selected_box = None
if 'progress_bars' not in st.session_state:
    st.session_state.progress_bars = [{
        'progress_value': 0,
        'validated_squares': set(),
        'completed': False
    } for _ in range(len(st.session_state.liste_themes))]

def refresh():
    st.session_state.rerun_trigger += 1
    st.rerun()  # Force a rerun of the script to update the UI immediately

def init_game():
    st.session_state.current_player_index = random.randint(0, len(st.session_state.players) - 1)
    st.session_state.game_state = 'box_selection'
    st.rerun()  # Refresh immediately after initializing the game

    
def add_player():
    if st.session_state.new_player and st.session_state.new_player not in [p['name'] for p in st.session_state.players]:
        st.session_state.players.append({
            'name': st.session_state.new_player,
            'points': 0
        })
        st.session_state.new_player = ''
        st.rerun()  # Refresh immediately after adding a player

def next_player():
    st.session_state.current_player_index = (st.session_state.current_player_index + 1) % len(st.session_state.players)
    st.rerun()  # Refresh immediately after switching players

def get_level_points(square_number):
    if square_number <= 3:
        return 1
    elif square_number <= 6:
        return 2
    elif square_number <= 9:
        return 3
    else:
        return 5

def select_box(box_index):
    st.session_state.selected_box = box_index
    st.session_state.game_state = 'progress_bar'
    st.rerun()  # Refresh immediately after selecting a box

def return_to_boxes():
    st.session_state.game_state = 'box_selection'
    st.session_state.selected_box = None
    st.rerun()  # Refresh immediately after returning to the box selection screen

# Main menu
if st.session_state.game_state == 'main_menu':
    st.title('LE GRAND TUNNEG')
    st.subheader('Menu principal')

    # Injection de CSS personnalisé pour centrer verticalement les éléments
    st.markdown(
        """
        <style>
            .stTextInput, .stButton {
                display: flex;
                justify-content: right;
                align-items: right;
            }
        </style>
        """, unsafe_allow_html=True
    )

    
    col1, col2 = st.columns((4, 1))
    with col1:
        st.text_input('', key='new_player')
    with col2:
        st.button('Ajouter Joueur', on_click=add_player, use_container_width=True)
    
    if st.session_state.players:
        st.subheader('Joueurs')
        for player in st.session_state.players:
            st.write(f"{player['name']}")
            
    if len(st.session_state.players) >= 2:
        if st.button('Lancer la partie'):
            init_game()
    else:
        st.warning('Ajoutez au moins 2 joueurs pour lancer la partie')

# Box selection screen
elif st.session_state.game_state == 'box_selection':
    current_player = st.session_state.players[st.session_state.current_player_index]
    st.title(f"C'est le tour de : {current_player['name']}")

    # Display scores
    st.subheader('Points')
    score_cols = st.columns(len(st.session_state.players))
    for idx, player in enumerate(st.session_state.players):
        with score_cols[idx]:
            st.metric(player['name'], player['points'])

    # Display grid of boxes with Streamlit buttons
    st.markdown("""
        <style>
            .box-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 20px;
                padding: 20px;
            }
            .game-box {
                background-color: #F5F5F5;
                border: 3px solid #1E3D59;
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                cursor: pointer;
                transition: all 0.3s ease;
                color: black; /* Texte noir pour les boîtes non complétées */
            }
            .game-box:hover {
                transform: scale(1.02);
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            .completed-box {
                background-color: #4F6D7A;
                color: red; /* Texte rouge pour les boîtes complétées */
            }
        </style>
    """, unsafe_allow_html=True)

    # Display the grid of boxes
    cols = st.columns(3)  # Grid with 3 columns
    for i in range(len(st.session_state.liste_themes)):
        with cols[i % 3]:  # Cycle through columns
            # Define the class based on whether the box is completed
            box_class = 'completed-box' if st.session_state.progress_bars[i]['completed'] else 'game-box'
            # Render each box as a button
            if st.button(f"Thème {st.session_state.liste_themes[i]}", key=f'box_{i}', use_container_width=True, ):
                select_box(i)  # Handle box selection when clicked
            points_a_voler = 0
            for j in range(len(st.session_state.progress_bars[i]["validated_squares"]) + 1, st.session_state.progress_bars[i]["progress_value"] + 1):
                    print(j)
                    points_a_voler += get_level_points(j)
            st.markdown(f'<div class="game-box {box_class}"><p>Progression: {st.session_state.progress_bars[i]["progress_value"]}/10</p><p>Coffrés: {len(st.session_state.progress_bars[i]["validated_squares"])}</p><p>Points à voler: {points_a_voler}</p></div>', unsafe_allow_html=True)

    # Return to main menu button
    if st.button('Retour au menu'):
        st.session_state.game_state = 'main_menu'
        for player in st.session_state.players:
            player['points'] = 0
        st.session_state.progress_bars = [{
            'progress_value': 0,
            'validated_squares': set(),
            'completed': False
        } for _ in range(len(st.session_state.liste_themes))]
        st.rerun()  # Refresh immediately after returning to the main menu


# Progress bar screen
elif st.session_state.game_state == 'progress_bar':
    current_player = st.session_state.players[st.session_state.current_player_index]
    st.title(f"C'est le tour de : {current_player['name']} - Thème {st.session_state.liste_themes[st.session_state.selected_box]}")
    
    # Display scores 
    st.subheader('Points')
    score_cols = st.columns(len(st.session_state.players))
    for idx, player in enumerate(st.session_state.players):
        with score_cols[idx]:
            st.metric(player['name'], player['points'])

    # Progress bar styling
    st.markdown("""
        <style>
            .progress-container {
                padding: 30px;
                background-color: #F5F5F5;
                border-radius: 15px;
                margin: 20px 0;
            }
            .square {
                width: 50px;
                height: 50px;
                border: 2px solid #1E3D59;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                margin: 3px;
                font-weight: bold;
                border-radius: 5px;
                font-size: 20px;
            }
            .separator {
                width: 4px;
                height: 25px;
                background: linear-gradient(to bottom, #1E3D59, #4F6D7A);
                margin: 0 10px;
                display: inline-block;
                border-radius: 2px;
            }
            .red { background-color: #FF6B6B; color: white; }
            .grey { background-color: #4F6D7A; color: white; }
            .empty { background-color: white; color: #1E3D59; }
        </style>
    """, unsafe_allow_html=True)
    
    # Display progress bar
    progress_html = '<div class="progress-container">'
    bar = st.session_state.progress_bars[st.session_state.selected_box]
    
    for i in range(1, 11):
        if i in bar['validated_squares']:
            square_class = "square grey"
        elif i <= bar['progress_value']:
            square_class = "square red"
        else:
            square_class = "square empty"
            
        progress_html += f'<div class="{square_class}">{i}</div>'
        
        if i in [3, 6, 9]:
            progress_html += '<div class="separator"></div>'
            
    progress_html += '</div>'
    st.markdown(progress_html, unsafe_allow_html=True)
    
    # Control buttons
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button('Question suivante', use_container_width=True):
            if bar['progress_value'] < 10:
                bar['progress_value'] += 1
                st.rerun()  # Refresh immediately after incrementing progress
                
    with col2:
        if st.button('Coffrer', use_container_width=True):
            points_gained = 0
            for i in range(1, bar['progress_value'] + 1):
                if i not in bar['validated_squares']:
                    points_gained += get_level_points(i)
                    bar['validated_squares'].add(i)
            current_player['points'] += points_gained
            next_player()
            if len(bar['validated_squares']) == 10:
                bar['completed'] = True
            
                
    with col3:
        if st.button('Passer', use_container_width=True):
            next_player()

            
    with col4:
        if st.button('Retirer', use_container_width=True):
            bar['progress_value'] -= 1
            if bar['progress_value'] + 1 in bar['validated_squares']:
                bar['validated_squares'].remove(bar['progress_value'] + 1)
            st.rerun()

    with col5:
        if st.button('Retour au tèmes', use_container_width=True):
            return_to_boxes()
            