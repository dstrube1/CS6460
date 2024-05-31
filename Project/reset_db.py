from models.all_models import *
from managers.quiz_manager import QuizManager
from managers.question_manager import QuestionManager
from managers.answer_manager import AnswerManager
import requests

# Make sure to start the server (flask run) BEFORE running this script!!!
db.create_all()

# Prepare some test data
new_quiz = QuizManager.create_quiz("Demo simple math quiz")

# Create question 1
question_one = QuestionManager.create_question(
            content="What is 2 + 2?",
            points=50,
            answer_type="mcq",
            difficulty_lvl="Easy",
            quiz_id=new_quiz.id
        )

# Create answers for question 1
AnswerManager.create_answer(content="4", is_correct=True, question_id=question_one.id)
AnswerManager.create_answer(content="2", is_correct=False, question_id=question_one.id)
AnswerManager.create_answer(content="7", is_correct=False, question_id=question_one.id)
AnswerManager.create_answer(content="8", is_correct=False, question_id=question_one.id)

question_two = QuestionManager.create_question(
            content="What is a * b?",
            points=50,
            answer_type="mcq",
            difficulty_lvl="Medium",
            quiz_id=new_quiz.id
        )

AnswerManager.create_answer(content="ab", is_correct=True, question_id=question_two.id)
AnswerManager.create_answer(content="aa", is_correct=False, question_id=question_two.id)
AnswerManager.create_answer(content="2ab", is_correct=False, question_id=question_two.id)
AnswerManager.create_answer(content="2b", is_correct=False, question_id=question_two.id)

question_three = QuestionManager.create_question(
            content="What is 2 x 6?",
            points=80,
            answer_type="mcq",
            difficulty_lvl="Medium",
            quiz_id=new_quiz.id
        )

AnswerManager.create_answer(content="12", is_correct=True, question_id=question_three.id)
AnswerManager.create_answer(content="11", is_correct=False, question_id=question_three.id)
AnswerManager.create_answer(content="13", is_correct=False, question_id=question_three.id)
AnswerManager.create_answer(content="15", is_correct=False, question_id=question_three.id)

question_four = QuestionManager.create_question(
            content="What is 5 + 5 * 5?",
            points=40,
            answer_type="mcq",
            difficulty_lvl="Impossible",
            quiz_id=new_quiz.id
        )

AnswerManager.create_answer(content="70", is_correct=False, question_id=question_four.id)
AnswerManager.create_answer(content="30", is_correct=True, question_id=question_four.id)
AnswerManager.create_answer(content="50", is_correct=False, question_id=question_four.id)
AnswerManager.create_answer(content="15", is_correct=False, question_id=question_four.id)

question_five = QuestionManager.create_question(
            content="What is 5 / 5?",
            points=30,
            answer_type="mcq",
            difficulty_lvl="Hard",
            quiz_id=new_quiz.id
        )

AnswerManager.create_answer(content="0", is_correct=False, question_id=question_five.id)
AnswerManager.create_answer(content="1", is_correct=True, question_id=question_five.id)
AnswerManager.create_answer(content="2", is_correct=False, question_id=question_five.id)

question_six = QuestionManager.create_question(
            content="What is (0! + 0! + 0!) ?",
            points=40,
            answer_type="mcq",
            difficulty_lvl="Hard",
            quiz_id=new_quiz.id
        )

AnswerManager.create_answer(content="3", is_correct=True, question_id=question_six.id)
AnswerManager.create_answer(content="0", is_correct=False, question_id=question_six.id)
AnswerManager.create_answer(content="1", is_correct=False, question_id=question_six.id)
AnswerManager.create_answer(content="4", is_correct=False, question_id=question_six.id)

question_seven = QuestionManager.create_question(
            content="What is the sum of first 3 prime numbers?",
            points=40,
            answer_type="mcq",
            difficulty_lvl="Hard",
            quiz_id=new_quiz.id
        )

AnswerManager.create_answer(content="6", is_correct=True, question_id=question_seven.id)
AnswerManager.create_answer(content="5", is_correct=False, question_id=question_seven.id)
AnswerManager.create_answer(content="4", is_correct=False, question_id=question_seven.id)
AnswerManager.create_answer(content="7", is_correct=False, question_id=question_seven.id)

question_eight = QuestionManager.create_question(
            content="What is 7 * 7 + 5",
            points=30,
            answer_type="mcq",
            difficulty_lvl="Hard",
            quiz_id=new_quiz.id
        )

AnswerManager.create_answer(content="45", is_correct=False, question_id=question_eight.id)
AnswerManager.create_answer(content="56", is_correct=False, question_id=question_eight.id)
AnswerManager.create_answer(content="23", is_correct=False, question_id=question_eight.id)
AnswerManager.create_answer(content="54", is_correct=True, question_id=question_eight.id)

question_nine = QuestionManager.create_question(
            content="What is the highest common factor 30 and 132?",
            points=70,
            answer_type="mcq",
            difficulty_lvl="Hard",
            quiz_id=new_quiz.id
        )

