class Database:
    def __init__(self):
        self.team_list = []
        self.landmarks = []
        self.game = []
        self.guess_penalty = -1
        self.time_penalty = -1
        self.current_user = None
        self.game_maker_cred = {"username":"maker", "password":"password"}

    def add_team(self, team):
        self.team_list.append(team)

    def delete_team(self, team):
        try:
            self.team_list.remove(team)

        except ValueError:
            pass

    def get_teams(self):
        return self.team_list

    def add_landmark(self, landmark):
        self.landmarks.append(landmark)

    def remove_landmark(self, landmark):
        try:
            self.landmarks.remove(landmark)
            return True

        except ValueError:
            return False

    def get_landmarks(self):
        return self.landmarks

    def add_to_game(self, landmark):
        if not game_is_running:
            self.game.append(landmark)
        else:
            return "Cannot add a landmark when the game is running!"


    def delete_from_game(self, landmark):
        if not game_is_running:
            try:
                self.landmark_path.remove(landmark)

            except ValueError:
                pass
        else:
            return "Cannot delete a landmark when the game is running!"
    def get_game(self):
        return self.game

    def set_guess_penalty(self, penalty):
        self.guess_penalty = penalty

    def get_guess_penalty(self):
        return self.guess_penalty

    def set_time_penalty(self, penalty):
        self.time_penalty = penalty

    def get_time_penalty(self):
        return self.time_penalty

    def get_game_maker_cred(self):
        return self.game_maker_cred

    def get_current_user(self):
        return self.current_user

    def set_current_user(self, user):
        self.current_user = user