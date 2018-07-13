from validators.abstractValidator import AbstractValidator

class BetweenValidator(AbstractValidator):
    minValue = 0
    maxValue = 100

    @classmethod
    def validValue(cls, value: int):
        return cls.minValue <= int(value) <= cls.maxValue

    @classmethod
    def getErrorMessage(cls, caller= None):
        if caller is None:
            caller = cls
        return "Value must be between {0} and {1} (inclusively)".format(caller.minValue, caller.maxValue) 