class GameMaker:
  def __init__(self, database):
    self.database = database
  
  def login(self, name, password):
    returnValue = ""
    if (self.database.curUser != name && self.database.gameMakerCred = {name, password}):
      self.database.curUser = name
      returnValue = "User " + name + " logged in!"
    elif: (self.database.curUser == name) returnValue = "" + name + " already logged in!"
    else: returnValue = "Bad username or password!"
    
  def checkStatus(self):
    string = ' '.join(self.database.teams.keys())
    if (string == ''): return "No teams!"
    else: return string
  
  def logout(self):
    returnValue = ""
    if (self.database.curUser != "maker"): returnValue = "maker is not logged in!"
    else:
      self.database.curUser = null
      returnValue = "maker logged out!"
    return returnValue
