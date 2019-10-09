class Listener:
    def __init__(self):
        self.count = 0

    def checkValue(self):
        return self.count

    def increment(self):
        self.count = self.count +1