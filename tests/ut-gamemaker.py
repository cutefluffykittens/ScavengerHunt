import unittest
import gamemaker
import database

class TestLogin(unittest.TestCase):
  def setUp(self):
    self.database = database.Database()
    self.maker1 = gamemaker.GameMaker()
  
  def test_makerLogin(self):
     assertEquals(self.maker1.login("Notvalidusername","Notvalidpassword"), false, "test_makerLogin should not have logged in"))
     assertEquals(self.maker1.login("maker","password"), true, "test_makerLogin should have logged in"))
    
