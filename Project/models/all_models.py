from app import db
from sqlalchemy.sql import func


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    total_points = db.Column(db.Integer)
    user_game_sessions = db.relationship("UserGameSession", backref='user', lazy=True)
    user_events = db.relationship("UserEvent", backref='user', lazy=True, cascade="all, delete-orphan")
    gems_collected = db.relationship("GemsCollected", backref='user', lazy=True, cascade="all, delete-orphan")


class UserGameSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    game_session_id = db.Column(db.Integer, db.ForeignKey("game_session.id"))
    score = db.Column(db.Integer)
    attempts_remaining = db.Column(db.Integer)


class UserEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    answer_id = db.Column(db.Integer, db.ForeignKey("answer.id"))
    session_id = db.Column(db.Integer, db.ForeignKey("game_session.id"))
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    game_event_id = db.Column(db.Integer, db.ForeignKey("game_event.id"))


class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    round_number = db.Column(db.Integer)
    is_complete = db.Column(db.Boolean)
    game_session_id = db.Column(db.Integer, db.ForeignKey("game_session.id"))

    game_events = db.relationship('GameEvent', backref='round', lazy=True, cascade="all, delete-orphan")


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade="all, delete-orphan")
    game_sessions = db.relationship('GameSession', backref='quiz', lazy=True, cascade="all, delete-orphan")


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    points = db.Column(db.Integer)
    answer_type = db.Column(db.String(20))
    difficulty_lvl = db.Column(db.String(20))
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"))

    answers = db.relationship('Answer', backref='question', lazy=True, cascade="all, delete-orphan")
    questions_rounds = db.relationship('GameEvent', backref='question', lazy=True, cascade="all, delete-orphan")
    user_events = db.relationship('UserEvent', backref='question', lazy=True, cascade="all, delete-orphan")


class GemsCollected(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gem_count = db.Column(db.Integer)
    potential_gems = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    session_id = db.Column(db.Integer, db.ForeignKey("game_session.id"))


class GameSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Boolean)
    start_time = db.Column(db.DateTime(timezone=True), server_default=func.now())
    end_time = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    current_round = db.Column(db.Integer)
    max_rounds = db.Column(db.Integer)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"))
    participation_code = db.Column(db.String(10), unique=True)

    rounds = db.relationship("Round", backref='game_session', lazy=True, cascade="all, delete-orphan")
    user_game_sessions = db.relationship("UserGameSession", backref='game_session', lazy=True, cascade="all, delete-orphan")
    user_events = db.relationship("UserEvent", backref='game_session', lazy=True, cascade="all, delete-orphan")
    gems_collected = db.relationship("GemsCollected", backref='game_session', lazy=True, cascade="all, delete-orphan")
    game_events = db.relationship("GameEvent", backref='game_session', lazy=True, cascade="all, delete-orphan")


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    is_correct = db.Column(db.Boolean)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))

    user_events = db.relationship('UserEvent', backref='answer', lazy=True, cascade="all, delete-orphan")


class GameEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    round_id = db.Column(db.Integer, db.ForeignKey("round.id"))
    session_id = db.Column(db.Integer, db.ForeignKey("game_session.id"))
    event_type = db.Column(db.String(50))
    event_data = db.Column(db.String(100))
    event_completed = db.Column(db.Boolean)
    event_skipped = db.Column(db.Boolean)
    event_order = db.Column(db.Integer)
    user_events = db.relationship('UserEvent', backref='game_event', lazy=True, cascade="all, delete-orphan")

