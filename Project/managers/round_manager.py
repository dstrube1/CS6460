from models.all_models import Round
from app import db


class RoundManager:
    @staticmethod
    def create_round(round_number: int, is_complete: bool, game_session_id: int):
        # Check that all values are set. Looks better than just doing a bunch of "and" stmts
        if all(v is not None for v in [round_number, is_complete, game_session_id]):
            round = Round(
                round_number=round_number,
                is_complete=is_complete,
                game_session_id=game_session_id
            )
            db.session.add(round)
            db.session.commit()
            return round
        else:
            return None

    @staticmethod
    def get_round(round_id):
        return Round.query.get(round_id)

    @staticmethod
    def get_round_from_game_session_id(game_session_id, round_num):
        return Round.query.filter_by(game_session_id=game_session_id, round_number=round_num).first()
