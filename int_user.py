import abc

class User(abc.ABC):
    @abc.abstractmethod
    def login(self, database, username, password):
        pass
    @abc.abstractmethod
    def logout(self, database):
        pass
    @abc.abstractmethod
    def display_menu(self):
        pass