from abc import ABC, abstractmethod

class User(ABC):
    @abstractmethod
    def login(self, database, username, password):
        pass
    @abstractmethod
    def logout(self, database):
        pass
    @abstractmethod
    def display_menu(self):
        pass