import team
import database
import landmark
import gamemaker
from Interface.models import HuntUser, Landmark,Game
from django.test import TestCase
import unittest
from datetime import datetime, timedelta

# class TestTeamEditUsername(TestCase):
#    def setUp(self):
#        self.team1 = HuntUser.objects.get(name="team1")
#    def test_edit_username_no_team_logged_in(self):
#        self.assertFalse(self.team1.edit_username(["bestteam"]), "Error: cannot edit username with no team logged in")
#    def test_edit_username(self):
#        self.assertEqual("Username successfully changed to bestteam", self.team1.edit_username(["bestteam"]),
#                         "Error: username change did not return True")
#        self.assertEqual("bestteam", self.team1.username, "Error: username was not changed")
#        teams = HuntUser.objects.all()
#        for team in teams:
#            self.assertFalse(HuntUser.objects.get(name=team) is "team1", "The old team's username still exists")


class TestTeamDisplayStatus(TestCase):
    def setUp(self):
        dummy_landmark = Landmark(name="dummy",clue="dummy",question="dummy",answer="dummy",order_num=-1)
        dummy_landmark.save()
        Game.objects.all().delete()
        game = Game(name="game", running=False)
        game.save()
        self.maker = gamemaker.GameMaker()
        self.maker.make_team(["team1","password1"])
        self.maker.make_team(["team2","password1"])
        self.maker.add_landmark(["landmark1","clue1","q1","a1"])
        self.maker.add_landmark(["landmark2","clue2","q2","a2"])
        self.maker.create_game(["landmark1", "landmark2"])
        self.t = team.Team()

    def test_team_default_display(self):
        self.assertEqual("Team: team1\nScore: 0\nPenalties: 0\nThere is currently no game running",
                         self.t.display_status("team1"),"Error: incorrect default status")

    def test_team_display_game_running(self):
        self.maker.start_game()
        self.assertEqual("Team: team1\nScore: 0\nPenalties: 0\nCurrent landmark: start\n",
                         self.t.display_status("team1"),"Error: incorrect status when game is running")

    def test_team_display_game_finished(self):
        self.maker.start_game()
        self.t.request_question("team1")
        self.t.answer_question("team1",["a1"])
        self.t.request_question("team1")
        self.t.answer_question("team1", ["a2"])
        self.assertEqual("Team: team1\nScore: 70\nPenalties: 0\n\nYour team has finished the game\nFinal score: 70\n",
                         self.t.display_status("team1"),"Error: incorrect status when team has finished game")


class TestTeamEditPassword(TestCase):
    def setUp(self):
        dummy_landmark = Landmark(name="dummy",clue="dummy",question="dummy",answer="dummy",order_num=-1)
        dummy_landmark.save()
        team1 = HuntUser(name="team1", password="password1", current_landmark=dummy_landmark)
        team1.save()
        self.t = team.Team()

    def test_edit_password(self):
        self.assertEqual("Password successfully changed to kittens", self.t.edit_password("team1",["kittens"]),
                         "Error: password change did not return True")
        self.assertEqual("kittens", HuntUser.objects.get(name="team1").password, "Error: password was not changed")


class TestTeamCommands(TestCase):
    def setUp(self):
        self.t = team.Team()
        self.assertEqual("Options\n\nlog out\ndisplay status\nedit username\nedit password\nanswer\nrequest clue\n",
                         self.t.display_menu(),"Error: incorrect menu displayed")


class TestTeamAnswerQuestions(TestCase):
    def setUp(self):
        Landmark.objects.all().delete()
        lm_dum = Landmark(name="dummy", clue="dummy", question="dummy", answer="dummy", order_num=-1)
        lm_dum.save()
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

    def test_answer_did_not_ask_for_question(self):
        self.maker.start_game()
        self.assertEqual("You need to receive the question first!",self.t.answer_question("team1",["a1"]),
                         "Error: need to prompt the user for the question first")


    def test_answer_game_time_up(self):
        self.maker.start_game()
        team1 = HuntUser.objects.get(name="team1")
        period = timedelta(hours=1)
        game = Game.objects.get(name="game")
        game.time_start -= period
        game.save()
        self.assertEqual("Time is up!",self.t.answer_question("team1",["a1"]),
                         "Error: game should have ended when 1 hour passed")
        game = Game.objects.get(name="game")
        self.assertFalse(game.running, "Error: game_running should be false when 1 hour passed")


    def test_answer_game_at_end(self):
        self.maker.start_game()
        team1 = HuntUser.objects.get(name="team1")
        team1.game_ended = True
        team1.question_requested = True
        team1.save()
        self.assertEqual("You've already finished the game!",self.t.answer_question("team1",["a1"]),
                         "Error: shouldn't be able to receive clue when at the end of the game")

    def test_correct_one_landmark(self):
        self.maker.start_game()
        team1 = HuntUser.objects.get(name="team1")
        team1.question_requested = True
        team1.save()
        self.assertEqual("Correct answer given! You can now request the clue for the next landmark",
                         self.t.answer_question("team1",["a1"]),
                         "Error: should have returned True when answered correctly")
        self.assertEqual(1,HuntUser.objects.get(name="team1").current_landmark.order_num,
                         "Error: current landmark was not updated from 0 to 1 when answer was correct")

    def test_team_incorrect_answer(self):
        self.maker.start_game()
        team1 = HuntUser.objects.get(name="team1")
        team1.question_requested = True
        team1.save()
        self.assertEqual("Incorrect answer, please try again",
                         self.t.answer_question("team1","wrong answer"),
                         "Error: should have returned False when answered incorrectly")
        self.assertEqual(0,HuntUser.objects.get(name="team1").current_landmark.order_num,
                         "Error: current landmark should remain 0 when answer was incorrect")

    def test_correct_end_game(self):
        self.maker.start_game()
        team1 = HuntUser.objects.get(name="team1")
        team1.question_requested = True
        team1.save()
        self.t.answer_question("team1", ["a1"])
        self.t.request_question("team1")
        self.assertEqual("Congrats! You've reached the end of the game!",self.t.answer_question("team1",["a2"]),
                         "Error: should have indicated that the game has ended")
        self.assertTrue(HuntUser.objects.get(name="team1").game_ended,
                        "Error: game_ended should be true at end of game")


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


