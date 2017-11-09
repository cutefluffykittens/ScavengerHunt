import team
import database
import unittest

class TestTeamLogin(unittest.TestCase):
    def setUp(self):
        self.database = database.Database();
        self.team1 = team.Team("teamname1","password1",self.database)
        self.team2 = team.Team("teamname2","password2",self.database)
    def test_set_team_username(self):
        self.team1.set_team_username("u1")
        self.assertEquals("u1", self.team1.username, "Error: changing team user name failed")
    def test_set_team_password(self):
        self.team1.set_team_password("p1")
        self.assertEquals("p1", self.team1.password, "Error: changing team password failed")
    def test_incorrect_login(self):
        self.assertFalse(self.team1.login("wrong username","wrong password"), "Error: should not log in team1 with incorrect login info")
    def test_login_first_team(self):
        #self.team1.login("teamname1, password1")
        self.assertTrue(self.team1.login("teamname1","password1"), "Error: failed to log in team1")
    def test_login_second_team(self):
        self.team1.login("teamname1","password1")
        self.assertFalse(self.team2.login("teamname2","password2"), "Error: team1 is already logged in; cannot have two users logged in at once")
    def test_logout_first_team(self):
        self.team1.login("teamname1","password1")
        self.assertTrue(self.team1.logout(), "Error: failed to log out team1")
    def test_logout_second_team(self):
        self.team1.login("teamname1","password1")
        self.assertFalse(self.team2.logout(), "Error: can't log out team2 when team1 is logged in")
    def test_logout_no_team_logged_in(self):
        self.assertFalse(self.team1.logout(), "Error: cannot log out when no team is logged in")
    def test_display_menu(self):
        self.team1.login("teamname1","password1")
        self.assertEquals("Options\n\nlog out\ndisplay status\n",self.team1.display_menu(),"Error: incorrect menu displayed")

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestTeamLogin))


runner = unittest.TextTestRunner()
res=runner.run(suite)
print(res)
print("*"*20)
for i in res.failures: print(i[1])