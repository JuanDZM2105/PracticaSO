import threading
from typing import Generic, TypeVar

T = TypeVar('T')

class GenProdCons(Generic[T]):
    def __init__(self, size: int = 10):
        if size <= 0:
            raise ValueError("El tamaño del buffer debe ser mayor a cero.")

        self.size = size
        self.buffer = []
        self.lock = threading.Lock()
        self.empty_slots = threading.Semaphore(size)  # Cuántos espacios libres hay
        self.full_slots = threading.Semaphore(0)      # Cuántos elementos disponibles hay

    def put(self, item: T):
        self.empty_slots.acquire()   # Espera espacio libre
        with self.lock:
            self.buffer.append(item)
        self.full_slots.release()    # Señala elemento disponible

    def get(self) -> T:
        self.full_slots.acquire()    # Espera elemento disponible
        with self.lock:
            item = self.buffer.pop(0)
        self.empty_slots.release()   # Señala espacio libre
        return item
    
    def __len__(self):
        with self.lock:
            return len(self.buffer)