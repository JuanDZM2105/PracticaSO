from typing import TypeVar, Generic
import threading

E = TypeVar('E')
T = TypeVar('T')

class RendezvousDEchange(Generic[E, T]):
    def __init__(self):
        self.condition = threading.Condition()
        self.value: E | None = None
        self.has_value = False

    def echanger(self, value: E) -> T:
        with self.condition:
            if not self.has_value:
                self.value = value
                self.has_value = True
                self.condition.wait()
                result = self.value
                self.has_value = False
                self.condition.notify()
                return result
            else:
                temp = self.value
                self.value = value
                self.condition.notify()
                self.condition.wait()
                return temp  # tipo T