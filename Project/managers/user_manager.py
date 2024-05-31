from models.all_models import User
from app import db


class UserManager:
    @staticmethod
    def create_user(name: str, total_points: int):
        if all(v is not None for v in [name, total_points]):
            user = User(
                name=name,
                total_points=total_points
            )
            db.session.add(user)
            db.session.commit()
            return user
        else:
            return None

    @staticmethod
    def get_user(user_id):
        # user = get_user(5)
        return User.query.get(user_id)

    @staticmethod
    def get_all_users():
        return db.session.query(User).all()
