import database
import gamemaker

class Escavenge():
  user = ""
  password = ""
  cmd = ""
  response = ""

  def __init__(self):
    self.db = database.Database()
    self.gameMaker = gamemaker.GameMaker()
  
  def login(self):
    pass


    
