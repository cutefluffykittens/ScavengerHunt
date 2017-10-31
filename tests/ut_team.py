import team
import unittest

class TestTeamLogin(unittest.TestCase):
    def setUp(self):
        self.team1 = Team("Name1","Username1","Password1")
        self.team2 = Team("Name2","Username2","Password2")
    def test_LoginFirstTeam(self):
        assertTrue(login(self.team1.username,self.team1.password), "Error: failed to log in team1")
    def test_LoginSecondTeam(self):
        assertFalse(login(self.team2.username,self.team2.password), "Error: team1 is already logged in; cannot have two users logged in at once")
    def test_LogoutFirstTeam(self):
        assertTrue(logout(team1), "Error: failed to log out team1")
    def test_LogoutSecondTeam(self):
        assertFalse(logout(team2), "Error: can't log out team2 when team1 is logged in")