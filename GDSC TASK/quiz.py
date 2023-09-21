from random import shuffle
from questions import Question, question_data
import time


def get_user_name():
    return input("Hello, what's your name: ")


class Quiz:
    def __init__(self, player_name):
        self.player_name = player_name
        self.questions = [Question(q["text"], q["answer"]) for q in question_data]
        self.score = 0
        self.current_question_index = 0
        self.lifelines = 2
        shuffle(self.questions)

    def next_question(self):
        if self.current_question_index < len(self.questions):
            return self.questions[self.current_question_index]

    def check_answer(self, user_answer):
        current_question = self.next_question()
        if not current_question:
            return  # No more questions
        if current_question.check_answer(user_answer):
            self.score += 2
        else:
            self.score -= 1
        self.current_question_index += 1

    def use_lifeline(self):
        if self.lifelines > 0:
            current_question = self.questions[self.current_question_index - 1]
            options = ["True", "False"]
            correct_answer = "True" if current_question.answer else "False"

            if correct_answer == "True":
                options.remove("False")  # Remove False as it's incorrect
            else:
                options.remove("True")  # Remove True as it's incorrect

            print(f"You used a lifeline. The options are now: {options}")
            self.lifelines -= 1
        else:
            print("You've used all your lifelines!")

    def start_quiz(self):
        print(f"Welcome, {self.player_name}, to the Quiz!")
        while self.current_question_index < len(self.questions):
            question = self.next_question()
            print(question.text)

            # Timer (10 seconds)
            timer = 10
            print(f"Time remaining: {timer} seconds")
            while timer > 0:

                # Check if user answered
                if timer <= 0:
                    print("Time's up! You lose 1 point.")
                    self.score -= 1

                if timer <= 5:
                    print(f"Time remaining: {timer} seconds")
                    user_answer = input("Enter 'True' or 'False': ").strip().lower()
                    if user_answer in ['true', 'false']:
                        user_answer = user_answer == 'true'
                        print("You answered in the nick of time!")
                        self.check_answer(user_answer)
                        break  # Exit the timer loop if an answer is provided

                else:
                    if timer % 5 == 0:
                        lifeline_choice = input("Do you want to use a lifeline? (yes/no): ").strip().lower()
                        if lifeline_choice == 'yes':
                            self.use_lifeline()
                timer -= 1

        self.display_score()

    def questions_remain(self):
        return self.current_question_index < len(self.questions)

    def display_score(self):
        print(f"Quiz over, {self.player_name}! Your score is: {self.score}")


if __name__ == "__main__":
    player_name = get_user_name()
    quiz = Quiz(player_name)
    quiz.start_quiz()
