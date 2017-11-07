import team
import unittest

class TestTeamLogin(unittest.TestCase):
    def setUp(self):
        self.team1 = team.Team("Name1")
        self.team2 = team.Team("Name2")
    def test_setTeamName(self):
        self.team1.setTeamName("n1")
        self.assertEquals("n1", self.team1.name, "Error: changing team name failed")
        #self.assertEquals("Team name changed to n1", self.team1.setTeamName("n1"), "Error: changing team name failed")
    def test_setTeamUserName(self):
        self.team1.setTeamUserName("u1")
        self.assertEquals("u1", self.team1.username, "Error: changing team user name failed")
        #self.assertEquals("Team username changed to un1", self.team1.setTeamUserName("un1"), "Error: changing team user name failed")
    def test_setTeamPassword(self):
        self.team1.setTeamPassword("p1")
        self.assertEquals("p1", self.team1.password, "Error: changing team password failed")
        #self.assertEquals("Team password changed to p1", self.team1.setTeamPassword("p1"), "Error: changing team password failed")
    def test_IncorrectLogin(self):
        self.assertEquals("Unable to log in",self.team1.login("wrong username","wrong password"), "Error: should not log in team1 with incorrect login info")
    def test_LoginFirstTeam(self):
        self.team1.login("username, password");
        self.assertEquals("Name1 logged in",self.team1.login(self.team1.username,self.team1.password), "Error: failed to log in team1")
    def test_LoginSecondTeam(self):
        self.team1.login("username","password")
        self.assertEquals("Unable to log in",self.team2.login(self.team2.username,self.team2.password), "Error: team1 is already logged in; cannot have two users logged in at once")
    def test_LogoutFirstTeam(self):
        self.team1.login("username","password")
        self.assertEquals("Name1 logged out",self.team1.logout(), "Error: failed to log out team1")
    def test_LogoutSecondTeam(self):
        self.team1.login("username","password")
        self.assertEquals("Unable to log out",self.team2.logout(), "Error: can't log out team2 when team1 is logged in")
    def test_LogoutNoTeamLoggedIn(self):
        self.assertEquals("Unable to log out",self.team1.logout(), "Error: cannot log out when no team is logged in")

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestTeamLogin))


runner = unittest.TextTestRunner()
res=runner.run(suite)
print(res)
print("*"*20)
for i in res.failures: print(i[1])