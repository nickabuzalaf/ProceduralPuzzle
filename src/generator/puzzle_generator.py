import random
import numpy as np
from objects.puzzle import Puzzle

layout_list = ["Start", "Goal", "Floor", "Wall", "Spikes"]
layout_dict = dict([(obj, i) for obj, i in zip(layout_list, range(len(layout_list)))])

symbol_dict = {"s": "Start",
               "g": "Goal",
               "_": "Floor",
               "#": "Wall",
               "x": "Spikes"}


class PuzzleGenerator(Puzzle):
    def empty(self, size):
        # Check if size is not an iterable type
        if type(size) != list and type(size) != tuple:
            size = (size,)

        # Error handling for wrong input shape
        if len(size) > 2:
            raise Exception("Parameter 'size' should have a shape of length 1 (for a square) or 2.")

        # Error handling if shape is too small
        if True in [i < 3 for i in size]:
            raise Exception("All values of parameter 'size' should be 3 or greater.")

        # Make one element tuple into two element tuple
        if len(size) == 1:
            size = (size[0], size[0])

        # Create layout with walls around outsize and floor elsewhere
        self.layout = np.full([s - 2 for s in size], layout_dict["Floor"], dtype=int)
        self.layout = np.pad(self.layout, (1,1), constant_values=layout_dict["Wall"])

    def set_start_and_goal(self, start_location=None, start_side=None, goal_location=None, goal_side=None):
        # Error handling for start-goal distance restriction
        if self.manhattan_distance(start_location, goal_location) <= 2:
            raise Exception('Start and goal locations must have Manhattan Distance greater than 2.')

        # Get valid edges based on specified side
        valid_sides_dict = {"top": [[0, i] for i in range(1, self.layout.shape[0] - 1)],
                            "bottom": [[self.layout.shape[0] - 1, i] for i in range(1, self.layout.shape[0] - 1)],
                            "left": [[i, 0] for i in range(1, self.layout.shape[1] - 1)],
                            "right": [[i, self.layout.shape[1] - 1] for i in range(1, self.layout.shape[1] - 1)]}

        # Error handling for invalid inputs for start_side and goal_side
        if not all(elem in list(valid_sides_dict.keys()) + [None] for elem in [start_side, goal_side]):
            raise Exception("start_side and goal_side must be one of: 'top', 'bottom', 'left', 'right', or None.")

        # Get all valid edges for all sides
        valid_edges = np.array(sum(list(valid_sides_dict.values()), []))

        if not all(elem in valid_edges for elem in list(filter(None, [start_location, goal_location]))):
            raise Exception("start_location and goal_location must be on outer edge if specified.")

        # If specific goal location or side is set and start location and side are not set, set goal location first
        if not (start_location or start_side) and (goal_location or goal_side):
            # Set goal location if not already set
            if not goal_location:
                goal_location = random.choice(valid_sides_dict[goal_side])

            # Update valid edges based on start-goal distance restriction
            valid_edges = valid_edges[np.array([self.manhattan_distance(goal_location, v_e) for v_e in valid_edges]) > 2]
            valid_sides_dict = dict(
                [(key, [v for v in val if v in valid_edges]) for key, val in valid_sides_dict.items()])

            # Set start location
            start_location = random.choice(valid_sides_dict[start_side]) if start_side else random.choice(valid_edges)

            # Update start and goal positions
            self.layout[start_location[0]][start_location[1]] = layout_dict["Start"]
            self.layout[goal_location[0]][goal_location[1]] = layout_dict["Goal"]

            return

        # Set start location
        if not start_location:
            start_location = random.choice(valid_sides_dict[start_side]) if start_side else random.choice(valid_edges)

        # Update valid edges based on start-goal distance restriction
        valid_edges = valid_edges[np.array([self.manhattan_distance(start_location, v_e) for v_e in valid_edges]) > 2]
        valid_sides_dict = dict([(key, [v for v in val if v in valid_edges]) for key, val in valid_sides_dict.items()])

        # Set goal location
        if not goal_location:
            goal_location = random.choice(valid_sides_dict[goal_side]) if goal_side else random.choice(valid_edges)

        # Update start and goal positions
        self.layout[start_location[0]][start_location[1]] = layout_dict["Start"]
        self.layout[goal_location[0]][goal_location[1]] = layout_dict["Goal"]

        return

    def wfc(self):
        pass

if __name__ == "__main__":
    empty_puzzle = PuzzleGenerator()
    empty_puzzle.empty(10)
    empty_puzzle.set_start_and_goal()
    empty_puzzle.print()

    pass