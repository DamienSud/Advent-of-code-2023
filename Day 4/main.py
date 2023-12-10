import re
import time

from constants import *


class Card:
    def __init__(self, card_as_str: str):
        self.id = 0
        self.wining_numbers = []
        self.owned_numbers = []

        self._build_card_datas(card_as_str)

    def __str__(self):
        literal = f"Card {self.id}: "

        for win in self.wining_numbers:
            literal += str(win) + " "

        literal += "|"

        for owned in self.owned_numbers:
            literal += str(owned) + " "

        return literal

    def _build_card_datas(self, card_as_str):
        card_id, cards = card_as_str.split(':')

        wining, owned = cards.split('|')

        self.id = re.search(r'[0-9]+', card_id).group(0)

        for wining in re.findall(r'[0-9]+', wining):
            self.wining_numbers.append(wining)

        for owned in re.findall(r'[0-9]+', owned):
            self.owned_numbers.append(owned)

    def get_matching_numbers(self):

        results = []

        for win in self.wining_numbers:
            for owned in self.owned_numbers:
                if win == owned:
                    results.append(win)

        return results

    def get_worth_value(self):

        results = self.get_matching_numbers()

        worth_value = 0

        for val in results:
            if worth_value == 0:
                worth_value = 1
            else:
                worth_value *= 2

        return worth_value

    def get_list_of_winned_card(self):

        return [int(self.id) + value for value in range(1, len(self.get_matching_numbers()) + 1)]


class Day4:
    def __init__(self, crd_pile: str):
        self.card_pile = []

        for card in crd_pile.split('\n'):
            self.card_pile.append(
                Card(card)
            )

        self.qtt_in_card_pile = {}

        for card in self.card_pile:
            if card.id in self.qtt_in_card_pile:
                self.qtt_in_card_pile[card.id] += 1
            else:
                self.qtt_in_card_pile[card.id] = 1

    def step1(self):
        total = 0

        for card in self.card_pile:
            total += card.get_worth_value()

        return total

    def step2(self):

        for card in self.card_pile:

            cards_won = []

            for card_qtt in range(self.qtt_in_card_pile[card.id]):
                cards_won += card.get_list_of_winned_card()

            for won_card in cards_won:
                won_card = str(won_card)
                if won_card in self.qtt_in_card_pile:
                    self.qtt_in_card_pile[won_card] += 1
                else:
                    self.qtt_in_card_pile[won_card] = 1

        final_card_qtt = 0

        for _, qtt in self.qtt_in_card_pile.items():
            final_card_qtt += qtt

        return final_card_qtt


if __name__ == "__main__":
    print("main instance is running...")

    day4 = Day4(card_pile)

    # print(f"step1 result : {day4.step1()}")

    start_time = time.time_ns()

    print(f"step2 result : {day4.step2()}")

    print(f"time taken by the function : {time.time_ns() - start_time}")