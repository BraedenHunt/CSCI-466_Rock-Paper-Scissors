from client_state import ClientManager

options = "0) Connect to game\n" \
          "1) Send Move\n" \
          "2) Check Results\n" \
          "q) Exit game"
line_break = '--------------------'
move_options = "1) Rock\n" \
               "2) Paper\n" \
               "3) Scissors\n" \
               "r) Request Reset"
client_mgr = ClientManager('http://localhost:5000')

def main():
    print("Welcome to Braeden's Rock Paper Scissors Game!")
    while 1:
        menu()

def menu():
    print(line_break)
    print(options)
    sel = input("Selection: ")
    print(line_break)
    if sel in main_menu:
        main_menu[sel]()
        return
    else:
        print("That is not a valid option")


def game_menu():
    print(line_break)
    print("How would you like to connect?")
    print("0) Create game\n"
          "1) Join game\n"
          "q) Return to Main Menu")
    sel = input("Selection: ")
    if sel in connect_menu:
        connect_menu[sel]()


def create_game():
    print("Creating game...")
    game_id, p1_id, p2_id = client_mgr.create_game()
    client_mgr.game_id = game_id
    client_mgr.user_id = p1_id
    client_mgr.p2_id = p2_id
    print("Share this Game ID with your opponent: " + str(game_id))

def connect_to_game():
    game_id = input("Game ID: ")
    client_mgr.connect_to_game(int(game_id))
    print('Connecting to existing game ' + game_id)

def send_move():
    # TODO create menu to select move and send move
    print("Select the move you want to send: ")
    print(move_options)
    sel = input("Selection: ")
    client_mgr.send_move(moves[sel])

def check_results():
    winner, player_move, opponent_move = client_mgr.get_results()
    if winner == 0:
        print("You tied! You both played " + str(player_move))
    elif winner == 1:
        print("You won! Your {} beat their {}".format(player_move, opponent_move))
    elif winner == 2:
        print("You lost! Their {} beat your {}".format(opponent_move, player_move))
    else:
        print("There isn't a result ready.")

main_menu = {"0": game_menu, "1": send_move, "2": check_results, "q": exit }
connect_menu = {"0": create_game, "1": connect_to_game, 'q': main}
moves = {"1": "rock", "2": "paper", "3": "scissors", "r": "reset"}

if __name__ == "__main__":
    main()
