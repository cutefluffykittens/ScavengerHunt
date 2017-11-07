import user

class Team(user.User):
    def __init__(self,name):
        self.name = name
        self.username = "username"
        self.password = "password"
    def setTeamName(self,newName):
        self.name = newName
        return "Team name changed to " + newName
    def setTeamUserName(self,newUsername):
        self.username = newUsername
        return "Team username changed to " + newUsername
    def setTeamPassword(self,newPassword):
        self.password = newPassword
        return "Team password changed to " + newPassword
    def login(self,username,password):
        result = "Unable to log in"
        # TODO: if someone is already logged in, just return result
        if username == self.username and password == self.password:
            # TODO: set currentUser to this user
            result = self.name + " logged in"
        return result
    def logout(self):
        result = "Unable to log out"
        # TODO: if someone is not logged in, or if team trying to log out is not the team currently logged in, return result
        result = self.name + " logged out"
        return result
    def displayMenu(self):
        pass
