import database
import gamemaker
import team


class Escavenge():
    def __init__(self):
        self.database = database.Database()
        self.game_maker = gamemaker.GameMaker(database)

        self.maker = {
            "logout": self.game_maker.logout(),
            "login": self.main(),
            "display status": self.game_maker.display_status()
        }

        self.user = {
            "logout": team.logout(database),
            "display status": team.display_status()
        }

    def login(self, username, password):
        if (username is "maker"):
            return self.game_maker.login(username, password)
        else:
            teams = database.get_teams()
            for team in teams:
                if (team.username is username):
                    return team.login(database, username, password)
            print("There is no such user. Please create a new team")
            return False

    def maker_cmd(self):
        cmd = None
        while(cmd is not "logout"):
            cmd = input(self.game_maker.display_menu())
            self.maker[cmd]()
        self.main()

    def user_cmd(self):
        cmd = None
        while(cmd is not "logout"):
            cmd = input(team.display_menu())
            self.user[cmd]()
        self.main()

    def main(self):

        print("Welcome to Escavenge!\n")

        while (True):

            username = input("Please enter your username: ")
            password = input("Please enter your password: ")

            if (self.login(username, password)):
                if (database.get_current_user() is "maker"):
                    print("Log in as game maker successful!")
                    self.maker_cmd()

                else:
                    print("Log in as " + database.get_current_user() + " successful!")
                    self.user_cmd()
            else:
                print "Invalid username and password. Please try again!"


if __name__ == '__main__':
    Escavenge()
