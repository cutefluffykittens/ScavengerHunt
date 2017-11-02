import database.py
import gamemaker.py

class main():
  
  def __init__(self):
    self.db = database.Database()
    self.gameMaker = gameMaker.GameMaker()
  
  def login(self):
    
