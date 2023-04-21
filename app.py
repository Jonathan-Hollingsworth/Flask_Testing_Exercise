from boggle import Boggle
import pdb
from flask import Flask, session, request, jsonify, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'do not guess it'

boggle_game = Boggle()
found_words = []

@app.route('/')
def begin_boggle():
    "Initializes the boggle game"
    board = boggle_game.make_board()
    session['board'] = board
    high_score = session.get('high_score', 0)
    play_count = session.get('play-count', 0)
    found_words.clear()

    return render_template('board.html', board=board, high_score=high_score, play_count=play_count)

@app.route('/guess')
def process_guess():
    "Checks the players guess and returns JSON information"
    guess = request.args['guess']
    if guess in found_words:
        response = {'result': 'already-found'}
        return jsonify(response)
    board = session['board']
    result = boggle_game.check_valid_word(board, guess)
    response = {'result':result, 'score':len(guess)}
    if result == 'ok':
        found_words.append(guess)
    return jsonify(response)
    
@app.route('/game-over', methods=['POST'])
def handle_end_of_game():
    "Finalizes the high score and play count when the game ends"
    score = request.json["score"]
    high_score = session.get('high_score', 0)
    if score > high_score:
        session['high_score'] = score
    play_count = session.get('play-count', 0)
    session['play-count'] = play_count + 1
    return jsonify(newRecord=score > high_score)