AnswerManager.create_answer(content="4", is_correct=False, question_id=question_nine.id)
AnswerManager.create_answer(content="5", is_correct=False, question_id=question_nine.id)
AnswerManager.create_answer(content="6", is_correct=True, question_id=question_nine.id)
AnswerManager.create_answer(content="7", is_correct=False, question_id=question_nine.id)

question_ten = QuestionManager.create_question(
            content="If 1=3, 2=3, 3=5, 4=4, and 5=4, what is 6=?",
            points=80,
            answer_type="mcq",
            difficulty_lvl="Hard",
            quiz_id=new_quiz.id
        )

AnswerManager.create_answer(content="3", is_correct=True, question_id=question_ten.id)
AnswerManager.create_answer(content="4", is_correct=False, question_id=question_ten.id)
AnswerManager.create_answer(content="5", is_correct=False, question_id=question_ten.id)
AnswerManager.create_answer(content="6", is_correct=False, question_id=question_ten.id)

question_eleven = QuestionManager.create_question(
            content="What is the year 1982 in Roman Numerals?",
            points=100,
            answer_type="mcq",
            difficulty_lvl="Hard",
            quiz_id=new_quiz.id
        )

AnswerManager.create_answer(content="MIMMLXXXI", is_correct=False, question_id=question_eleven.id)
AnswerManager.create_answer(content="MCVLXXXII", is_correct=False, question_id=question_eleven.id)
AnswerManager.create_answer(content="MCMLXXXII", is_correct=True, question_id=question_eleven.id)
AnswerManager.create_answer(content="MCVLVVXXI", is_correct=False, question_id=question_eleven.id)

question_twelve = QuestionManager.create_question(
            content="What is x in: -15 + (-5x)=0 ?",
            points=100,
            answer_type="mcq",
            difficulty_lvl="Hard",
            quiz_id=new_quiz.id
        )

AnswerManager.create_answer(content="-3", is_correct=True, question_id=question_twelve.id)
AnswerManager.create_answer(content="-2", is_correct=False, question_id=question_twelve.id)
AnswerManager.create_answer(content="4", is_correct=False, question_id=question_twelve.id)
AnswerManager.create_answer(content="-6", is_correct=False, question_id=question_twelve.id)


# Make sure to start the server (flask run) BEFORE running this script!!!
r = requests.post(url="http://localhost:5000/make_game",
                  data={
                      'max_rounds': '3',
                      'make_game_with_quiz_id': new_quiz.id,
                      'is_active': 'yes',
                      'current_round': '1'
                  })


new_quiz = QuizManager.create_quiz("Demo geography quiz")

# Create question 1
question_one = QuestionManager.create_question(
            content="What is the capital of India?",
            points=15,
            answer_type="mcq",
            difficulty_lvl="Easy",
            quiz_id=new_quiz.id
        )

# Create answers for question 1
AnswerManager.create_answer(content="New Delhi", is_correct=True, question_id=question_one.id)
AnswerManager.create_answer(content="Pune", is_correct=False, question_id=question_one.id)
AnswerManager.create_answer(content="Bangalore", is_correct=False, question_id=question_one.id)
AnswerManager.create_answer(content="Mumbai", is_correct=False, question_id=question_one.id)

question_two = QuestionManager.create_question(
            content="In which country can you find the Leaning Tower of Pisa?",
            points=20,
            answer_type="mcq",
            difficulty_lvl="Medium",
            quiz_id=new_quiz.id
        )

AnswerManager.create_answer(content="Italy", is_correct=True, question_id=question_two.id)
AnswerManager.create_answer(content="Spain", is_correct=False, question_id=question_two.id)
AnswerManager.create_answer(content="Portugal", is_correct=False, question_id=question_two.id)
AnswerManager.create_answer(content="USA", is_correct=False, question_id=question_two.id)

question_three = QuestionManager.create_question(
            content="Which planet is nearest to Earth?",
            points=20,
            answer_type="mcq",
            difficulty_lvl="Medium",
            quiz_id=new_quiz.id
        )

AnswerManager.create_answer(content="Mercury", is_correct=True, question_id=question_three.id)
AnswerManager.create_answer(content="Mars", is_correct=False, question_id=question_three.id)
AnswerManager.create_answer(content="Jupiter", is_correct=False, question_id=question_three.id)
AnswerManager.create_answer(content="Uranus", is_correct=False, question_id=question_three.id)

question_four = QuestionManager.create_question(
            content="What is the name of the biggest ocean on Earth?",
            points=30,
            answer_type="mcq",
            difficulty_lvl="Impossible",
            quiz_id=new_quiz.id
        )

AnswerManager.create_answer(content="Atlantic", is_correct=False, question_id=question_four.id)
AnswerManager.create_answer(content="Pacific", is_correct=True, question_id=question_four.id)
AnswerManager.create_answer(content="Arctic", is_correct=False, question_id=question_four.id)
AnswerManager.create_answer(content="Indian", is_correct=False, question_id=question_four.id)

