class Team:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.eliminated = False
        self.victorious = False
        self.space = 0
        self.text = f"{self.name}: ${self.score}"

    def add(self):
        self.score += 100

    def sub(self):
        self.score -= 100

    def halve(self):
        self.score //= 2

    def double(self):
        self.score *= 2

    def move_space(self, step):
        self.space += step

    def reset(self):
        self.score = 0
        self.space = 1
        self.text = f"{self.name}: ${self.score}"
        self.eliminated = False
        self.victorious = False
