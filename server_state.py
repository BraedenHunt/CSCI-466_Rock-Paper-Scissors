import json


class ServerState:
    def __init__(self, total_games=0, total_players=0):
        self.total_games = total_games
        self.total_players = total_players


class ServerStateEncoder(json.JSONEncoder):
    def default(self, state):
        if isinstance(state, ServerState):
            return state.__dict__
        else:
            return json.JSONEncoder.default(self, state)


class ServerStateManager:
    def __init__(self, file_name='server_state.json'):
        self.file_name = file_name
        try:
            with open(self.file_name, 'r') as file:
                self.server_state = ServerState(**json.load(file))
        except:
            with open(self.file_name, 'w+') as file:
                self.server_state = ServerState()
                json.dump(self.server_state, file, cls=ServerStateEncoder)

    def get_next_player(self):
        self.server_state.total_players += 1
        self.save_state()
        return self.server_state.total_players

    def get_next_game(self):
        self.server_state.total_games += 1
        self.save_state()
        return self.server_state.total_games

    def save_state(self):
        with open(self.file_name, 'w') as file:
            json.dump(self.server_state, file, cls=ServerStateEncoder)
