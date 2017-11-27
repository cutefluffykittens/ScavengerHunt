#import int_user
import database
import landmark

#class Team(int_user.User):
class Team():
    def __init__(self,username,password,database):
        self.username = username
        self.password = password
        self.database = database
        self.current_landmark = 0
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
        return "Team: " + self.username

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
        landmarks = self.database.get_landmark_path()
        try:
            check_landmark = landmarks[self.current_landmark]
        except IndexError:
            return "Not at a valid landmark"
        ret_string = ""
        if check_landmark.verify_answer(user_answer):
            self.current_landmark += 1
            ret_string = "Correct answer given! You can now request the clue for the next landmark"
        else:
            ret_string = "Incorrect answer, please try again"
        return ret_string