import database
import gamemaker
import team


class Escavenge():
    def __init__(self):
        self.database = database.Database()
        self.game_maker = gamemaker.GameMaker(self.database)

        self.maker = {
            "logout": lambda params: self.game_maker.logout(),
            "login": lambda params: self.main,
            "displaystatus": lambda params: print(self.game_maker.display_status()),
            "help": lambda params: print(self.game_maker.display_menu()),
            "maketeam": lambda params: self.game_maker.make_team(params),
            "editteam": lambda params: self.game_maker.edit_team(params),
            "setpenalties": lambda params: self.game_maker.set_penalties(params),
            "addlandmark": lambda params: print(self.game_maker.add_landmark(params)),
            "displaylandmarks": lambda params: print(self.game_maker.display_landmarks()),
            "removelandmark": lambda params: print(self.game_maker.remove_landmark(params)),
            "startgame": lambda params: print(self.game_maker.start_game()),
            "endgame": lambda params: print(self.game_maker.end_game())
        }

        self.team = {
            "logout": lambda team, params: team.logout(),
            "displaystatus": lambda team, params: print(team.display_status()),
            "help": lambda team, params: print(team.display_menu()),
            "editusername" : lambda team, params: print(team.edit_username(params)),
            "editpassword" : lambda team, params: print(team.edit_password(params)),
            "answer" : lambda team, params: print(team.answer_question(params))
        }

        # Hard-coding this for now until we have this functionality:

        self.database.add_team(team.Team("team1", "password1", self.database))
        self.database.add_team(team.Team("team2", "password2", self.database))

    def login(self, username, password):
        if username == "maker":
            return self.game_maker.login(username, password)
        else:
            teams = self.database.get_teams()
            for team in teams:
                if team.username == username:
                    return team.login(username, password)
            print("There is no such user. Please create a new team")
            return False

    def maker_cmd(self):
        cmd = None
        while cmd != "logout":
            cmd = input("What would you like to do (type \"help\" to display menu): ")
            try:
                cmd = cmd.lower()
                params = cmd.split(", ")
                cmd = cmd.split(" ")[0]
                if len(cmd.split(" ")) > 1:
                    params[0] = cmd.split(" ")[1]
                self.maker[cmd](params)
            except KeyError:
                print("That is not a valid command.")
        self.main()

    def team_cmd(self):
        team = self.database.get_current_user()
        cmd = None
        while cmd != "logout":
            cmd = input("What would you like to do (type \"help\" to display menu): ")
            try:
                cmd = cmd.lower()
                params = cmd.split(", ")
                cmd = cmd.split(" ")[0]
                if len(cmd.split(" ")) > 1:
                    params[0] = cmd.split(" ")[1]
                self.team[cmd](team, params)
            except KeyError:
                print("That is not a valid command.")
        self.main()

    def main(self):

        print("Welcome to Escavenge!\n")

        while True:

            username = input("Please enter your username: ")
            password = input("Please enter your password: ")

            if self.login(username, password):
                if isinstance(self.database.get_current_user(), gamemaker.GameMaker):
                    print("Logged in as gamemaker!")
                    self.maker_cmd()

                else:
                    print("Log in as " + self.database.get_current_user().username + " successful!")
                    self.team_cmd()
            else:
                print("Invalid username and password. Please try again!")


if __name__ == '__main__':
    Escavenge().main()
