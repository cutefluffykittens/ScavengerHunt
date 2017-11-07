import database
import gamemaker
import team

class Escavenge():

  def __init__(self):
    self.database = database.Database()
    self.game_maker = gamemaker.GameMaker(database)
    self.team = team.Team(database)
    maker = {}
    user = {}

    maker["logout"] = lambda: self.game_maker.logout()
    user["logout"] = lambda: self.team.logout()

  def login(self,username, password):
      if(username is "maker"):
          print(self.game_maker.login(username, password))
          return True
      else:
          print(self.team.login(username, password))
          return True

  def main(self):

    print("Welcome to Escavenge!\n")
    while(True):
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")

        if(self.login(username, password)):
            if(database.get_current_user() is "maker"):
                cmd = input(self.game_maker.display_menu())
                self.maker[cmd]
            else:
                cmd = input(team.display_menu())
                self.user[cmd]


