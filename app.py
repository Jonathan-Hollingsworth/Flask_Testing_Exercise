from boggle import Boggle
import pdb
from flask import Flask, session, redirect, request, jsonify, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'do not guess it'

boggle_game = Boggle()
found_words = []

@app.route('/')
def begin_boggle():
    board = boggle_game.make_board()
    session['board'] = board
    high_score = session.get('high_score', 0)
    found_words.clear()

    return render_template('board.html', board=board, high_score=high_score)

@app.route('/guess')
def process_guess():
    guess = request.args['guess']
    board = session['board']
    result = boggle_game.check_valid_word(board, guess)
    response = {'result':result, 'score':len(guess)}
    if result == 'ok':
        found_words.append(guess)
    return jsonify(response)
    
@app.route('/game-over', methods=['POST'])
def handle_end_of_game():
    request = request.json["score"]
    pdb.set_trace()
    session['play-count'] += 1