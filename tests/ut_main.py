import unittest
import database
import escavenge
import team

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
    self.db = database.Database()
    self.game = escavenge.Escavenge()

  def testLoginNoTeams(self):
    self.assertFalse(self.game.login("bob","password"),"Login did not return false when there was no user")

  def testLoginTeam(self):
    #is this the correct way?
    new = team.Team("bob","password")
    self.db.add_team(new)
    self.assertTrue(self.game.login("bob","password"),"Logging in was not successful but it should have been")
    self.assertEquals(self.db.get_current_user(), "bob", "The correct user is not logged in")

  def testLoginMasterFAIL(self):
    #Is this the correct username?
    self.assertFalse(self.game.login("maker","wrongpassword"), "Logged in as " + self.db.get_current_user() + " and log in returned True but should have been false")
    
  def testLoginMaster(self):
    self.assertTrue(self.game.login("maker","password"),"Was NOT able to log in as master and should have been able to")
    self.assertEquals(self.db.get_current_user(), "maker", "Logged in as " + self.db.get_current_user() + " but should have been logged in as maker")

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestDatabaseCreation))
suite.addTest(unittest.makeSuite(TestLogin))

runner = unittest.TextTestRunner()
res = runner.run(suite)
print(res)
print("*" * 20)
for i in res.failures: print(i[1])




# class TestMain(unittest.TestCase):
#   #Test prompts and functionality of main script
#
#   def setUp(self):
#     self.db = database.Database()
#     self.game = escavenge.Escavenge()
#
#   def testPromptAsGameMaker(self):
#     # Should I continue with this? Should I move game maker & team to another class? :(
#     self.inputs.user = "maker"
#     self.inputs.password = "password"
#     escavenge.login()
#
#     self.assertEquals(self.inputs.cmd="add-team"), "You chose to add a team. Please enter the username: ", "add-team does not work")
#     self.assertEquals(self.inputs.cmd) = "team", "Please enter the password for team: ", "adding team username did not work")
#     self.assertEquals(self.inputs.cmd) = "password", "You have added team: team with password: password", "adding team password did not work");
  

