import unittest
import database
import landmark

class TestQuestions(unittest.TestCase):
    def setUp(self):
        self.question1 = "Question1"
        self.answer1 = "Answer1"
        self.question2 = "Question2"
        self.answer2 = "Answer2"
        self.landmark1 = landmark.Landmark("name1", "clue1", self.question1, self.answer1)

    def test_set_question(self):
        self.landmark1.set_question(self.question1)
        self.assertEquals(self.landmark1.get_question(), self.question1, "add_question_empty_list: Question list not correct")

    def test_edit_question(self):
        self.landmark1.set_question(self.question1)
        self.landmark1.set_question(self.question2)
        self.assertEquals(self.landmark1.get_question(), self.question2, "edit_question: Question was not edited correctly")

    def test_set_answer(self):
        self.landmark1.set_answer(self.answer1)
        self.assertEquals(self.landmark1.get_answer(), self.answer1, "add_question_empty_list: Question list not correct")

    def test_edit_answer(self):
        self.landmark1.set_answer(self.answer1)
        self.landmark1.set_answer(self.answer2)
        self.assertEquals(self.landmark1.get_answer(), self.answer2, "edit_question: Question was not edited correctly")


class TestVerifyAnswer(unittest.TestCase):
    def setUp(self):
        self.question1 = "Question1"
        self.answer1 = "Answer1"
        self.answer2 = "Answer2"
        self.landmark1 = landmark.Landmark("name1", "clue1", self.question1, self.answer1)

    def test_answer_correct(self):
        self.assertEquals(self.landmark1.verify_answer(self.answer1), True, "answer_correct: answer should have been correct")

    def test_answer_incorrect(self):
        self.assertEquals(self.landmark1.verify_answer(self.answer2), False, "answer_correct: answer should not have been correct")

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestQuestions))
suite.addTest(unittest.makeSuite(TestVerifyAnswer))

runner = unittest.TextTestRunner()
res=runner.run(suite)
print(res)
print("*"*20)
for i in res.failures: print(i[1])