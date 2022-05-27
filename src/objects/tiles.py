class Tile:
    def __init__(self, canOccupy, canRollOver, canThrowOver):
        self.canOccupy = canOccupy
        self.canRollOver = canRollOver
        self.canThrowOver = canThrowOver


class Floor(Tile):
    def __init__(self, isStart, isGoal):
        super().__init__(canOccupy=True, canRollOver=True, canThrowOver=True)
        self.isStart = isStart
        self.isGoal = isGoal


class Wall(Tile):
    def __init__(self):
        super().__init__(canOccupy=False, canRollOver=False, canThrowOver=False)


class Spikes(Tile):
    def __init__(self):
        super().__init__(canOccupy=False, canRollOver=False, canThrowOver=True)

class Start(Floor):
    pass

class Goal(Floor):
    pass