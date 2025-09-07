import sys
from colorama import Fore, init
from data import JAK_QUESTIONS

# initialise colorama
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
        elif choice == "4":
            print(Fore.YELLOW + "Goodbye!")
            sys.exit(0)
        else:
            print(Fore.RED + "Option not implemented yet. Please try again.")


if __name__ == "__main__":
    menu()
