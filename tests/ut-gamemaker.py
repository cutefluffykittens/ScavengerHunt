import unittest
import gamemaker
import database

class TestLogin(unittest.TestCase):
  def setUp(self):
    self.database = database.Database()
    self.maker1 = gamemaker.GameMaker()
  
  def test_makerLogin(self):
     assertEquals(self.maker1.login("Notvalidusername","Notvalidpassword"), false, "test_makerLogin should not have logged in"))
     assertEquals(self.database.curUser, null, "Current user is not null") //Make sure null is starting value!
     assertEquals(self.maker1.login("maker","password"), true, "test_makerLogin should have logged in")
     assertEquals(self.database.curUser, "maker", "Current user is not maker") //Make sure maker is what we will name it!
    
  def test_makerCheckStatus(self):
     assertEquals(self.database.get_teams, null, "Get status is not null with an empty list of teams")
     self.database.add_teams("Team1")
     assertEquals(self.database.get_teams, "Team1", "Get status is not Team1 when there is only Team1 in the list")
     self.database.add_teams("team2")
     assertEquals(self.database.get_teams, "Team1, team2", "Get status does not return Team1 and team2")
  
  def test_makerLogout(self):
    maker1.logout()
    assertEquals(self.database.curUser, null, "Current user is not null after logging out")
     
