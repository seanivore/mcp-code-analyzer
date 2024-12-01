import os
from datetime import datetime

class TestClass:
    def __init__(self, name: str):
        self.name = name
        self.value = 0
        
    def complex_method(self, x: int) -> bool:
        result = False
        counter = 0
        
        if x > 0:
            if self.value > 10:
                result = True
            elif self.value < -10:
                result = False
            else:
                for i in range(x):
                    counter += i
                    if counter > 100:
                        break
                result = counter > 50
                
        while self.value > 0 and not result:
            self.value -= 1
            
        return result

def simple_function():
    return True