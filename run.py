"""
run.py

Main entry point for the Fandom Challenge V2 project.

Features:
- Handles menu navigation (Rules, About, Quiz).
- Runs quiz gameplay loop with randomised questions.
- Saves and displays leaderboard scores via Google Sheets.
- Uses Colorama for coloured console output.
- Designed to run locally or on Heroku with environment-based creds.
"""

# Standard library imports
import sys
import os
import json
import random
import re
from datetime import datetime

# Third-party imports
from colorama import Fore, init
import gspread
from google.oauth2.service_account import Credentials

# Import all quiz question sets from external data file
from data import JAK_QUESTIONS, RATCHET_QUESTIONS, GOD_OF_WAR_QUESTIONS

# Google Sheets configuration

# Define the Google API scopes for authentication
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials from environment (Heroku) or local JSON file
if os.environ.get("CREDS"):
    # On Heroku: JSON stored in CREDS config var
    creds_json = json.loads(os.environ["CREDS"])
    CREDS = Credentials.from_service_account_info(creds_json, scopes=SCOPE)
else:
    # Local development fallback: quiz_creds.json file
    CREDS = Credentials.from_service_account_file(
        "quiz_creds.json",
        scopes=SCOPE
    )

# Authenticate and open the project’s Google Sheet
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
        # If Google Sheets is unavailable, allow local play to continue
        print("Leaderboard unavailable. Score not saved to cloud.")
        print("Error:", e)


# Retrieve and display the leaderboard for a given quiz
def display_leaderboard(quiz_name, top_n=10):
    """Fetch, sort, and display the top scores for a specific quiz."""
    try:
        records = SHEET.worksheet(f"{quiz_name}_leaderboard").get_all_records()
        if not records:
            print("No scores yet!")
            return

        # Helper to convert values safely to int
        def safe_int(value, default=0):
            try:
                return int(value)
            except (ValueError, TypeError):
                return default

        # Sort by score (descending), then time (ascending)
        sorted_records = sorted(
            records,
            key=lambda x: (-safe_int(x.get("Score")), safe_int(x.get("Time")))
        )

        # Print formatted leaderboard
        print(f"\n=== {quiz_name.upper()} LEADERBOARD ===")
        print(f"{'Rank':<5}{'User':<12}{'Score':<6}{'Time(s)':<8}")
        print("-" * 40)
        for i, rec in enumerate(sorted_records[:top_n], start=1):
            print(
                f"{i:<5}"
                f"{rec['Username']:<12}"
                f"{rec['Score']:<6}"
                f"{rec['Time']:<8}"
            )
        print()

    except Exception as e:
        print("Leaderboard unavailable.")
        print("Error:", e)

# Utility and menu functions


# Initialise colorama for coloured console text
init(autoreset=True)


# Show the quiz rules to the user
def rules():
    """Display quiz rules to the player."""
    print(Fore.MAGENTA + "\n=== QUIZ RULES ===")
    print("1. You will be asked a series of questions.")
    print("2. Each question has four options: A, B, C, and D.")
    print("3. The questions and answer positions are randomised each time.")
    print("4. Type the letter of your chosen answer and press Enter.")
    print("5. Your score will be shown at the end of the quiz.")
    print("6. Try to get the highest score you can!")
    input(Fore.CYAN + "\nPress Enter to return to the menu...")


# Show information about the project
def about():
    """Display information about the quiz."""
    print(Fore.BLUE + "\n=== ABOUT THIS QUIZ ===")
    print("Welcome to Fandom Challenge!")
    print("Test your knowledge with quizzes from your favourite fandoms.")
    print(
        "Each quiz is randomised and challenges "
        "both your knowledge and speed.")
    print(
        "\nCurrent categories include "
        "Jak and Daxter, Ratchet & Clank, and God of War.")
    print(
        "This version was developed by Louis as part of a "
        "Python project to test programming and UX skills.")
    print(
        "Future versions may include more categories and "
        "interactive features!")
    print("\nView the original project on GitHub:")
    print("https://github.com/LouisCE/fandom-challenge-v2")
    input(Fore.CYAN + "\nPress Enter to return to the menu...")


