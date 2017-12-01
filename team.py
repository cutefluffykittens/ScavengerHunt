#import int_user
import database
import landmark

#class Team(int_user.User):
class Team():
    def __init__(self,username,password,database):
        self.username = username
        self.password = password
        self.database = database
        self.current_landmark = -1
        self.penalties = 0
    def login(self,username,password):
        if self.database.get_current_user() != None:
            return False
        if username == self.username and password == self.password:
            self.database.set_current_user(self)
            return True
        return False
    def logout(self):
        if self.database.get_current_user() is not self:
            return False
        self.database.set_current_user(None)
        return True
    def display_menu(self):
        return "Options\n\nlog out\ndisplay status\nedit username\nedit password\nanswer\n"

    def display_status(self):
        landmark_string = "\n"
        if self.database.game_running:
            landmark_string = "\nCurrent landmark: "
            if self.current_landmark == -1:
                landmark_string += "none\n"
            else:
                landmark_string += self.database.get_landmark_path[self.current_landmark].get_name() + "\n"
        return "Team: " + self.username + landmark_string + "Current penalties: " + str(self.penalties) + "\n"

    def edit_username(self, input):
        username = input[0]
        if self.database.get_current_user() is not self:
            return False
        self.username = username
        ret = "Username successfully changed to " + username
        return ret

    def edit_password(self, input):
        password = input[0]
        if self.database.get_current_user() is not self:
            return False
        self.password = password
        ret = "Password successfully changed to " + password
        return ret

    def answer_question(self, input):
        user_answer = input[0]
        if self.database.get_current_user() is not self:
            return "Cannot answer question when not logged in!"
        if not self.database.game_running:
            return "There is no current game to answer a question for"
        landmarks = self.database.get_landmark_path()
        try:
            check_landmark = landmarks[self.current_landmark+1]
        except IndexError:
            return "Not at a valid landmark"
        if check_landmark.verify_answer(user_answer):
            self.current_landmark += 1
            if self.current_landmark == (len(landmarks)-1):
                self.database.game_running = False
                return "Congratulations! Your team has won the game!"
            return "Correct answer given! You can now request the clue for the next landmark"
        else:
            self.penalties += 1
            return "Incorrect answer, please try again"
