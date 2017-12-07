import unittest
import gamemaker
from Interface.models import HuntUser, Landmark
import database
import team
import landmark
from django.test import TestCase

class TestMakerAddLandmark(TestCase):
    def setUp(self):
        self.maker1 = gamemaker.GameMaker()

    def test_add_one_landmark(self):
        self.maker1.add_landmark("land,clue,question,answer")
        self.assertEqual(self.maker1.display_landmarks(), "There are no landmarks", "Bad landmark")

    def test_add_two_landmarks(self):
        self.maker1.add_landmark("land clue question answer")
        self.maker1.add_landmark("land1 clue1 question1 answer1")
        self.assertEqual(self.maker1.display_landmarks(), "l\nl\n", "Bad landmarks")

class TestMakerDisplayLandmarks(TestCase):
    def setUp(self):
        self.maker1 = gamemaker.GameMaker()

    def test_display_one_landmark(self):
        self.maker1.add_landmark("land clue question answer")
        self.assertEqual(self.maker1.display_landmarks(), "There are no landmarks", "Bad display")

    def test_display_two_landmarks(self):
        self.maker1.add_landmark("land clue question answer")
        self.maker1.add_landmark("land1 clue1 question1 answer1")
        self.assertEqual(self.maker1.display_landmarks(), "l\nl\n", "Bad displays")

class TestMakerRemoveLandmarks(TestCase):
    def setUp(self):
        self.maker1 = gamemaker.GameMaker()

    def test_remove_one_landmark(self):
        self.maker1.add_landmark("land clue question answer")
        self.maker1.remove_landmark("land")
        self.assertEqual(self.maker1.display_landmarks(), "", "Did not remove landmark")

    def test_remove_multiple_landmarks_to_none(self):
        self.maker1.add_landmark("land clue question answer")
        self.maker1.add_landmark("land1 clue1 question1 answer1")
        self.assertEqual(self.maker1.display_landmarks(), "l\nl\n", "Did not remove landmarks")

    def test_remove_multiple_landmarks_to_one(self):
        self.maker1.add_landmark("land clue question answer")
        self.maker1.add_landmark("land1 clue1 question1 answer1")
        self.assertEqual(self.maker1.display_landmarks(), "l\nl\n", "Did not remove landmarks")

class TestMakerCheckStatus(TestCase):
    def setUp(self):
        HuntUser.objects.all().delete()
        self.game_maker = gamemaker.GameMaker()

    def test_single_team(self):
        self.game_maker.make_team(["team1", "password"])
        self.assertEquals(self.game_maker.display_status(), "team1\n", "Bad single team return")

    def test_multiple_teams(self):
        self.game_maker.make_team(["team1", "password"])
        self.game_maker.make_team(["team2", "password"])
        self.assertEqual(self.game_maker.display_status(), "team1\nteam2\n", "Cannot find entries in two team list")

class TestMakerDisplayMenu(TestCase):
    def setUp(self):
        self.game_maker = gamemaker.GameMaker()

    def test_display_menu(self):
        self.assertEqual(self.game_maker.display_menu(), "Options\n\ndisplaystatus\nmaketeam [team name], [team password]\neditteam [team name to edit], [new team name], [new team password]\n" \
        "addlandmark [name], [clue], [question], [answer]\ndisplaylandmarks\nremovelandmark [name]\nsetpenalties [new time penalty], [new guess penalty]\n" \
        "creategame [landmark name]...\nstartgame\nendgame\nlogout\n", "Wrong menu")

class TestMakerCreateTeam(TestCase):
    def setUp(self):
        HuntUser.objects.all().delete()
        Landmark.objects.all().delete()
        try:
            landmark = Landmark(name="dummy", clue="dummy", question="dummy", answer="dummy", order_num=-1)
            landmark.save()
        except Landmark.DoesNotExist:
            pass
        self.game_maker = gamemaker.GameMaker()

    def test_single_team(self):
        self.game_maker.make_team(["team1", "password"])
        self.assertEquals(self.game_maker.display_status(), "team1\n", "Bad single team return")

    def test_multiple_teams(self):
        self.game_maker.make_team(["team1", "password"])
        self.game_maker.make_team(["team2", "password"])
        self.assertEqual(self.game_maker.display_status(), "team1\nteam2\n", "Cannot find entries in two team list")

class TestMakerEditTeams(TestCase):
    def setUp(self):
        HuntUser.objects.all().delete()
        self.game_maker = gamemaker.GameMaker()

    def test_single_team(self):
        self.game_maker.make_team(["team1", "password"])
        self.assertEquals(self.game_maker.edit_team(["team1", "team2", "passnew"]), "Edited team1 to have username team2 and password passnew", "Bad single team edit")

    def test_multiple_teams(self):
        self.game_maker.make_team(["team1", "password"])
        self.game_maker.make_team(["team2", "password"])
        self.assertEquals(self.game_maker.edit_team(["team1", "team", "passnew"]), "Edited team1 to have username team and password passnew",
                          "Bad single team edit")
        self.assertEquals(self.game_maker.edit_team(["team2", "team3", "passnew"]), "Edited team2 to have username team3 and password passnew",
                          "Bad single team edit")

class TestMakerDeleteTeam(TestCase):
    def setUp(self):
        self.game_maker = gamemaker.GameMaker()

    def test_single_team(self):
        self.game_maker.make_team(["Team1 password"])
        self.assertEquals(self.game_maker.delete_team("Team1"), "Invalid input!", "Bad single team delete")

    def test_multiple_teams(self):
        self.game_maker.make_team("Team1 password")
        self.game_maker.make_team("team2 password")
        self.assertEquals(self.game_maker.delete_team("Team1"), "Invalid input!", "Bad two team delete")
        self.assertEquals(self.game_maker.delete_team("team2"), "Invalid input!", "Bad 2nd two team delete")

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestMakerCheckStatus))
suite.addTest(unittest.makeSuite(TestMakerCreateTeam))
suite.addTest(unittest.makeSuite(TestMakerEditTeams))
suite.addTest(unittest.makeSuite(TestMakerDeleteTeam))


runner = unittest.TextTestRunner()
res=runner.run(suite)
print(res)
print("*"*20)
for i in res.failures: print(i[1])
