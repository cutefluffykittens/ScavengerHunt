import gamemaker
import team
import logging
from Interface.models import HuntUser

class Escavenge():
    def __init__(self):
        self.game_maker = gamemaker.GameMaker()
        self.t = team.Team()

        self.maker = {
            "logout": lambda params: self.game_maker.logout(),
            "login": lambda params: self.main,
            "displaystatus": lambda params: self.game_maker.display_status(),
            "help": lambda params: self.game_maker.display_menu(),
            "maketeam": lambda params: self.game_maker.make_team(params),
            "editteam": lambda params: self.game_maker.edit_team(params),
            "setpenalties": lambda params: self.game_maker.set_penalties(params),
            "addlandmark": lambda params: self.game_maker.add_landmark(params),
            "editlandmark": lambda params: self.game_maker.edt_landmark(params),
            "displaylandmarks": lambda params: self.game_maker.display_landmarks(),
            "removelandmark": lambda params: self.game_maker.remove_landmark(params),
            "creategame": lambda params: self.game_maker.create_game(params),
            "startgame": lambda params: self.game_maker.start_game(),
            "endgame": lambda params: self.game_maker.end_game()
        }

        self.team = {
            "logout": lambda teamname, params: self.t.logout(teamname),
            "displaystatus": lambda teamname, params: self.t.display_status(teamname),
            "help": lambda teamname, params: self.t.display_menu(),
            "editpassword" : lambda teamname, params: self.t.edit_password(teamname, params),
            "requestclue": lambda teamname, params: self.t.request_clue(teamname),
            "requestquestion": lambda teamname, params: self.t.request_question(teamname),
            "answer" : lambda teamname, params: self.t.answer_question(teamname, params)
        }

    def maker_cmd(self, string):
        try:
            string = string.lower()
            params = string.split(", ")
            cmd = string.split(" ")[0]
            if len(params[0].split(" ")) > 1:
                params[0] = params[0].split(" ")[1]
            return self.maker[cmd](params)
        except KeyError:
            return "That is not a valid command."

    def team_cmd(self, teamname, string):
        try:
            string = string.lower()
            params = string.split(", ")
            cmd = string.split(" ")[0]
            if len(params[0].split(" ")) > 1:
                params[0] = params[0].split(" ")[1]
            return self.team[cmd](teamname, params)
        except KeyError:
            return "That is not a valid command."

    def main(self, string, user):

        print(string)

        if user == "maker":
            return self.maker_cmd(string)

        else:
            return self.team_cmd(user, string)


if __name__ == '__main__':
    Escavenge().main()
