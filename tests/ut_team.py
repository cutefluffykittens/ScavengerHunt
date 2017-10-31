import team
import unittest

class TestTeamLogin(unittest.TestCase):
    def setUp(self):
        self.team1 = team.Team("Name1","Username1","Password1")
        self.team2 = team.Team("Name2","Username2","Password2")
    def test_IncorrectLogin(self):
        self.assertFalse(self.team1.login("wrong username","wrong password"), "Error: should not log in team1 with incorrect login info")
    def test_LoginFirstTeam(self):
        self.assertTrue(self.team1.login(self.team1.username,self.team1.password), "Error: failed to log in team1")
    def test_LoginSecondTeam(self):
        self.assertFalse(self.team2.login(self.team2.username,self.team2.password), "Error: team1 is already logged in; cannot have two users logged in at once")
    def test_LogoutFirstTeam(self):
        self.assertTrue(self.team1.logout(), "Error: failed to log out team1")
    def test_LogoutSecondTeam(self):
        self.assertFalse(self.team2.logout(), "Error: can't log out team2 when team1 is logged in")

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestTeamLogin))


runner = unittest.TextTestRunner()
res=runner.run(suite)
print(res)
print("*"*20)
for i in res.failures: print(i[1])