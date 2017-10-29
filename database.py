class Database:
    def __init__(self):
        self.teamList = []
        self.landmarks = []
        self.landmarkPath = []
        self.guessPenalty = -1
        self.timePenalty = -1
        self.gameMakerCred = {"username":"username", "password":"password"}

    def add_team(self, team):
        self.teamList.append(team)

    def delete_team(self, team):
        try:
            self.teamList.remove(team)

        except ValueError:
            pass

    def get_teams(self):
        return self.teamList

    def add_landmark(self, landmark):
        self.landmarks.append(landmark)

    def delete_landmark(self, landmark):
        try:
            self.landmarks.remove(landmark)

        except ValueError:
            pass

    def get_landmarks(self):
        return self.landmarks

    def add_to_path(self, landmark):
        self.landmarkPath.append(landmark)

    def delete_from_path(self, landmark):
        try:
            self.landmarkPath.remove(landmark)

        except ValueError:
            pass

    def get_landmark_path(self):
        return self.landmarkPath

    def set_guess_penalty(self, penalty):
        self.guessPenalty = penalty

    def get_guess_penalty(self):
        return self.guessPenalty

    def set_time_penalty(self, penalty):
        self.timePenalty = penalty

    def get_time_penalty(self):
        return self.timePenalty

    def get_game_maker_cred(self):
        return self.gameMakerCred