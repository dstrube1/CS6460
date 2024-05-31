from models.all_models import Question, Quiz, GameEvent
from app import db


class QuestionManager:
    @staticmethod
    def create_question(content: str, points: int, answer_type: str, difficulty_lvl: str, quiz_id: int):
        # Check that all values are set. Looks better than just doing a bunch of "and" stmts
        if all(v is not None for v in [content, points, answer_type, difficulty_lvl, quiz_id]):
            question = Question(
                content=content,
                points=points,
                answer_type=answer_type,
                difficulty_lvl=difficulty_lvl,
                quiz_id=quiz_id
            )
            db.session.add(question)
            db.session.commit()
            return question
        else:
            return None

    @staticmethod
    def get_question(question_id):
        return Question.query.get(question_id)
    
    @staticmethod
    def delete_question(question_id):
        db.session.delete(QuestionManager.get_question(question_id))
        db.session.commit()

    @staticmethod
    def get_all_questions_for_specific_quiz(quiz_id):
        table_join = db.session.query(Question).join(Quiz)  # This might be the other way around
        questions = table_join.filter(Question.quiz_id == quiz_id).all()
        return questions[3:]  # ignore the first three, since these are templates

    @staticmethod
    def get_vote_question_for_quiz_id(quiz_id):
        return db.session.query(Question).filter(Question.quiz_id == quiz_id).order_by(Question.id.asc())[0]

    @staticmethod
    def get_danger_card_question_for_quiz_id(quiz_id):
        return db.session.query(Question).filter(Question.quiz_id == quiz_id).order_by(Question.id.asc())[1]

    @staticmethod
    def get_round_over_question_for_quiz_id(quiz_id):
        return db.session.query(Question).filter(Question.quiz_id == quiz_id).order_by(Question.id.asc())[2]

    @staticmethod
    def get_questions_for_specified_ids(question_ids):
        questions = Question.query.filter(Question.id.in_(question_ids)).all()
        return questions




