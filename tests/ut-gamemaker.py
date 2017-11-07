import unittest
import gamemaker
import database
import team
import user
import landmark

class TestMakerLogin(unittest.TestCase):
    def set_up(self):
        self.database = database.Database()
        self.maker1 = gamemaker.GameMaker()
  
    def test_bad_login(self):
        self.assertEquals(self.maker1.login("Notvalidusername","Notvalidpassword"), False, "Bad response to invalid login")
        self.assertEquals(self.database.get_current_user(), {}, "Current user is not null")
    def test_good_login(self):
        self.assertEquals(self.maker1.login("maker","password"), True, "Maker should have logged in")
        self.assertEquals(self.database.get_current_user(), {"maker" : "password"}, "Current user should be maker")
    def test_good_login_while_logged_in(self):
        self.maker1.login("maker","password")
        self.assertEquals(self.maker1.login("maker","password"), False, "Bad response to second login attempt")


class TestMakerLogout(unittest.TestCase):
    def set_up(self):
        self.database = database.Database()
        self.maker1 = gamemaker.GameMaker()
    
    def test_logout_while_not_logged_in(self):
        self.assertEquals(self.maker1.logout(), False, "Bad response to maker logging out while not logged in")
    def test_good_logout(self):
        self.maker1.login()
        self.assertEquals(self.maker1.logout(), True, "Bad response to maker logging out correctly")
    def test_current_user_is_not_maker(self):
        self.maker1.login("maker","password")
        self.maker1.logout()
        self.assertEquals(self.database.get_current_user(), None, "Current user is not null after logging out")


class TestMakerCheckStatus(unittest.TestCase):
    def set_up(self):
        self.database = database.Database()
        self.maker1 = gamemaker.GameMaker()
    
    def test_empty_team(self):
        self.assertEquals(self.maker1.check_status(), "No teams!", "CheckStatus did not return proper response to empty team list")
    
    def test_single_team(self):
        self.team1 = team.Team("Team1", "password", )
        dict = self.maker1.check_status()
        self.assertEquals(dict, "Team1", "Status incorrect for single team existing")
  
    def test_multiple_teams(self):
        self.team1 = team.Team("Team1", "password")
        self.team2 = team.Team("team2", "password")
        dict = self.maker1.check_status()
        self.assertEquals(dict, "Team1 team2", "Cannot find entries in two team list")

class TestMakerLandmark(unittest.TestCase):
    def set_up(self):
        self.database = database.Database()
        self.landmark1 = landmark.Landmark()
        self.landmark2 = landmark.Landmark()
        self.maker1 = gamemaker.GameMaker()

    def test_add_clue(self):
        self.landmark1.add_clue("In an area with tall buildings and a metal tower")
        self.assertEquals(self.landmark1.get_clue(), "In an area with tall buildings and a metal tower", "Bad first clue")

    def test_add_two_clues(self):
        self.landmark1.add_clue("In an area with tall stuff")
        self.landmark2.add_clue("In a building with a picture of a lady")
        self.assertEquals(self.landmark1.get_clue(), "In an area with tall stuff", "First clue not given back for two clues")
        self.assertEquals(self.landmark2.get_clue(), "In a building with a picture of a lady", "Second clue not given back")


suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestMakerLogin))
suite.addTest(unittest.makeSuite(TestMakerLogout))
suite.addTest(unittest.makeSuite(TestMakerCheckStatus))

runner = unittest.TextTestRunner()
res=runner.run(suite)
print(res)
print("*"*20)
for i in res.failures: print(i[1])