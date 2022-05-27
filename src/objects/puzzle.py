import json
import random

import numpy as np
import pandas as pd

from tiles import Floor, Wall, Spikes, Start, Goal

layout_list = ["Start", "Goal", "Floor", "Wall", "Spikes", "Orb"]
layout_dict = dict([(obj, i) for obj, i in zip(layout_list, range(len(layout_list)))])

symbol_dict = {"s": "Start",
               "g": "Goal",
               "_": "Floor",
               "#": "Wall",
               "x": "Spikes",
               "o": "Orb"}

class Puzzle:
    def __init__(self):
        self.layout = None
        self.tiles = None
        self.tile_data = None
        self.objects = None

    def load_tile_data(self, filepath):
        self.tile_data = pd.read_csv(filepath)

    @staticmethod
    def get_tile(tile_name):
        if tile_name == "Floor":
            return Floor()

        if tile_name == "Wall":
            return Wall()

        if tile_name == "Spikes":
            return Spikes()

        return None

    def load_from_json(self, filepath):
        pass

    def load_from_text(self, filepath):
        # Open text file as list of strings
        with open(filepath) as f:
            text = f.readlines()

            # Remove trailing newlines
            text = [t.rstrip() for t in text]

            h_size = len(text[0])

            if not all(len(t) == h_size for t in text[1:]):
                raise Exception("All lines in text file must have the same length (excluding trailing newlines).")

            # Convert text characters to layout objects, then to layout ids, and set puzzle layout
            layout = np.array([[self.tile_data.tile[self.tile_data.symbols == sym].values[0] for sym in t] for t in text])

        # Close file
        f.close()

        return

    def write_to_json(self, filepath):
        pass

    def write_to_text(self, filepath):
        with open(filepath, 'a') as f:
            for row in self.layout:
                f.write("".join([self.get_key_from_val(self.get_key_from_val(i, layout_dict), symbol_dict) for i in row] + ['\n']))

    def print(self):
        for row in self.layout:
            print(" ".join([self.get_key_from_val(self.get_key_from_val(i, layout_dict), symbol_dict) for i in row]))

    @staticmethod
    def get_key_from_val(val, dict):
        for k, v in dict.items():
            if v == val:
                return k

        return None

    @staticmethod
    def manhattan_distance(loc_1, loc_2):
        if loc_1 is None or loc_2 is None:
            return np.inf

        # Return sum of absolute differences of Cartesian coordinates
        return np.sum([np.abs(l1 - l2) for l1, l2 in zip(loc_1, loc_2)])

    def get_tiles(self):
        pass


def main():
    puzzle = Puzzle()
    puzzle.load_tile_data("C:/Users/nicho/PycharmProjects/ProceduralPuzzle/src/utils/tile_data.csv")
    puzzle.load_from_text("C:/Users/nicho/PycharmProjects/ProceduralPuzzle/src/puzzles/test_puzzle")

    pass

if __name__ == "__main__":
    main()