class GameMaker:
  def __init__(self, database):
    self.database = database
  
  def login(self, name, password):
    returnValue = ""
    if (self.database.curUser != name && self.database.gameMakerCred = {name, password}):
      self.database.curUser = name
      returnValue = "User " + name + " logged in!"
    else if (self.database.curUser == name) returnValue = "" + name + " already logged in!"
    else returnValue = "Bad username or password!"
      
  //TODO Implement checkStatus
  def checkStatus(self):
    
  def logout(self):
    returnValue = ""
    if (self.database.curUser != "maker") returnValue = "maker is not logged in!"
    else {
      self.database.curUser = null
      returnValue = "maker logged out!"
    return returnValue
