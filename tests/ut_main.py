import unittest

class TestDatabaseCreation(unittest.TestCase):
  def setUp(self):
    pass

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestDatabaseCreation))

runner = unittest.TextTestRunner()
res=runner.run(suite)
print(res)
print("*"*20)
for i in res.failures: print(i[1])
