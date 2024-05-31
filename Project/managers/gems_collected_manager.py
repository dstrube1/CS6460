from models.all_models import GemsCollected, User, GameSession
from app import db


class GemsCollectedManager:
    @staticmethod
    def create_gems_collected(gem_count: int, user_id: int, session_id: int, potential_gems: int):
        # Check that all values are set. Looks better than just doing a bunch of "and" stmts
        if all(v is not None for v in [gem_count, user_id, session_id, potential_gems]):
            gems_collected = GemsCollected(
                gem_count=gem_count,
                user_id=user_id,
                session_id=session_id,
                potential_gems=potential_gems
            )
            db.session.add(gems_collected)
            db.session.commit()
            return gems_collected
        else:
            return None

    @staticmethod
    def get_gems_collected(gems_collected_id):
        return GemsCollected.query.get(gems_collected_id)

    @staticmethod
    def get_gems_for_specific_users_and_game_session(users, game_session_id):
        user_ids = [user.id for user in users]
        gem_counts_tuples = db.session.query(User.id, GemsCollected.gem_count) \
            .join(GemsCollected, User.id == GemsCollected.user_id) \
            .join(GameSession, GemsCollected.session_id == GameSession.id) \
            .filter(GameSession.id == game_session_id) \
            .filter(User.id.in_(user_ids)) \
            .all()

        # At this point gem_counts_tuples is a list of tuples.
        # Each tuple contains the User ID and gems
        # collected during the specified game session (e.g. (1, 4))
        # It would be easier to read the data if it was in a dictionary format,
        # so that is done below.

        dict_to_return = {}
        for user_id, gems_collected in gem_counts_tuples:
            if user_id not in dict_to_return.keys():
                dict_to_return[user_id] = gems_collected

        return dict_to_return

    @staticmethod
    def get_gems_for_user_id(user_id):
        return GemsCollected.query.filter(GemsCollected.user_id == user_id).first()

    @staticmethod
    def update_gems_collected_column(gems_collected: GemsCollected, column_name, new_value):
        if gems_collected is not None:
            # Check if the provided column name exists in the GameSession model
            if hasattr(gems_collected, column_name):
                # Set the new column value
                setattr(gems_collected, column_name, new_value)
                db.session.commit()
                return True  # Successful update
            else:
                return False  # Invalid column name
        else:
            return False


