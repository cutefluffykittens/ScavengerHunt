class GameMaker:
    def __init__(self, database):
        self.database = database

    def login(self, name, password):
        return_value = False
        current_user = self.database.get_current_user()
        maker_cred = self.database.get_game_maker_cred()
        if current_user is None:
            if maker_cred["username"] == name and maker_cred["password"] == password:
                self.database.set_current_user(self)
                return_value = True
        return return_value

    def display_status(self):
        string = ''
        teams = self.database.get_teams()
        for team in teams:
            string += team.username + '\n' #+ ' is at ' + team.landmark + ' with ' + team.penalties + ' penalties\n'
        if string == '':
            string = 'No teams!'
        return string
        
    def logout(self):
        return_value = False
        current_user = self.database.get_current_user()
        if current_user is self:
            self.database.set_current_user(None)
            return_value = True
        return return_value

    def display_menu(self):
        return "Options\n\nlog out\ndisplay status\n"
