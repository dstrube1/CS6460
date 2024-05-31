from models.all_models import UserGameSession
from models.all_models import User
from managers.user_event_manager import UserEventManager
from collections import defaultdict
from app import db


class UserGameSessionManager:
    @staticmethod
    def create_user_game_session(user_id: int, game_session_id: int, score: int, attempts_remaining: int):
        # Check that all values are set. Looks better than just doing a bunch of "and" stmts
        if all(v is not None for v in [user_id, game_session_id, score, attempts_remaining]):
            user_game_session = UserGameSession(
                user_id=user_id,
                game_session_id=game_session_id,
                score=score,
                attempts_remaining=attempts_remaining,
            )
            db.session.add(user_game_session)
            db.session.commit()
            return user_game_session
        else:
            return None

    @staticmethod
    def get_user_game_session(user_game_session_id):
        return UserGameSession.query.get(user_game_session_id)

    @staticmethod
    def get_all_users_for_specific_game_session(game_session_id):
        table_join = db.session.query(User).join(UserGameSession)
        users = table_join.filter(UserGameSession.game_session_id == game_session_id).all()
        return users

    @staticmethod
    def user_in_camp(user_id, round_id):
        user_events = UserEventManager.get_all_rows_for_user_id_and_round(user_id, round_id)

        wrong_answers = 0
        for event in user_events:
            # User voted NO
            if event.game_event.event_type == "vote" and event.answer.content == "No":
                return True

            # User got 2 answers wrong
            if not event.answer.is_correct:
                wrong_answers += 1

            if wrong_answers >= 2:
                return True

            # User got 2 danger cards
            game_over_counter = defaultdict(int)
            if event.game_event.event_type == "danger":
                if game_over_counter[event.game_event.event_data] == 0:
                    game_over_counter[event.game_event.event_data] += 1
                else:
                    return True

            # User got 1 danger card and 1 answer wrong
            if game_over_counter[event.game_event.event_data] == 1 and wrong_answers == 1:
                return True

        return False
