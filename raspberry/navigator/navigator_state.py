from abc import ABC, abstractmethod

class NavigatorState(ABC): 
    _context = None

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, context) -> None:
        self._context = context

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass
    
    @abstractmethod
    def stop(self) -> None:
        pass