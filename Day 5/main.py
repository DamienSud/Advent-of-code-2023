from constants import almanac_entry

import re


class AlmanacMapStep:
    def __init__(self, brut_txt_map: str, step: int):
        self.step_id = step
        self.brut_map_step = brut_txt_map
        title_datas = self.extract_title()
        self.title, self.source, self.destination = title_datas
        self.maps = self.extract_maps()

    def extract_title(self):
        title = re.search(r'(([a-zA-Z]*)-to-([a-zA-Z]*))\smap:', self.brut_map_step)
        return title.group(1), title.group(2), title.group(3)

    def extract_maps(self):
        _, maps = self.brut_map_step.split(":\n")

        maps_as_list = []

        for map in maps.split("\n"):
            maps_as_list.append(map.split())

        return maps_as_list

    def get_destination(self):
        return self.destination

    def get_source(self):
        return self.source

    def convert(self, source_value: int):

        mapped = False
        value = -1

        for map in self.maps:
            maped_value_bounds = (int(map[1]), int(map[1]) + int(map[2]))
            corresponding_mapped_destination_bounds = (int(map[0]), int(map[0]) + int(map[2]))
            if maped_value_bounds[0] <= source_value <= maped_value_bounds[1]:
                value = corresponding_mapped_destination_bounds[0] + source_value - int(map[1])
                mapped = True

        if not mapped:
            value = source_value

        return value


class Almanac:
    def __init__(self, almanac_as_txt: str):
        self.brut_almanac = almanac_as_txt
        self.source = self._extract_seeds()
        self.destination = []
        self.map_step = self._extract_map_step()
        self.current_source = self.map_step[0].get_source()
        self.current_destination = self.map_step[0].get_destination()

        # break point spawner
        pass

    def _extract_seeds(self):
        seeds_line = re.search(r'seeds:( \d+)*', self.brut_almanac).group(0)

        seed_values = seeds_line.split(":")[1]

        return [seed for seed in seed_values.split()]

    def _extract_map_step(self):
        map_title_regex = r'\n[a-zA-Z]+-to-[a-zA-Z]+\smap:\n'

        map_step_title = [map_title for map_title in re.findall(map_title_regex, self.brut_almanac)]

        maps_step_title_pos = [len(self.brut_almanac)]

        # find starting position of every maps
        for map_title in map_step_title:
            maps_step_title_pos.insert(-1, self.brut_almanac.find(map_title))

        map_category = []

        # give corresponding brut text to every almanac's map objects
        for index, map_title in enumerate(map_step_title):
            map_category.append(AlmanacMapStep(self.brut_almanac[maps_step_title_pos[index]:
                                                                 maps_step_title_pos[index + 1]].strip(),
                                               step=index))
        return map_category

    def convert_source_to_destination(self):

        for source in self.source:
            source = int(source)
            for map_step in self.map_step:
                if map_step.get_source() == self.current_source:
                    self.destination.append(str(map_step.convert(source)))
                    break

        self.source = self.destination.copy()
        self.destination.clear()

        self.roll_to_next_source_and_destination()

    def roll_to_next_source_and_destination(self):

        self.current_source = self.current_destination

        for map_step in self.map_step:
            if map_step.get_source() == self.current_source:
                self.current_destination = map_step.get_destination()

    def get_current_source(self):
        return self.current_source

    def get_current_destination(self):
        return self.current_destination

    def get_sources(self):
        return self.source


class Day5:
    def __init__(self, almanac: Almanac):
        self.almanac = almanac

    def step1(self):
        while almanac.get_current_source() != 'location':
            self.almanac.convert_source_to_destination()

        return min(map(int, almanac.get_sources()))

    def step2(self):
        pass


if __name__ == "__main__":
    print("main instance is running...")

    almanac = Almanac(almanac_entry)

    day5 = Day5(almanac)

    print(f"step1 result : {day5.step1()}")
    # print(f"step2 result : {day5.step2()}")
