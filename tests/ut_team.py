import team
import database
import unittest

class TestTeamLogin(unittest.TestCase):
    def setUp(self):
        self.database = database.Database()
        self.team1 = team.Team("teamname1","password1",self.database)
        self.team2 = team.Team("teamname2","password2",self.database)
    def test_incorrect_login(self):
        self.assertFalse(self.team1.login("wrong username","wrong password"),
                         "Error: should not log in team1 with incorrect login info")
    def test_login_first_team(self):
        self.assertTrue(self.team1.login("teamname1","password1"), "Error: failed to log in team1")
    def test_login_second_team(self):
        self.team1.login("teamname1","password1")
        self.assertFalse(self.team2.login("teamname2","password2"),
                         "Error: team1 is already logged in; cannot have two users logged in at once")

class TestTeamLogout(unittest.TestCase):
    def setUp(self):
        self.database = database.Database()
        self.team1 = team.Team("teamname1","password1",self.database)
        self.team2 = team.Team("teamname2","password2",self.database)
    def test_logout_first_team(self):
        self.team1.login("teamname1","password1")
        self.assertTrue(self.team1.logout(), "Error: failed to log out team1")
    def test_logout_second_team(self):
        self.team1.login("teamname1","password1")
        self.assertFalse(self.team2.logout(), "Error: can't log out team2 when team1 is logged in")
    def test_logout_no_team_logged_in(self):
        self.assertFalse(self.team1.logout(), "Error: cannot log out when no team is logged in")


class TestTeamEditUsername(unittest.TestCase):
    def setUp(self):
        self.database = database.Database()
        self.team1 = team.Team("teamname1","password1",self.database)
        self.database.add_team(self.team1)
    def test_edit_username_no_team_logged_in(self):
        self.assertFalse(self.team1.edit_username("bestteam"), "Error: cannot edit username with no team logged in")
    def test_edit_username(self):
        self.team1.login("teamname1","password1")
        self.assertEqual("Username successfully changed to bestteam", self.team1.edit_username(["bestteam"]), "Error: username change did not return True")
        self.assertEqual("bestteam", self.team1.username, "Error: username was not changed")
        self.assertEqual("bestteam", self.database.get_current_user().username,
                         "Error: Database does not have correct username as current user")
        self.assertEqual(1,len(self.database.get_teams()),"blah")
        self.assertEqual("bestteam", self.database.get_teams().pop(0).username,
                         "Error: username was not updated in database's list of teams")


class TestTeamEditPassword(unittest.TestCase):
    def setUp(self):
        self.database = database.Database()
        self.team1 = team.Team("teamname1","password1",self.database)
        self.database.add_team(self.team1)
    def test_edit_password_no_team_logged_in(self):
        self.assertFalse(self.team1.edit_password("kittens"),"Error: cannot edit password with no team logged in")
    def test_edit_password(self):
        self.team1.login("teamname1","password1")
        self.assertEqual("Password successfully changed to kittens", self.team1.edit_password(["kittens"]), "Error: password change did not return True")
        self.assertEqual("kittens", self.team1.password, "Error: password was not changed")
        self.assertEqual("kittens", self.database.get_teams().pop(0).password,
                         "Error: password was not updated in database's list of teams")


class TestTeamCommands(unittest.TestCase):
    def setUp(self):
        self.database = database.Database()
        self.team1 = team.Team("teamname1","password1",self.database)
    def test_display_menu(self):
        self.team1.login("teamname1","password1")
        self.assertEqual("Options\n\nlog out\ndisplay status\nedit username\nedit password\n",self.team1.display_menu(),"Error: incorrect menu displayed")


suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestTeamLogin))
suite.addTest(unittest.makeSuite(TestTeamLogout))
suite.addTest(unittest.makeSuite(TestTeamEditUsername))
suite.addTest(unittest.makeSuite(TestTeamEditPassword))
suite.addTest(unittest.makeSuite(TestTeamCommands))


runner = unittest.TextTestRunner()
res=runner.run(suite)
print(res)
print("*"*20)
for i in res.failures: print(i[1])