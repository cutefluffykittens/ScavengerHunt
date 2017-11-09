import unittest
import team
import landmark
import database


class TestTeamList(unittest.TestCase):
    def setUp(self):
        self.db = database.Database()
        self.team1 = team.Team("team1", "password1", self.db);
        self.team2 = team.Team("team2", "password2", self.db)

    def test_add_team_empty_list(self):
        self.db.add_team(self.team1)
        self.assertEquals(self.db.get_teams(), [self.team1], "addTeamEmptyList: Team list not correct")

    def test_add_team_non_empty_list(self):
        self.db.add_team(self.team1)
        self.db.add_team(self.team2)
        self.assertEquals(self.db.get_teams(), [self.team1, self.team2], "addTeamNonEmptyList: Team list not correct")

    def test_delete_team_empty_list(self):
        self.db.delete_team(self.team1)
        self.assertEquals(self.db.get_teams(), [], "deleteTeamEmptyList: Team list not correct")

    def test_delete_team_non_empty_list(self):
        self.db.add_team(self.team1)
        self.db.delete_team(self.team1)
        self.assertEquals(self.db.get_teams(), [], "deleteTeamNonEmptyList: Team list not correct")


class TestLandmarks(unittest.TestCase):
    def setUp(self):
        self.db = database.Database()
        self.landmark1 = landmark.Landmark("clue")
        self.landmark2 = landmark.Landmark("clue")

    def test_addLandmarkEmptyList(self):
        self.db.add_landmark(self.landmark1)
        self.assertEquals(self.db.get_landmarks(), [self.landmark1], "addLandmarkEmptyList: Team list not correct")

    def test_addLandmarkNonEmptyList(self):
        self.db.add_landmark(self.landmark1)
        self.db.add_landmark(self.landmark2)
        self.assertEquals(self.db.get_landmarks(), [self.landmark1, self.landmark2], "addLandmarkNonEmptyList: Team list not correct")

    def test_deleteLandmarkEmptyList(self):
        self.db.delete_landmark(self.landmark1)
        self.assertEquals(self.db.get_landmarks(), [], "deleteLandmarkEmptyList: Team list not correct")

    def test_deleteLandmarkNonEmptyList(self):
        self.db.add_landmark(self.landmark1)
        self.db.delete_landmark(self.landmark1)
        self.assertEquals(self.db.get_landmarks(), [], "deleteLandmarkNonEmptyList: Team list not correct")


class TestLandmarkPath(unittest.TestCase):
    def setUp(self):
        self.db = database.Database()
        self.landmark1 = landmark.Landmark("clue")
        self.landmark2 = landmark.Landmark("clue")

    def test_addLandmarkEmptyList(self):
        self.db.add_to_path(self.landmark1)
        self.assertEquals(self.db.get_landmark_path(), [self.landmark1], "addLandmarkEmptyList: Team list not correct")

    def test_addLandmarkNonEmptyList(self):
        self.db.add_to_path(self.landmark1)
        self.db.add_to_path(self.landmark2)
        self.assertEquals(self.db.get_landmark_path(), [self.landmark1, self.landmark2], "addLandmarkNonEmptyList: Team list not correct")

    def test_deleteLandmarkEmptyList(self):
        self.db.delete_from_path(self.landmark1)
        self.assertEquals(self.db.get_landmark_path(), [], "deleteLandmarkEmptyList: Team list not correct")

    def test_deleteLandmarkNonEmptyList(self):
        self.db.add_to_path(self.landmark1)
        self.db.delete_from_path(self.landmark1)
        self.assertEquals(self.db.get_landmark_path(), [], "deleteLandmarkNonEmptyList: Team list not correct")


class TestPenalties(unittest.TestCase):
    def setUp(self):
        self.db = database.Database()
        self.guessPenalty = 0
        self.timePenalty = 0

    def test_editGuessPenalty(self):
        self.db.set_guess_penalty(5)
        self.assertEquals(self.db.get_guess_penalty(), 5, "editGuessPenalty: Edit didn't work")

    def test_editTimePenalty(self):
        self.db.set_time_penalty(5)
        self.assertEquals(self.db.get_time_penalty(), 5, "editTimePenalty: Edit didn't work")


class TestGameMakerCred(unittest.TestCase):
    def setUp(self):
        self.db = database.Database()

    def test_getGameMakerCred(self):
        self.assertEquals(self.db.get_game_maker_cred(), {"username":"maker", "password":"password"}, "getGameMakerCred: Cred was incorrect")


suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestTeamList))
suite.addTest(unittest.makeSuite(TestLandmarks))
suite.addTest(unittest.makeSuite(TestLandmarkPath))
suite.addTest(unittest.makeSuite(TestPenalties))
suite.addTest(unittest.makeSuite(TestGameMakerCred))

runner = unittest.TextTestRunner()
res=runner.run(suite)
print(res)
print("*"*20)
for i in res.failures: print(i[1])