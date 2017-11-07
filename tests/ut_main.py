import unittest
import database
import escavenge
import gamemaker

class TestDatabaseCreation(unittest.TestCase):
  #Test that we can access the database. Should not test that the database DS is correct, that should be
  #covered by the database tests.
  
  def setUp(self):
    self.db = database.Database()
    self.gameMaker = gamemaker.GameMaker()
    self.game = escavenge.Escavenge()

  def accessDB(self):
    self.assertFalse(self.game.database, None, "The database is Null")
    # Add more tests probably

class TestLogin(unittest.TestCase):
  #Test log in functionality. Will determine if username belongs to gamemaker or team and call correct method
  
  def setUp(self):
    self.db = database.Database()
    self.inputs = escavenge.EScavenge()
    self.inputs.user = "Bob"            #Set the user inputs (so the test can be automatic, no user input necessary)
    self.inputs.password = "password"
        
  def testLoginNoTeams(self):
    self.assertEquals(escavenge.login(), "There is no such user. Please create a new team", "Login did not give the correct error message")

  def testLoginTeam(self):
    self.db.add_team(self.inputs.user,self.inputs.password) #What is the syntax to add a team to the DB?????????
    self.assertEquals(escavenge.login(), "Currently logged in as Bob", "Login was not with the correct user")
    
  def testLoginMasterFAIL(self):
    self.inputs.user = "maker"
    self.inputs.password = "wrongpassword"
    self.assertEquals(escavenge.login(), "Failed to log in as Master", "Was able to log in as master and should not have been able to")
    
  def testLoginMaster(self):
    self.inputs.user = "maker"        #is this what we decided for username and password
    self.inputs.password = "password"
    self.assertEquals(escavenge.login(), "Logged in as Master. What would you like to do? [add-team, add-landmark, add-game]", "Was NOT able to log in as master and should have been able to")
 
class TestMain(unittest.TestCase):
  #Test prompts and functionality of main script
  
  def setUp(self):
    self.db = database.Database()
    self.inputs = escavenge.main()
   
  def testPromptLogin(self):
    self.assertEquals(escavenge.main(), "Welcome to EScavange! Please log in: ", "Main function does not print expected value")
    
  def testPromptAsGameMaker(self):
    # Should I continue with this? Should I move game maker & team to another class? :( 
    self.inputs.user = "maker"
    self.inputs.password = "password"
    escavenge.login()
    
    self.assertEquals(self.inputs.cmd="add-team"), "You chose to add a team. Please enter the username: ", "add-team does not work")
    self.assertEquals(self.inputs.cmd) = "team", "Please enter the password for team: ", "adding team username did not work")
    self.assertEquals(self.inputs.cmd) = "password", "You have added team: team with password: password", "adding team password did not work");
  
suite = unittest.TestSuite()

suite.addTest(unittest.makeSuite(TestDatabaseCreation))
suite.addTest(unittest.makeSuite(TestMain))
suite.addTest(unittest.makeSuite(TestLogin))

runner = unittest.TextTestRunner()
res=runner.run(suite)
print(res)
print("*"*20)
for i in res.failures: print(i[1])
