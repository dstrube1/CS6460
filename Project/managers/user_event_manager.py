from models.all_models import UserEvent, GameEvent
from app import db


class UserEventManager:
    @staticmethod
    def create_user_event(user_id:int, answer_id: int, session_id: int, question_id: int, game_event_id: int):
        # Check that all values are set. Looks better than just doing a bunch of "and" stmts
        if all(v is not None for v in [user_id, answer_id, session_id, question_id, game_event_id]):
            user_event = UserEvent(
                user_id=user_id,
                answer_id=answer_id,
                session_id=session_id,
                question_id=question_id,
                game_event_id=game_event_id
            )
            db.session.add(user_event)
            db.session.commit()
            return user_event
        else:
            return None

    @staticmethod
    def get_user_event(user_event_id):
        return UserEvent.query.get(user_event_id)

    @staticmethod
    def get_votes_for_game_event(game_event_id):
        return UserEvent.query.filter(UserEvent.game_event_id == game_event_id).all()

    @staticmethod
    def get_all_rows_for_user_id(user_id):
        return UserEvent.query.filter(UserEvent.user_id == user_id).all()

    @staticmethod
    def get_all_rows_for_user_id_and_round(user_id, round_id):
        table_join = db.session.query(UserEvent).join(GameEvent)
        result = table_join.filter(GameEvent.round_id == round_id, UserEvent.user_id == user_id).all()
        return result

    @staticmethod
    def player_already_completed_event(user_id, game_event_id):
        return UserEvent.query.filter(UserEvent.user_id == user_id, UserEvent.game_event_id == game_event_id).first()

    @staticmethod
    def get_players_that_voted(game_event_id, answer_id):
        return UserEvent.query.filter(UserEvent.game_event_id == game_event_id, UserEvent.answer_id == answer_id).all()

