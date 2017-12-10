import unittest
import gamemaker
from Interface.models import HuntUser, Landmark, Game
#import database
import team
#import landmark
from django.test import TestCase


class TestMakerAddLandmark(TestCase):
    def setUp(self):
        Landmark.objects.all().delete()
        lm = Landmark(name="dummy", clue="dummy", question="dummy", answer="dummy", order_num=-1)
        lm.save()
        self.maker1 = gamemaker.GameMaker()

    def test_add_one_landmark(self):
        self.maker1.add_landmark(["land","clue","question","answer"])
        self.assertEqual(self.maker1.display_landmarks(), "land\n", "Bad landmark")

    def test_add_landmark_same_name(self):
        self.maker1.add_landmark(["land", "clue", "question", "answer"])
        self.assertEqual("Landmark land already exists!",self.maker1.add_landmark(["land","clue","question","answer"]),
                         "Error: landmark with same name should not have been added to database")

    def test_add_two_landmarks(self):
        self.maker1.add_landmark(["land","clue","question","answer"])
        self.maker1.add_landmark(["land1","clue1","question1","answer1"])
        self.assertEqual(self.maker1.display_landmarks(), "land\nland1\n", "Bad landmarks")


class TestMakerDisplayLandmarks(TestCase):
    def setUp(self):
        Landmark.objects.all().delete()
        lm = Landmark(name="dummy", clue="dummy", question="dummy", answer="dummy", order_num=-1)
        lm.save()
        self.maker1 = gamemaker.GameMaker()

    def test_display_one_landmark(self):
        self.maker1.add_landmark(["land","clue","question","answer"])
        self.assertEqual(self.maker1.display_landmarks(), "land\n", "Bad display")

    def test_display_two_landmarks(self):
        self.maker1.add_landmark(["land","clue","question","answer"])
        self.maker1.add_landmark(["land1","clue1","question1","answer1"])
        self.assertEqual(self.maker1.display_landmarks(), "land\nland1\n", "Bad displays")


class TestMakerRemoveLandmarks(TestCase):
    def setUp(self):
        Landmark.objects.all().delete()
        lm = Landmark(name="dummy", clue="dummy", question="dummy", answer="dummy", order_num=-1)
        lm.save()
        self.maker1 = gamemaker.GameMaker()

    def test_remove_one_landmark(self):
        self.maker1.add_landmark(["land","clue","question","answer"])
        self.maker1.remove_landmark(["land"])
        self.assertEqual(self.maker1.display_landmarks(), "There are no landmarks", "Did not remove landmark")

    def test_remove_multiple_landmarks_to_none(self):
        self.maker1.add_landmark(["land","clue","question","answer"])
        self.maker1.add_landmark(["land1","clue1","question1","answer1"])
        self.maker1.remove_landmark(["land"])
        self.maker1.remove_landmark(["land1"])
        self.assertEqual(self.maker1.display_landmarks(), "There are no landmarks", "Did not remove landmarks")

    def test_remove_multiple_landmarks_to_one(self):
        self.maker1.add_landmark(["land","clue","question","answer"])
        self.maker1.add_landmark(["land1","clue1","question1","answer1"])
        self.maker1.remove_landmark(["land"])
        self.assertEqual(self.maker1.display_landmarks(), "land1\n", "Did not remove landmarks")


class TestMakerCheckStatus(TestCase):
    def setUp(self):
        HuntUser.objects.all().delete()
        Landmark.objects.all().delete()
        lm = Landmark(name="dummy", clue="dummy", question="dummy", answer="dummy", order_num=-1)
        lm.save()
        self.game_maker = gamemaker.GameMaker()

    def test_single_team(self):
        self.game_maker.make_team(["team1", "password1"])
        self.assertEquals(self.game_maker.display_status(), "team1\n", "Bad single team return")

    def test_multiple_teams(self):
        self.game_maker.make_team(["team1", "password1"])
        self.game_maker.make_team(["team2", "password2"])
        self.assertEqual(self.game_maker.display_status(), "team1\nteam2\n", "Cannot find entries in two team list")