class TestTeamRequestQuestion(TestCase):
    def setUp(self):
        Landmark.objects.all().delete()
        lm_dum = Landmark(name="dummy", clue="dummy", question="dummy", answer="dummy", order_num=-1)
        lm_dum.save()
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

    def test_request_question_no_game_running(self):
        self.assertEqual("There is no game running!", self.t.request_question("team1"),
                         "Error: can't get question if there is no game running")

    def test_request_question_good(self):
        self.maker.start_game()
        self.assertEqual("q1",self.t.request_question("team1"),
                         "Error: question should have been received")
        team1 = HuntUser.objects.get(name="team1")
        self.assertTrue(team1.question_requested, "Error: should have marked that the question was requested")

    def test_request_question_time_up(self):
        self.maker.start_game()
        team1 = HuntUser.objects.get(name="team1")
        period = timedelta(hours=1)
        game = Game.objects.get(name="game")
        game.time_start -= period
        game.save()
        self.assertEqual("Time is up!",self.t.request_question("team1"),
                         "Error: game should have ended when 1 hour passed")
        game = Game.objects.get(name="game")
        self.assertFalse(game.running, "Error: game_running should be false when 1 hour passed")

    def test_request_question_game_at_end(self):
        self.maker.start_game()
        team1 = HuntUser.objects.get(name="team1")
        team1.game_ended = True
        team1.save()
        self.assertEqual("You've already finished the game!",self.t.request_question("team1"),
                         "Error: can't get a question when team is at the end of the game")


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

    def test_request_no_game_running(self):
        self.assertEqual("There is no game running!", self.t.request_clue("team1"),
                         "Error: can't get a clue when there is no game running")

    def test_request_no_landmarks_added(self):
        self.game.running = True
        self.game.save()
        self.assertEqual("Not at a valid landmark",self.t.request_clue("team1"),
                         "Error: cannot get a clue when there are no landmarks")

    def test_request_good(self):
        self.maker.add_landmark(["landmark1","clue1","q1","a1"])
        self.maker.create_game(["landmark1"])
        self.maker.start_game()
        self.assertEqual("clue1", self.t.request_clue("team1"),
                         "Error: should have returned clue1")

    def test_clue_time_up(self):
        self.maker.add_landmark(["landmark1","clue1","q1","a1"])
        self.maker.create_game(["landmark1"])
        self.maker.start_game()
        team1 = HuntUser.objects.get(name="team1")
        period = timedelta(hours=1)
        game = Game.objects.get(name="game")
        game.time_start -= period
        game.save()
        self.assertEqual("Time is up!",self.t.request_clue("team1"),
                         "Error: game should have ended when 1 hour passed")
        game = Game.objects.get(name="game")
        self.assertFalse(game.running, "Error: game_running should be false when 1 hour passed")

    def test_request_at_end(self):
        self.maker.add_landmark(["landmark1", "clue1", "q1", "a1"])
        self.maker.create_game(["landmark1"])
        self.maker.start_game()
        team1 = HuntUser.objects.get(name="team1")
        team1.game_ended = True
        team1.save()
        self.assertEqual("You've already finished the game!",self.t.request_clue("team1"),
                         "Error: shouldn't be able to receive clue when at the end of the game")


