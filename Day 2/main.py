from constants import game_list
import re


class Draw:
    def __init__(self):
        self.cubes = {}

    def add_cube(self, cube_qtt: int, cube_color: str):
        self.cubes[cube_color] = cube_qtt

    def __str__(self):
        desc = ""
        for index, cube, qtt in enumerate(self.cubes.items()):
            desc += f"{qtt} {cube} {',' if index < len(self.cubes) else ''}"

        return desc


class Game:
    def __init__(self, id: int):
        self.id = id
        self.draws = []

    def add_round(self, draw: Draw):
        self.draws.append(draw)

    def rounds(self):
        for draw in self.draws:
            yield draw

    def __str__(self):
        desc = f"Game {id}: "

        for index, draw in enumerate(self.draws):
            desc += draw + (";" if index < len(self.draws) else "")

        return desc


class Day2:
    def __init__(self, game_list : list):
        self.game_list = game_list

    def step1(self, red_limit: int, green_limit: int, blue_limit: int):

        total_score = 0

        for game in self.game_list:
            valid_game = True

            for draw in game.rounds():
                if draw.cubes["red"] > red_limit or draw.cubes["green"] > green_limit or \
                   draw.cubes["blue"] > blue_limit:
                    valid_game = False
                    break

            if valid_game:
                total_score += game.id

        return total_score

    def step2(self):
        total_score = 0

        for game in self.game_list:

            max_red = 0
            max_green = 0
            max_blue = 0

            for draw in game.rounds():
                if draw.cubes["red"] > max_red:
                    max_red = draw.cubes["red"]
                if draw.cubes["green"] > max_green:
                    max_green = draw.cubes["green"]
                if draw.cubes["blue"] > max_blue:
                    max_blue = draw.cubes["blue"]

            total_score += max_red * max_green * max_blue

        return total_score

    @staticmethod
    def get_game_list_from_information_recorded_as_str(record: str):
        game_list = []

        for line in record.split("\n"):
            game, draws = line.split(":")

            game_id = int(re.search(r"Game (\d*)", game).group(1))

            game = Game(game_id)

            for draw in draws.split(";"):
                new_draw = Draw()

                qtts = {
                    "red" : re.search(r"(\d*) red", draw),
                    "blue" : re.search(r"(\d*) blue", draw),
                    "green" : re.search(r"(\d*) green", draw)
                }

                for color in qtts:
                    if qtts[color] is not None:
                        new_draw.add_cube(int(qtts[color].group(1)), color)
                    else:
                        new_draw.add_cube(0, color)

                game.add_round(new_draw)

            game_list.append(game)

        return game_list


if __name__ == "__main__":
    print(f"main instance is running...")

    day2 = Day2(Day2.get_game_list_from_information_recorded_as_str(game_list))

    print(f"step1 result : {day2.step1(12, 13, 14)}")
    print(f"step2 result : {day2.step2()}")