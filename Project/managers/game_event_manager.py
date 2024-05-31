from models.all_models import GameEvent
from app import db
from managers.question_manager import QuestionManager

class GameEventManager:
    @staticmethod
    def create_game_event(question_id: int, round_id: int, session_id: int, event_order: int,
                          event_type: str, event_data: str, event_completed: bool):
        # Check that all values are set. Looks better than just doing a bunch of "and" stmts
        if all(v is not None for v in [round_id, session_id]):
            game_event = GameEvent(
                question_id=question_id,
                round_id=round_id,
                session_id=session_id,

                event_type=event_type,
                event_data=event_data,
                event_completed=event_completed,
                event_order=event_order,
                event_skipped=False
            )
            db.session.add(game_event)
            db.session.commit()
            return game_event
        else:
            return None

    @staticmethod
    def get_game_event(game_event_id):
        return GameEvent.query.get(game_event_id)

    @staticmethod
    def get_game_event_from_session_round_question_ids(session_id, round_id, question_id):
        return GameEvent.query.filter(
            GameEvent.session_id == session_id,
            GameEvent.round_id == round_id,
            GameEvent.question_id == question_id)\
            .first()

    @staticmethod
    def update_game_event_column(game_event, column_name, new_value):
        # Retrieve the GameEvent by its ID
        if game_event is not None:
            # Check if the provided column name exists in the GameEvent model
            if hasattr(game_event, column_name):
                # Set the new column value
                setattr(game_event, column_name, new_value)
                db.session.commit()
                return True  # Successful update
            else:
                return False  # Invalid column name
        else:
            return False  # GameEvent not found

    @staticmethod
    def round_complete(session_id, round_id):
        return GameEvent.query.filter(
            GameEvent.session_id == session_id,
            GameEvent.round_id == round_id,
            GameEvent.event_completed == False).first() is None

    @staticmethod
    def get_game_events_for_current_round(game_session_id, round_id):
        round_game_events = db.session.query(GameEvent)\
            .filter(GameEvent.session_id == game_session_id, GameEvent.round_id == round_id).all()

        rows = sorted(round_game_events, key=lambda row: row.event_order, reverse=False)
        try:
            index = [row.event_completed for row in rows].index(False)
        except ValueError:
            index = len(rows) - 1
        rows = rows[:index + 1]
        return rows

    @staticmethod
    def complete_all_events_until_game_or_round_over(session_id, round_id):
        rows = (GameEvent.query.filter(
            GameEvent.session_id == session_id,
            GameEvent.round_id == round_id,
            GameEvent.event_completed == False)
                .order_by(GameEvent.id)
                .all())

        for row in rows:
            if row.event_type not in ["round_over", "game_over"] and not row.event_completed:
                row.event_completed = True
                row.event_skipped = True

        db.session.commit()

    @staticmethod
    def set_questions_up_to_current_event_id_to_looted(session_id, round_id, current_event_id):
        events = GameEvent.query.filter(
            GameEvent.session_id == session_id,
            GameEvent.round_id == round_id,
            GameEvent.event_type == "question",
            GameEvent.id < current_event_id
        )
        for event in events:
            GameEventManager.update_game_event_column(
                event,
                "event_data",
                "looted"
            )

    @staticmethod
    def get_looted_questions_up_to_specific_event_id(session_id, round_id, current_event_id):
        events = GameEvent.query.filter(
            GameEvent.session_id == session_id,
            GameEvent.round_id == round_id,
            GameEvent.event_type == "question",
            GameEvent.event_data == "looted",
            GameEvent.id < current_event_id
        )

        question_ids = [event.question_id for event in events]

        return QuestionManager.get_questions_for_specified_ids(question_ids)



