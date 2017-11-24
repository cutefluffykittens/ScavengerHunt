import team

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
        return "Options\n\nmake team\n\nlog out\ndisplay status\n"

    def make_team(self, input):
        input = input.split(" ")
        if len(input) == 2:
            name = input[0]
            password = input[1]
            self.database.add_team(team.Team(name, password, self.database))
            ret_string = "Added " + name
        else:
            ret_string = "Invalid input!"
        return ret_string

    def edit_team(self, input):
        found = False
        input = input.split(" ")
        if len(input) == 3:
            list = self.database.get_teams()
            for teams in list:
                if teams.username == input[0]:
                    found = True
                    teams.username = input[1]
                    teams.password = input[2]
                    ret_string = "" + input[0] + " changed to " + input[1] + " with password " + input[2]
        else:
            ret_string = "Invalid input!"
            found = True
        if not found:
            ret_string = "Could not find that team!"
        return ret_string

    def set_penalties(self, input):
        exception = False
        input = input.split(" ")
        if len(input) == 2:
            try:
                time = int(input[0])
                guess = int(input[1])
            except ValueError:
                exception = True
            if not exception and time > 0 and guess > 0:
                self.database.time_penalty = time
                self.database.guess_penalty = guess
                ret_string = "Time penalty is " + input[0] + " minutes and guess penalty is " + input[1] + " guesses"
            else:
                ret_string = "Invalid input! Need integers greater than 0"
        else:
            ret_string = "Bad spacing! Need one space between time penalty and guess penalty"
        return ret_string
