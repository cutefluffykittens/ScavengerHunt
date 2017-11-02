import unittest
import gamemaker
import database

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
    
  def 
     
suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestMakerLogin))
suite.addTest(unittest.makeSuite(TestMakerLogout))

runner = unittest.TextTestRunner()
res=runner.run(suite)
print(res)
print("*"*20)
for i in res.failures: print(i[1])
