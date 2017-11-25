import landmark

class GameMaker:
    def __init__(self, database):
        self.database = database

    def login(self, name, password):
        return_value = False
        current_user = self.database.get_current_user()
        maker_cred = self.database.get_game_maker_cred()
        if current_user is None:
            if maker_cred["username"] == name and maker_cred["password"] == password:
                self.database.set_current_user(self)
                return_value = True
        return return_value

    def add_landmark(self, input):
        name = input[0]
        clue = input[1]
        question = input[2]
        answer = input[3]

        self.database.add_landmark(landmark.Landmark(name, clue, question, answer))

        return "Landmark " + name + " has been added!"

    def display_landmarks(self):
        landmarks = self.database.get_landmarks()
        ret = ""

        if len(landmarks) == 0:
            ret = "There are no landmarks"

        else:
            for landmark in landmarks:
                ret += landmark.get_name() + "\n"

        return ret

    def remove_landmark(self, input):
        landmarks = self.database.get_landmarks()
        found = False

        for landmark in landmarks:
            if landmark.get_name() == input[0]:
                if self.database.remove_landmark(landmark):
                    found = True

        if found:
            return "Removed " + input[0] + " from landmarks."
        else:
            return "Couldn't find landmark with name " + input[0]

    def display_status(self):
        string = ''
        teams = self.database.get_teams()
        for team in teams:
            string += team.username + '\n' #+ ' is at ' + team.landmark + ' with ' + team.penalties + ' penalties\n'
        if string == '':
            string = 'No teams!'
        return string
        
    def logout(self):
        return_value = False
        current_user = self.database.get_current_user()
        if current_user is self:
            self.database.set_current_user(None)
            return_value = True
        return return_value

    def display_menu(self):
        return "Options\n\ndisplaystatus\naddlandmark [name], [clue], [question], [answer]\ndisplaylandmarks\nremovelandmark [name]\nlogout\n"