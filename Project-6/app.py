from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app)

pile1 = 0
pile2 = 0
pile3 = 0
player1_name = ""
player2_name = ""
current_player = ""
player1_score = 0
player2_score = 0
min_pickup = 1
max_pickup = 1
judge_name = ""
game_ended = False
winner = ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    global pile1, pile2, pile3, player1_name, player2_name, current_player, player1_score, player2_score, min_pickup, max_pickup, judge_name, game_ended, winner

    pile1 = int(request.form['pile1'])
    pile2 = int(request.form['pile2'])
    pile3 = int(request.form['pile3'])
    player1_name = request.form['player1_name']
    player2_name = request.form['player2_name']
    current_player = player1_name
    player1_score = 0
    player2_score = 0
    min_pickup = int(request.form['min_pickup'])
    max_pickup = int(request.form['max_pickup'])
    judge_name = request.form['judge_name']
    game_ended = False
    winner = ""

    socketio.emit('start_game', {
        'pile1': pile1,
        'pile2': pile2,
        'pile3': pile3,
        'player1_name': player1_name,
        'player2_name': player2_name,
        'current_player': current_player,
        'min_pickup': min_pickup,
        'player1_score'  : 0,
        'player2_score' : 0,
        'max_pickup': max_pickup,
        'judge_name': judge_name,
        'game_ended': game_ended,
        'winner': winner
    })
    return redirect(url_for('play_game'))

@app.route('/play_game')
def play_game():
    return render_template('game.html', pile1=pile1, pile2=pile2, pile3=pile3,player1_name=player1_name, player2_name=player2_name, player1_score=player1_score, player2_score=player2_score,current_player=current_player, min_pickup=min_pickup,max_pickup=max_pickup, judge_name=judge_name,game_ended=game_ended, winner=winner)

@app.route('/take_turn', methods=['POST'])
def take_turn():
    global pile1, pile2, pile3, player1_score, player2_score, current_player, game_ended, winner

    pile = request.form['pile']
    num_stones = int(request.form['num_stones'])
    pilen = 0
    if pile == 'pile1':
        pilen = pile1
        if num_stones<=pilen:
         pile1 -= min(num_stones, pile1)
    elif pile == 'pile2':
        pilen = pile2
        if num_stones<=pilen:
         pile2 -= min(num_stones, pile2)
    elif pile == 'pile3':
        pilen = pile3
        if num_stones<=pilen:
         pile3 -= min(num_stones, pile3)

    if current_player == player1_name and pilen >= 0 and num_stones<=pilen:
        player1_score += num_stones
    elif pilen > 0 and num_stones<=pilen:
        player2_score += num_stones
    if current_player == player1_name and pilen > 0 and num_stones<=pilen:
        current_player = player2_name
    elif pilen > 0 and num_stones<=pilen:
        current_player = player1_name
    socketio.emit('take_turn', {
        'pile1':pile1,
        'pile2':pile2,
       'pile3':pile3,

        'pile': pile,
        'num_stones': num_stones,
        'player1_score': player1_score,
        'player2_score': player2_score,
        'current_player': current_player,
        'game_ended': game_ended,
        'winner': winner
    })
    if pile1 == 0 and pile2 == 0 and pile3 == 0:
        game_ended = True
        if player1_score > player2_score:
            winner = player1_name
        elif player2_score > player1_score:
            winner = player2_name
        else:
            winner = "Tie"
    return redirect(url_for('play_game'))


@app.route('/end_game', methods=['POST'])
def end_game():
    global game_ended, winner
    game_ended = True

    if player1_score > player2_score:
        winner = player1_name
    elif player2_score > player1_score:
        winner = player2_name
    else:
        winner = "Tie"

    socketio.emit('end_game', {
        'game_ended': game_ended,
        'winner': winner
    })

    return redirect(url_for('play_game'))


@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True)
