from client_state import ClientManager
import sys

options = "1) Connect to game\n" \
          "2) Send Move\n" \
          "3) Check Results\n" \
          "4) Get Game Stats\n" \
          "q) Exit game"
line_break = '--------------------'
move_options = "1) Rock\n" \
               "2) Paper\n" \
               "3) Scissors\n" \
               "r) Request Reset"

client_mgr = ClientManager('http://localhost:5000')

def main(address='http://localhost:5000'):
    global client_mgr
    client_mgr = ClientManager(address)
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
    print("1) Create game\n"
          "2) Join game\n"
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
    print('Connecting to existing game ' + game_id)
    if client_mgr.connect_to_game(int(game_id)):
        print("Connected!")
    else:
        print("Failed to connect!")

def send_move():
    print("Select the move you want to send: ")
    print(move_options)
    sel = input("Selection: ")
    print("Sending " + moves[sel])
    result, reset = client_mgr.send_move(moves[sel])
    if result:
        print('Successfully sent.')
        if moves[sel] == 'reset':
            if reset:
                print('The game has been reset.')
            else:
                print('Your opponent has not requested a reset yet.')
    else:
        print('Something went wrong. Move not sent')

def check_results():
    try:
        winner, player_move, opponent_move = client_mgr.get_results()
        if winner == 0:
            print("You tied! You both played " + str(player_move))
        elif winner == 1:
            print("You won! Your {} beat their {}".format(player_move, opponent_move))
        elif winner == 2:
            print("You lost! Their {} beat your {}".format(opponent_move, player_move))
        else:
            print("There isn't a result ready. There may have been a reset.")
    except Exception:
        print('An error occurred while checking the results.')


def get_stats():
    try:
        wins, losses, ties = client_mgr.get_game_stats()
        print('Out of {} game(s), you won {} time(s) and lost {} time(s). You tied {} times.'.format(wins + losses + ties, wins, losses, ties))
    except Exception:
        print('An error occured while trying to retrieve the game stats.')

main_menu = {"1": game_menu, "2": send_move, "3": check_results, "4": get_stats, "q": exit }
connect_menu = {"1": create_game, "2": connect_to_game, 'q': main}
moves = {"1": "rock", "2": "paper", "3": "scissors", "r": "reset"}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("Using address: " + sys.argv[1])
        main(address=sys.argv[1])
    else:
        print("Using default address: http://localhost:5000")
        main()