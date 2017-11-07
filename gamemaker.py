class GameMaker:
    def __init__(self, database):
        self.database = database

    def login(self, name, password):
        returnValue = ""
        current_user = self.database.get_current_user()
        maker_cred = self.database.get_game_maker_cred()
        if current_user != None and current_user.username != name:
            if name == "maker" and maker_cred["maker"] == password:
            self.database.curUser.name = name
            returnValue = "User " + name + " logged in!"
        elif self.database.curUser.name == name:
            returnValue = "" + name + " already logged in!"
        else:
            returnValue = "Bad username or password!"
        return returnValue

    def check_status(self):
        dict = self.database.teams.keys()
        if None in dict:
            return "No teams!"
        else:
            return dict

    def logout(self):
        returnValue = ""
        if self.database.curUser != "maker":
            returnValue = "maker is not logged in!"
        else:
            self.database.curUser = None
            returnValue = "maker logged out!"
        return returnValue
