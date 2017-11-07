import database
import gamemaker
import team

class Escavenge():

  def __init__(self):
    self.database = database.Database()
    self.gameMaker = gamemaker.GameMaker(database)
    self.user = team.Team(database)
    maker = {}
    team = {}

    maker["logout"] = lambda: self.gameMaker.logout()
    team["logout"] = lambda: self.user.logout()

  def login(self,username, password):
      if(username is "maker"):
          self.gameMaker.login(username, password)
      else:
          self.user.login(username, password)

  def main(self):

    print("Welcome to Escavenge!\n")
    while(True):
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")

        if(self.login(username, password)):
            if(database.get_current_user() is "maker"):
                cmd = input(self.gameMaker.display_menu())
                self.maker[cmd]
            else:
                cmd = input(team.display_menu())
                self.team[cmd]


