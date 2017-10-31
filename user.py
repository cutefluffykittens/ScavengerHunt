import abc

class User(abc.ABC):
    @abc.abstractmethod
    def login(username,password):
        pass
    @abc.abstractmethod
    def logout(self):
        pass
    @abc.abstractmethod
    def displayMenu(self):
        pass