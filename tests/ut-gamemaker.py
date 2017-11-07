import unittest
import gamemaker
import database
import team
import user

class TestMakerLogin(unittest.TestCase):
  def set_up(self):
    self.database = database.Database()
    self.maker1 = gamemaker.GameMaker()
  
  def test_bad_login(self):
     self.assertEquals(self.maker1.login("Notvalidusername","Notvalidpassword"), "Bad username or password!", "Bad response to invalid login")
     self.assertEquals(self.database.curUser, None, "Current user is not null")
  def test_good_login(self):
     self.assertEquals(self.maker1.login("maker","password"), "User maker logged in!", "Maker should have logged in")
     self.assertEquals(self.database.curUser.name, "maker", "Current user should be maker")
  def test_good_login_while_logged_in(self):
    self.maker1.login("maker","password")
    self.assertEquals(self.maker1.login("maker","password"), "Maker already logged in!", "Bad response to second login attempt")
      
  class TestMakerLogout(unittest.TestCase):
    def set_up(self):
      self.database = database.Database()
      self.maker1 = gamemaker.GameMaker()
    
    def test_logout_while_not_logged_in(self):
      self.assertEquals(self.maker1.logout(), "maker is not logged in!", "Bad response to maker logging out while not logged in")
    def test_good_logout(self):
      self.maker1.login()
      self.assertEquals(self.maker1.logout(), "maker logged out!", "Bad response to maker logging out correctly")
    def test_current_user_is_not_maker(self):
      self.maker1.login("maker","password")
      self.maker1.logout("maker")
      self.assertEquals(self.database.curUser, None, "Current user is not null after logging out")
      
 class TestMakerCheckStatus(unittest.TestCase):
  def set_up(self):
    self.database = database.Database()
    self.maker1 = gamemaker.GameMaker()
    
  def test_empty_team(self):
    self.assertEquals(self.maker1.check_status(), "No teams!", "CheckStatus did not return proper response to empty team list")
    
  def test_single_team(self):
    self.team1 = team.Team("Team1")
    dict = self.maker1.check_status()
    self.assertEquals("Team1" in dict, True, "Status incorrect for single team existing")
  
  def test_multiple_teams(self):
    self.team1 = team.Team("Team1")
    self.team2 = team.Team("team2")
    dict = self.maker1.check_status()
    self.assertEquals("Team1" in dict, True, "Cannot find first entry in two team list")
    self.assertEquals("team2" in dict, True, "Cannot find second entry in two team list")
     
suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestMakerLogin))
suite.addTest(unittest.makeSuite(TestMakerLogout))
suite.addTest(unittest.makeSuite(TestMakerCheckStatus))

runner = unittest.TextTestRunner()
res=runner.run(suite)
print(res)
print("*"*20)
for i in res.failures: print(i[1])
