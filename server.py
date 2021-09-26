import functools
import json
import sys
from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler

import result
from game_history import GameHistoryManager
from server_state import ServerStateManager

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    """A custom HTTP Request Handler based on SimpleHTTPRequestHandler"""

    server_version = "My_HTTP_Server/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # initialize the base handler

    def do_GET(self):
        """Serve a GET request."""

        print('\nHandling GET: ' + self.path)
        print('------Headers------\n' + str(self.headers).strip())
        if self.path == "/result":
            game_id = self.headers.get('gameId')
            user_id = int(self.headers.get('userId'))
            player2_id = int(self.headers.get('player2Id'))
            move_id = self.headers.get('moveId')
            move_id = int(move_id) if move_id else -1
            move_result = self.get_result(game_id, user_id, player2_id, move_id)

            self.send_response(HTTPStatus.OK)
            self.end_headers()
            string = json.dumps(move_result, cls=result.MoveResultEncoder)
            self.wfile.write(bytes(string, 'utf-8'))

        elif self.path == "/create_game":
            serv_mgr = ServerStateManager()
            game_id = serv_mgr.get_next_game()
            p1 = serv_mgr.get_next_player()
            p2 = serv_mgr.get_next_player()
            GameHistoryManager(game_id, p1, p2)
            response = {'gameId': game_id, 'player1Id': p1, 'player2Id': p2}
            self.send_response(HTTPStatus.OK)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(response), 'utf-8'))

        elif self.path == "/get_game":
            game_id = self.headers.get('gameId')
            ids = self.get_game(str(game_id))
            if len(ids) < 2:
                self.send_response(HTTPStatus.BAD_REQUEST)
                self.end_headers()
                return
            response = {'player1Id': ids[0], "player2Id": ids[1]}
            self.send_response(HTTPStatus.OK)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(response), 'utf-8'))

        elif self.path == "/get_next_move_id":
            game_id = int(self.headers.get('gameId'))
            user_id = int(self.headers.get('userId'))
            player2_id = int(self.headers.get('player2Id'))
            response = {'moveId': self.get_next_move_id(game_id, user_id, player2_id)}
            self.send_response(HTTPStatus.OK)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(response), 'utf-8'))

        elif self.path == "/get_game_stats":
            game_id = int(self.headers.get('gameId'))
            user_id = int(self.headers.get('userId'))
            player2_id = int(self.headers.get('player2Id'))
            p1_id, p2_id, p1_wins, p2_wins, ties = self.get_game_stats(game_id, user_id, player2_id)
            response = {'player1Wins': p1_wins, 'player2Wins': p2_wins, "ties": ties, 'player1Id': p1_id, 'player2Id': p2_id}
            self.send_response(HTTPStatus.OK)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(response), 'utf-8'))

    def get_result(self, game_id, user_id, player2_id, move_id):
        game_manager = GameHistoryManager(game_id, min(user_id, player2_id), max(user_id, player2_id))
        return game_manager.find_result(move_id)

    def get_game(self, game_id):
        return GameHistoryManager.get_player_ids(game_id)

    def get_game_stats(self, game_id, user_id, player2_id):
        game_manager = GameHistoryManager(game_id, min(user_id, player2_id), max(user_id, player2_id))
        return game_manager.get_game_stats()

    def get_next_move_id(self, game_id, user_id, player2_id):
        game_mgr = GameHistoryManager(game_id, min(user_id, player2_id), max(user_id, player2_id))
        return game_mgr.get_next_move_id(user_id)

    def do_POST(self):
        print("\nHandling POST")
        print('------Headers------\n' + str(self.headers).strip())
        game_id = int(self.headers.get("gameId"))
        user_id = int(self.headers.get("userId"))
        player2_id = int(self.headers.get("player2Id"))

        # Source:
        # https://stackoverflow.com/questions/5975952/how-to-extract-http-message-body-in-basehttprequesthandler-do-post
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)

        json_body = json.loads(post_body)
        print('------Body------\n' + str(json_body).strip())

        game_manager = GameHistoryManager(game_id, min(user_id, player2_id), max(user_id, player2_id))
        move = json_body["move"]
        if move == "reset":
            reset = game_manager.request_reset(user_id)
            self.send_response(HTTPStatus.OK)
            self.send_header('reset', str(reset))
        elif game_manager.add_move(user_id, int(json_body["moveId"]), json_body["move"]):
            self.send_response(HTTPStatus.OK)
        else:
            self.send_response(HTTPStatus.ALREADY_REPORTED)
        self.end_headers()


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler, port=5000):
    print('Starting server at http://localhost:' + str(port))
    server_address = ('', port)

    handler = functools.partial(handler_class)
    httpd = server_class(server_address, handler)
    httpd.serve_forever()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run(HTTPServer, MyHTTPRequestHandler, port=int(sys.argv[1]))
    else:
        run(HTTPServer, MyHTTPRequestHandler)
