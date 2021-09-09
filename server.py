import io
import functools
import json
import sys
from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler


class GameHistoryManager:

    player1_wins = 0
    player2_wins = 0
    player1_moves = []
    player2_moves = []

    def __init__(self, game_id, player1_id, player2_id):
        self.game_id = game_id
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.file_name = str(game_id) + '.txt'
        with open(self.file_name, 'w+') as file:
            lines = file.readlines()
            if len(lines) == 0:
                file.write('{}|0\n{}|0\n\n'.format(player1_id, player2_id))
            else:
                self.player1_moves = lines[2].split('|')
                self.player2_moves = lines[3].split('|')

    def add_move(self, player_id, move_number, move):
        with open(self.file_name, 'r+') as file:
            history = file.readlines()
            if player_id == self.player1_id and len(self.player1_moves) == move_number - 1:
                self.player1_moves.append(move)
                history[2] = '|'.join(self.player1_moves)
            elif player_id == self.player2_id and len(self.player2_moves) == move_number - 1:
                self.player2_moves.append(move)
                history[3] = '|'.join(self.player2_moves)
            else:
                return False
            file.seek(0)
            file.writelines(history)
            return True

    def find_last_move(self, player_id):
        with open(self.file_name, 'r+') as file:
            history = file.readlines()

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    """A custom HTTP Request Handler based on SimpleHTTPRequestHandler"""

    server_version = "My_HTTP_Server/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # initialize the base handler

    def do_GET(self):
        """Serve a GET request."""

        # get info from the HTTP request
        # look at https://docs.python.org/3/library/http.server.html for other BaseHTTPRequestHandler instance variables
        print(self.client_address)

        # update the path with the prefix of server files
        print(self.headers)

        # reply to client
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        '''try:
            f = open(self.path, 'rb')
            self.send_response(HTTPStatus.OK)
            self.end_headers()
            shutil.copyfileobj(f, self.wfile)
            f.close()
        except OSError:
            self.send_response(HTTPStatus.NOT_FOUND)
            self.end_headers()
            '''

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