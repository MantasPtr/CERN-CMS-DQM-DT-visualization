class AbstractValidator():
    
    @staticmethod
    def validate(value):
        pass
    
    @staticmethod
    def getErrorMessage():
        pass

def validateAndRaiseException(value, validator: AbstractValidator):
    if not validator.validate(value):
        raise ValueError(validator.getErrorMessage)