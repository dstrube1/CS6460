from flask import render_template, session, redirect, url_for
from app import app
from managers.question_manager import QuestionManager
from managers.answer_manager import AnswerManager
from managers.game_session_manager import GameSessionManager
from managers.gems_collected_manager import GemsCollectedManager
from managers.quiz_manager import QuizManager
from managers.round_manager import RoundManager
from managers.user_event_manager import UserEventManager
from managers.user_game_session_manager import UserGameSessionManager
from managers.user_manager import UserManager
from managers.game_event_manager import GameEventManager
from models.all_models import Question
from flask import request
from flask import json
from flask_session import Session
from collections import defaultdict
import random


Session(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/join_game', methods=["GET", "POST"])
def join_game_route():
    if request.method == "POST":
        # Catch the new game request that is made when the "Submit" button is pressed
        # The request.form dictionary contains all the values from the form. 
        # The UserGameSessionManager.create_user_game_session will use the
        # Flask-SQLAlchemy ORM to insert the data in the database.
        game_code = request.form["game_code"]
        game_session = GameSessionManager.get_game_session_from_participation_code(game_code)
        if not game_session:
            return "<h1>Incorrect game code</h1><br> Please try again<br> Go back <a href=./>home</a>"
        else:
            first = ["The", "A", "Your"]
            second = ["Good", "Strong", "Smart", "Weird", "Wise", "Comfy", "Great", "Odd"]
            last = ["Monkey", "Horse", "Panda", "Snake", "Owl", "Cat", "Dog"]
            name = random.choice(first) + random.choice(second) + random.choice(last)

            new_user = UserManager.create_user(name=name, total_points=0)
            session["user_id"] = new_user.id
            session["active_game_id"] = game_session.id
            session["active_game_quiz_id"] = game_session.quiz_id
            session["active_game_code"] = game_code

            # TODO: Is the user_game_session relevant here? If so, how should it be used?
            UserGameSessionManager.create_user_game_session(
                user_id=session["user_id"],
                game_session_id=game_session.id,
                score=0,
                attempts_remaining=2,  # TODO: Attempts remaining only applies to wrongly answered questions
            )
            return redirect(url_for('main_game_route'))
    # If the request is NOT POST (i.e. the request comes from index.html)
    # display the input for user to enter the game code
    return render_template('join_game.html')


@app.route('/main_game')
def main_game_route():

    if "active_game_id" not in session.keys():
        return redirect(url_for('index'))

    game_session = GameSessionManager.get_game_session(session["active_game_id"])
    session_users = UserGameSessionManager.get_all_users_for_specific_game_session(game_session.id)

    # When someone new joins the game, create an entry in the GemsCollected table for them, to keep track of score
    if not GemsCollectedManager.get_gems_for_user_id(session["user_id"]):
        GemsCollectedManager.create_gems_collected(0, session["user_id"], game_session.id, 0)

    user_gem_dict = GemsCollectedManager.get_gems_for_specific_users_and_game_session(
        session_users,
        game_session.id)

    game_round = RoundManager.get_round_from_game_session_id(game_session.id, game_session.current_round)
    game_events = GameEventManager.get_game_events_for_current_round(game_session.id, game_round.id)

    current_event = game_events[-1]
    history = game_events[:-1]

    # Compute the amount of questions that are yet to come
    num_questions = len([event for event in game_round.game_events if event.event_type in ["question", "danger"]])
    num_questions -= len([event for event in history if event.event_type == ["question", "danger"]])
    if current_event.event_type in ["question", "danger"]:
        num_questions -= 1

    # TODO: Make a dict with question_id: user_answer
    user_event_rows = UserEventManager.get_all_rows_for_user_id_and_round(session["user_id"], game_round.id)
    question_user_answer_dict = {}
    for row in user_event_rows:
        question_user_answer_dict[row.question_id] = AnswerManager.get_answer(row.answer_id)

    player_already_answered = UserEventManager.player_already_completed_event(session["user_id"], current_event.id)

    if current_event.event_type == "game_over":
        return redirect(url_for('scoreboard_route'))

    return render_template("main_game_window.html",
                           users=session_users,
                           gem_dict=user_gem_dict,
                           current_event=current_event,
                           history=history,
                           player_id=session["user_id"],
                           current_round=game_session.current_round,
                           max_rounds=game_session.max_rounds,
                           round_id=game_round.id,
                           num_questions=num_questions,  # TODO: this needs to be fixed
                           game_code=session["active_game_code"],
                           user_game_session_manager=UserGameSessionManager,
                           user_answer_dict=question_user_answer_dict,
                           player_already_answered=True if player_already_answered else False,
                           )

@app.route("/scoreboard")
def scoreboard_route():
    users_in_game = UserGameSessionManager.get_all_users_for_specific_game_session(session["active_game_id"])
    gems_collected = GemsCollectedManager.get_gems_for_specific_users_and_game_session(
        users_in_game,
        session["active_game_id"]
    )
    return render_template(
        "scoreboard.html",
        gem_dict=gems_collected,
        users=users_in_game
    )

@app.route('/make_game', methods=["GET", "POST"])
def make_game_route():
    if request.method == "POST":
        if request.headers["Content-Type"] == "application/json":
            data = request.get_json()
            quiz_id = data.get('quiz_id')
            questions = QuestionManager.get_all_questions_for_specific_quiz(quiz_id)

            response_data = {}
            for question in questions:
                response_data[question.id] = question.content

            return json.jsonify(response_data=response_data)
        else:
            # Catch the new game request that is made when the "Submit" button is pressed
            # The request.form dictionary contains all the values from the form.
            # The GameSessionManager.create_game_session will use the
            # Flask-SQLAlchemy ORM to insert the data in the database.
            max_rounds = int(request.form["max_rounds"])
            quiz_id = int(request.form["make_game_with_quiz_id"])
            new_game = GameSessionManager.create_game_session(
                is_active=True,
                current_round=1,
                max_rounds=max_rounds,
                quiz_id=quiz_id
            )

            # TODO: Create order Rounds and Questions within those rounds
            questions = QuestionManager.get_all_questions_for_specific_quiz(quiz_id)
            random.shuffle(questions)

            def split_into_rounds(questions, max_rounds):
                questions_per_round = round(len(questions) / max_rounds)
                # TODO: Double check if this makes sense
                rounds = []
                for _ in range(max_rounds):
                    qs = questions[:questions_per_round]
                    rounds.append(qs)
                    questions = questions[questions_per_round:]
                if questions:
                    rounds[-1] += questions
                return rounds

            rounds = split_into_rounds(questions, max_rounds)

            for round_num in range(1, max_rounds + 1):
                new_round = RoundManager.create_round(round_num, False, new_game.id)

                danger_cards = []
                round_questions = rounds[round_num - 1]
                num_danger_cards = len(round_questions)
                number_of_types = num_danger_cards // 3
                # TODO: Evaluate how the rules should work for really small or really big rounds

                for danger_type in range(number_of_types):
                    danger_cards.append(danger_type)
                    danger_cards.append(danger_type)
                    danger_cards.append(danger_type)

                round_questions = round_questions + danger_cards
                random.shuffle(round_questions)

                game_over_counter = defaultdict(int)
                for idx, entry in enumerate(round_questions):
                    idx = idx * 2

                    # Create the questions for each round in a game
                    GameEventManager.create_game_event(
                        question_id=entry.id if isinstance(entry, Question)
                                    else QuestionManager.get_danger_card_question_for_quiz_id(new_game.quiz_id).id,
                        round_id=new_round.id,
                        session_id=new_game.id,
                        event_completed=False,
                        event_order=idx,
                        event_type="question" if isinstance(entry, Question) else "danger",
                        event_data=None if isinstance(entry, Question) else entry
                    )

                    # If it is not a danger card, and it is not the last question
                    if not isinstance(entry, int) and (idx // 2) != max_rounds:
                        idx += 1

                        # Add a voting round
                        GameEventManager.create_game_event(
                            question_id=QuestionManager.get_vote_question_for_quiz_id(new_game.quiz_id).id,
                            round_id=new_round.id,
                            session_id=new_game.id,
                            event_completed=False,
                            event_order=idx,
                            event_type="vote",
                            event_data=""
                        )

                    else:
                        # If there has been just one
                        if game_over_counter[entry] == 0:
                            game_over_counter[entry] += 1

                            idx += 1

                            # but still add the voting round
                            # Add a voting round
                            GameEventManager.create_game_event(
                                question_id=QuestionManager.get_vote_question_for_quiz_id(new_game.quiz_id).id,
                                round_id=new_round.id,
                                session_id=new_game.id,
                                event_completed=False,
                                event_order=idx,
                                event_type="vote",
                                event_data=""
                            )
                        else:
                            break

                if round_num == max_rounds:
                    # We are at the end of the game
                    # add the game over event
                    GameEventManager.create_game_event(
                        question_id=None,
                        round_id=new_round.id,
                        session_id=new_game.id,
                        event_completed=False,
                        event_order=idx + 1,  # this idx is still in memory
                        event_type="game_over",
                        event_data=""
                    )

                else:
                    # We are at the end of the round
                    # add the round over event
                    GameEventManager.create_game_event(
                        question_id=QuestionManager.get_round_over_question_for_quiz_id(new_game.quiz_id).id,
                        round_id=new_round.id,
                        session_id=new_game.id,
                        event_completed=False,
                        event_order=idx + 1,  # this idx is still in memory
                        event_type="round_over",
                        event_data=""
                    )

        # new_game now contains an instance of GameSession. It will have all the
        # necessary attributes, that we can pass on to the html and they will be displayed to the user.
        return render_template('make_game_success.html', new_game_id=new_game.id, participation_code=new_game.participation_code)
        #("<h1>NEW GAME WITH ID: {} added</h1>".format(new_game.id) +
               # "Use this game code to <a href='join_game'>join</a>: {} <br><br> Go back <a href=./>home</a>"
               # .format(new_game.participation_code))

    # If the request is NOT POST (i.e. the request comes from index.html)
    # just display the question creation page
    quizzes = QuizManager.get_all_quizzes()
    quiz_dict = {}

    for quiz in quizzes:
        questions = QuestionManager.get_all_questions_for_specific_quiz(quiz.id)
        quiz_dict[quiz.id] = questions

    return render_template('make_game.html', quizzes=quizzes, quiz_dict=quiz_dict)


@app.route('/new_quiz', methods=["GET", "POST"])
def new_quiz_route():
    return render_template('new_quiz.html')


@app.route('/new_quiz_<name>', methods=["GET", "POST"])
def new_quiz_named_route(name):
    new_quiz = QuizManager.create_quiz(name, add_vote=True)

    # When a quiz is created we automatically want to add a voting question. There should be just 1 voting question
    # per quiz, and it will be asked before every new event.
    # QuestionManager.get_vote_question_for_quiz_id(new_quiz.id).id
    return render_template('new_quiz_success.html', quiz_id=new_quiz.id)


@app.route('/submit_answer', methods=["POST"])
def submit_answer_route():
    answer_id = int(request.form["answer_id"])
    game_event_id = int(request.form["game_event_id"])

    game_event = GameEventManager.get_game_event(game_event_id)
    UserEventManager.create_user_event(
        session["user_id"],
        answer_id,
        session["active_game_id"],
        game_event.question_id,
        game_event.id
    )

    # Check if the current question is done (everyone has answered)
    user_events = UserEventManager.get_votes_for_game_event(game_event.id)
    game_session = GameSessionManager.get_game_session(session["active_game_id"])
    vote_question_for_game = QuestionManager.get_vote_question_for_quiz_id(game_session.quiz_id)
    yes_answer_id = AnswerManager.get_yes_answer_for_vote_question(vote_question_for_game.id).id
    no_answer_id = AnswerManager.get_no_answer_for_vote_question(vote_question_for_game.id).id
    completed = True
    all_users_in_camp = True
    for user_game_session in game_session.user_game_sessions:
        user_in_camp = UserGameSessionManager.user_in_camp(user_game_session.user_id, game_event.round_id)
        if not user_in_camp and user_game_session.user_id not in [event.user_id for event in user_events]:
            completed = False
            all_users_in_camp = False
        elif not user_in_camp:
            all_users_in_camp = False

    answer = AnswerManager.get_answer(answer_id)
    gems_so_far_obj = GemsCollectedManager.get_gems_for_user_id(session["user_id"])
    GemsCollectedManager.update_gems_collected_column(
        gems_so_far_obj,
        "potential_gems",
        gems_so_far_obj.potential_gems + answer.question.points
    )
    if completed and game_event.event_type == "vote":
        leavers = UserEventManager.get_players_that_voted(game_event.id, no_answer_id)
        explorers = UserEventManager.get_players_that_voted(game_event.id, yes_answer_id)
        for player in leavers:
            gems_so_far_obj = GemsCollectedManager.get_gems_for_user_id(player.user_id)
            GemsCollectedManager.update_gems_collected_column(
                gems_so_far_obj,
                "gem_count",
                gems_so_far_obj.potential_gems // len(leavers)
            )

        if len(leavers) > 0:
            for player in explorers:
                gems_so_far_obj = GemsCollectedManager.get_gems_for_user_id(player.user_id)
                GemsCollectedManager.update_gems_collected_column(
                    gems_so_far_obj,
                    "potential_gems",
                    0
                )

    if completed:
        GameEventManager.update_game_event_column(game_event, "event_completed", True)
        # If all players are in camp after this answer, then the round/game_over event should be triggered
        # To do this, we set all events up to the first round/game_over event to complete.
        if all_users_in_camp:
            GameEventManager.complete_all_events_until_game_or_round_over(game_event.session_id, game_event.round_id)

        # If all the questions in the round have been answered, go to the next round
        if GameEventManager.round_complete(session["active_game_id"], game_event.round_id):
            GameSessionManager.update_game_session_column(game_session, "current_round",
                                                          min(game_session.current_round + 1,
                                                              game_session.max_rounds))

    return redirect(url_for('main_game_route'))


@app.route('/new_question_and_answers_<quiz_id>', methods=["GET", "POST"])
def new_question_and_answers_quiz_id_route(quiz_id):
    # Just like new_question_and_answers, but with a quiz_id
    if request.method == "POST":
        new_question = QuestionManager.create_question(
            content=request.form["question"],
            points=int(request.form["gem_count"]),
            answer_type=request.form["answer_type"],
            difficulty_lvl=request.form["difficulty_lvl"],
            quiz_id=int(request.form["quiz_id"])
        )
        answer_texts = request.form.getlist('answer_texts[]')
        correct_answers = [value for key, value in request.form.items() if "correct_answer" in key]
        answers = []
        for i in range(len(answer_texts)):
            new_answer = AnswerManager.create_answer(
                content=answer_texts[i],
                is_correct=bool(correct_answers[i] == "true"),
                question_id=new_question.id
            )
            answers.append(new_answer)
        return render_template('new_question_and_answers_added_success.html', question=new_question, answers=answers)
    quizzes = QuizManager.get_all_quizzes()
    return render_template('new_question_and_answers.html', quizzes=quizzes, quiz_id=quiz_id)


@app.route('/new_question_and_answers', methods=["GET", "POST"])
def new_question_and_answers_route():
    # Combine the functionality of new_question_route and new_answer_route in one page
    if request.method == "POST":
        # Catch the new question request that is made when the "Submit" button is pressed
        # The request.form dictionary contains all the values from the form.
        # The QuestionManager.create_question will use the
        # Flask-SQLAlchemy ORM to insert the data in the database.
        new_question = QuestionManager.create_question(
            content=request.form["question"],
            points=int(request.form["gem_count"]),
            answer_type=request.form["answer_type"],
            difficulty_lvl=request.form["difficulty_lvl"],
            quiz_id=int(request.form["quiz_id"])
        )
        # Catch the new answer request that is made when the "Submit" button is pressed
        # The request.form dictionary contains all the values from the form.
        # The AnswerManager.create_answer will use the
        # Flask-SQLAlchemy ORM to insert the data in the database.
        answer_texts = request.form.getlist('answer_texts[]')
        correct_answers = [value for key, value in request.form.items() if "correct_answer" in key]
        answers = []
        for i in range(len(answer_texts)):
            new_answer = AnswerManager.create_answer(
                content=answer_texts[i],
                is_correct=bool(correct_answers[i] == "true"),
                question_id=new_question.id
            )
            answers.append(new_answer)
        return render_template('new_question_and_answers_added_success.html', question=new_question, answers=answers)
    quizzes = QuizManager.get_all_quizzes()
    return render_template('new_question_and_answers.html', quizzes=quizzes)


@app.route('/list_questions_<quiz_id>')
def list_questions_route(quiz_id):
    questions = QuestionManager.get_all_questions_for_specific_quiz(quiz_id)
    return render_template("list_questions.html", questions=questions)


@app.route('/test_db_models')
def test_models_route():
    new_quiz = QuizManager.create_quiz("Test quiz {}".format(str(random.randint(0, 1000))), add_vote=True)
    new_question = QuestionManager.create_question("Test question for Quiz {}".format(new_quiz.id), 1, "mcq", "Easy",
                                                   new_quiz.id)
    new_answer = AnswerManager.create_answer("Test answer for question {}".format(new_question.id), False,
                                             new_question.id)
    new_user = UserManager.create_user("TestUser {}".format(str(random.randint(0, 1000))), 0)
    new_game_session = GameSessionManager.create_game_session(False, 1, new_quiz.id, 5)
    new_gems_collected = GemsCollectedManager.create_gems_collected(1, 1, 1, 0)
    new_round = RoundManager.create_round(1, False, new_game_session.id)
    new_user_event = UserEventManager.create_user_event(new_user.id, new_answer.id, new_game_session.id, new_question.id)
    new_user_game_session = UserGameSessionManager.create_user_game_session(new_user.id, 1, 1, 2)

    return "The following Ids were created: " \
           "Quiz: {}, Question: {}, Answer: {}, " \
           "User: {}, Game session: {}, " \
           "Gems collected: {}, Round: {}, User answer: {}, " \
           "UserGameSession: {}".format(new_quiz.id, new_question.id, new_answer.id,
                                        new_user.id, new_game_session.id,
                                        new_gems_collected.id, new_round.id, new_user_event.id,
                                        new_user_game_session.id) + " <br> Go back <a href=./>home</a>"


@app.route('/delete_quiz_<id>')
def delete_quiz_route(id):
    QuizManager.delete_quiz(id)
    return render_template('delete_quiz_success.html', quiz_id=id)


@app.route('/delete_question_<id>')
def delete_question_route(id):
    QuestionManager.delete_question(id)
    return "Question id: " + id + " was deleted. Go back <a href=./>home</a>"


@app.route('/quiz_overview')
def quiz_overview_route():
    db_quizzes = QuizManager.get_all_quizzes()
    return render_template("quiz_overview.html", quizzes=db_quizzes)


@app.route('/should_refresh_<game_id>_<order_id>_<round_id>_<num_players>')
def should_refresh_route(game_id, order_id, round_id, num_players):
    game_events = GameEventManager.get_game_events_for_current_round(game_id, round_id)
    current_event = game_events[-1]
    refresh = False

    if current_event.event_completed:
        refresh = True

    if str(order_id) != str(current_event.event_order):
        refresh = True

    if int(num_players) != len(GameSessionManager.get_game_session(game_id).user_game_sessions):
        refresh = True

    return {"refresh": refresh}


@app.route('/how_to')
def how_to_route():
    return render_template("how_to.html")