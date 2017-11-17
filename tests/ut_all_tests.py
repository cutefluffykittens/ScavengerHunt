import tests.ut_database as db
import tests.ut_gamemaker as gm
import tests.ut_landmark as lm
import tests.ut_main as main
import tests.ut_team as team
import unittest

suite = unittest.TestSuite()

# DB TESTS
suite.addTest(unittest.makeSuite(db.TestTeamList))
suite.addTest(unittest.makeSuite(db.TestLandmarks))
suite.addTest(unittest.makeSuite(db.TestLandmarkPath))
suite.addTest(unittest.makeSuite(db.TestPenalties))
suite.addTest(unittest.makeSuite(db.TestGameMakerCred))

# GAMEMAKER TESTS
suite.addTest(unittest.makeSuite(gm.TestMakerLogin))
suite.addTest(unittest.makeSuite(gm.TestMakerLogout))
suite.addTest(unittest.makeSuite(gm.TestMakerCheckStatus))

# MAIN TESTS
suite.addTest(unittest.makeSuite(main.TestDatabaseCreation))
suite.addTest(unittest.makeSuite(main.TestLogin))

# TEAM TESTS
suite.addTest(unittest.makeSuite(team.TestTeamLogin))

# LANDMARK TESTS
suite.addTest(unittest.makeSuite(lm.TestQuestions))
suite.addTest(unittest.makeSuite(lm.TestVerifyAnswer))

runner = unittest.TextTestRunner()
res=runner.run(suite)
print(res)
print("*"*20)
for i in res.failures: print(i[1])