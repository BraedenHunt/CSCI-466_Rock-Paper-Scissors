import requests


class ClientManager:

    def __init__(self, server_url):
        self.server_url = server_url
        self.move_id = 0
        self.game_id = 0
        self.user_id = 0
        self.p2_id = 0

    def connect_to_game(self, game_id):
        self.game_id = game_id
        r = requests.get(self.server_url + '/get_game', headers={"gameId": self.game_id})
        body = r.json()
        self.user_id = body['player2Id']
        self.p2_id = body['player1Id']

    def create_game(self):
        r = requests.get(self.server_url + '/create_game')
        body = r.json()

    def get_results(self):
        r = requests.get(self.server_url + '/result',
                         headers={"gameId": self.game_id,
                                  "userId": self.user_id,
                                  "player2Id": self.p2_id,
                                  "moveId": self.move_id})
        body = r.json()
