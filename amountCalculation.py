class AmountCalculation:
    def __init__(self):
        self.maxLenDict = {}

    def setValueMaxLength(self, key, value):
        # If the value length is less than the current value length, set the value length to the current value length.
        # If the key does not exist, create one and set the value to the length of the current value
        try:
            if self.maxLenDict[key] < len(value):
                self.maxLenDict[key] = len(value)
        except:
            self.maxLenDict[key] = len(value)