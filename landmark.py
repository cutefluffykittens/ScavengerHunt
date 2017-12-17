class Landmark:
    def __init__(self, name, clue, question, answer):
        self.name = name
        self.clue = clue
        self.question = question
        self.answer = answer

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_question(self):
        return self.question

    def set_question(self, question):
        self.question = question

    def get_clue(self):
        return self.clue

    def set_clue(self, clue):
        self.clue = clue

    def set_answer(self, answer):
        self.answer = answer

    def get_answer(self):
        return self.answer

    def verify_answer(self, answer):
        return self.answer == answer