class TestMakerDisplayMenu(TestCase):
    def setUp(self):
        self.game_maker = gamemaker.GameMaker()

    def test_display_menu(self):
        self.assertEqual(self.game_maker.display_menu(),
                         "Options\n\ndisplaystatus\nmaketeam [team name], [team password]\n"
                         "editteam [team name to edit], [new team name], [new team password]\n"
                         "addlandmark [name], [clue], [question], [answer]\ndisplaylandmarks\nremovelandmark [name]\n"
                         "setpenalties [new time penalty], [new guess penalty]\n"
                         "creategame [landmark name]...\nstartgame\nendgame\nlogout\n", "Wrong menu")


class TestMakerCreateTeam(TestCase):
    def setUp(self):
        HuntUser.objects.all().delete()
        Landmark.objects.all().delete()
        lm = Landmark(name="dummy", clue="dummy", question="dummy", answer="dummy", order_num=-1)
        lm.save()
        self.game_maker = gamemaker.GameMaker()

    def test_single_team(self):
        self.game_maker.make_team(["team1", "password"])
        self.assertEquals(self.game_maker.display_status(), "team1\n", "Bad single team return")

    def test_make_team_same_name(self):
        self.game_maker.make_team(["team1", "password"])
        self.assertEqual("Team team1 already exists!",self.game_maker.make_team(["team1", "password"]),
                         "Error: team1 was added into the database twice")

    def test_multiple_teams(self):
        self.game_maker.make_team(["team1", "password"])
        self.game_maker.make_team(["team2", "password"])
        self.assertEqual(self.game_maker.display_status(), "team1\nteam2\n", "Cannot find entries in two team list")


class TestMakerEditTeams(TestCase):
    def setUp(self):
        HuntUser.objects.all().delete()
        Landmark.objects.all().delete()
        lm = Landmark(name="dummy", clue="dummy", question="dummy", answer="dummy", order_num=-1)
        lm.save()
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


class TestMakerCreateGame(TestCase):
    def setUp(self):
        HuntUser.objects.all().delete()
        Landmark.objects.all().delete()
        Game.objects.all().delete()
        self.game = Game(name="game",running=False)
        self.game.save()
        lm = Landmark(name="dummy", clue="dummy", question="dummy", answer="dummy", order_num=-1)
        lm.save()
        self.maker = gamemaker.GameMaker()
        self.maker.make_team(["team1","password1"])
        self.t = team.Team()
        lm1 = Landmark(name="landmark1", clue="clue1", question="question1", answer="answer1", order_num=-1)
        lm2 = Landmark(name="landmark2", clue="clue2", question="question2", answer="answer2", order_num=-1)
        lm1.save()
        lm2.save()

    def test_create_game_no_landmarks(self):
        self.assertEqual("Need at least one landmark to create a game",self.maker.create_game([]),
                         "Error: can't create a game without any landmarks")

    def test_create_game_one_landmark(self):
        self.assertEqual("Game has been created!",self.maker.create_game(["landmark1"]),
                         "Error: game with one landmark should have been created")
        cur = HuntUser.objects.get(name="team1").current_landmark
        lm1 = Landmark.objects.get(name="landmark1")
        self.assertEqual(0,lm1.order_num,
                         "Error: landmark1 order_num should be 0, instead is " + str(lm1.order_num))

    def test_create_game_invalid_landmark(self):
        self.assertEqual("Landmark inv is not a valid landmark!",self.maker.create_game(["inv"]),
                         "Error: adding a landmark that doesn't exist shouldn't be valid")

    def test_create_game_started(self):
        self.maker.create_game(["landmark1"])
        self.game.running = True
        self.game.save()
        self.assertEqual("Game is already in progress!",self.maker.create_game(["landmark1"]),
                         "Error: game shouldn't have been created while a game is currently running")

    def test_create_game_multiple_landmarks(self):
        self.assertEqual("Game has been created!",self.maker.create_game(["landmark1","landmark2"]),
                         "Error: game with two landmarks should have been created")
        cur = HuntUser.objects.get(name="team1").current_landmark
        lm1 = Landmark.objects.get(name="landmark1")
        lm2 = Landmark.objects.get(name="landmark2")
        self.assertEqual(0,lm1.order_num,
                         "Error: landmark1 order_num should be 0, instead is " + str(lm1.order_num))
        self.assertEqual(1,lm2.order_num,
                         "Error: landmark2 order_num should be 1, instead is " + str(lm2.order_num))


