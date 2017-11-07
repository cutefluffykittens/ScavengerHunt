class GameMaker:
    def __init__(self, database):
        self.database = database

    def login(self, name, password):
        return_value = False
        current_user = self.database.get_current_user()
        maker_cred = self.database.get_game_maker_cred()
        if current_user is None:
            if maker_cred["maker"] == "maker" and maker_cred["password"] == password:
                self.database.set_current_user(self)
                return_value = True
        return return_value

    def check_status(self):
        string = ''
        teams = self.database.get_teams()
        if len(teams) > 0:
            for team in teams:
                string += team.user_name + ' is at ' + team.landmark + ' with ' + team.penalties + ' penalties\n'
        else:
            string = 'No teams!'
        return string
        
    def logout(self):
        return_value = False
        current_user = self.database.get_current_user()
        if "maker" in current_user:
            self.database.set_current_user(None)
            return_value = True
        return return_value
