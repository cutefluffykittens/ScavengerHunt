class GameMaker:
    def __init__(self, database):
        self.database = database

    def login(self, name, password):
        returnValue = False
        current_user = self.database.get_current_user()
        maker_cred = self.database.get_game_maker_cred()
        if current_user == None:
            if maker_cred["maker"] == "maker" and maker_cred["password"] == password:
                self.database.set_current_user(self)
                returnValue = True
        return returnValue

    def check_status(self):
        dict = self.database.teams.keys():
        if len(dict) == 0:
            return "No teams!"
        else:
            return ' '.join(dict)
        
    def logout(self):
        returnValue = False
        current_user = self.database.get_current_user()
        if "maker" in current_user:
            self.database.set_current_user(None)
            returnValue = True
        return returnValue
