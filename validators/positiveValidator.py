from validators.abstractValidator import AbstractValidator
    
class PositiveValidator(AbstractValidator):
    minValue = 0

    @classmethod
    def validValue(cls, value: int):
        return value > 0 

    @classmethod
    def getErrorMessage(cls):
        return "Value must be higher than {0}".format(cls.minValue) 