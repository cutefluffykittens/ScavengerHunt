import unittest
import gamemaker
import database
import team
import user

class TestMakerLogin(unittest.TestCase):
  def setUp(self):
    self.database = database.Database()
    self.maker1 = gamemaker.GameMaker()
  
  def test_BadLogin(self):
     self.assertEquals(self.maker1.login("Notvalidusername","Notvalidpassword"), "Bad username or password!", "Bad response to invalid login")
     self.assertEquals(self.database.curUser, null, "Current user is not null") //Make sure null is starting value!
  def test_GoodLogin(self):
     self.assertEquals(self.maker1.login("maker","password"), "User maker logged in!", "Maker should have logged in")
     self.assertEquals(self.database.curUser, "maker", "Current user should be maker")
  def test_GoodLoginWhileLoggedIn(self):
    self.maker1.login("maker","password")
     self.assertEquals(self.maker1.login("maker","password"), "Maker already logged in!", "Bad response to second login attempt")
      
  class TestMakerLogout(unittest.TestCase):
    def setUp(self):
      self.database = database.Database()
      self.maker1 = gamemaker.GameMaker()
    
    def test_LogoutWhileNotLoggedIn(self):
      self.assertEquals(self.maker1.logout(), "maker is not logged in!", "Bad response to maker logging out while not logged in")
    def test_GoodLogout(self):
      self.maker1.login()
      self.assertEquals(self.maker1.logout(), "maker logged out!", "Bad response to maker logging out correctly")
    def test_CurrentUserIsNotMaker(self):
      self.maker1.login("maker","password")
      self.maker1.logout("maker")
      self.assertEquals(self.database.curUser, null, "Current user is not null after logging out")
      
 class TestMakerCheckStatus(unittest.TestCase):
  def setUp(self):
    self.database = database.Database()
    self.maker1 = gamemaker.GameMaker()
    
  def test_SingleTeam(self)
    self.team1 = team.Team("Team1")
    self.assertEquals(self.maker1.checkStatus(), "Team1", "Status incorrect for single team existing")
  
  def test_TwoTeams(self)
    self.team1 = team.Team("Team1")
    self.team2 = team.Team("team2")
    self.assertEquals(self.maker1.checkStatus(), "Team1, team2", "Status incorrect for two teams existing")
    
  def test_ThreeTeams(self)
    self.team1 = team.Team("Team1")
    self.team2 = team.Team("team2")
    self.team3 = team.Team("thirdteam")
    self.assertEquals("self.maker1.checkStatus(), "Team1, team2, thirdteam", "Status incorrect for three teams existing")
     
suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestMakerLogin))
suite.addTest(unittest.makeSuite(TestMakerLogout))
suite.addTest(unittest.makeSuite(TestMakerCheckStatus))

runner = unittest.TextTestRunner()
res=runner.run(suite)
print(res)
print("*"*20)
for i in res.failures: print(i[1])
