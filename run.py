import sys
import random
import re
from colorama import Fore, init
# Import all quiz question sets
from data import JAK_QUESTIONS, RATCHET_QUESTIONS, GOD_OF_WAR_QUESTIONS

import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

import os
import json

# Google Sheets setup
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

if os.environ.get("CREDS"):
    # Load creds from Heroku config var
    creds_json = json.loads(os.environ["CREDS"])
    CREDS = Credentials.from_service_account_info(creds_json, scopes=SCOPE)
else:
    # Fallback for local development with file
    CREDS = Credentials.from_service_account_file("quiz_creds.json", scopes=SCOPE)

SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("fandom-challenge-v2-data")

# Leaderboard functions
def save_score(username, score, quiz_name, time_taken):
    """Append a quiz result with time to the correct leaderboard."""
    try:
        SHEET.worksheet(f"{quiz_name}_leaderboard").append_row([
            username,
            score,
            time_taken
        ])
    except Exception as e:
        print("Leaderboard unavailable. Score not saved to cloud.")
        print("Error:", e)


def display_leaderboard(quiz_name, top_n=10):
    """Fetch, sort, and display the top scores for a specific quiz."""
    try:
        records = SHEET.worksheet(f"{quiz_name}_leaderboard").get_all_records()
        if not records:
            print("No scores yet!")
            return

        def safe_int(value, default=0):
            try:
                return int(value)
            except (ValueError, TypeError):
                return default

        # Sort by descending score, then ascending time
        sorted_records = sorted(
            records,
            key=lambda x: (-safe_int(x.get("Score")), safe_int(x.get("Time")))
        )

        print(f"\n=== {quiz_name.upper()} LEADERBOARD ===")
        print(f"{'Rank':<5}{'User':<12}{'Score':<6}{'Time(s)':<8}")
        print("-" * 40)
        for i, rec in enumerate(sorted_records[:top_n], start=1):
            print(f"{i:<5}{rec['Username']:<12}{rec['Score']:<6}{rec['Time']:<8}")
        print()
    except Exception as e:
        print("Leaderboard unavailable.")
        print("Error:", e)

# Initialise colorama
init(autoreset=True)
print(Fore.GREEN + "Colorama test passed!")

def rules():
    """Display quiz rules to the player."""
    print(Fore.MAGENTA + "\n=== QUIZ RULES ===")
    print("1. You will be asked a series of questions.")
    print("2. Each question has 4 options. Only one is correct.")
    print("3. Type the number of your chosen answer and press Enter.")
    print("4. Your score will be shown at the end of the quiz.")
    print("5. Try to get the highest score you can!")
    input(Fore.CYAN + "\nPress Enter to return to the menu...")

def about():
    """Display information about the quiz."""
    print(Fore.BLUE + "\n=== ABOUT THIS QUIZ ===")
    print("The Fandom Quiz challenges your knowledge across different fandoms,")
    print("starting with Jak and Daxter trivia.")
    print("It was created as part of a Python project to test programming and UX skills.")
    print("Future versions may include more categories and interactive features!")
    input(Fore.CYAN + "\nPress Enter to return to the menu...")

def play_quiz(questions, quiz_name):
    """Run a quiz with the given question set."""
    score = 0
    start_time = datetime.now()  # record quiz start

    # Select 10 random questions
    selected_questions = random.sample(questions, 10)

    # Loop through the selected questions
    for i, q in enumerate(selected_questions, start=1):
        print(Fore.MAGENTA + f"\nQ{i}: {q['question']}")

        # Shuffle options safely
        options = q["options"][:]  # copy to avoid changing original
        # Strip original letter prefix
        clean_options = [opt[3:].strip() if len(opt) > 3 else opt for opt in options]
        random.shuffle(clean_options)

        # Map labels A-D to shuffled options
        labels = ["A", "B", "C", "D"]
        option_mapping = {}
        for label, option in zip(labels, clean_options):
            option_mapping[label] = option
            print(f"{label}) {option}")

        # Keep asking until valid input
        while True:
            answer = input("Your choice (A-D) or X to return to quiz menu: ").strip().upper()

            if answer == "X":
                print(Fore.YELLOW + "Returning to quiz selection menu...")
                return  # exit play_quiz() immediately

            if answer in option_mapping:
                break  # valid A-D answer, continue
            else:
                print(Fore.RED + "Invalid choice. Please enter A, B, C, D, or X.")
                # Reprint question + options so user can see them again
                print(Fore.MAGENTA + f"\nQ{i}: {q['question']}")
                for label, option in option_mapping.items():
                    print(f"{label}) {option}")

        # Check answer
        chosen_text = option_mapping[answer]
        if chosen_text == q["answer"]:
            print(Fore.GREEN + "Correct!")
            score += 1
        else:
            print(Fore.RED + f"Wrong! The correct answer was: {q['answer']}")

    end_time = datetime.now()
    time_taken = (end_time - start_time).seconds  # Time in seconds        

    # Final score and result message
    print(Fore.CYAN + f"\nYou scored {score}/{len(selected_questions)}!")
    print(Fore.YELLOW + f"Time taken: {time_taken} seconds")

    if score < 7:
        print(Fore.YELLOW + "You can do better. Try again.")
    elif score in [7, 8]:
        print(Fore.GREEN + "Good job! You know your stuff.")
    else:  # 9 or above
        print(Fore.MAGENTA + "Congratulations! You're a superfan!")
        # Only show ASCII if superfan
        print(Fore.CYAN + """
           ☆ ☆ ☆ ☆ ☆
          ☆ SUPERFAN! ☆
           ☆ ☆ ☆ ☆ ☆
        """)
        print(Fore.MAGENTA + "Amazing job! 🎉 Keep up the great work!")

    # Leaderboard username prompt
    while True:
        username = input("Enter your 3-letter username to save score or X to return to quiz menu ").strip().upper()
    
        if username == "X":
            print(Fore.YELLOW + "Score not saved. Returning to quiz selection menu...")
            return  # exit play_quiz() immediately
    
        if re.fullmatch(r"[A-Z]{3}", username):
            break  # valid 3-letter username, continue
        print(Fore.RED + "Invalid username. Enter exactly 3 letters (A-Z) or X to cancel.")

    # Save score and display leaderboard
    save_score(username, score, quiz_name, time_taken)
    display_leaderboard(quiz_name)

def select_quiz():
    """Sub-menu for selecting which quiz to play."""
    while True:
        print(Fore.CYAN + "\n=== SELECT A QUIZ ===")
        print("1 - Jak and Daxter")
        print("2 - Ratchet & Clank")
        print("3 - God of War")
        print("4 - Back to main menu")
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            play_quiz(JAK_QUESTIONS, "jak") # Calls play_quiz
        elif choice == "2":
            play_quiz(RATCHET_QUESTIONS, "ratchet")
        elif choice == "3":
            play_quiz(GOD_OF_WAR_QUESTIONS, "gow")
        elif choice == "4":
            return  # Back to main menu
        else:
            print(Fore.RED + "Invalid choice. Please enter 1, 2, 3, or 4.")

def menu():
    while True:
        print(Fore.CYAN + "\n=== FANDOM QUIZ ===")
        print("1 - Rules")
        print("2 - About")
        print("3 - Start Quiz")
        print("4 - Exit")
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            rules()
        elif choice == "2":
            about()
        elif choice == "3":
            select_quiz()
        elif choice == "4":
            print(Fore.YELLOW + "Goodbye!")
            sys.exit(0)
        else:
            print(Fore.RED + "Option not implemented yet. Please try again.")


if __name__ == "__main__":
    menu()
