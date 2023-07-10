import random
from copy import copy


class Deck:
    def __init__(self, deck_list):
        self.decklist = copy(deck_list)
        self.shuffle_deck()

    def shuffle_deck(self):
        random.shuffle(self.decklist)

    def draw(self, num_cards):
        if len(self.decklist) == 0:
            print(f"Deck is empty! Unable to draw any cards!")
            return []
        _cards = []
        for n in range(0, num_cards):
            if len(self.decklist) == 0:
                print(f"Deck is empty! Only able to draw {n + 1} out of {num_cards} cards!")
                return _cards
            _cards.append(self.decklist.pop(0))
        return _cards


def get_land_count(hand):
    # Counts the number of lands drawn
    _num_lands = hand.count('land')
    return _num_lands
