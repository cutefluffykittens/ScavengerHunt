import unittest
import database
import landmark

class TestQuestions(unittest.TestCase):
    def setUp(self):
        self.landmark1 = landmark.Landmark("clue")
        self.question1 = "Question1"
        self.answer1 = "Answer1"
        self.question2 = "Question2"
        self.answer2 = "Answer2"

    def test_add_question_empty_list(self):
        self.assertEquals(self.landmark1.add_question(self.question1, self.answer1), True, "add_question_empty_list: Question didn't add correctly")
        self.assertEquals(self.landmark1.get_questions(), {self.question1:self.answer1}, "add_question_empty_list: Question list not correct")

    def test_add_question_non_empty_list(self):
        self.assertEquals(self.landmark1.add_question(self.question1, self.answer1), True, "add_question_empty_list: Question didn't add correctly")
        self.assertEquals(self.landmark1.add_question(self.question2, self.answer2), True, "add_question_empty_list: Question didn't add correctly")
        self.assertEquals(self.landmark1.get_questions()[self.question2], self.answer2, "add_question_non_empty_list: Question list not correct")

    def test_add_question_question_exists(self):
        self.landmark1.add_question(self.question1, self.answer1)
        self.assertEquals(self.landmark1.add_question(self.question1, self.answer2), False, "add_question_question_exists: Question should not have been added")

    def test_remove_question_question_exists(self):
        self.landmark1.add_question(self.question1, self.answer1)
        self.assertEquals(self.landmark1.remove_question(self.question1), True, "remove_question_question_exists: Should have removed correctly")

    def test_remove_question_question_does_not_exist(self):
        self.assertEquals(self.landmark1.remove_question(self.question1), False, "remove_question_question_exists: Should not have removed question")

    def test_edit_question(self):
        self.landmark1.add_question(self.question1, self.answer1)
        self.landmark1.edit_question(self.question1, self.answer2)
        self.assertEquals(self.landmark1.questions[self.question1], self.answer2, "edit_question: Question was not edited correctly")

class TestVerifyAnswer(unittest.TestCase):
    def setUp(self):
        self.landmark1 = landmark.Landmark("clue")
        self.question1 = "Question1"
        self.answer1 = "Answer1"
        self.answer2 = "Answer2"
        self.landmark1.add_question(self.question1, self.answer1)

    def test_answer_correct(self):
        self.assertEquals(self.landmark1.verify_answer(self.question1, self.answer1), True, "answer_correct: answer should have been correct")

    def test_answer_incorrect(self):
        self.assertEquals(self.landmark1.verify_answer(self.question1, self.answer2), False, "answer_correct: answer should not have been correct")

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestQuestions))
suite.addTest(unittest.makeSuite(TestVerifyAnswer))

runner = unittest.TextTestRunner()
res=runner.run(suite)
print(res)
print("*"*20)
for i in res.failures: print(i[1])