question_five = QuestionManager.create_question(
            content="What is the biggest desert?",
            points=30,
            answer_type="mcq",
            difficulty_lvl="Hard",
            quiz_id=new_quiz.id
        )

AnswerManager.create_answer(content="Gobi", is_correct=False, question_id=question_five.id)
AnswerManager.create_answer(content="Sahara", is_correct=True, question_id=question_five.id)
AnswerManager.create_answer(content="Arabian", is_correct=False, question_id=question_five.id)
AnswerManager.create_answer(content="Mojave", is_correct=False, question_id=question_five.id)

question_six = QuestionManager.create_question(
            content="Which is the highest mountain?",
            points=15,
            answer_type="mcq",
            difficulty_lvl="Hard",
            quiz_id=new_quiz.id
        )

AnswerManager.create_answer(content="Kilimanjaro", is_correct=False, question_id=question_six.id)
AnswerManager.create_answer(content="Everest", is_correct=True, question_id=question_six.id)
AnswerManager.create_answer(content="Himalayas", is_correct=False, question_id=question_six.id)

question_seven = QuestionManager.create_question(
            content="What is the capital of Canada?",
            points=20,
            answer_type="mcq",
            difficulty_lvl="Hard",
            quiz_id=new_quiz.id
        )

AnswerManager.create_answer(content="Ottawa", is_correct=True, question_id=question_seven.id)
AnswerManager.create_answer(content="Toronto", is_correct=False, question_id=question_seven.id)
AnswerManager.create_answer(content="Montreal", is_correct=False, question_id=question_seven.id)
AnswerManager.create_answer(content="Vancouver", is_correct=False, question_id=question_seven.id)

question_eight = QuestionManager.create_question(
            content="Ljubljana is the capital of which country?",
            points=50,
            answer_type="mcq",
            difficulty_lvl="Hard",
            quiz_id=new_quiz.id
        )

AnswerManager.create_answer(content="Slovenia", is_correct=True, question_id=question_eight.id)
AnswerManager.create_answer(content="Belarus", is_correct=False, question_id=question_eight.id)
AnswerManager.create_answer(content="Finland", is_correct=False, question_id=question_eight.id)
AnswerManager.create_answer(content="Kazakhstan", is_correct=False, question_id=question_eight.id)

question_nine = QuestionManager.create_question(
            content="Which country is also known as the Netherlands?",
            points=30,
            answer_type="mcq",
            difficulty_lvl="Hard",
            quiz_id=new_quiz.id
        )

AnswerManager.create_answer(content="Holland", is_correct=True, question_id=question_nine.id)
AnswerManager.create_answer(content="Belgium", is_correct=False, question_id=question_nine.id)
AnswerManager.create_answer(content="Frisland", is_correct=False, question_id=question_nine.id)
AnswerManager.create_answer(content="Sweden", is_correct=False, question_id=question_nine.id)

question_ten = QuestionManager.create_question(
            content="What is the capital of Spain?",
            points=30,
            answer_type="mcq",
            difficulty_lvl="Hard",
            quiz_id=new_quiz.id
        )

AnswerManager.create_answer(content="Madrid", is_correct=True, question_id=question_ten.id)
AnswerManager.create_answer(content="Barcelona", is_correct=False, question_id=question_ten.id)
AnswerManager.create_answer(content="Vatican", is_correct=False, question_id=question_ten.id)
AnswerManager.create_answer(content="Venice", is_correct=False, question_id=question_ten.id)

question_eleven = QuestionManager.create_question(
            content="What is the coldest place on Earth?",
            points=10,
            answer_type="mcq",
            difficulty_lvl="Hard",
            quiz_id=new_quiz.id
        )

AnswerManager.create_answer(content="Siberia", is_correct=False, question_id=question_eleven.id)
AnswerManager.create_answer(content="Antarctica", is_correct=True, question_id=question_eleven.id)
AnswerManager.create_answer(content="Iceland", is_correct=False, question_id=question_eleven.id)
AnswerManager.create_answer(content="Ehypt", is_correct=False, question_id=question_eleven.id)

question_twelve = QuestionManager.create_question(
            content="What is the capital of Senegal?",
            points=30,
            answer_type="mcq",
            difficulty_lvl="Hard",
            quiz_id=new_quiz.id
        )

AnswerManager.create_answer(content="Touba", is_correct=False, question_id=question_twelve.id)
AnswerManager.create_answer(content="Saint Louis", is_correct=False, question_id=question_twelve.id)
AnswerManager.create_answer(content="Diourbel", is_correct=False, question_id=question_twelve.id)
AnswerManager.create_answer(content="Dakar", is_correct=True, question_id=question_twelve.id)


# Make sure to start the server (flask run) BEFORE running this script!!!
r = requests.post(url="http://localhost:5000/make_game",
                  data={
                      'max_rounds': '3',
                      'make_game_with_quiz_id': new_quiz.id,
                      'is_active': 'yes',
                      'current_round': '1'
                  })

print(r.text)



