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
        return "Options\n\nlog out\ndisplay status\nedit username\nedit password\n"

    def display_status(self):
        return "Team: " + self.username

    def edit_username(self, username):
        if self.database.get_current_user() is not self:
            return False
        self.username = username
        ret = "Username successfully changed to " + username
        return ret


    def edit_password(self, password):
        if self.database.get_current_user() is not self:
            return False
        self.password = password
        ret = "Password successfully changed to " + password
        return ret

    def get_current_landmark(self):
        if self.database.get_current_user() is not self:
            return False
        pass

    def answer_question(self, user_answer):
        if self.database.get_current_user() is not self:
            return False
        landmarks = self.database.get_landmark_path()
        try:
            l = landmarks[self.current_landmark]
        except IndexError:
            return False
        question = list(l.get_questions().keys())[0]
        ret = landmarks[self.current_landmark].verify_answer(question,user_answer)
        if ret:
            self.current_landmark += 1
        return ret