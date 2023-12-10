from constants import puzzle_input, digits_in_letters


class Day1:
    def __init__(self, pzzl_input: str):
        self.puzzle_input = pzzl_input

    def step1(self):

        result = 0

        for line in self.puzzle_input.split("\n"):
            print(line)
            print(Day1.find_first_and_last_number(line))

            temp_res = int(str(Day1.find_first_and_last_number(line)[0]) \
                           + str(Day1.find_first_and_last_number(line)[1]))

            result += temp_res
            print(temp_res)

        return result

    def step2(self):
        result = 0

        for line in self.puzzle_input.split("\n"):
            print(line)
            print(Day1.find_first_and_last_number_V2(line))

            temp_res = int(str(Day1.find_first_and_last_number_V2(line)[0]) \
                           + str(Day1.find_first_and_last_number_V2(line)[1]))

            result += temp_res
            print(temp_res)

        return result

    @staticmethod
    def find_first_and_last_number(line: str):

        first_number = -1
        last_number = 0

        for char in line:
            if char in "0123456789":
                if first_number == -1:
                    first_number = int(char)

                last_number = int(char)

        return first_number, last_number

    @staticmethod
    def find_first_and_last_number_V2(line: str):

        first_number = -1
        last_number = 0

        for index, char in enumerate(line):
            if char in "0123456789":
                if first_number == -1:
                    first_number = int(char)

                last_number = int(char)

            for digit in digits_in_letters:
                if index+len(digit)<=len(line):
                    if line[index:index+len(digit)] == digit:
                        if first_number == -1:
                            first_number = Day1.find_num_value_from_list_digits_in_letters(digit)

                        last_number = Day1.find_num_value_from_list_digits_in_letters(digit)

        return first_number, last_number

    @staticmethod
    def find_num_value_from_list_digits_in_letters(digit_in_letter: str):
        for index, digit in enumerate(digits_in_letters):
            if digit == digit_in_letter:
                return index + 1


if __name__ == "__main__":
    print("main instance is running...")

    day1 = Day1(puzzle_input)

    print(f"result step1 : {day1.step1()}")
    print(f"result step2 : {day1.step2()}")




