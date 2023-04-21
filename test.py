from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True

    def test_boggle(self):
        "Test the creation of a boggle board"
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<p>You have played 0 times</p>', html)
            self.assertIn('board', session)

    def test_high_score(self):
        "Does the high score display properly?"
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['high_score'] = 7
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2 id="high-score">High score: 7</h2>', html)

    def test_play_count(self):
        "Does the play count display properly?"
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['play-count'] = 4
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<p>You have played 4 times</p>', html)

    def test_guess(self):
        "Proccess valid guesses using a predetermined board"
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [['T', 'U', 'R', 'T', 'T'],
                                           ['G', 'E', 'H', 'K', 'G'],
                                           ['T', 'S', 'A', 'C', 'R'],
                                           ['F', 'P', 'S', 'J', 'Z'],
                                           ['U', 'U', 'Y', 'P', 'F']]

            resp = client.get('/guess?guess=test')
            resp_2 = client.get('/guess?guess=guess')

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp_2.status_code, 200)
            self.assertEqual(resp.json['result'], 'ok')
            self.assertEqual(resp_2.json['result'], 'ok')

    def test_bad_guess(self):
        "Tests all variations of an invalid guess"
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [['T', 'U', 'R', 'T', 'T'],
                                           ['G', 'E', 'H', 'K', 'G'],
                                           ['T', 'S', 'A', 'C', 'R'],
                                           ['F', 'P', 'S', 'J', 'Z'],
                                           ['U', 'U', 'Y', 'P', 'F']]

            not_a_word = client.get('/guess?guess=haarsgdf')
            not_on_Board = client.get('/guess?guess=missing')
            test_word = client.get('/guess?guess=test')
            same_word = client.get('/guess?guess=test')

            self.assertEqual(not_a_word.status_code, 200)
            self.assertEqual(not_on_Board.status_code, 200)
            self.assertEqual(same_word.status_code, 200)
            self.assertEqual(not_a_word.json['result'], 'not-word')
            self.assertEqual(not_on_Board.json['result'], 'not-on-board')
            self.assertEqual(same_word.json['result'], 'already-found')

