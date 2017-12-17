import team
import database
import landmark
import gamemaker
from Interface.models import HuntUser, Landmark,Game
from django.test import TestCase
import unittest

#class TestTeamEditUsername(TestCase):
#    def setUp(self):
#        self.team1 = HuntUser.objects.get(name="team1")
#    def test_edit_username_no_team_logged_in(self):
#        self.assertFalse(self.team1.edit_username(["bestteam"]), "Error: cannot edit username with no team logged in")
#    def test_edit_username(self):
#        self.assertEqual("Username successfully changed to bestteam", self.team1.edit_username(["bestteam"]), "Error: username change did not return True")
#        self.assertEqual("bestteam", self.team1.username, "Error: username was not changed")
#        teams = HuntUser.objects.all()
#        for team in teams:
#            self.assertFalse(HuntUser.objects.get(name=team) is "team1", "The old team's username still exists")


class TestTeamEditPassword(TestCase):
    def setUp(self):
        dummy_landmark = Landmark(name="dummy",clue="dummy",question="dummy",answer="dummy",order_num=-1)
        dummy_landmark.save()
        team1 = HuntUser(name="team1", password="password1", current_landmark=dummy_landmark)
        team1.save()
        self.t = team.Team()

    def test_edit_password(self):
        self.assertEqual("Password successfully changed to kittens", self.t.edit_password("team1",["kittens"]), "Error: password change did not return True")
        self.assertEqual("kittens", HuntUser.objects.get(name="team1").password, "Error: password was not changed")


class TestTeamCommands(TestCase):
    def setUp(self):
        self.t = team.Team()
        self.assertEqual("Options\n\nlog out\ndisplay status\nedit username\nedit password\nanswer\nrequest clue\n",
                         self.t.display_menu(),"Error: incorrect menu displayed")


class TestTeamAnswerQuestions(TestCase):
    def setUp(self):
        Landmark.objects.all().delete()
        lm = Landmark(name="dummy", clue="dummy", question="dummy", answer="dummy", order_num=-1)
        lm.save()

        Game.objects.all().delete()
        game = Game(name="game", running=False)
        game.save()

        self.t = team.Team()
        self.maker = gamemaker.GameMaker()
        self.maker.make_team(["team1","password1"])
        self.maker.make_team(["team2","password1"])
        self.maker.add_landmark(["landmark1","clue1","q1","a1"])
        self.maker.add_landmark(["landmark2","clue2","q2","a2"])
        self.maker.create_game(["landmark1", "landmark2"])

    def test_answer_no_game_running(self):
        self.assertEqual("There is no game running!",self.t.answer_question("team1",["a1"]),
                         "Error: cannot answer a question when there is no game running")

    def test_correct_one_landmark(self):
        self.maker.start_game()
        self.assertEqual("Correct answer given! You can now request the clue for the next landmark",
                         self.t.answer_question("team1",["a1"]),
                         "Error: should have returned True when answered correctly")
        self.assertEqual(1,HuntUser.objects.get(name="team1").current_landmark.order_num,
                         "Error: current landmark was not updated from 0 to 1 when answer was correct")

    def test_team_incorrect_answer(self):
        self.maker.start_game()
        self.assertEqual("Incorrect answer, please try again",
                         self.t.answer_question("team2","wrong answer"),
                         "Error: should have returned False when answered incorrectly")
        self.assertEqual(0,HuntUser.objects.get(name="team2").current_landmark.order_num,
                         "Error: current landmark should remain 0 when answer was incorrect")

    def test_correct_end_game(self):
        self.maker.start_game()
        self.t.answer_question("team1", ["a1"])
        self.assertEqual("Congrats! You win!",self.t.answer_question("team1",["a2"]),
                         "Error: should have indicated that the team has won")
        self.assertEqual(1,HuntUser.objects.get(name="team1").current_landmark.order_num,
                         "Error: current landmark was not updated from 0 to 1 when answer was correct")


class TestTeamInitialization(TestCase):
    def setUp(self):
        Landmark.objects.all().delete()
        dummy_landmark = Landmark(name="dummy", clue="dummy", question="dummy", answer="dummy", order_num=-1)
        dummy_landmark.save()
        self.team1 = HuntUser(name="team1", password="password1", current_landmark=dummy_landmark)
        self.team1.save()
        self.assertEqual("team1",self.team1.name,"Error: username not initialized correctly")

    def test_initial_password(self):
        self.assertEqual("password1",self.team1.password,"Error: password not initialized correctly")

    def test_initial_landmark(self):
        self.assertEqual(-1,self.team1.current_landmark.order_num,"Error: current landmark should be initialized to -1")


class TestTeamRequestClue(TestCase):
    def setUp(self):
        Landmark.objects.all().delete()
        dummy_landmark = Landmark(name="dummy", clue="dummy", question="dummy", answer="dummy", order_num=-1)
        dummy_landmark.save()
        team1 = HuntUser(name="team1", password="password1", current_landmark=dummy_landmark)
        team1.save()
        Game.objects.all().delete()
        self.game = Game(name="game", running=False)
        self.game.save()
        self.t = team.Team()
        self.maker = gamemaker.GameMaker()

    def test_request_no_landmarks_added(self):
        self.game.running = True
        self.game.save()
        self.assertEqual("Not at a valid landmark",self.t.request_clue("team1"),
                         "Error: cannot answer a question when there are no landmarks")

    def test_request_good(self):
        self.maker.add_landmark(["landmark1","clue1","q1","a1"])
        self.maker.create_game(["landmark1"])
        self.maker.start_game()
        self.assertEqual("clue1", self.t.request_clue("team1"),
                         "Error: should have returned clue1")


suite = unittest.TestSuite()

#suite.addTest(unittest.makeSuite(TestTeamEditUsername))
suite.addTest(unittest.makeSuite(TestTeamEditPassword))
suite.addTest(unittest.makeSuite(TestTeamCommands))
suite.addTest(unittest.makeSuite(TestTeamAnswerQuestions))
suite.addTest(unittest.makeSuite(TestTeamRequestClue))

runner = unittest.TextTestRunner()
res=runner.run(suite)
print(res)
print("*"*20)
for i in res.failures: print(i[1])