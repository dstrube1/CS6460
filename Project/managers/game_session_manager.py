from models.all_models import GameSession
from app import db
import hashlib


class GameSessionManager:

    def create_game_session(is_active: bool, current_round: int, quiz_id: int, max_rounds:  int = 5):
        # Check that all values are set. Looks better than just doing a bunch of "and" stmts
        if all(v is not None for v in [is_active, current_round, max_rounds]):
            game_session = GameSession(
                is_active=is_active,
                current_round=current_round,
                max_rounds=max_rounds,
                quiz_id=quiz_id
            )
            db.session.add(game_session)
            db.session.commit()
            # the participation code is based on id, which we got only AFTER the row is created
            participation_code = GameSessionManager.create_participation_code(game_session.id)
            GameSessionManager.update_game_session_column(game_session, "participation_code", participation_code)
            return game_session
        else:
            return None

    @staticmethod
    def get_game_session(game_session_id):
        return GameSession.query.get(game_session_id)

    @staticmethod
    def get_game_session_from_participation_code(participation_code):
        return GameSession.query.filter_by(participation_code=participation_code).first() or False

    @staticmethod
    def create_participation_code(session_id):
        id_string = str(session_id)
        sha256_hash = hashlib.sha256(id_string.encode())
        hash_hex = sha256_hash.hexdigest()
        # Use only the first 6 chars of produced hash
        short_hash = hash_hex[:6].upper()
        return short_hash

    @staticmethod
    def update_game_session_column(game_session, column_name, new_value):
        # Retrieve the GameSession by its ID
        if game_session is not None:
            # Check if the provided column name exists in the GameSession model
            if hasattr(game_session, column_name):
                # Set the new column value
                setattr(game_session, column_name, new_value)
                db.session.commit()
                return True  # Successful update
            else:
                return False  # Invalid column name
        else:
            return False  # GameSession not found


