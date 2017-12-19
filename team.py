from Interface.models import HuntUser, Game, Landmark
from datetime import datetime, timedelta, timezone

class Team():
    def __init__(self):
        pass

    def display_menu(self):
        return "Options\n\ndisplaystatus\neditpassword [new password]\nrequestclue\nrequestquestion\nanswer [your guess]\nlogout"

    def display_status(self, teamname):
        try:
            team = HuntUser.objects.get(name=teamname)
        except HuntUser.DoesNotExist:
            return "Team does not exist"
        ret = "Team: " + team.name + "\nScore: " + str(team.score) + "\nPenalties: " + str(team.penalties)
        game = Game.objects.get(name="game")
        if game.running:
            if team.game_ended:
                ret += "\n\nYour team has finished the game\nFinal score: " + str(team.score - team.penalties)
            elif team.current_landmark.order_num == 0:
                ret += "\nCurrent landmark: start"
            else:
                cur = team.current_landmark.order_num - 1
                ret += "\nCurrent landmark: " + Landmark.objects.get(order_num=cur).name
            ret += "\n"
        else:
            ret += "\nThere is currently no game running"
        return ret

    def edit_password(self, teamname, input):
        # teamname: string
        # input: List of length 1
        password = input[0]
        try:
            team = HuntUser.objects.get(name=teamname)
            team.password = password
            team.save()
            ret = "Password successfully changed to " + password
        except HuntUser.DoesNotExist:
            ret = "Team does not exist"
        return ret

    def answer_question(self, teamname, input):
        # teamname: string
        # input: list of length 1
        time_check = self.check_time_up()
        current_time = datetime.now(tz=timezone.utc)
        answer = input[0]
        game = Game.objects.get(name="game")
        if not game.running:
            if time_check:
                return "Time is up!"
            return "There is no game running!"
        try:
            team = HuntUser.objects.get(name=teamname)
        except HuntUser.DoesNotExist:
            return "Not a valid team!"
        if team.game_ended:
            return "You've already finished the game!"
        if team.current_landmark.name == "dummy":
            return "Not at a valid landmark"
        if not team.question_requested:
            return "You need to receive the question first!"
        if answer != team.current_landmark.answer:
            team.guesses += 1
            if team.guesses >= game.num_guesses:
                team.penalties += game.guess_penalty
            team.save()
            ret_string = "Incorrect answer, please try again"
        else:
            team.score += team.current_landmark.points
            period = timedelta(minutes=game.guess_period)
            if (current_time - team.time_requested) >= period:
                team.penalties += game.time_penalty
            try:
                next_landmark = Landmark.objects.get(order_num=team.current_landmark.order_num + 1)
            except Landmark.DoesNotExist:
                team.game_ended = True
                if self.check_first(teamname):
                    team.score += game.last_landmark_bonus
                team.save()
                if self.check_game_over():
                    game.running = False
                    game.save()
                return "Congrats! You've reached the end of the game!"
            team.current_landmark = next_landmark
            team.question_requested = False
            team.save()
            ret_string = "Correct answer given! You can now request the clue for the next landmark"
        return ret_string

    def request_clue(self, teamname):
        # teamname: string
        time_check = self.check_time_up()
        game = Game.objects.get(name="game")
        if not game.running:
            if time_check:
                return "Time is up!"
            return "There is no game running!"
        try:
            team = HuntUser.objects.get(name=teamname)
        except HuntUser.DoesNotExist:
            return "Not a valid team!"
        if team.game_ended:
            return "You've already finished the game!"
        if team.current_landmark.name == "dummy":
            return "Not at a valid landmark"
        return team.current_landmark.clue

    def request_question(self, teamname):
        # teamname: string
        time_check = self.check_time_up()
        game = Game.objects.get(name="game")
        if not game.running:
            if time_check:
                return "Time is up!"
            return "There is no game running!"
        try:
            team = HuntUser.objects.get(name=teamname)
        except HuntUser.DoesNotExist:
            return "Not a valid team!"
        if team.game_ended:
            return "You've already finished the game!"
        if team.current_landmark.name == "dummy":
            return "Not at a valid landmark"
        if not team.question_requested:
            team.time_requested = datetime.now(tz=timezone.utc)
            team.question_requested = True
        team.save()
        return team.current_landmark.question

    def check_first(self, teamname):
        teams = HuntUser.objects.all()
        for team in teams:
            if team.name == "maker" or team.name == teamname:
                continue
            if team.game_ended:
                return False
        return True

    def check_game_over(self):
        teams = HuntUser.objects.all()
        for team in teams:
            if team.name == "maker":
                continue
            if not team.game_ended:
                return False
        return True

    def check_time_up(self):
        # First, check if there is a game running. If not, return False
        game = Game.objects.get(name="game")
        if not game.running:
            return False
        # Get the current time
        current_time = datetime.now(tz=timezone.utc)
        # Get game time = 1 hour
        period = timedelta(minutes=game.game_period)
        game = Game.objects.get(name="game")
        # Check that time hasn't run out
        if (game.time_start + period) <= current_time:
            # If yes, end the game and return True
            game.running = False
            game.save()
            return True
        # Otherwise, return False
        else:
            return False
