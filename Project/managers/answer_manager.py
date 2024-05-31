from models.all_models import Answer, Question
from app import db


class AnswerManager:
    @staticmethod
    def create_answer(content: str, is_correct: bool, question_id: int):
        # Check that all values are set. Looks better than just doing a bunch of "and" stmts
        if all(v is not None for v in [content, is_correct, question_id]):
            answer = Answer(
                content=content,
                is_correct=is_correct,
                question_id=question_id
            )
            db.session.add(answer)
            db.session.commit()
            return answer
        else:
            return None

    @staticmethod
    def get_answer(answer_id):
        return Answer.query.get(answer_id)

    @staticmethod
    def get_yes_answer_for_vote_question(question_id):
        return Answer.query.filter(Answer.question_id == question_id, Answer.content == "Yes").first()

    @staticmethod
    def get_no_answer_for_vote_question(question_id):
        return Answer.query.filter(Answer.question_id == question_id, Answer.content == "No").first()
