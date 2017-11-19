#import int_user
import database

#class Team(int_user.User):
class Team():
    def __init__(self,username,password,database):
        self.username = username
        self.password = password
        self.database = database
    def set_team_username(self,new_username):
        self.username = new_username
        return "Team username changed to " + new_username
    def set_team_password(self,new_password):
        self.password = new_password
        return "Team password changed to " + new_password
    def login(self,username,password):
        if self.database.get_current_user() != None:
            return False
        if username == self.username and password == self.password:
            self.database.set_current_user(self)
            return True
        return False
    def logout(self):
        if self.database.get_current_user() is not self:
            return False
        self.database.set_current_user(None)
        return True
    def display_menu(self):
        return "Options\n\nlog out\ndisplay status\n"

    def display_status(self):
        return "Team: " + self.username

    def edit_username(self, username):
        return True

    def edit_password(self, password):
        return True