import requests
import html
import time
import random

def clear_console():
    print("\033c", end="")

# Function to get the list of categories from the Open Trivia Database
def get_categories():
    url = "https://opentdb.com/api_category.php"
    response = requests.get(url)
    categories = response.json()['trivia_categories']
    return {category['name']: category['id'] for category in categories}

# Function to fetch questions from the Open Trivia Database
def fetch_questions(amount=10, category='', difficulty='', type=''):
    url = f"https://opentdb.com/api.php?amount={amount}&category={category}&difficulty={difficulty}&type={type}"
    response = requests.get(url)
    return response.json()['results']

# Function to display a question, take user's answer and return if it was correct
def ask_question(question):
    print(html.unescape(question['question']))
    choices = [html.unescape(choice) for choice in question['incorrect_answers']]
    correct_answer = html.unescape(question['correct_answer'])
    choices.append(correct_answer)
    random.shuffle(choices)
    for index, choice in enumerate(choices, start=1):
        print(f"{index}: {choice}")
    user_answer = input("Your answer (number): ")
    return (choices[int(user_answer) - 1] == correct_answer, correct_answer)

# Function to display menu and get user's choice for category and difficulty
def get_user_preferences():
    categories = get_categories()
    print("Choose a category:")
    for index, (name, _) in enumerate(categories.items(), start=1):
        print(f"{index}: {name}")
    category_choice = int(input("Enter the number of your choice: "))
    category_id = list(categories.values())[category_choice - 1]
    clear_console()

    difficulties = ['easy', 'medium', 'hard']
    print("\nChoose a difficulty:")
    for index, difficulty in enumerate(difficulties, start=1):
        print(f"{index}: {difficulty}")
    difficulty_choice = int(input("Enter the number of your choice: "))
    difficulty = difficulties[difficulty_choice - 1]
    clear_console()

    return category_id, difficulty

# Function to display the timer
def display_timer(start_time, time_limit):
    elapsed_time = int(time.time() - start_time)
    time_left = max(0, time_limit - elapsed_time)
    print(f"Time left: {time_left} seconds")

# Main game function
def quiz_game(total_questions=50, time_limit=60):
    replay = True
    
    while replay:
        category_id, difficulty = get_user_preferences()
        questions = fetch_questions(amount=total_questions, category=category_id, difficulty=difficulty)
        correct_answers = 0
        start_time = time.time()
    
        for question in questions:
            if time.time() - start_time > time_limit:
                print("Time's up!")
                replay = input("Do you want to replay the game? (y/N)").lower() == 'y'
                break
            display_timer(start_time, time_limit)
        
            if ask_question(question):
                print("Correct!")
                correct_answers += 1
            else:
                print("Wrong answer!")
        
            # Prompt the user to press Enter to continue
            input("Press Enter to continue...")
            clear_console()
        
            if correct_answers == 5:
                print("Congratulations, you've won the game!")
                replay = input("Do you want to replay the game? (y/N)").lower() == 'y'
                break

        if not replay:
            print(f"Game over! You answered {correct_answers}/{total_questions} questions correctly.")
            # Prompt the user to press Enter to continue
            input("Press Enter to exit...")

# Start the game
quiz_game()
