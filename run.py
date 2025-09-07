import sys
from colorama import Fore, init
# Import all quiz question sets
from data import JAK_QUESTIONS, RATCHET_QUESTIONS, GOD_OF_WAR_QUESTIONS

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

def play_quiz(questions):
    """Run a quiz with the given question set."""
    score = 0
    for i, q in enumerate(questions, start=1):
        print(Fore.MAGENTA + f"\nQ{i}: {q['question']}")
        for option in q["options"]:
            print(option)

        # Player input
        answer = input("Your choice (A-D): ").strip().upper()

        # Map A/B/C/D to option text
        mapping = {"A": 0, "B": 1, "C": 2, "D": 3}
        if answer not in mapping:
            print(Fore.RED + "Invalid choice. Skipping question.")
            continue

        chosen_text = q["options"][mapping[answer]][3:]  # strip "A) "
        if chosen_text == q["answer"]:
            print(Fore.GREEN + "Correct!")
            score += 1
        else:
            print(Fore.RED + f"Wrong! The correct answer was: {q['answer']}")


    # Final score and result message
    print(Fore.CYAN + f"\nYou scored {score}/{len(questions)}!")

    # Result messages based on performance
    if score < 7:
        print(Fore.YELLOW + "You can do better. Try again.")  # Under 7
    elif score in [7, 8]:
        print(Fore.GREEN + "Good job! You know your stuff.")  # 7 or 8
    else:  # 9 or above
        print(Fore.MAGENTA + "Congratulations! You're a superfan!")  # 9+

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
            play_quiz(JAK_QUESTIONS) # Calls play_quiz
        elif choice == "2":
            play_quiz(RATCHET_QUESTIONS)
        elif choice == "3":
            play_quiz(GOD_OF_WAR_QUESTIONS)
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
