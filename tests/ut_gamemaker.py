from django.test import TestCase
from Interface.models import HuntUser, Landmark, Penalty, Game
import unittest
import gamemaker
import team
import landmark

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
        self.game_maker = gamemaker.GameMaker()

    def test_single_team(self):
        self.game_maker.make_team("Team1 password")
        self.assertEquals(self.game_maker.display_status(), "No teams!", "Bad single team return")

    def test_multiple_teams(self):
        self.game_maker.make_team("Team1 password")
        self.game_maker.make_team("team2 password")
        self.assertEqual(self.game_maker.display_status(), "No teams!", "Cannot find entries in two team list")

class TestMakerDisplayMenu(TestCase):
    def setUp(self):
        self.game_maker = gamemaker.GameMaker()

    def test_display_menu(self):
        self.assertEqual(self.game_maker.display_menu(), "Options\n\ndisplaystatus\nmaketeam [team name], [team password]\neditteam [team name to edit], [new team name], [new team password]\n" \
        "addlandmark [name], [clue], [question], [answer]\ndisplaylandmarks\nremovelandmark [name]\nsetpenalties [new time penalty], [new guess penalty]\n" \
        "creategame [landmark name]...\nstartgame\nendgame\nlogout\n", "Wrong menu")

class TestMakerCreateTeam(TestCase):
    def setUp(self):
        self.game_maker = gamemaker.GameMaker()

    def test_single_team(self):
        self.game_maker.make_team("Team1 password")
        self.assertEquals(self.game_maker.display_status(), "No teams!", "Bad single team return")

    def test_multiple_teams(self):
        self.game_maker.make_team("Team1 password")
        self.game_maker.make_team("team2 password")
        self.assertEqual(self.game_maker.display_status(), "No teams!", "Cannot find entries in two team list")