# Core Quiz Logic

# Run the main quiz loop for a given category
def play_quiz(questions, quiz_name):
    """Run a quiz with the given question set."""
    score = 0
    start_time = datetime.now()  # Record quiz start time

    # Select ten random questions from the pool
    selected_questions = random.sample(questions, 10)

    # Loop through the selected questions
    for i, q in enumerate(selected_questions, start=1):
        print(Fore.MAGENTA + f"\nQ{i}: {q['question']}")

        # Copy and shuffle options to prevent altering original dataset
        options = q["options"][:]
        clean_options = [
            opt[3:].strip() if len(opt) > 3 else opt
            for opt in options]
        random.shuffle(clean_options)

        # Assign A-D labels to shuffled options
        labels = ["A", "B", "C", "D"]
        option_mapping = {}
        for label, option in zip(labels, clean_options):
            option_mapping[label] = option
            print(f"{label}) {option}")

        # Input loop: keep asking until valid
        while True:
            answer = input(
                "Your choice (A-D) or X to return to quiz menu: "
                ).strip().upper()

            if answer == "X":
                print(Fore.YELLOW + "Returning to quiz selection menu...")
                return  # exit play_quiz() immediately

            if answer in option_mapping:
                break  # valid A-D answer, continue
            else:
                print(
                    Fore.RED
                    + "Invalid choice. Please enter A, B, C, D, or X."
                )
                # Reprint question + options so user can see them again
                print(Fore.MAGENTA + f"\nQ{i}: {q['question']}")
                for label, option in option_mapping.items():
                    print(f"{label}) {option}")

        # Check if chosen option matches the correct answer
        chosen_text = option_mapping[answer]
        if chosen_text == q["answer"]:
            print(Fore.GREEN + "Correct!")
            score += 1
        else:
            print(Fore.RED + f"Wrong! The correct answer was: {q['answer']}")

    # Quiz finished: calculate total time
    end_time = datetime.now()
    time_taken = (end_time - start_time).seconds  # Time in seconds

    # Display final score and result message
    print(Fore.CYAN + f"\nYou scored {score}/{len(selected_questions)}!")
    print(Fore.YELLOW + f"Time taken: {time_taken} seconds")

    # Feedback based on score
    if score < 7:
        print(Fore.YELLOW + "You can do better. Try again.")
    elif score in [7, 8]:
        print(Fore.GREEN + "Good job! You know your stuff.")
    else:  # 9 or above
        print(Fore.MAGENTA + "Congratulations! You're a superfan! 🎉")
        # Only show ASCII if superfan
        print(Fore.CYAN + """
           ☆ ☆ ☆ ☆ ☆
          ☆ SUPERFAN! ☆
           ☆ ☆ ☆ ☆ ☆
        """)

    # Prompt to save score to leaderboard
    while True:
        username = input(
            "Enter your 3-letter username to save score "
            "or X to return to quiz menu "
        ).strip().upper()

        if username == "X":
            print(
                Fore.YELLOW
                + "Score not saved. Returning to quiz selection menu..."
            )
            return  # exit play_quiz() immediately

        if re.fullmatch(r"[A-Z]{3}", username):
            break  # valid 3-letter username, continue
        print(
            Fore.RED
            + "Invalid username. Enter exactly 3 letters "
            "(A-Z) or X to cancel."
        )

    # Save score and display leaderboard
    save_score(username, score, quiz_name, time_taken)
    display_leaderboard(quiz_name)


# Sub-menu for choosing which quiz category to play
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
            play_quiz(JAK_QUESTIONS, "jak")  # Calls play_quiz
        elif choice == "2":
            play_quiz(RATCHET_QUESTIONS, "ratchet")
        elif choice == "3":
            play_quiz(GOD_OF_WAR_QUESTIONS, "gow")
        elif choice == "4":
            return  # Back to main menu
        else:
            print(Fore.RED + "Invalid choice. Please enter 1, 2, 3, or 4.")


# Main menu and entry point

# Main menu that controls navigation between features
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
    # Program starts here
    menu()