class TestHelperFunctions(TestCase):
    def setUp(self):
        Landmark.objects.all().delete()
        lm_dum = Landmark(name="dummy", clue="dummy", question="dummy", answer="dummy", order_num=-1)
        lm_dum.save()
        Game.objects.all().delete()
        game = Game(name="game", running=False)
        game.save()
        self.t = team.Team()
        self.maker = gamemaker.GameMaker()
        self.maker.make_team(["team1","password1"])
        self.maker.make_team(["team2","password2"])
        self.maker.make_team(["team3","password3"])
        self.maker.add_landmark(["landmark1", "clue1", "q1", "a1"])
        self.maker.create_game(["landmark1"])
        self.maker.start_game()

    def test_game_over_start(self):
        self.assertFalse(self.t.check_game_over(), "Error: game shouldn't be over at the start of the game!")

    def test_game_over_one_team(self):
        self.t.answer_question("team1",["a1"])
        self.assertTrue(self.t.check_first("team1"),
                        "Error: check_first should return True when team1 reaches end game")
        self.assertFalse(self.t.check_game_over(),
                         "Error: check_game_over should return False since teams 2 and 3 have not reached the end")

    def test_game_over_two_teams(self):
        self.t.request_question("team1")
        self.t.request_question("team2")
        self.t.answer_question("team1", ["a1"])
        self.t.answer_question("team2", ["a1"])
        self.assertFalse(self.t.check_first("team2"),
                         "Error: check_first should return False when team2 reaches end game after team1")
        self.assertFalse(self.t.check_game_over(),
                         "Error: check_game_over should return False since team3 has not reached the end")

    def test_game_over_all_teams(self):
        self.t.request_question("team1")
        self.t.answer_question("team1", ["a1"])
        self.t.request_question("team2")
        self.t.answer_question("team2", ["a1"])
        self.t.request_question("team3")
        self.t.answer_question("team3", ["a1"])
        self.assertFalse(self.t.check_first("team3"),
                         "Error: check_first should return False when team3 reaches end game last")
        self.assertTrue(self.t.check_game_over(),
                        "Error: check_game_over should return True since all three teams reached the end")

    def test_game_over_time_up(self):
        game = Game.objects.get(name="game")
        period = timedelta(hours=1)
        game.time_start -= period
        game.save()
        self.assertTrue(self.t.check_time_up(), "Error: game should have ended since the time is up")
        game = Game.objects.get(name="game")
        self.assertFalse(game.running, "Error: game_running should be False since game is over")


class TestScoreSystem(TestCase):
    def setUp(self):
        Landmark.objects.all().delete()
        lm_dum = Landmark(name="dummy", clue="dummy", question="dummy", answer="dummy", order_num=-1)
        lm_dum.save()
        Game.objects.all().delete()
        game = Game(name="game", running=False)
        game.save()
        self.t = team.Team()
        self.maker = gamemaker.GameMaker()
        self.maker.make_team(["team1","password1"])
        self.maker.make_team(["team2","password2"])
        self.maker.make_team(["team3","password3"])
        self.maker.add_landmark(["landmark1", "clue1", "q1", "a1"])
        self.maker.create_game(["landmark1"])
        self.maker.start_game()

    def test_score_end_game_team_one(self):
        self.t.request_question("team1")
        self.t.answer_question("team1", ["a1"])
        team1 = HuntUser.objects.get(name="team1")
        self.assertEqual(60,team1.score, "Error: point total for team1 was " + str(team1.score) + " instead of 60")

    def test_score_end_game_team_two(self):
        self.t.request_question("team1")
        self.t.request_question("team2")
        self.t.answer_question("team1", ["a1"])
        self.t.answer_question("team2", ["a1"])
        team2 = HuntUser.objects.get(name="team2")
        self.assertEqual(10, team2.score, "Error: point total for team2 was " + str(team2.score) + " instead of 10")

    def test_score_end_game_team_three(self):
        self.t.request_question("team1")
        self.t.request_question("team2")
        self.t.request_question("team3")
        self.t.answer_question("team1", ["a1"])
        self.t.answer_question("team2", ["a1"])
        self.t.answer_question("team3", ["a1"])
        team3 = HuntUser.objects.get(name="team3")
        self.assertEqual(10, team3.score,"Error: point total for team3 was " + str(team3.score) + " instead of 10")

    def test_score_wrong_answer(self):
        self.t.request_question("team1")
        for x in range(0, 5):
            self.t.answer_question("team1", ["incorrect"])
        team1 = HuntUser.objects.get(name="team1")
        self.assertEqual(5, team1.penalties, "Error: penalties was " + str(team1.penalties) + " instead of 5")

    def test_score_too_much_time(self):
        self.t.request_question("team1")
        team1 = HuntUser.objects.get(name="team1")
        period = timedelta(minutes=5)
        team1.time_requested -= period
        team1.save()
        self.t.answer_question("team1", ["a1"])
        team1 = HuntUser.objects.get(name="team1")
        self.assertEqual(5, team1.penalties, "Error: penalties was " + str(team1.penalties) + " instead of 5")


suite = unittest.TestSuite()
# suite.addTest(unittest.makeSuite(TestTeamEditUsername))
suite.addTest(unittest.makeSuite(TestTeamEditPassword))
suite.addTest(unittest.makeSuite(TestTeamCommands))
suite.addTest(unittest.makeSuite(TestTeamRequestQuestion))
suite.addTest(unittest.makeSuite(TestTeamAnswerQuestions))
suite.addTest(unittest.makeSuite(TestTeamRequestClue))
suite.addTest(unittest.makeSuite(TestHelperFunctions))
suite.addTest(unittest.makeSuite(TestScoreSystem))

runner = unittest.TextTestRunner()
res=runner.run(suite)
print(res)
print("*"*20)
for i in res.failures: print(i[1])