class TestMakerEditTeams(TestCase):
    def setUp(self):
        self.game_maker = gamemaker.GameMaker()

    def test_single_team(self):
        self.game_maker.make_team(["Team1 password"])
        self.assertEquals(self.game_maker.edit_team(["Team1", "team2", "passnew"]), "Could not find that team!", "Bad single team edit")

    def test_multiple_teams(self):
        self.game_maker.make_team("Team1 password")
        self.game_maker.make_team("team2 password")
        self.assertEquals(self.game_maker.edit_team(["Team1", "team", "passnew"]), "Could not find that team!",
                          "Bad single team edit")
        self.assertEquals(self.game_maker.edit_team(["team2", "team3", "passnew"]), "Could not find that team!",
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

#class TestMakerLogin(TestCase):
#     def setUp(self):
#         self.maker1 = HuntUser.objects.get(name="maker")
#         self.maker1.password = "password"
#         self.maker1.save()
#
#     def test_bad_login(self):
#         self.assertEqual(self.maker1.login("Notvalidusername","Notvalidpassword"), False, "Bad response to invalid login")
#         self.assertEqual(self.maker1.display_status(), None, "Current user is not null")
#     def test_good_login(self):
#         self.assertEqual(self.maker1.login("maker","password"), True, "Maker should have logged in")
#         self.assertEqual(self.maker1.display_status, "Team maker", "Current user should be maker")
#     def test_good_login_while_logged_in(self):
#         self.assertEqual(self.maker1.login("maker","password"), False, "Bad response to second login attempt")
#
#
# class TestMakerLogout(TestCase):
#     def setUp(self):
#         self.maker1 = HuntUser.objects.get(name="maker")
#         self.maker1.password = "password"
#         self.maker1.save()
#
#     def test_logout_while_not_logged_in(self):
#         self.assertEqual(self.maker1.logout(), False, "Bad response to maker logging out while not logged in")
#     def test_good_logout(self):
#         self.maker1.login("maker", "password")
#         self.assertEqual(self.maker1.logout(), True, "Bad response to maker logging out correctly")
#     def test_current_user_is_not_maker(self):
#         self.maker1.login("maker","password")
#         self.maker1.logout()
#         self.assertEqual(self.database.get_current_user(), None, "Current user is not null after logging out")
#
# class TestMakerCreateTeam(TestCase):
#     def test_single_team(self):
#         self.game_maker.make_team("Team1 password")
#         self.assertEquals(self.game_maker.display_status(), "No teams!", "Bad single team return")
#
#
#     def test_multiple_teams(self):
#         self.game_maker.make_team("Team1 password")
#         self.game_maker.make_team("team2 password")
#         self.assertEqual(self.game_maker.display_status(), "No teams!", "Cannot find entries in two team list")
#
# class TestMakerCreateTeam(TestCase):
#     def setUp(self):
#         self.game_maker = gamemaker.GameMaker()
#
#     def test_add_first_team(self):
#         self.game_maker.make_team("Team1 password")
#
#         def test_add_bad_team_no_space(self):
#             input = ["addteam", "Team1password"]
#             self.assertEqual(self.maker1.make_team(input), "Invalid input!", "Invalid input (not enough spaces) accepted")
#             self.team1 = self.database.get_teams()
#             self.assertEqual(len(self.team1), 0, "Team added but should not have been!")
#
#         def test_add_bad_team_3_spaces(self):
#             input = ["addteam", "Team1", "password", " "]
#             self.assertEqual(self.maker1.make_team(input), "Invalid input!", "Invalid input (too many spaces) accepted")
#             self.team1 = self.database.get_teams()
#             self.assertEqual(len(self.team1), 0, "Team added but should not have been!")
#
#         def test_add_second_team(self):
#             input = ["addteam", "Team1", "password1"]
#             self.assertEqual(self.maker1.make_team(input), "Added Team1", "First team return not correct 2 teams")
#             input = ["addteam", "team2", "password2"]
#             self.assertEqual(self.maker1.make_team(input), "Added team2", "Second team return not correct 2 teams")
#             self.teams = self.database.get_teams()
#             self.assertEqual(self.teams[0].username, "Team1", "First team name not added correctly in 2 team list")
#             self.assertEqual(self.teams[1].username, "team2", "Second team name not added correctly")
#             self.assertEqual(self.teams[0].password, "password1", "First team password not added correctly 2 teams")
#             self.assertEqual(self.teams[1].password, "password2", "Second team password not added correctly")
#             self.assertEqual(len(self.teams), 2, "Team list length incorrect!")
#
#         def test_add_second_team_one_no_space(self):
#             input = ["addteam", "Team1password"]
#             self.assertEqual(self.maker1.make_team(input), "Invalid input!", "Invald input (not enough spaces) accepted 2 teams")
#             input = ["addteam", "team2", "password"]
#             self.assertEqual(self.maker1.make_team(input), "Added team2", "Second team not added correctly")
#             self.team2 = self.database.get_teams()
#             self.assertEqual(self.team2[0].username, "team2", "Team username in list not correct")
#             self.assertEqual(self.team2[0].password, "password", "Team password in list not correct")
#             self.assertEqual(len(self.team2), 1, "Team list length incorrect!")
#
#         def test_add_second_team_too_many_spaces(self):
#             input = ["addteam", "Team1", "password", " "]
#             self.assertEqual(self.maker1.make_team(input), "Invalid input!", "Invalid input (too many spaces) accepted 2 teams")
#             input = ["addteam", "team2", "password"]
#             self.assertEqual(self.maker1.make_team(input), "Added team2", "Second team not added correctly")
#             self.team2 = self.database.get_teams()
#             self.assertEqual(self.team2[0].username, "team2", "Team username in list not correct")
#             self.assertEqual(self.team2[0].password, "password", "Team password in list not correct")
#         self.assertEqual(len(self.team2), 1, "Team list length incorrect!")

    # class TestMakerCreateTeam(TestCase):
    #     def setUp(self):
    #         self.game_maker = gamemaker.GameMaker()
    #
    #         def test_add_first_team(self):
    #             input = ["addteam", "Team1", "password"]
    #             self.assertEqual(self.maker1.make_team(input), "Added Team1",
    #                              "Invalid return value for valid team added")
    #             self.team1 = self.database.get_teams()
    #             self.assertEqual(self.team1[0].username, "Team1", "First team name not added correctly")
    #             self.assertEqual(self.team1[0].password, "password", "First team password not added correctly")
    #             self.assertEqual(len(self.team1), 1, "Team list length incorrect!")
    #
    #         def test_add_bad_team_no_space(self):
    #             input = ["addteam", "Team1password"]
    #             self.assertEqual(self.maker1.make_team(input), "Invalid input!",
    #                              "Invalid input (not enough spaces) accepted")
    #             self.team1 = self.database.get_teams()
    #             self.assertEqual(len(self.team1), 0, "Team added but should not have been!")
    #
    #         def test_add_bad_team_3_spaces(self):
    #             input = ["addteam", "Team1", "password", " "]
    #             self.assertEqual(self.maker1.make_team(input), "Invalid input!",
    #                              "Invalid input (too many spaces) accepted")
    #             self.team1 = self.database.get_teams()
    #             self.assertEqual(len(self.team1), 0, "Team added but should not have been!")
    #
    #         def test_add_second_team(self):
    #             input = ["addteam", "Team1", "password1"]
    #             self.assertEqual(self.maker1.make_team(input), "Added Team1", "First team return not correct 2 teams")
    #             input = ["addteam", "team2", "password2"]
    #             self.assertEqual(self.maker1.make_team(input), "Added team2", "Second team return not correct 2 teams")
    #             self.teams = self.database.get_teams()
    #             self.assertEqual(self.teams[0].username, "Team1", "First team name not added correctly in 2 team list")
    #             self.assertEqual(self.teams[1].username, "team2", "Second team name not added correctly")
    #             self.assertEqual(self.teams[0].password, "password1", "First team password not added correctly 2 teams")
    #             self.assertEqual(self.teams[1].password, "password2", "Second team password not added correctly")
    #             self.assertEqual(len(self.teams), 2, "Team list length incorrect!")
    #
    #         def test_add_second_team_one_no_space(self):
    #             input = ["addteam", "Team1password"]
    #             self.assertEqual(self.maker1.make_team(input), "Invalid input!",
    #                              "Invald input (not enough spaces) accepted 2 teams")
    #             input = ["addteam", "team2", "password"]
    #             self.assertEqual(self.maker1.make_team(input), "Added team2", "Second team not added correctly")
    #             self.team2 = self.database.get_teams()
    #             self.assertEqual(self.team2[0].username, "team2", "Team username in list not correct")
    #             self.assertEqual(self.team2[0].password, "password", "Team password in list not correct")
    #             self.assertEqual(len(self.team2), 1, "Team list length incorrect!")
    #
    #         def test_add_second_team_too_many_spaces(self):
    #             input = ["addteam", "Team1", "password", " "]
    #             self.assertEqual(self.maker1.make_team(input), "Invalid input!",
    #                              "Invalid input (too many spaces) accepted 2 teams")
    #             input = ["addteam", "team2", "password"]
    #             self.assertEqual(self.maker1.make_team(input), "Added team2", "Second team not added correctly")
    #             self.team2 = self.database.get_teams()
    #             self.assertEqual(self.team2[0].username, "team2", "Team username in list not correct")
    #             self.assertEqual(self.team2[0].password, "password", "Team password in list not correct")
    #
    #         self.assertEqual(len(self.team2), 1, "Team list length incorrect!")
#
# class TestMakerEditTeams(TestCase):
#     def setUp(self):
#         self.database = database.Database()
#         self.maker1 = gamemaker.GameMaker(self.database)
#
#     def test_edit_single_team(self):
#         self.database.add_team(team.Team("Team1", "password", self.database))
#         self.assertEqual(self.maker1.edit_team(["editteam", "Team1", "NewTeam1", "NewPassword"]),
#                     "Team1 changed to NewTeam1 with password NewPassword", "Valid edit failed")
#         self.team1 = self.database.get_teams()
#         self.assertEqual(self.team1[0].username, "NewTeam1", "Single team name edit failed")
#         self.assertEqual(self.team1[0].password, "NewPassword", "Single team password edit failed")
#         self.assertEqual(len(self.team1), 1, "Team list length incorrect!")
#
#     def test_edit_single_team_no_spaces(self):
#         self.database.add_team(team.Team("Team1", "password", self.database))
#         self.assertEqual(self.maker1.edit_team(["editteamTeam1NewTeam1NewPassword"]), "Invalid input!",
#                          "Edit with no spaces didn't fail!")
#         self.team1 = self.database.get_teams()
#         self.assertEqual(len(self.team1), 1, "Team list length incorrect!")
#
#     def test_edit_two_team(self):
#         self.database.add_team(team.Team("Team1", "password1", self.database))
#         self.database.add_team(team.Team("team2", "password2", self.database))
#         self.assertEqual(self.maker1.edit_team(["editteam", "Team1", "NewTeam1", "NewPassword1"]),
#                          "Team1 changed to NewTeam1 with password NewPassword1", "Bad edit 1")
#         self.assertEqual(self.maker1.edit_team(["editteam","team2", "NewTeam2", "NewPassword2"]),
#                          "team2 changed to NewTeam2 with password NewPassword2", "Bad edit 2")
#         self.teams = self.database.get_teams()
#         self.assertEqual(self.teams[0].username, "NewTeam1", "Double team first name edit failed")
#         self.assertEqual(self.teams[0].password, "NewPassword1", "Double team first password edit failed")
#         self.assertEqual(self.teams[1].username, "NewTeam2", "Double team second name edit failed")
#         self.assertEqual(self.teams[1].password, "NewPassword2", "Double team second password edit failed")
#         self.assertEqual(len(self.teams), 2, "Team list length incorrect!")
#
#     def test_edit_no_team(self):
#         self.assertEqual(self.maker1.edit_team(["editteam", "someteam", "NewTeam1", "NewPassword"]), "Could not find that team!",
#                          "No team, but found")
#
#     def test_bad_edit_with_team_valid(self):
#         self.database.add_team(team.Team("Team1", "password", self.database))
#         self.assertEqual(self.maker1.edit_team(["editteam", "NotATeam", "blah", "bablah"]), "Could not find that team!", "Wrong team found")
#
#     def test_bad_edit_with_team_invalid_not_enough_spaces(self):
#         self.database.add_team(team.Team("Team1", "password", self.database))
#         self.assertEqual(self.maker1.edit_team(["Team1"]), "Invalid input!", "Invalid input accepted! Not enough spaces")
#
#     def test_bad_edit_with_team_invalid_too_many_spaces(self):
#         self.database.add_team(team.Team("Team1", "password", self.database))
#         self.assertEqual(self.maker1.edit_team(["editteam", "Team1", "NewTeam1", "password1", " "]), "Invalid input!",
#                          "Invalid input accepted! Too many spaces")
#
#     def test_bad_edit_two_teams_invalid(self):
#         self.database.add_team(team.Team("Team1", "password1", self.database))
#         self.database.add_team(team.Team("team2", "password2", self.database))
#         self.assertEqual(self.maker1.edit_team(["editteam", "Team1NewTeam1", "password1"]), "Invalid input!",
#                                               "Invalid input accepted! Two teams")
#         self.assertEqual(self.maker1.edit_team(["editteam", "team2", "NewTeam2", "NewPassword2"]),
#                          "team2 changed to NewTeam2 with password NewPassword2", "Valid input not accepted! Two teams")
#         self.teams = self.database.get_teams()
#         self.assertEqual(self.teams[0].username, "Team1", "Invalid input changed team name!")
#         self.assertEqual(self.teams[0].password, "password1", "Invalid input changed team password!")
#         self.assertEqual(self.teams[1].username, "NewTeam2", "Valid input did not change team name!")
#         self.assertEqual(self.teams[1].password, "NewPassword2", "Valid input did not change team password!")
#
# class TestMakerSetPenalties(TestCase):
#     def setUp(self):
#         self.database = database.Database()
#         self.maker1 = gamemaker.GameMaker(self.database)
#
#     def test_valid(self):
#         self.assertEqual(self.maker1.set_penalties(["setpenalties", "15", "3"]), "Time penalty is 15 minutes and guess penalty is 3 guesses",
#                          "Valid penalties not set!")
#         self.assertEqual(self.database.get_time_penalty(), 15, "Time penalty not correct!")
#         self.assertEqual(self.database.get_guess_penalty(), 3, "Guess penalty not correct!")
#
#     def test_invalid_not_ints(self):
#         self.assertEqual(self.maker1.set_penalties(["setpenalties", "a", "b"]), "Invalid input! Need integers",
#                          "Invalid penalties set!")
#         self.assertEqual(self.database.get_time_penalty(), -1, "Time penalty not correct!")
#         self.assertEqual(self.database.get_guess_penalty(), -1, "Guess penalty not correct!")
#
#     def test_invalid_not_greater_than_0(self):
#         self.assertEqual(self.maker1.set_penalties(["setpenalties", "-1", "5"]), "Invalid input! Need integers greater than 0",
#                          "Invalid penalties set!")
#         self.assertEqual(self.database.get_time_penalty(), -1, "Time penalty not correct!")
#         self.assertEqual(self.database.get_guess_penalty(), -1, "Guess penalty not correct!")
#
#     def test_invalid_no_space(self):
#         self.assertEqual(self.maker1.set_penalties(["setpenalties", "36"]),
#                          "Bad spacing! Need one space between time penalty and guess penalty", "Invalid penalties set!")
#         self.assertEqual(self.database.get_time_penalty(), -1, "Time penalty not correct!")
#         self.assertEqual(self.database.get_guess_penalty(), -1, "Guess penalty not correct!")
#
#     def test_invalid_too_many_spaces(self):
#         self.assertEqual(self.maker1.set_penalties(["setpentalties", "15", "3", " "]),
#                          "Bad spacing! Need one space between time penalty and guess penalty", "Invalid penalties set!")
#         self.assertEqual(self.database.get_time_penalty(), -1, "Time penalty not correct!")
#         self.assertEqual(self.database.get_guess_penalty(), -1, "Guess penalty not correct!")
#
# class TestMakerLandmark(TestCase):
#     def setUp(self):
#         self.database = database.Database()
#         self.maker1 = gamemaker.GameMaker(self.database)
#         self.input1 = ["name1", "clue1", "question1", "answer1"]
#         self.input2 = ["name2", "clue2", "question2", "answer2"]
#
#     def test_add_landmark_empty(self):
#         self.maker1.add_landmark(self.input1)
#         self.assertEqual(self.database.get_landmarks()[0].get_name(), self.input1[0], "test_add_landmark_empty: Landmark name wasn't correct")
#         self.assertEqual(self.database.get_landmarks()[0].get_clue(), self.input1[1], "test_add_landmark_empty: Landmark clue wasn't correct")
#         self.assertEqual(self.database.get_landmarks()[0].get_question(), self.input1[2], "test_add_landmark_empty: Landmark question wasn't correct")
#         self.assertEqual(self.database.get_landmarks()[0].get_answer(), self.input1[3], "test_add_landmark_empty: Landmark answer wasn't correct")
#
#     def test_add_landmark_not_empty(self):
#         self.maker1.add_landmark(self.input1)
#         self.maker1.add_landmark(self.input2)
#         self.assertEqual(self.database.get_landmarks()[0].get_name(), self.input1[0], "test_add_landmark_not_empty: Landmark name wasn't correct")
#         self.assertEqual(self.database.get_landmarks()[0].get_clue(), self.input1[1], "test_add_landmark_not_empty: Landmark clue wasn't correct")
#         self.assertEqual(self.database.get_landmarks()[0].get_question(), self.input1[2], "test_add_landmark_not_empty: Landmark question wasn't correct")
#         self.assertEqual(self.database.get_landmarks()[0].get_answer(), self.input1[3], "test_add_landmark_not_empty: Landmark answer wasn't correct")
#         self.assertEqual(self.database.get_landmarks()[1].get_name(), self.input2[0], "test_add_landmark_not_empty: Landmark name wasn't correct")
#         self.assertEqual(self.database.get_landmarks()[1].get_clue(), self.input2[1], "test_add_landmark_not_empty: Landmark clue wasn't correct")
#         self.assertEqual(self.database.get_landmarks()[1].get_question(), self.input2[2], "test_add_landmark_not_empty: Landmark question wasn't correct")
#         self.assertEqual(self.database.get_landmarks()[1].get_answer(), self.input2[3], "test_add_landmark_not_empty: Landmark answer wasn't correct")
#
#
#     def test_remove_landmark_correct(self):
#         self.maker1.add_landmark(self.input1)
#         self.assertEqual(self.maker1.remove_landmark([self.input1[0]]), "Removed " + self.input1[0] + " from landmarks.", "test_delete_landmark_correct: Didn't delete correctly")
#
#     def test_remove_landmark_incorrect(self):
#         self.assertEqual(self.maker1.remove_landmark([self.input1[0]]), "Couldn't find landmark with name " + self.input1[0], "test_remove_landmark_incorrect: Shouldn't have deleted")
#
# class TestStartGame(TestCase):
#     def setUp(self):
#         self.database = database.Database()
#         self.maker1 = gamemaker.GameMaker(self.database)
#         self.team1 = team.Team("username1","password1",self.database)
#         self.landmark1 = landmark.Landmark("l1","c1","q1","a1")
#     def test_initial_value(self):
#         self.assertFalse(self.database.game_running,"Error: game_started should be initialized to False")
#     def test_start_game_no_one_logged_in(self):
#         self.assertEqual("Game can only be started by Gamemaker",self.maker1.start_game(),
#                          "Error: can't start a game when not logged in")
#         self.assertFalse(self.database.game_running,"Error: game_started should remain False")
#     def test_start_game_team_logged_in(self):
#         self.team1.login("username1","password1")
#         self.assertEqual("Game can only be started by Gamemaker",self.maker1.start_game(),
#                          "Error: can't start a game when not logged in")
#         self.assertFalse(self.database.game_running,"Error: game_started should remain False")
#     def test_start_game_no_landmarks(self):
#         self.maker1.login("maker","password")
#         self.assertEqual("Can't start when there are no landmarks in the game!",self.maker1.start_game(),
#                          "Error: game shouldn't start when there are no landmarks in the game")
#         self.assertFalse(self.database.game_running,
#                          "Error: game_started should remain False when there are no landmarks in the game")
#     def test_start_game_valid(self):
#         self.maker1.login("maker","password")
#         self.database.add_to_path(self.landmark1)
#         self.assertEqual("Game started!",self.maker1.start_game(),
#                          "Error: game should have been started when Gamemaker calls start_game()")
#         self.assertTrue(self.database.game_running,"Error: game_started should have been True")
#
# class TestMakerEndGame(TestCase):
#     def setUp(self):
#         self.database = database.Database()
#         self.maker1 = gamemaker.GameMaker(self.database)
#         self.team1 = team.Team("username1","password1",self.database)
#         self.landmark1 = landmark.Landmark("l1","c1","q1","a1")
#     def test_end_game_no_one_logged_in(self):
#         self.assertEqual("Can't prematurely end game when Gamemaker is not logged in",self.maker1.end_game(),
#                          "Error: when no one is logged in, end_game() cannot be executed")
#     def test_end_game_team_logged_in(self):
#         self.team1.login("username1","password1")
#         self.assertEqual("Can't prematurely end game when Gamemaker is not logged in",self.maker1.end_game(),
#                          "Error: when a team is logged in, end_game() cannot be executed")
#     def test_end_game_no_game_started(self):
#         self.maker1.login("maker","password")
#         self.assertEqual("Can't end the game if it hasn't started yet",self.maker1.end_game(),
#                          "Error: game can't be ended if it hasn't even begun")
#     def test_end_game_valid(self):
#         self.maker1.login("maker","password")
#         self.database.add_to_path(self.landmark1)
#         self.maker1.start_game()
#         self.assertEqual("Game over",self.maker1.end_game(),"Error: game wasn't ended properly by Gamemaker")
#         self.assertFalse(self.database.game_running)
#
# class TestMakerDeleteTeam(TestCase):
#     def setUp(self):
#         self.database = database.Database()
#         self.maker1 = gamemaker.GameMaker(self.database)
#
#     def test_delete_only_team(self):
#         self.database.add_team(team.Team("Team1", "password", self.database))
#         self.assertEqual(self.maker1.delete_team(["deleteteam", "Team1"]),
#                     "Team1 has been deleted.", "Valid edit failed")
#         self.assertEqual(self.database.get_teams(), [], "team was not deleted")
#         self.assertEqual(len(self.database.get_teams()), 0, "Team list length incorrect!")
#
#     def test_delete_team_front(self):
#         self.database.add_team(team.Team("Team1", "password", self.database))
#         self.database.add_team(team.Team("Team2", "password", self.database))
#         self.assertEqual(self.maker1.delete_team(["deleteteam", "Team1"]),
#                     "Team1 has been deleted.", "Valid edit failed")
#         team2 = self.database.get_teams()[0].username
#         self.assertEqual(team2, "Team2", "Team1 was not deleted")
#         self.assertEqual(len(self.database.get_teams()), 1, "Team list length incorrect!")
#
#     def test_delete_team_middle(self):
#         self.database.add_team(team.Team("Team1", "password", self.database))
#         self.database.add_team(team.Team("Team2", "password", self.database))
#         self.database.add_team(team.Team("Team3", "password", self.database))
#         self.assertEqual(self.maker1.delete_team(["deleteteam", "Team2"]),
#                     "Team2 has been deleted.", "Valid edit failed")
#         team1 = self.database.get_teams()[0].username
#         team3 = self.database.get_teams()[1].username
#         self.assertEqual(team1, "Team1", "Team2 was not deleted")
#         self.assertEqual(team3, "Team3", "Team2 was not deleted")
#         self.assertEqual(len(self.database.get_teams()), 2, "Team list length incorrect!")
#
#     def test_delete_team_end(self):
#         self.database.add_team(team.Team("Team1", "password", self.database))
#         self.database.add_team(team.Team("Team2", "password", self.database))
#         self.database.add_team(team.Team("Team3", "password", self.database))
#         self.assertEqual(self.maker1.delete_team(["deleteteam", "Team3"]),
#                     "Team3 has been deleted.", "Valid edit failed")
#         team1 = self.database.get_teams()[0].username
#         team2 = self.database.get_teams()[1].username
#         self.assertEqual(team1, "Team1", "Team1 was not deleted")
#         self.assertEqual(team2, "Team2", "Team2 was not deleted")
#         self.assertEqual(len(self.database.get_teams()), 2, "Team list length incorrect!")

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


runner = unittest.TextTestRunner()
res=runner.run(suite)
print(res)
print("*"*20)
for i in res.failures: print(i[1])
