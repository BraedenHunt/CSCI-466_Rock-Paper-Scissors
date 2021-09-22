import requests
import json
import os

options = "0) Connect to game\n" \
          "1) Send Move\n" \
          "2) Check Results\n" \
          "q) Exit game"


def main():
    print("Welcome to Braeden's Rock Paper Scissors Game!")
    while 1:
        main_menu[display_options()]()

def display_options():
    print(options)
    sel = input("Selection: ")
    if sel in main_menu:
        return sel
    else:
        print("That is not a valid option")
        return display_options()

def game_menu():
    print("Connecting to game")
    print("0) Create game\n"
          "1) Join game\n"
          "q) Return to Main Menu\n")
    sel = input("Selection: ")
    if sel in connect_menu:
        connect_menu[sel]()


def create_game():
    #TODO call server's create game
    pass

def connect_to_game():
    #TODO get game id and connect to server
    pass

def send_move():
    #TODO create menu to select move and send move
    print("Sending move")
    pass

def check_results():
    #TODO call the check results url on the server
    print("Checking results")
    pass

main_menu = {"0": game_menu, "1": send_move, "2": check_results, "q": exit }
connect_menu = {"0": create_game, "1": connect_to_game, 'q': display_options}

if __name__ == "__main__":
    main()
