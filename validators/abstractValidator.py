class AbstractValidator():
    
    @staticmethod
    def validValue(value):
        pass
    
    @staticmethod
    def getErrorMessage():
        pass

def validateAndRaiseException(value, validator: AbstractValidator):
    if not validator.validValue(value):
        raise ValueError(validator.getErrorMessage())