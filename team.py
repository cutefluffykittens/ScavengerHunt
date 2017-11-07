import int_user

class Team(int_user.User):
    def __init__(self,name,username,password):
        self.name = name
        self.username = username
        self.password = password
    def set_team_name(self,new_name):
        self.name = new_name
        return "Team name changed to " + new_name
    def set_team_username(self,new_username):
        self.username = new_username
        return "Team username changed to " + new_username
    def set_team_password(self,new_password):
        self.password = new_password
        return "Team password changed to " + new_password
    def login(self,database,username,password):
        result = "Unable to log in"
        if database.current_user != self:
            return result
        if username == self.username and password == self.password:
            database.current_user = self
            result = self.name + " logged in"
        return result
    def logout(self,database):
        result = "Unable to log out"
        database.current_user = None
        result = self.name + " logged out"
        return result
    def display_menu(self):
        pass
