import database
import gamemaker
import team


class Escavenge():
    def __init__(self):
        self.database = database.Database()
        self.game_maker = gamemaker.GameMaker(self.database)

        self.test = {"test":"test"}

        self.maker = {
            "log out": lambda: self.game_maker.logout(),
            "login": lambda: self.main,
            "display status": lambda: print(self.game_maker.display_status()),
            "help": lambda: print(self.game_maker.display_menu())
        }

        self.team = {
            "log out": lambda team: team.logout(),
            "display status": lambda team: print(team.display_status()),
            "help": lambda team: print(team.display_menu())
        }

        # Hard-coding this for now until we have this functionality:

        self.database.add_team(team.Team("team1", "password1", self.database))
        self.database.add_team(team.Team("team2", "password2", self.database))

    def login(self, username, password):
        if (username == "maker"):
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
        while(cmd != "log out"):
            cmd = input("What would you like to do (type \"help\" to display menu): ")
            try:
                self.maker[cmd]()
            except KeyError:
                print("That is not a valid command.")
        self.main()

    def team_cmd(self):
        team = self.database.get_current_user()
        cmd = None
        while cmd != "log out":
            cmd = input("What would you like to do (type \"help\" to display menu): ")
            try:
                self.team[cmd](team)
            except KeyError:
                print("That is not a valid command.")
        self.main()

    def main(self):

        print("Welcome to Escavenge!\n")

        while (True):

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
