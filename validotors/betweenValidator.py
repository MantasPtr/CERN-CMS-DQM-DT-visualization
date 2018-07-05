from validotors.abstractValidator import AbstractValidator

class BetweenValidator(AbstractValidator):
    def __init__(self):
        self.min = 0
        self.max = 100

    def validate(self, value: int):
        return self.min <= value <= self.max

    def getErrorMessage(self):
        return "Value must be between {0} and {1} (inclusively)".format(self.min, self.max) 