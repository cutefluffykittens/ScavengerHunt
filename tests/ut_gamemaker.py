import unittest
import gamemaker
import database
import team
import landmark

class TestMakerLogin(unittest.TestCase):
    def setUp(self):
        self.database = database.Database()
        self.maker1 = gamemaker.GameMaker(self.database)
  
    def test_bad_login(self):
        self.assertEquals(self.maker1.login("Notvalidusername","Notvalidpassword"), False, "Bad response to invalid login")
        self.assertEquals(self.database.get_current_user(), None, "Current user is not null")
    def test_good_login(self):
        self.assertEquals(self.maker1.login("maker","password"), True, "Maker should have logged in")
        self.assertEquals(self.database.get_current_user(), self.maker1, "Current user should be maker")
    def test_good_login_while_logged_in(self):
        self.maker1.login("maker","password")
        self.assertEquals(self.maker1.login("maker","password"), False, "Bad response to second login attempt")


class TestMakerLogout(unittest.TestCase):
    def setUp(self):
        self.database = database.Database()
        self.maker1 = gamemaker.GameMaker(self.database)
    
    def test_logout_while_not_logged_in(self):
        self.assertEquals(self.maker1.logout(), False, "Bad response to maker logging out while not logged in")
    def test_good_logout(self):
        self.maker1.login("maker", "password")
        self.assertEquals(self.maker1.logout(), True, "Bad response to maker logging out correctly")
    def test_current_user_is_not_maker(self):
        self.maker1.login("maker","password")
        self.maker1.logout()
        self.assertEquals(self.database.get_current_user(), None, "Current user is not null after logging out")


class TestMakerCheckStatus(unittest.TestCase):
    def setUp(self):
        self.database = database.Database()
        self.maker1 = gamemaker.GameMaker(self.database)
    
    def test_empty_team(self):
        self.assertEquals(self.maker1.display_status(), "No teams!", "CheckStatus did not return proper response to empty team list")
    
    def test_single_team(self):
        self.team1 = team.Team("Team1", "password", self.database)
        self.database.add_team(self.team1)
        dict = self.maker1.display_status()
        self.assertEquals(dict, "Team1\n", "Status incorrect for single team existing")
  
    def test_multiple_teams(self):
        self.team1 = team.Team("Team1", "password", self.database)
        self.team2 = team.Team("team2", "password", self.database)
        self.database.add_team(self.team1)
        self.database.add_team(self.team2)
        dict = self.maker1.display_status()
        self.assertEquals(dict, "Team1\nteam2\n", "Cannot find entries in two team list")

class TestMakerLandmark(unittest.TestCase):
    def setUp(self):
        self.database = database.Database()
        self.maker1 = gamemaker.GameMaker(self.database)
        self.input1 = ["name1", "clue1", "question1", "answer1"]
        self.input2 = ["name2", "clue2", "question2", "answer2"]

    def test_add_landmark_empty(self):
        self.maker1.add_landmark(self.input1)
        self.assertEqual(self.database.get_landmarks()[0].get_name(), self.input1[0], "test_add_landmark_empty: Landmark name wasn't correct")
        self.assertEqual(self.database.get_landmarks()[0].get_clue(), self.input1[1], "test_add_landmark_empty: Landmark clue wasn't correct")
        self.assertEqual(self.database.get_landmarks()[0].get_question(), self.input1[2], "test_add_landmark_empty: Landmark question wasn't correct")
        self.assertEqual(self.database.get_landmarks()[0].get_answer(), self.input1[3], "test_add_landmark_empty: Landmark answer wasn't correct")

    def test_add_landmark_not_empty(self):
        self.maker1.add_landmark(self.input1)
        self.maker1.add_landmark(self.input2)
        self.assertEqual(self.database.get_landmarks()[0].get_name(), self.input1[0], "test_add_landmark_not_empty: Landmark name wasn't correct")
        self.assertEqual(self.database.get_landmarks()[0].get_clue(), self.input1[1], "test_add_landmark_not_empty: Landmark clue wasn't correct")
        self.assertEqual(self.database.get_landmarks()[0].get_question(), self.input1[2], "test_add_landmark_not_empty: Landmark question wasn't correct")
        self.assertEqual(self.database.get_landmarks()[0].get_answer(), self.input1[3], "test_add_landmark_not_empty: Landmark answer wasn't correct")
        self.assertEqual(self.database.get_landmarks()[1].get_name(), self.input2[0], "test_add_landmark_not_empty: Landmark name wasn't correct")
        self.assertEqual(self.database.get_landmarks()[1].get_clue(), self.input2[1], "test_add_landmark_not_empty: Landmark clue wasn't correct")
        self.assertEqual(self.database.get_landmarks()[1].get_question(), self.input2[2], "test_add_landmark_not_empty: Landmark question wasn't correct")
        self.assertEqual(self.database.get_landmarks()[1].get_answer(), self.input2[3], "test_add_landmark_not_empty: Landmark answer wasn't correct")


    def test_remove_landmark_correct(self):
        self.maker1.add_landmark(self.input1)
        self.assertEqual(self.maker1.remove_landmark([self.input1[0]]), "Removed " + self.input1[0] + " from landmarks.", "test_delete_landmark_correct: Didn't delete correctly")

    def test_remove_landmark_incorrect(self):
        self.assertEqual(self.maker1.remove_landmark([self.input1[0]]), "Couldn't find landmark with name " + self.input1[0], "test_remove_landmark_incorrect: Shouldn't have deleted")

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestMakerLogin))
suite.addTest(unittest.makeSuite(TestMakerLogout))
suite.addTest(unittest.makeSuite(TestMakerCheckStatus))

runner = unittest.TextTestRunner()
res=runner.run(suite)
print(res)
print("*"*20)
for i in res.failures: print(i[1])
