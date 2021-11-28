import random


class Lobby:

    def __init__(self, user1, user2):
        self.user_ids = [user1, user2]
        self.current_turn = random.randint(0, 1)
        self.used_cities = []
        self.last_letter = None

    def get_active_player_id(self):
        return self.user_ids[self.current_turn]

    def is_correct_letter(self, letter):
        return self.last_letter == letter


def change_last_letter(self, city):
    incorrect_last_letter = ["ы", "", ""]
    for letter in city[::-1]:
        if letter not in incorrect_last_letter:
            self.last_letter = letter
            break


def change_current_turn(self):
    def get_inactive_player_id():
        pass
