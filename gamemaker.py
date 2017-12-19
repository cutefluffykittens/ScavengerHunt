from Interface.models import HuntUser, Landmark, Penalty, Game
from django.utils import timezone
from datetime import datetime


class GameMaker:
    def __init__(self):
        pass

    def add_landmark(self, input):
        # input: List of length 4
        if len(input) != 4:
            return "Invalid input!"
        name = input[0]
        clue = input[1]
        question = input[2]
        answer = input[3]
        try:
            # Check that no landmarks of the same name are already in the database
            Landmark.objects.get(name=name)
        except Landmark.DoesNotExist:
            # If the landmark doesn't exist, add it to the database
            lm = Landmark(name=name, clue=clue, question=question, answer=answer)
            lm.save()
            return "Landmark " + name + " has been added!"
        # Should only get here if a landmark of the same name exists
        return "Landmark " + name + " already exists!"

    def edit_landmark(self, input):
        change = False
        # Begin with empty strings for a full concatenation of which fields were altered on return
        new_name = ""
        clue = ""
        question = ""
        answer = ""
        order = ""
        ret_string_order = ""
        points = ""
        ret_string_points = ""
        # We always assume we are at least trying to edit; this will return for every case
        ret_string = "Edit to " + input[0] + " "
        name = input[0]
        lm = Landmark.objects.get(name=name)
        # If name field is empty, do nothing
        if input[1] != "":
            lm.name = input[1]
            change = True
            new_name = "name "
        # If clue field is empty, do nothing
        if input[2] != "":
            lm.clue = input[2]
            change = True
            clue = "clue "
        # If question field is empty, do nothing
        if input[3] != "":
            lm.question = input[3]
            change = True
            question = "question "
        # If answer field is empty, do nothing
        if input[4] != "":
            lm.answer = input[4]
            change = True
            answer = "answer "
        # If order number field is empty, do nothing. Must be an integer!
        if input[5] != "":
            try:
                lm.order_num = int(input[5])
                change = True
                order = "order "
            except ValueError:
                ret_string_order = " order number must be an integer!"
        # If points field is empty, do nothing. Must be an integer!
        if input[6] != "":
            try:
                lm.points = int(input[6])
                change = True
                points = "points "
            except ValueError:
                ret_string_points = " points must be an integer!"
        lm.save()
        # If no changes were made, the edit was unsuccessful. Return such
        if not change:
            return ret_string + "unsuccessful" + ret_string_order + ret_string_points
        # Otherwise, return what fields were changed as well as any issues with order or points
        return ret_string + new_name + clue + question + answer + order + points + "successful"\
               + ret_string_order + ret_string_points

    def display_landmarks(self):
        landmarks = Landmark.objects.all()
        ret = ""
        if len(landmarks) == 1:
            ret = "There are no landmarks"
        else:
            for landmark in landmarks:
                if landmark.name != "dummy":
                    ret += landmark.name + "\n"
        return ret

    def remove_landmark(self, input):
        # input: List of length 1
        name = input[0]
        try:
            lm = Landmark.objects.get(name=name)
            lm.delete()
            found = True
        except Landmark.DoesNotExist:
            return "Couldn't find landmark with name " + name
        return "Removed " + name + " from landmarks."

    def display_status(self):
        string = ''
        teams = HuntUser.objects.all()
        game = Game.objects.get(name="game")
        game_over = True
        for team in teams:
            if team.name != "maker":
                string += "Team: " + team.name + "\nScore: " + str(team.score) \
                          + "\nPenalties: " + str(team.penalties) + "\n"
                if game.running:
                    if team.current_landmark.order_num == 0:
                        string += "Current landmark: start\n"
                    elif team.game_ended:
                        string += "Current landmark: finish\n"
                    else:
                        cur = team.current_landmark.order_num - 1
                        string += "Current landmark: " + Landmark.objects.get(order_num=cur).name + "\n"
                string += "\n"
                if not team.game_ended:
                    game_over = False
        if game.running:
            string += "Game in progress"
        elif game_over:
            string += "The game has ended"
        else:
            string += "There is currently no game running"
        if string == '':
            string = 'No teams!'
        return string

    def display_menu(self):
        return "Options\n\ndisplaystatus\nmaketeam [team name], [team password]\n" \
               "editteam [team name to edit], [new team name], [new team password]\n" \
               "addlandmark [name], [clue], [question], [answer]\n" \
               "editlandmarks [name], [clue], [question], [answer], [order number], [points]\n" \
               "displaylandmarks\nremovelandmark [name]\n" \
               "setpenaltyscores [time points], [guess points]\n" \
               "setpenalties [new time penalty], [new guess penalty]\n" \
               "creategame [landmark name]...\nstartgame\nendgame\nlogout\n"

    def make_team(self, input):
        # input: List of length 2
        if len(input) == 2:
            name = input[0]
            password = input[1]
            dummy_landmark = Landmark.objects.get(name="dummy")
            try:
                # Check that there isn't already a team with that name in the database
                HuntUser.objects.get(name=name)
            except HuntUser.DoesNotExist:
                # If team doesn't exist, add the team and return
                team = HuntUser(name=name, password=password, current_landmark=dummy_landmark)
                team.save()
                return "Added " + name
            # Should only reach this return statement if a team with the same name exists
            return "Team " + name + " already exists!"
        else:
            # If input length was not 2, return
            return "Invalid input!"

    def edit_team(self, input):
        # input: List of length 3
        found = False
        if len(input) == 3:
            orig_name = input[0]
            new_name = input[1]
            new_pass = input[2]
            ret_string = "Edited " + orig_name + " to have username " + new_name + " and password " + new_pass
            try:
                team = HuntUser.objects.get(name=orig_name)
                team.name = new_name
                team.password = new_pass
                team.save()
                found = True
            except HuntUser.DoesNotExist:
                ret_string = "Could not find that team!"
        else:
            ret_string = "Invalid input!"
            found = True
        if not found:
            ret_string = "Could not find that team!"
        return ret_string

    def delete_team(self, input):
        found = False
        if len(input) == 1:
            try:
                team = HuntUser.objects.get(name=input[0])
                team.delete()
                found = True
            except Landmark.DoesNotExist:
                pass
            if found:
                return "Removed " + input[0] + " from teams."
            else:
                return "Couldn't find team with name " + input[0]
        else:
            ret_string = "Invalid input!"
            found = True
        if not found:
            ret_string = "That team does not exist."
        return ret_string

    def set_penalty_scores(self, input):
        if len(input) != 2:
            return "Bad input!"
        try:
            time_value = int(input[0])
            guess_value = int(input[1])
        except ValueError:
            return "Bad input! Need integers"
        if time_value > 0 and guess_value > 0:
            game = Game.objects.get(name="game")
            game.time_penalty = time_value
            game.guess_penalty = guess_value
            game.save()
        return "Set time penalty to " + input[0] + " and guess penalty to " + input[1]

    def set_penalties(self, input):
        # input: List of length 2
        if len(input) == 2:
            try:
                time = int(input[0])
                guess = int(input[1])
                if time > 0 and guess > 0:
                    game = Game.objects.get(name="game")
                    game.guess_period = time
                    game.num_guesses = guess
                    game.save()
                    ret_string = "Time penalty is " + input[0] + " minutes and guess penalty is " + input[1] + " guesses"
                else:
                    ret_string = "Invalid input! Need integers greater than 0"
            except ValueError:
                ret_string = "Invalid input! Need integers"
        else:
            ret_string = "Bad spacing! Need one space between time penalty and guess penalty"
        return ret_string

    def create_game(self, input):
        # input: List of length > 1
        i = 0
        # First, check that game is not currently running
        if Game.objects.get(name="game").running:
            return "Game is already in progress!"
        if len(input) == 0:
            return "Need at least one landmark to create a game"
        for landmark in Landmark.objects.all():
            # Reset all of the landmarks to index -1
            landmark.order_num = -1
            landmark.save()
        # Loop through all of the names in the input and make sure they are all valid
        for name in input:
            try:
                landmark = Landmark.objects.get(name=name)
            except Landmark.DoesNotExist:
                return "Landmark " + name + " is not a valid landmark!"
        # Now that we know they're all valid landmarks, we can add them all to the game
        for name in input:
            landmark = Landmark.objects.get(name=name)
            landmark.order_num = i
            landmark.save()
            i += 1
        return "Game has been created!"

    def start_game(self):
        game = Game.objects.get(name="game")
        if game.running:
            return "Game already started!"
        try:
            # Check that the game was actually created before we can start it
            lm = Landmark.objects.get(order_num=0)
        except Landmark.DoesNotExist:
            # If no landmarks have an order_num of 0, it means the game wasn't created
            # Thus, return an error statement to the user
            return "No landmarks are part of the game!"
        game.running = True
        game.time_start = datetime.now(tz=timezone.utc)    # Set the official start time of the game
        game.save()
        teams = HuntUser.objects.all()
        first_landmark = Landmark.objects.get(order_num=0)
        for team in teams:
            if team.name != "maker":
                team.current_landmark = first_landmark
                team.score = 0
                team.penalties = 0
                team.guesses = 0
                team.game_ended = False
                team.question_requested = False
                team.save()
        return "Game started!"

    def end_game(self):
        game = Game.objects.get(name="game")
        if not game.running:
            return "There is no game running!"
        game.running = False
        game.save()
        return "Game over"