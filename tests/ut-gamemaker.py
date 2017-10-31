import unittest
import gamemaker
import database

class TestMakerLogin(unittest.TestCase):
  def setUp(self):
    self.database = database.Database()
    self.maker1 = gamemaker.GameMaker()
  
  def test_makerLogin(self):
     self.assertEquals(self.maker1.login("Notvalidusername","Notvalidpassword"), false, "test_makerLogin should not have logged in"))
     self.assertEquals(self.database.curUser, null, "Current user is not null") //Make sure null is starting value!
     self.assertEquals(self.maker1.login("maker","password"), true, "test_makerLogin should have logged in")
     self.assertEquals(self.database.curUser, "maker", "Current user is not maker") //Make sure maker is what we will name it!
   
 class TestMakerCheckStatus(unittest.TestCase):
  def setUp(self):
    self.database = database.Database()
    self.maker1 = gamemaker.GameMaker()
    self.maker1.login("maker","password")
    
  def test_makerCheckStatus(self):
     self.assertEquals(self.database.get_teams, null, "Get status is not null with an empty list of teams")
     self.database.add_teams("Team1")
     self.assertEquals(self.database.get_teams, "Team1", "Get status is not Team1 when there is only Team1 in the list")
     self.database.add_teams("team2")
     self.assertEquals(self.database.get_teams, "Team1, team2", "Get status does not return Team1 and team2")
      
  class TestMakerLogout(unittest.TestCase):
    def setUp(self):
      self.database = database.Database()
      self.maker1 = gamemaker.GameMaker()
      self.maker1.login("maker","password")
    
    def test_makerLogout(self):
      self.maker1.logout()
      self.assertEquals(self.database.curUser, null, "Current user is not null after logging out")
     