class TestMakerStartAndEndGame(TestCase):
    def setUp(self):
        HuntUser.objects.all().delete()
        Landmark.objects.all().delete()
        Game.objects.all().delete()
        game = Game(name="game",running=False)
        game.save()
        lm = Landmark(name="dummy", clue="dummy", question="dummy", answer="dummy", order_num=-1)
        lm.save()
        self.maker = gamemaker.GameMaker()
        self.maker.make_team(["team1","password1"])
        self.t = team.Team()
        lm1 = Landmark(name="landmark1", clue="clue1", question="question1", answer="answer1", order_num=-1)
        lm2 = Landmark(name="landmark2", clue="clue2", question="question2", answer="answer2", order_num=-1)
        lm1.save()
        lm2.save()

    def test_start_game_no_landmarks(self):
        self.assertEqual("No landmarks are part of the game!",self.maker.start_game(),
                         "Error: game can't start if the game wasn't created")
        self.assertFalse(Game.objects.get(name="game").running)

    def test_start_game(self):
        self.maker.create_game(["landmark1"])
        self.assertEqual("Game started!",self.maker.start_game(),
                         "Error: game should have been started")
        self.assertTrue(Game.objects.get(name="game").running)
        cur = HuntUser.objects.get(name="team1").current_landmark
        lm1 = Landmark.objects.get(name="landmark1")
        self.assertEqual(lm1,cur,
                         "Error: team1 current landmark should have updated to landmark1, instead is " + cur.name)

    def test_start_game_already_started(self):
        self.maker.create_game(["landmark1"])
        self.maker.start_game()
        self.assertEqual("Game already started!",self.maker.start_game(),
                         "Error: game cannot be started twice")

    def test_end_game_not_started(self):
        self.maker.create_game(["landmark1"])
        self.assertEqual("There is no game running!",self.maker.end_game(),
                         "Error: a game that hasn't started can't end")

    def test_end_game_started(self):
        self.maker.create_game(["landmark1"])
        self.maker.start_game()
        self.assertEqual("Game over",self.maker.end_game(),
                         "Error: game should have ended when end_game() was called")
        self.assertFalse(Game.objects.get(name="game").running)

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestMakerAddLandmark))
suite.addTest(unittest.makeSuite(TestMakerDisplayLandmarks))
suite.addTest(unittest.makeSuite(TestMakerRemoveLandmarks))
suite.addTest(unittest.makeSuite(TestMakerCheckStatus))
suite.addTest(unittest.makeSuite(TestMakerDisplayMenu))
suite.addTest(unittest.makeSuite(TestMakerCreateTeam))
suite.addTest(unittest.makeSuite(TestMakerEditTeams))
# suite.addTest(unittest.makeSuite(TestMakerSetPenalties))
# suite.addTest(unittest.makeSuite(TestStartGame))
# suite.addTest(unittest.makeSuite(TestMakerEndGame))
suite.addTest(unittest.makeSuite(TestMakerDeleteTeam))
suite.addTest(unittest.makeSuite(TestMakerCreateGame))
suite.addTest(unittest.makeSuite(TestMakerStartAndEndGame))


runner = unittest.TextTestRunner()
res=runner.run(suite)
print(res)
print("*"*20)
for i in res.failures: print(i[1])
