from db import create_tables
from game import main_menu, play_game

create_tables()

while True:
    action = main_menu()
    if action == "play":
        play_game()