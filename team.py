import user

class Team(user.User):
    def __init__(self,n):
        self.name = n
        self.username = "team"
        self.password = "password"
    def setTeamName(self,n):
        pass
    def setTeamUserName(self,u):
        pass
    def setTeamPassword(self,p):
        pass
    def login(self,username,password):
        pass
    def logout(self):
        pass
