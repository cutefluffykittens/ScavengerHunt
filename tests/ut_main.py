import unittest
import database
import EScavange
import gameMaker

class TestDatabaseCreation(unittest.TestCase):
  def setUp(self):
    self.db = database.Database()
    self.gameMaker = gameMaker.GameMaker()
  
  def accessDB(self):
    pass
    #stub for now : check that we can access the database
 
class TestMain(unittest.TestCase):
  def setUp(self):
    self.db = database.Database()
    self.inputs = escavange.Main()
    self.inputs.user = "Bob"            #Set the user inputs
    self.inputs.password = "password"
    
  def testPrompt(self):
    self.assertEquals(escavange.Main(), "Welcome to EScavange! Please log in: ", "Main function does not print expected value")

  def testLoginNoTeams(self):
    self.assertEquals(escavange.login(), "There is no such user. Please create a new team", "Login did not give the correct error message")

  def testLoginTeam(self):
    self.db.addTeam(user,password) #90% sure this is wrong
    self.assertEquals(escavange.login(), "Currently logged in as Bob", "Login was not with the correct user")
    
  def testLoginMaster(self):
    self.inputs.user = "maker"
    self.inputs.password = "wrongpassword"
    self.assertEquals(escavange.login(), "Failed to log in as Master", "Was able to log in as master and should not have been able to")
    
  def testLoginMaster(self):
    self.inputs.user = "maker"
    self.inputs.password = "password"
    self.assertEquals(escavange.login(), "Logged in as Master", "Was NOT able to log in as master and should have been able to")
  
suite = unittest.TestSuite()

suite.addTest(unittest.makeSuite(TestDatabaseCreation))
suite.addTest(unittest.makeSuite(TestMain))

runner = unittest.TextTestRunner()
res=runner.run(suite)
print(res)
print("*"*20)
for i in res.failures: print(i[1])
