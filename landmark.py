class Landmark:
    def __init__(self, clue):
        self.questions = {}
        self.clue = clue

    def get_questions(self):
        return self.questions

    def add_question(self, question, answer):
        if question in self.questions.keys():
            return False
        else:
            self.questions[question] = answer
            return True

    def edit_question(self, question, answer):
        self.questions[question] = answer

    def remove_question(self, question):
        try:
            self.questions.pop(question)
            return True
        except KeyError:
            return False

    def verify_answer(self, question, answer):
        if self.questions[question] is answer:
            return True
        return False
