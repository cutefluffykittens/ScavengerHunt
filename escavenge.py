import database
import gamemaker
import team

class Escavenge():

  def __init__(self):
    self.database = database.Database()
    self.game_maker = gamemaker.GameMaker(database)
    self.team
    maker = {}
    user = {}

    maker["logout"] = lambda: self.game_maker.logout()

  def login(self,username, password):
      if(username is "maker"):
          return self.game_maker.login(username, password)
      else:
          teams = database.get_teams()
          for team in teams:
             if(team.username is username):
                 #this is gross. Any better way?
                 self.team = team
                 return team.login()

  def main(self):

    print("Welcome to Escavenge!\n")

    while(True):

        username = input("Please enter your username: ")
        password = input("Please enter your password: ")

        if(self.login(username, password)):
            if(database.get_current_user() is "maker"):
                print("Log in as game maker successful!")
                cmd = input(self.game_maker.display_menu())
                self.maker[cmd]
            else:
                print("Log in as " + database.get_current_user() + " successful!")
                cmd = input(team.display_menu())
                self.user[cmd]


    if __name__ == '__main__':
        self.main()