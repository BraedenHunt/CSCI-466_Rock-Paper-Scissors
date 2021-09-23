import requests
import json

from result import MoveResult


class ClientManager:

    def __init__(self, server_url):
        self.server_url = server_url
        self.move_id = 0
        self.game_id = 0
        self.user_id = 0
        self.p2_id = 0

    def connect_to_game(self, game_id):
        try:
            self.game_id = game_id
            r = requests.get(self.server_url + '/get_game', headers={"gameId": str(self.game_id)})
            body = json.loads(r.content.decode('utf-8'))
            self.user_id = body['player2Id']
            self.p2_id = body['player1Id']
            return True
        except Exception as e:
            return False

    def create_game(self):
        r = requests.get(self.server_url + '/create_game')
        body = json.loads(r.content.decode('utf-8'))
        return body['gameId'], body['player1Id'], body['player2Id']

    def get_results(self):
        r = requests.get(self.server_url + '/result',
                         headers={"gameId": str(self.game_id),
                                  "userId": str(self.user_id),
                                  "player2Id": str(self.p2_id),
                                  "moveId": str(self.move_id)})
        result = MoveResult(**json.loads(r.content.decode('utf-8')))
        if self.user_id == result.player1_id:
            winner = result.winner
            user_move = result.player1_move
            opponent_move = result.player2_move
        else:
            winner = (3 - result.winner) % 3
            user_move = result.player2_move
            opponent_move = result.player1_move
        return winner, user_move, opponent_move
