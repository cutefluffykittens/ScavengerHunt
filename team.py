from Interface.models import HuntUser, Game, Landmark
from datetime import datetime, timedelta, timezone

class Team():
    def __init__(self):
        pass

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
            ret = "Error: See game admin."
            print("Error! Team does not exist")
        return ret

    def answer_question(self, teamname, input):
        # teamname: string
        # input: list of length 1
        #time_check = self.check_time_up()
        current_time = datetime.now(tz=timezone.utc)
        answer = input[0]
        game = Game.objects.get(name="game")
        if not game.running:
            #if time_check:
             #   return "Time is up!"
            return "There is no game running!"
        try:
            team = HuntUser.objects.get(name=teamname)
        except HuntUser.DoesNotExist:
            print("Error. Hunt user doesn't exist")
            return "Error. Contact admin."
        if team.game_ended:
            return "Game has ended."
        if team.current_landmark.name == "dummy":
            print("Error: Not valid landmark. Should never be at landmark 'dummy'")
            return "Error. Contact admin."
        if not team.question_requested:
            print("Error: inconsistant state")
            return "Error. Contact admin."
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
                return "CONGRATS! YOU'VE WoN!!!!!"
            team.current_landmark = next_landmark
            team.question_requested = False
            team.save()
            ret_string = "You got it right! Yay!"
        return ret_string

    def request_clue(self, teamname):
        # teamname: string
        #time_check = self.check_time_up()
        game = Game.objects.get(name="game")
        if not game.running:
            #if time_check:
            #    return "Time is up!"
            return "There is no game running!"
        try:
            team = HuntUser.objects.get(name=teamname)
        except HuntUser.DoesNotExist:
            return "Not a valid team!"
        if team.game_ended:
            return " ~~~~~~~ "
        if team.current_landmark.name == "dummy":
            return "Not at a valid landmark"
        return team.current_landmark.clue

    def request_question(self, teamname):
        # teamname: string
        #time_check = self.check_time_up()
        game = Game.objects.get(name="game")
        if not game.running:
            #if time_check:
            #    return "Time is up!"
            return "There is no game running!"
        try:
            team = HuntUser.objects.get(name=teamname)
        except HuntUser.DoesNotExist:
            return "Not a valid team!"
        if team.game_ended:
            return " ~~~~~~~~~ "
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
        period = timedelta(hours=game.game_period)
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
