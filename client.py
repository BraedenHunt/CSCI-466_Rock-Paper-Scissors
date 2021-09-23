import requests
import json
import os

options = "0) Connect to game\n" \
          "1) Send Move\n" \
          "2) Check Results\n" \
          "q) Exit game"
line_break = '--------------------'

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
    #TODO call server's create game
    print("creating game...")
    pass

def connect_to_game():
    #TODO get game id and connect to server
    print('connecting to existing game')
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
connect_menu = {"0": create_game, "1": connect_to_game, 'q': main}

if __name__ == "__main__":
    main()
