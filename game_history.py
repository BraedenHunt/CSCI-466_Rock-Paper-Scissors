import json
import result

class GameHistory:
    def __init__(self, game_id='', player1_id=0, player2_id=0,
                 player1_wins=0, player2_wins=0, ties=0,
                 player1_moves=[], player2_moves=[],
                 player1_reset=False, player2_reset=False):
        self.game_id = game_id
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.player1_wins = player1_wins
        self.player2_wins = player2_wins
        self.ties = ties
        self.player1_moves = player1_moves
        self.player2_moves = player2_moves
        self.player1_reset = player1_reset
        self.player2_reset = player2_reset


class GameHistoryEncoder(json.JSONEncoder):
    def default(self, history):
        if isinstance(history, GameHistory):
            return history.__dict__
        else:
            return json.JSONEncoder.default(self, history)


class GameHistoryManager:
    def __init__(self, game_id, player1_id, player2_id):
        self.file_name = 'games/' + str(game_id) + '.json'
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

    @staticmethod
    def get_player_ids(game_id):
        try:
            with open('games/' + str(game_id) + '.json', 'r') as file:
                game_history = GameHistory(**json.load(file))
                return game_history.player1_id, game_history.player2_id
        except Exception:
            return ()

    def add_move(self, player_id, move_number, move):
        if player_id == self.game_history.player1_id and len(self.game_history.player1_moves) == move_number - 1:
            self.game_history.player1_moves.append(move)
        elif player_id == self.game_history.player2_id and len(self.game_history.player2_moves) == move_number - 1:
            self.game_history.player2_moves.append(move)
        else:
            return False

        if len(self.game_history.player1_moves) == len(self.game_history.player2_moves):
            winner = self.determine_winner(self.game_history.player1_moves[-1], self.game_history.player2_moves[-1])
            if winner == 1:
                self.game_history.player1_wins += 1
            elif winner == 2:
                self.game_history.player2_wins += 1
            elif winner == 0:
                self.game_history.ties += 1
        self.save_game_history()
        return True

    def get_game_stats(self):
        return self.game_history.player1_id, self.game_history.player2_id,  self.game_history.player1_wins, self.game_history.player2_wins, self.game_history.ties

    def request_reset(self, player_id):
        if player_id == self.game_history.player1_id:
            self.game_history.player1_reset = True
        elif player_id == self.game_history.player2_id:
            self.game_history.player2_reset = True
        if self.game_history.player1_reset and self.game_history.player2_reset:
            self.game_history.ties = self.game_history.player1_wins = self.game_history.player2_wins = 0
            self.game_history.player1_moves = self.game_history.player2_moves = []
            self.game_history.player1_reset = self.game_history.player2_reset = False
            self.save_game_history()
            return True
        self.save_game_history()
        return False

    def find_result(self, move):
        move_result = result.MoveResult()
        latest_move = min(len(self.game_history.player1_moves), len(self.game_history.player2_moves))
        if move <= latest_move and latest_move > 0:
            move_result.player1_move = self.game_history.player1_moves[move-1]
            move_result.player2_move = self.game_history.player2_moves[move-1]
            move_result.winner = self.determine_winner(self.game_history.player1_moves[move-1], self.game_history.player2_moves[move-1])
            move_result.player1_id = self.game_history.player1_id
            move_result.player2_id = self.game_history.player2_id
        return move_result

    def find_last_result(self, move=-1):
        last_move = min(len(self.game_history.player1_moves), len(self.game_history.player2_moves))
        return self.find_result(last_move)

    def get_next_move_id(self, user_id):
        if user_id == self.game_history.player1_id:
            return len(self.game_history.player1_moves)+1
        else:
            return len(self.game_history.player2_moves)+1

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
