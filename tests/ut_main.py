import unittest
import database
import escavenge
import team
import gamemaker

class TestDatabaseCreation(unittest.TestCase):
  #Test that we can access the database. Should not test that the database DS is correct, that should be
  #covered by the database tests.
  
  def setUp(self):
    self.db = database.Database()
    self.game = escavenge.Escavenge()

  def accessDB(self):
    self.assertIsNone(self.game.database, "The database is Null")
    # Add more tests probably

class TestLogin(unittest.TestCase):
  #Test log in functionality. Will determine if username belongs to gamemaker or team and call correct method
  
  def setUp(self):
    self.game = escavenge.Escavenge()

  def testLoginNoTeams(self):
    self.assertFalse(self.game.login("bob","password"),"Login did not return false when there was no user")

  def testLoginTeam(self):
    new = team.Team("bob","password",self.game.database)
    self.game.database.add_team(new)
    self.assertTrue(self.game.login("bob","password"),"Logging in was not successful but it should have been")
    self.assertEqual(self.game.database.get_current_user().username, "bob", "The correct user is not logged in")

  def testLoginMasterFAIL(self):
    self.assertFalse(self.game.login("maker","wrongpassword"), "Logged in with the wrong password")
    
  def testLoginMaster(self):
    self.assertTrue(self.game.login("maker","password"),"Was NOT able to log in as master and should have been able to")
    self.assertTrue(isinstance(self.game.database.get_current_user(),gamemaker.GameMaker), "Should be logged in as gamemaker but is not")

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestDatabaseCreation))
suite.addTest(unittest.makeSuite(TestLogin))

runner = unittest.TextTestRunner()
res = runner.run(suite)
print(res)
print("*" * 20)
for i in res.failures: print(i[1])



