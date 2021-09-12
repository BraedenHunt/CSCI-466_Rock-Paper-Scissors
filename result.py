from json import JSONEncoder

class MoveResult:
    def __init__(self, player1_id=0, player2_id=0, player1_move='', player2_move='', winner=0):
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.player1_move = player1_move
        self.player2_move = player2_move
        self.winner = winner


class MoveResultEncoder(JSONEncoder):
    def default(self, move):
        if isinstance(move, MoveResult):
            return move.__dict__
        else:
            return JSONEncoder.default(self, move)
