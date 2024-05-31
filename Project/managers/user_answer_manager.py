from models.all_models import UserAnswer
from app import db


class UserAnswerManager:
    @staticmethod
    def create_user_answer(user_id:int, answer_id: int, session_id: int, question_id: int):
        # Check that all values are set. Looks better than just doing a bunch of "and" stmts
        if all(v is not None for v in [user_id, answer_id, session_id, question_id]):
            user_answer = UserAnswer(
                user_id=user_id,
                answer_id=answer_id,
                session_id=session_id,
                question_id=question_id
            )
            db.session.add(user_answer)
            db.session.commit()
            return user_answer
        else:
            return None

    @staticmethod
    def get_user_answer(user_answer_id):
        return UserAnswer.query.get(user_answer_id)

    @staticmethod
    def get_user_answer_for_submission(session_id, question_id):
        return UserAnswer.query.filter(
            UserAnswer.session_id == session_id,
            UserAnswer.question_id == question_id) \
            .all()
