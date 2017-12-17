import tests.ut_gamemaker as gm
import tests.ut_team as team
from Interface.models import HuntUser, Landmark,Game
from django.test import TestCase
import gamemaker
import unittest

suite = unittest.TestSuite()


# GAMEMAKER TESTS
suite.addTest(unittest.makeSuite(gm.TestMakerAddLandmark))
suite.addTest(unittest.makeSuite(gm.TestMakerDisplayLandmarks))
suite.addTest(unittest.makeSuite(gm.TestMakerRemoveLandmarks))
suite.addTest(unittest.makeSuite(gm.TestMakerCheckStatus))
suite.addTest(unittest.makeSuite(gm.TestMakerDisplayMenu))
suite.addTest(unittest.makeSuite(gm.TestMakerCreateTeam))
suite.addTest(unittest.makeSuite(gm.TestMakerEditTeams))
# suite.addTest(unittest.makeSuite(gm.TestMakerSetPenalties))
# suite.addTest(unittest.makeSuite(gm.TestStartGame))
# suite.addTest(unittest.makeSuite(gm.TestMakerEndGame))
suite.addTest(unittest.makeSuite(gm.TestMakerDeleteTeam))
suite.addTest(unittest.makeSuite(gm.TestMakerCreateGame))
suite.addTest(unittest.makeSuite(gm.TestMakerStartAndEndGame))

# TEAM TESTS
suite.addTest(unittest.makeSuite(team.TestTeamEditPassword))
suite.addTest(unittest.makeSuite(team.TestTeamCommands))
suite.addTest(unittest.makeSuite(team.TestTeamRequestQuestion))
suite.addTest(unittest.makeSuite(team.TestTeamAnswerQuestions))
suite.addTest(unittest.makeSuite(team.TestTeamRequestClue))
suite.addTest(unittest.makeSuite(team.TestHelperFunctions))
suite.addTest(unittest.makeSuite(team.TestScoreSystem))

runner = unittest.TextTestRunner()
res=runner.run(suite)
print(res)
print("*"*20)
for i in res.failures: print(i[1])