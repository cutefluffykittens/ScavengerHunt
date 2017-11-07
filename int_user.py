from abc import ABCMeta, abstractmethod

class User(ABCMeta):
    @abstractmethod
    def login(self, database, username, password):
        pass
    @abstractmethod
    def logout(self, database):
        pass
    @abstractmethod
    def display_menu(self):
        pass