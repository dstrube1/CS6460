from models.all_models import Quiz
from managers.question_manager import QuestionManager
from managers.answer_manager import AnswerManager
from app import db


class QuizManager:
    @staticmethod
    def create_quiz(name: str, add_vote: bool = True, add_danger_card: bool = True, add_round_over: bool = True):
        # Check that all values are set. Looks better than just doing a bunch of "and" stmts
        if all(v is not None for v in [name]):
            quiz = Quiz(name=name)
            db.session.add(quiz)
            db.session.commit()

            if add_vote:
                vote_question = QuestionManager.create_question(content="Do you want to continue exploring?", points=0,
                                                                answer_type="mcq", difficulty_lvl="Easy",
                                                                quiz_id=quiz.id)
                AnswerManager.create_answer(content="Yes", is_correct=True, question_id=vote_question.id)
                AnswerManager.create_answer(content="No", is_correct=True, question_id=vote_question.id)

            if add_danger_card:
                danger_card_question = QuestionManager.create_question(content="[THIS IS A DANGER CARD]",
                                                                       points=0, answer_type="mcq",
                                                                       difficulty_lvl="Easy",
                                                                       quiz_id=quiz.id)
                AnswerManager.create_answer(content="Continue", is_correct=True, question_id=danger_card_question.id)

            if add_round_over:
                round_over_question = QuestionManager.create_question(content="[THIS IS A ROUND OVER CARD]",
                                                                       points=0, answer_type="mcq",
                                                                       difficulty_lvl="Easy",
                                                                       quiz_id=quiz.id)
                AnswerManager.create_answer(content="Continue", is_correct=True, question_id=round_over_question.id)

            return quiz
        else:
            return None

    @staticmethod
    def get_quiz(quiz_id):
        return Quiz.query.get(quiz_id)

    @staticmethod
    def delete_quiz(quiz_id):
        db.session.delete(QuizManager.get_quiz(quiz_id))
        db.session.commit()

    @staticmethod
    def get_all_quizzes():
        return db.session.query(Quiz).all()
