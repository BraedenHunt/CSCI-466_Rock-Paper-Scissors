import io
import functools
import json
import sys
from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler
import result


class GameHistory:
    def __init__(self, game_id='', player1_id=0, player2_id=0, player1_wins=0, player2_wins=0, ties=0, player1_moves=[], player2_moves=[]):
        self.game_id = game_id
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.player1_wins = player1_wins
        self.player2_wins = player2_wins
        self.ties = ties
        self.player1_moves = player1_moves
        self.player2_moves = player2_moves


class GameHistoryEncoder(json.JSONEncoder):
    def default(self, history):
        if isinstance(history, GameHistory):
            return history.__dict__
        else:
            return json.JSONEncoder.default(self, history)


class GameHistoryManager:
    def __init__(self, game_id, player1_id, player2_id):
        self.file_name = str(game_id) + '.json'
        try:
            with open(self.file_name, 'r') as file:
                self.game_history = GameHistory(**json.load(file))
        except:
            with open(self.file_name, 'w+') as file:
                self.game_history = GameHistory()
                self.game_history.game_id = game_id
                self.game_history.player1_id = player1_id
                self.game_history.player2_id = player2_id
                json.dump(self.game_history, file, cls=GameHistoryEncoder)

    def add_move(self, player_id, move_number, move):
            if player_id == self.game_history.player1_id and len(self.game_history.player1_moves) == move_number - 1:
                self.game_history.player1_moves.append(move)
            elif player_id == self.game_history.player2_id and len(self.game_history.player2_moves) == move_number - 1:
                self.game_history.player2_moves.append(move)
            else:
                return False
            self.save_game_history()
            return True

    def find_result(self, move):
        move_result = result.MoveResult()
        if move < min(len(self.game_history.player1_moves), len(self.game_history.player2_moves)):
            move_result.player1_move = self.game_history.player1_moves[move]
            move_result.player2_move = self.game_history.player2_moves[move]
            move_result.winner = self.determine_winner(self.game_history.player1_moves[move], self.game_history.player2_moves[move])
            move_result.player1_id = self.game_history.player1_id
            move_result.player2_id = self.game_history.player2_id
        return move_result

    def find_last_result(self, move=-1):
        last_move = min(len(self.game_history.player1_moves), len(self.game_history.player2_moves))
        return self.find_result(last_move)

    # 0: tie, 1: move1 won, 2: move2 won
    def determine_winner(self, move1, move2):
        if move1 == move2:
            return 0
        if move1 == "rock":
            if move2 == "scissors":
                return 1
            elif move2 == "paper":
                return 2
        if move1 == "paper":
            if move2 == "rock":
                return 1
            elif move2 == "scissors":
                return 2
        if move1 == "scissors":
            if move2 == "paper":
                return 1
            elif move2 == "rock":
                return 2
        return 0

    def save_game_history(self):
        with open(self.file_name, 'w') as file:
            json.dump(self.game_history, file, cls=GameHistoryEncoder)


class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    """A custom HTTP Request Handler based on SimpleHTTPRequestHandler"""

    server_version = "My_HTTP_Server/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # initialize the base handler

    def do_GET(self):
        """Serve a GET request."""

        print(self.client_address)
        print(self.headers)
        print(self.path)
        if self.path == "/result":
            game_id = self.headers.get('gameId')
            user_id = int(self.headers.get('userId'))
            player2_id = int(self.headers.get('player2Id'))
            move_id = int(self.headers.get('moveId'))
            move_result = self.getResult(game_id, user_id, player2_id, move_id)

            self.send_response(HTTPStatus.OK)
            self.end_headers()
            string = json.dumps(move_result, cls=result.MoveResultEncoder)
            self.wfile.write(bytes(string, 'utf-8'))


    def getResult(self, game_id, user_id, player2_id, move_id):
        player1 = min(user_id, player2_id)
        player2 = max(user_id, player2_id)
        game_manager = GameHistoryManager(game_id, min(user_id, player2_id), max(user_id, player2_id))
        return game_manager.find_result(move_id)

    def do_POST(self):
        print(type(self.headers))
        game_id = self.headers.get("gameId")
        user_id = int(self.headers.get("userId"))
        player2_id = int(self.headers.get("player2Id"))

        # Source:
        # https://stackoverflow.com/questions/5975952/how-to-extract-http-message-body-in-basehttprequesthandler-do-post
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)

        json_body = json.loads(post_body)

        game_manager = GameHistoryManager(game_id, min(user_id, player2_id), max(user_id, player2_id))
        if game_manager.add_move(user_id, json_body["moveNumber"], json_body["move"]):
            self.send_response(HTTPStatus.OK)
        else:
            self.send_response(HTTPStatus.ALREADY_REPORTED)
        self.end_headers()


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler, port=5000):
    server_address = ('', port)

    handler = functools.partial(handler_class)
    httpd = server_class(server_address, handler)
    httpd.serve_forever()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run(HTTPServer, MyHTTPRequestHandler, port=sys.argv[1])
    else:
        run(HTTPServer, MyHTTPRequestHandler)
