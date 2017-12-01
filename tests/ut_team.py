import team
import database
import landmark
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
        self.assertFalse(self.team1.edit_username(["bestteam"]), "Error: cannot edit username with no team logged in")
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
        self.assertFalse(self.team1.edit_password(["kittens"]),"Error: cannot edit password with no team logged in")
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
        self.assertEqual("Options\n\nlog out\ndisplay status\nedit username\nedit password\nanswer\nrequest clue\n",
                         self.team1.display_menu(),"Error: incorrect menu displayed")

class TestTeamAnswerQuestions(unittest.TestCase):
    def setUp(self):
        self.database = database.Database()
        self.team1 = team.Team("teamname1", "password1", self.database)
        self.team2 = team.Team("teamname2", "password2", self.database)
        self.database.add_team(self.team1)
        self.database.add_team(self.team2)
        self.landmark1 = landmark.Landmark("landmark1","clue1","q1","a1")
        self.landmark2 = landmark.Landmark("landmark2","clue2","q2","a2")
    def test_answer_no_team_logged_in(self):
        self.database.add_to_path(self.landmark1)
        self.assertEqual("Cannot answer question when not logged in!",self.team1.answer_question(["a1"]),
                         "Error: cannot answer a question when not logged in")
    def test_answer_wrong_team_logged_in(self):
        self.team1.login("teamname1","password1")
        self.database.add_to_path(self.landmark1)
        self.assertEqual("Cannot answer question when not logged in!",self.team2.answer_question(["a1"]),
                         "Error: a team that is not the current user cannot answer the question")
    def test_answer_no_landmarks_added(self):
        self.team1.login("teamname1","password1")
        self.database.game_running = True
        self.assertEqual("Not at a valid landmark",self.team1.answer_question(["a1"]),
                         "Error: cannot answer a question when there are no landmarks")
    def test_answer_no_game_running(self):
        self.team1.login("teamname1","password1")
        self.database.add_to_path(self.landmark1)
        self.assertEqual("There is no current game to answer a question for",self.team1.answer_question(["a1"]),
                         "Error: can't answer a question when there isn't a current game")
    def test_correct_one_landmark(self):
        self.team1.login("teamname1","password1")
        self.database.add_to_path(self.landmark1)
        self.database.add_to_path(self.landmark2)
        self.database.game_running = True
        self.assertEqual("Correct answer given! You can now request the clue for the next landmark",
                         self.team1.answer_question(["a1"]),
                         "Error: should have returned True when answered correctly")
        self.assertEqual(0,self.team1.current_landmark,
                         "Error: current landmark was not updated from -1 to 0 when answer was correct")
    def test_incorrect(self):
        self.team1.login("teamname1","password1")
        self.database.add_to_path(self.landmark1)
        self.database.game_running = True
        self.assertEqual("Incorrect answer, please try again",
                         self.team1.answer_question(["wrong answer"]),
                         "Error: should have returned False when answered incorrectly")
        self.assertEqual(-1,self.team1.current_landmark,
                         "Error: current landmark should remain -1 when answer was incorrect")
    def test_correct_end_game(self):
        self.team1.login("teamname1","password1")
        self.database.add_to_path(self.landmark1)
        self.database.add_to_path(self.landmark2)
        self.database.game_running = True
        self.team1.answer_question(["a1"])
        self.assertEqual("Congratulations! Your team has won the game!",
                        self.team1.answer_question(["a2"]),
                        "Error: should have indicated that the team has won")
        self.assertEqual(1,self.team1.current_landmark,
                         "Error: current landmark was not updated from 0 to 1 when answer was correct")
        self.assertFalse(self.database.game_running,
                         "Error: game_running should be changed from True to False once a team has won")

class TestTeamInitialization(unittest.TestCase):
    def setUp(self):
        self.database = database.Database()
        self.team1 = team.Team("username1","password1",self.database)
    def test_initial_username(self):
        self.assertEqual("username1",self.team1.username,"Error: username not initialized correctly")
    def test_initial_password(self):
        self.assertEqual("password1",self.team1.password,"Error: password not initialized correctly")
    def test_initial_landmark(self):
        self.assertEqual(-1,self.team1.current_landmark,"Error: current landmark should be initialized to -1")
    def test_initial_penalties(self):
        self.assertEqual(0,self.team1.penalties,"Error: penalties should be initialized to 0")

class TestTeamRequestClue(unittest.TestCase):
    def setUp(self):
        self.database = database.Database()
        self.team1 = team.Team("teamname1", "password1", self.database)
        self.team2 = team.Team("teamname2", "password2", self.database)
        self.database.add_team(self.team1)
        self.database.add_team(self.team2)
        self.landmark1 = landmark.Landmark("landmark1","clue1","q1","a1")
        self.landmark2 = landmark.Landmark("landmark2","clue2","q2","a2")
    def test_request_no_team_logged_in(self):
        self.database.add_to_path(self.landmark1)
        self.assertEqual("Cannot answer question when not logged in!",self.team1.request_clue(),
                         "Error: cannot answer a question when not logged in")
    def test_request_wrong_team_logged_in(self):
        self.team1.login("teamname1","password1")
        self.database.add_to_path(self.landmark1)
        self.assertEqual("Cannot answer question when not logged in!",self.team2.request_clue(),
                         "Error: a team that is not the current user cannot answer the question")
    def test_request_no_landmarks_added(self):
        self.team1.login("teamname1","password1")
        self.assertEqual("Not at a valid landmark",self.team1.request_clue(),
                         "Error: cannot answer a question when there are no landmarks")
    def test_request_good(self):
        self.team1.login("teamname1","password1")
        self.database.add_to_path(self.landmark1)
        self.assertEqual("clue1", self.team1.request_clue(),
                         "Error: should have returned clue1")

class TestTeamInitialization(unittest.TestCase):
    def setUp(self):
        self.database = database.Database()
        self.team1 = team.Team("username1","password1",self.database)
    def test_initial_username(self):
        self.assertEqual("username1",self.team1.username,"Error: username not initialized correctly")
    def test_initial_password(self):
        self.assertEqual("password1",self.team1.password,"Error: password not initialized correctly")
    def test_initial_landmark(self):
        self.assertEqual(-1,self.team1.current_landmark,"Error: current landmark should be initialized to -1")
    def test_initial_penalties(self):
        self.assertEqual(0,self.team1.penalties,"Error: penalties should be initialized to 0")

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestTeamLogin))
suite.addTest(unittest.makeSuite(TestTeamLogout))
suite.addTest(unittest.makeSuite(TestTeamEditUsername))
suite.addTest(unittest.makeSuite(TestTeamEditPassword))
suite.addTest(unittest.makeSuite(TestTeamCommands))
suite.addTest(unittest.makeSuite(TestTeamAnswerQuestions))
suite.addTest(unittest.makeSuite(TestTeamRequestClue))

runner = unittest.TextTestRunner()
res=runner.run(suite)
print(res)
print("*"*20)
for i in res.failures: print(i[1])