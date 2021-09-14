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

        elif self.path == "/create_game":
            serv_mgr = ServerStateManager()
            game_id = serv_mgr.get_next_game()
            p1 = serv_mgr.get_next_player()
            p2 = serv_mgr.get_next_player()
            response = {'gameId': game_id, 'player1Id': p1, 'player2Id': p2}
            self.send_response(HTTPStatus.OK)
            self.end_headers()
            self.wfile.write(bytes(json.dumps(response), 'utf-8'))

    def getResult(self, game_id, user_id, player2_id, move_id):
        player1 = min(user_id, player2_id)
        player2 = max(user_id, player2_id)
        game_manager = GameHistoryManager(game_id, min(user_id, player2_id), max(user_id, player2_id))
        return game_manager.find_result(move_id)

    def do_POST(self):
        print(type(self.headers))
        game_id = int(self.headers.get("gameId"))
        user_id = int(self.headers.get("userId"))
        player2_id = int(self.headers.get("player2Id"))

        # Source:
        # https://stackoverflow.com/questions/5975952/how-to-extract-http-message-body-in-basehttprequesthandler-do-post
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)

        json_body = json.loads(post_body)

        game_manager = GameHistoryManager(game_id, min(user_id, player2_id), max(user_id, player2_id))
        move = json_body["move"]
        if move == "reset":
            game_manager.request_reset(user_id)
            self.send_response(HTTPStatus.OK)
        elif game_manager.add_move(user_id, json_body["moveNumber"], json_body["move"]):
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
