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
        return "Options\n\nmaketeam [team name] [team password]\n" \
               "editteam [team name to edit] [new team name] [new team password]\nlogout\ndisplaystatus\n"

    def make_team(self, input):
        if len(input) == 3:
            name = input[1]
            password = input[2]
            self.database.add_team(team.Team(name, password, self.database))
            ret_string = "Added " + name
        else:
            ret_string = "Invalid input!"
        return ret_string

    def edit_team(self, input):
        found = False
        if len(input) == 4:
            list = self.database.get_teams()
            for team in list:
                if team.username == input[1]:
                    found = True
                    team.username = input[2]
                    team.password = input[3]
                    ret_string = "" + input[1] + " changed to " + input[2] + " with password " + input[3]
        else:
            ret_string = "Invalid input!"
            found = True
        if not found:
            ret_string = "Could not find that team!"
        return ret_string

    def set_penalties(self, input):
        exception = False
        if len(input) == 3:
            try:
                time = int(input[1])
                guess = int(input[2])
            except ValueError:
                ret_string = "Invalid input! Need an integer."
                exception = True
            if not exception and time > 0 and guess > 0:
                self.database.set_time_penalty(time)
                self.database.set_guess_penalty(guess)
                ret_string = "Time penalty is " + input[1] + " minutes and guess penalty is " + input[2] + " guesses"
            elif not exception:
                ret_string = "Invalid input! Need integers greater than 0"
        else:
            ret_string = "Bad spacing! Need one space between time penalty and guess penalty"
        return ret_string
