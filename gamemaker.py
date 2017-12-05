from Interface.models import HuntUser, Landmark, Penalty, Game

class GameMaker:
    def __init__(self):
        pass

    def add_landmark(self, input):
        name = input[0]
        clue = input[1]
        question = input[2]
        answer = input[3]

        lm = Landmark(name=name, clue=clue, question=question, answer=answer)
        lm.save()

        return "Landmark " + name + " has been added!"

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
        found = False
        name = input[0]

        try:
            landmark = Landmark.objects.get(name=name)
            landmark.delete()
            found = True
        except Landmark.DoesNotExist:
            pass

        if found:
            return "Removed " + name + " from landmarks."
        else:
            return "Couldn't find landmark with name " + name

    def display_status(self):
        string = ''
        teams = HuntUser.objects.all()
        for team in teams:
            if team.name != "maker":
                string += team.name + '\n' #+ ' is at ' + team.landmark + ' with ' + team.penalties + ' penalties\n'
        if string == '':
            string = 'No teams!'
        return string

    def display_menu(self):
        return "Options\n\ndisplaystatus\nmaketeam [team name], [team password]\neditteam [team name to edit], [new team name], [new team password]\n" \
        "addlandmark [name], [clue], [question], [answer]\ndisplaylandmarks\nremovelandmark [name]\nsetpenalties [new time penalty], [new guess penalty]\n" \
        "creategame [landmark name]...\nstartgame\nendgame\nlogout\n"

    def make_team(self, input):
        if len(input) == 2:
            name = input[0]
            password = input[1]
            dummy_landmark = Landmark.objects.get(name="dummy")
            team = HuntUser(name=name, password=password, current_landmark=dummy_landmark)
            team.save()
            ret_string = "Added " + name
        else:
            ret_string = "Invalid input!"
        return ret_string

    def edit_team(self, input):
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
                pass

        else:
            ret_string = "Invalid input!"
            found = True
        if not found:
            ret_string = "Could not find that team!"
        return ret_string

    def delete_team(self, input):
        found = False
        if len(input) == 2:
            list = self.database.get_teams()
            index = -1
            for team in list:
                ++index
                if team.username == input[1]:
                    try:
                        found = True
                        del list[index]
                        ret_string = "" + input[1] +" has been deleted."
                    except(ValueError):
                        ret_string = "" + input[1] +" does not exist"

        else:
            ret_string = "Invalid input!"
            found = True
        if not found:
            ret_string = "That team does not exist."
        return ret_string

    def set_penalties(self, input):
        if len(input) == 2:
            try:
                time = int(input[0])
                guess = int(input[1])
                if time > 0 and guess > 0:
                    time_penalty = Penalty.objects.get(name="time")
                    time_penalty.value = time
                    time_penalty.save()

                    guess_penalty = Penalty.objects.get(name="guesses")
                    guess_penalty.value = guess
                    guess_penalty.save()
                    ret_string = "Time penalty is " + input[0] + " minutes and guess penalty is " + input[1] + " guesses"
                else:
                    ret_string = "Invalid input! Need integers greater than 0"
            except ValueError:
                ret_string = "Invalid input! Need integers"
        else:
            ret_string = "Bad spacing! Need one space between time penalty and guess penalty"
        return ret_string

    def create_game(self, input):
        i = 0
        for landmark in Landmark.objects.all():
            landmark.order_num = -1
            landmark.save()
        for name in input:
            try:
                landmark = Landmark.objects.get(name=name)
                landmark.order_num = i
                landmark.save()
                i += 1
            except Landmark.DoesNotExist:
                return "One of the names you entered is invalid!"

        return "Game has been created!"

    def start_game(self):
        game = Game.objects.get(name="game")
        game.running = True
        game.save()

        teams = HuntUser.objects.all()
        first_landmark = Landmark.objects.get(order_num=0)
        for team in teams:
            if team.name != "maker":
                team.current_landmark = first_landmark
                team.save()

        return "Game started!"

    def end_game(self):
        game = Game.objects.get(name="game")
        if not game.running:
            return "There is no game running!"
        game.running = False
        game.save()
        return "Game over"
