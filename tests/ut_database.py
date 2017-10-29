import unittest
import database

# TODO: Uncomment these statements once implementations have been made
#import teamUser
#import landmark

# Stubs just for these classes until actual classes have been created

class TeamUser:
    def __init__(self):
        pass

class Landmark:
    def __init__(self):
        pass

class TestTeamList(unittest.TestCase):
    def setUp(self):
        self.db = database.Database()
        # TODO: Uncomment these statements once implementations have been made
        # self.team1 = teamUser.TeamUser()
        # self.team2 = teamUser.TeamUser()
        self.team1 = TeamUser()
        self.team2 = TeamUser()

    def test_addTeamEmptyList(self):
        self.db.add_team(self.team1)
        self.assertEquals(self.db.get_teams(), [self.team1], "addTeamEmptyList: Team list not correct")

    def test_addTeamNonEmptyList(self):
        self.db.add_team(self.team1)
        self.db.add_team(self.team2)
        self.assertEquals(self.db.get_teams(), [self.team1, self.team2], "addTeamNonEmptyList: Team list not correct")

    def test_deleteTeamEmptyList(self):
        self.db.delete_team(self.team1)
        self.assertEquals(self.db.get_teams(), [], "deleteTeamEmptyList: Team list not correct")

    def test_deleteTeamNonEmptyList(self):
        self.db.add_team(self.team1)
        self.db.delete_team(self.team1)
        self.assertEquals(self.db.get_teams(), [], "deleteTeamNonEmptyList: Team list not correct")


class TestLandmarks(unittest.TestCase):
    def setUp(self):
        self.db = database.Database()
        # TODO: Uncomment these statements once implementations have been made
        # self.landmark1 = landmark.Landmark()
        # self.landmark2 = landmark.Landmark()
        self.landmark1 = Landmark()
        self.landmark2 = Landmark()

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
        # TODO: Uncomment these statements once implementations have been made
        # self.landmark1 = landmark.Landmark()
        # self.landmark2 = landmark.Landmark()
        self.landmark1 = Landmark()
        self.landmark2 = Landmark()

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
        self.assertEquals(self.db.get_game_maker_cred(), {"username":"username", "password":"password"}, "getGameMakerCred: Cred was incorrect")


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