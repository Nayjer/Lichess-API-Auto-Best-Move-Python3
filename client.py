import requests
import json
from stockfish import Stockfish
import time

stockfish = Stockfish(r"C:\Users\Alex\Desktop\lichess_api\stockfish_13_win_x64_avx2\stockfish_13_win_x64_avx2.exe")


class Client:
    def __init__(self, secret_token, username):
        self.secret_token = secret_token
        self.username = username

    def get_game_id(self):
        current_game = requests.get('https://lichess.org/api/user/{}/current-game'.format(self.username))
        game_id = ""
        for i in range(27, len(current_game.text.split("\n")[1]) - 2):
            game_id = game_id + current_game.text.split("\n")[1][i]
        return game_id


def get_moves(game_id, secret_token):
    game_state = requests.get('https://lichess.org/api/board/game/stream/{}'.format(game_id),
                              headers={"Authorization": "Bearer {}".format(secret_token)},
                              stream=True)
    lines = game_state.iter_lines()
    for line in lines:
        x = json.loads(line)
        moves = x["state"]["moves"]
        return moves


def do_best_move(game_id, moves, secret_token):
    stockfish.set_position(moves.split())
    best_move = stockfish.get_best_move()
    requests.post('https://lichess.org/api/board/game/' + game_id + '/move/' + best_move,
                  headers={"Authorization": "Bearer {}".format(secret_token)})


def single_play():
    Test = Client("secret token here!! (game:play)", 'here your username')
    game_id_p = Test.get_game_id()
    do_best_move(game_id_p, get_moves(game_id_p, Test.secret_token), Test.secret_token)
