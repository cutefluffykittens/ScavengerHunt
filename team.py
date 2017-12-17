#import int_user
#import database
import landmark
from Interface.models import HuntUser, Game, Landmark

#class Team(int_user.User):
class Team():
    def __init__(self):
        pass

    def display_menu(self):
        return "Options\n\ndisplaystatus\neditpassword [new password]\nrequestclue\nrequestquestion\nanswer [your guess]\nlogout"

    def display_status(self, teamname):
        try:
            team = HuntUser.objects.get(name=teamname)
            ret = "Team: " + team.name
        except HuntUser.DoesNotExist:
            ret = "Team does not exist"
        return ret

    # def edit_username(self, teamname, input):
    #     # teamname: string
    #     # input: List of length 1
    #     username = input[0]
    #
    #     try:
    #         team = HuntUser.objects.get(name=teamname)
    #         team.name = username
    #         team.save()
    #         ret = "Username successfully changed to " + username
    #     except HuntUser.DoesNotExist:
    #         ret = "Team does not exist"
    #
    #     ret = "Username successfully changed to " + username
    #     return ret


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
        answer = input[0]
        game = Game.objects.get(name="game")
        if not game.running:
            return "There is no game running!"
        try:
            team = HuntUser.objects.get(name=teamname)
        except HuntUser.DoesNotExist:
            return "Not a valid team!"
        if answer != team.current_landmark.answer:
            ret_string = "Incorrect answer, please try again"
        else:
            try:
                next_landmark = Landmark.objects.get(order_num=team.current_landmark.order_num + 1)
            except Landmark.DoesNotExist:
                return "Congrats! You win!"
            team.current_landmark = next_landmark
            team.save()
            ret_string = "Correct answer given! You can now request the clue for the next landmark"
        return ret_string

    def request_clue(self, teamname):
        # teamname: string
        game = Game.objects.get(name="game")
        if not game.running:
            return "There is no game running!"
        try:
            team = HuntUser.objects.get(name=teamname)
        except HuntUser.DoesNotExist:
            return "Not a valid team!"
        if team.current_landmark.order_num == -1:
            return "Not at a valid landmark"
        return team.current_landmark.clue

    def request_question(self, teamname):
        # teamname: string
        game = Game.objects.get(name="game")
        if not game.running:
            return "There is no game running!"
        try:
            team = HuntUser.objects.get(name=teamname)
        except HuntUser.DoesNotExist:
            return "Not a valid team!"
        return team.current_landmark.question
