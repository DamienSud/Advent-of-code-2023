from __future__ import annotations

from constants import motor_card_scheme


class MotorCardValue:
    def __init__(self, x_pos: int, y_pos: int, value_size: int, value: str):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.value_size = value_size
        self.value = value

    def __str__(self):
        return f"{self.value} (x: {self.x_pos}; y: {self.y_pos}; size: {self.value_size})"


class MotorSymbol:
    def __init__(self, x_pos: int, y_pos: int, value: str):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.value = value
        self.value_size = 1

    def __str__(self):
        return f"{self.value} (x: {self.x_pos}; y: {self.y_pos})"


class CardScheme:
    def __init__(self, card_scheme_as_str: str):
        self.existing_symbols = CardScheme.scan_card_scheme_language(card_scheme_as_str)

        # the card is split in list of line
        self.card_scheme_datas = CardScheme.build_card_scheme_datas(card_scheme_as_str)

        # the card remember position of different value
        self.values = self._get_values_from_scheme()

        # the card remember the symbol position
        self.symbols = self._get_symbols_from_scheme()

    def _get_symbols_from_scheme(self):
        symbols = []

        for index_line, line in enumerate(self.card_scheme_datas):
            line_symbols = []
            for index_char, char in enumerate(line):
                if char in self.existing_symbols:
                    symbol = MotorSymbol(index_char, index_line, char)
                    line_symbols.append(symbol)
            symbols.append(line_symbols)

        return symbols

    def _get_values_from_scheme(self):
        values = []

        for line_index, line in enumerate(self.card_scheme_datas):

            line_values = []  # store the value in the current line

            do_not_read_again = -1

            for char_index, char in enumerate(line):
                if char not in self.existing_symbols and char != "." and char_index > do_not_read_again:
                    reading_offset = 1
                    while char_index + reading_offset < len(line):

                        if line[char_index + reading_offset] == "." or line[char_index + reading_offset] in self.existing_symbols:
                            do_not_read_again = char_index + reading_offset
                            break

                        reading_offset += 1
                    value = MotorCardValue(char_index, line_index, reading_offset,
                                           line[char_index : char_index+reading_offset])
                    line_values.append(value)
            values.append(line_values)
        return values

    def get_symbol_inside(self, line_index: int, low_bound: int, high_bound: int):
        corresponding_symbols = []

        for symbol in self.symbols[line_index]:
            if low_bound <= symbol.x_pos < high_bound:
                corresponding_symbols.append(symbol)

        return corresponding_symbols

    def get_value_inside(self, line_index: int, low_bound: int, high_bound: int):
        corresponding_value = []

        for value in self.values[line_index]:
            for pos in range(value.x_pos, value.x_pos + value.value_size):
                if low_bound <= pos < high_bound:
                    corresponding_value.append(value)
                    break

        return corresponding_value

    def is_entity_around(self, entity: MotorCardValue | MotorSymbol):

        entity_around = False
        entities = []

        if entity.y_pos > 0:
            if type(entity) == MotorCardValue:
                result = self.get_symbol_inside(entity.y_pos-1, entity.x_pos-1, entity.x_pos+entity.value_size + 1)
                if len(result) > 0:
                    entity_around = True
                    entities += result
            elif type(entity) == MotorSymbol:
                result = self.get_value_inside(entity.y_pos-1, entity.x_pos-1, entity.x_pos + entity.value_size + 1)
                if len(result) > 0:
                    entity_around = True
                    entities += result

        if type(entity) == MotorCardValue:
            result = self.get_symbol_inside(entity.y_pos, entity.x_pos - 1, entity.x_pos + entity.value_size + 1)
            if len(result) > 0:
                entity_around = True
                entities += result
        elif type(entity) == MotorSymbol:
            result = self.get_value_inside(entity.y_pos, entity.x_pos - 1, entity.x_pos + entity.value_size + 1)
            if len(result) > 0:
                entity_around = True
                entities += result

        if entity.y_pos < len(self.values) - 1:
            if type(entity) == MotorCardValue:
                result = self.get_symbol_inside(entity.y_pos + 1, entity.x_pos - 1, entity.x_pos + entity.value_size + 1)
                if len(result) > 0:
                    entity_around = True
                    entities += result
            elif type(entity) == MotorSymbol:
                result = self.get_value_inside(entity.y_pos + 1, entity.x_pos - 1, entity.x_pos + entity.value_size + 1)
                if len(result) > 0:
                    entity_around = True
                    entities += result

        return entity_around, entities

    def show_line_around(self, value: int):
        if value > 0:
            print(self.card_scheme_datas[value - 1])

        print(self.card_scheme_datas[value])

        if value < len(self.values) - 1:
            print(self.card_scheme_datas[value + 1])

    def get_gear_ratio(self, symbol: MotorSymbol):

        result = self.is_entity_around(symbol)

        return int(result[1][0].value) * int(result[1][1].value) if len(result[1]) == 2 else 0

    @staticmethod
    def scan_card_scheme_language(card_scheme_as_str: str):

        found_symbols = []

        for char in card_scheme_as_str:
            if char not in "0123456789\n." and char not in found_symbols:
                found_symbols.append(char)

        return found_symbols

    @staticmethod
    def build_card_scheme_datas(card_scheme_as_str: str):
        card_scheme_as_list = []

        for index, line in enumerate(card_scheme_as_str.split("\n")):
            card_scheme_as_list.append(line)

        return card_scheme_as_list


class Day3:
    def __init__(self, crd_scheme: CardScheme):
        self.card_scheme = crd_scheme

    def step1(self):
        valid_values = []

        for line_index, line_value in enumerate(self.card_scheme.values):

            # print("\n\n-----------------------------------\n\n")
            #
            # self.card_scheme.show_line_around(line_index)

            for value in line_value:
                if self.card_scheme.is_entity_around(value)[0]:
                    # print(value.value, end=" - ")
                    valid_values.append(int(value.value))

            # input("\n\npress any key to continue...\n\n")
            # print()

        return valid_values

    def step2(self):
        star_symbols = []

        for line in self.card_scheme.symbols:
            for symbol in line:
                if symbol.value == "*":
                    star_symbols.append(symbol)

        gear_ratios = []

        for symbol in star_symbols:
            gear_ratios.append(self.card_scheme.get_gear_ratio(symbol))

        return gear_ratios


def make_it_dict(entry):
    new_dict = {}

    for i in entry:
        if i in new_dict.keys():
            new_dict[i] += 1
        else:
            new_dict[i] = 1

    return new_dict


def compare_dict(dic1, dic2):

    for key, value in dic1.items():
        if key in dic2.keys():
            if dic2[key] == value:
                continue
            else:
                print(f"error with value {key} :\n dic1 : {key} -> {value}\n dic2 : {key} -> {dic2[key]}")
        else:
            print(f"dic1 key {key} not found in dic2")


if __name__ == "__main__":
    print(f"main instance is running...")

    card_scheme = CardScheme(motor_card_scheme)

    day3 = Day3(card_scheme)

    result_step1 = day3.step1()

    print(f"step1 result : {sum(result_step1)}")

    result_step2 = day3.step2()

    print(f"step2 result : {sum(result_step2)}")