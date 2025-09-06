from colorama import Fore, init
from data import JAK_QUESTIONS

# initialise colorama
init(autoreset=True)
print(Fore.GREEN + "Colorama test passed!")


def main():
    print("Fandom Challenge v2 - Test Run")
    print("Sample Jak Question:", JAK_QUESTIONS[0]["question"])


if __name__ == "__main__":
    main()
