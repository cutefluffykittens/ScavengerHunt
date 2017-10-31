import unittest
import gamemaker
import database

class TestMakerLogin(unittest.TestCase):
  def setUp(self):
    self.database = database.Database()
    self.maker1 = gamemaker.GameMaker()
  
  def test_BadLogin(self):
     self.assertEquals(self.maker1.login("Notvalidusername","Notvalidpassword"), false, "test_makerLogin should not have logged in"))
  def test_NoCurrentUser(self):
     self.assertEquals(self.database.curUser, null, "Current user is not null") //Make sure null is starting value!
  def test_GoodLogin(self):
     self.assertEquals(self.maker1.login("maker","password"), true, "Maker should have logged in")
  def test_GoodLoginWhileLoggedIn(self):
     self.assertEquals(self.maker1.login("maker","password"), false, "Maker was already logged in but logged in again")
  def test_CurrentUserIsMaker(self):
     self.assertEquals(self.database.curUser, "maker", "Current user is not maker") //Make sure maker is what we will name it!
      
  class TestMakerLogout(unittest.TestCase):
    def setUp(self):
      self.database = database.Database()
      self.maker1 = gamemaker.GameMaker()
    
    def test_LogoutWhileNotLoggedIn(self):
      self.assertEquals(self.maker1.logout(), false, "Maker logged out while not logged in")
    def test_GoodLogout(self):
      self.maker1.login()
      self.assertEquals(self.maker1.logout(), true, "Maker didn't log out")
    def test_LogoutWhileLoggedOut(self):
      self.assertEquals(self.database.curUser, null, "Current user is not null after logging out")
     
suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestMakerLogin))
suite.addTest(unittest.makeSuite(TestMakerLogout))

runner = unittest.TextTestRunner()
res=runner.run(suite)
print(res)
print("*"*20)
for i in res.failures: print(i[1])
