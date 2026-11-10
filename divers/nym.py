import random

NB_BATONS = 13
last_player = "cpu"

def random_choice():
    return random.choice([1,2,3])

def display_stick():
    print("| " * NB_BATONS)

def who_first():
    return random.choice(["player", "cpu"])

def turn(player):
    if player == "cpu":
        choice = random_choice()
        print(f"{player} combien de batons souhaites tu prendres ? (1, 2 ou 3) {choice}")
        return choice
    else:
        return int(input(f"{player} combien de batons souhaites tu prendres ? (1, 2 ou 3) "))

def winer(player):
    print("#" * 30, "\n")
    print(f"Félicitation {player} tu as gagné")

first_player = who_first()
second_player = "player" if first_player == "cpu" else "cpu"

print("  BIENVENUE DANS LE JEU NYM")
print("#" * 30, "\n")
print(f"{first_player.upper()} c'est toi qui commence")
display_stick()


while NB_BATONS > 0:
    last_player = first_player
    nb_batons_pris = turn(first_player)
    NB_BATONS -= nb_batons_pris
    display_stick()
    if NB_BATONS > 0:
        last_player = second_player
        nb_batons_pris = turn(second_player)
        NB_BATONS -= nb_batons_pris
        display_stick()

winer(last_player)