import requests
import json
from stockfish import Stockfish

stockfish = Stockfish(r"C:\Users\Alex\Desktop\lichess_api\stockfish_13_win_x64_avx2\stockfish_13_win_x64_avx2.exe") #path to stockfish executable (https://stockfishchess.org/)


class Client:
    def __init__(self, secret_token, game_id):
        self.secret_token = secret_token
        self.game_id = game_id

    def move(self):
        game_state = requests.get('https://lichess.org/api/board/game/stream/{}'.format(self.game_id),
                                  headers={"Authorization": "Bearer {}".format(self.secret_token)},
                                  stream=True)
        lines = game_state.iter_lines()
        for line in lines:
            x = json.loads(line)
            moves = x["state"]["moves"]
            return moves


def do_move(game_id, moves, secret_token):
    stockfish.set_position(moves.split())
    best_move = stockfish.get_best_move()
    requests.post('https://lichess.org/api/board/game/'+game_id+'/move/'+best_move,
                  headers={"Authorization": "Bearer {}".format(secret_token)})


Test = Client('type here secret token', 'here the gameID')
do_move(Test.game_id, Test.move(), Test.secret_token)
