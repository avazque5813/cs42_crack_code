
import click
import sys, time 
import math
import random
import os
import numpy as np

HIGH_COLOR = 'blue'
LOW_COLOR = 'magenta'
NEWLINE_DELAY = 0.5

"""
    print_slow:
        - simulates typed print output 
        - outputs in green 
"""
def print_slow(str, sleep=0.04, fg='green', nl=True):
    for letter in str:
        click.secho(letter, fg=fg, nl=False)
        time.sleep(sleep)
    if nl:
        click.echo("") # New line

def loading_bar():
    fill_char = click.style(u"\u25A0", fg="green")
    empty_char = click.style(" ", fg="white", dim=True)
    with click.progressbar(
            iterable=range(100),
            label=click.style("Trying password", fg="green"),
            fill_char=fill_char,
            empty_char=empty_char
        ) as items:
        for _ in items:
            time.sleep(
                np.random.exponential(np.random.choice([0.01, 0.015, 0.02]))
            )

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Checks if input is w/in bound
def check_bound(user_input, high, low):
    if user_input not in range(low, high +1):
        print_slow(f"Number needs to be within {low} and {high}")
        return False
    return True

def levels(level):
    if level == 0:
        return (1, 10)
    elif level == 1:
        return (1, 20)
    elif level == 2:
        return (1, 50)
    else:
        return (1, 100)



def game_init(start_level):   
    clear()
    click.secho('\n\n\n')
    click.secho('Crack the Code\n'.center(130), fg='green', blink=True, bold=True)
    click.secho('WELCOME Detective!\n',fg='green')
    click.secho('Mission:\n',fg='green')

    print_slow('We need your help to crack the password.')
    time.sleep(NEWLINE_DELAY)
    print_slow("The password is a number. We will let you know how small and large it can be.")
    time.sleep(NEWLINE_DELAY)
    print_slow("Try to guess the password, but be careful, too many guesses and the system will reset!")
    time.sleep(NEWLINE_DELAY)
    click.echo("")

    if click.confirm("Ready to start?"):
        print()
        game_loop(start_level)
    print_slow("Feel free to come back and try later!")

def final_end(level):
    print_slow(f"Great job you passed {level + 1} levels!")
    print_slow("You learned how 'binary searches' work.")

def game_end(level, guess_tries, ideal_tries):
    print_slow(f"Congrats!! You guessed the password in {guess_tries}.")
    if ideal_tries >= guess_tries:      
        print_slow("You were able to get it within the ideal number of tries.")
    else: 
        print_slow(f"Congrats!! You guessed the password in {guess_tries}.")

    if level == 2:
        final_end(level)

    if click.confirm("Do you want to try the next level?"):
        clear()
        game_loop(level+1)
    final_end(level)

def game_loop(level):
    low_bound, high_bound = levels(level)
    print_slow("We know the password is between the numbers "+ str(low_bound) +" and " + str(high_bound) + ".")

    ideal_tries = math.ceil(math.log2(high_bound+1))

    print_slow("Try to get it in " + str(ideal_tries) + " or less guesses.")
    click.echo("")
    
    answer = random.randint(low_bound, high_bound + 1)
    guess = click.prompt("Please enter the password", type=int)
    guessed = []
    guessed.append(guess)

    while True:
        loading_bar()
        if guess == answer:
            break
        elif guess > answer:
            print_slow("INCORRECT.\n", fg='red')
            print_slow(f"Try again, {guess} was ", nl=False)
            print_slow("TOO LARGE.", fg=HIGH_COLOR)
        else:
            print_slow("INCORRECT.\n", fg='red')
            print_slow(f"Try again, {guess} was ", nl=False)
            print_slow("TOO SMALL.", fg=LOW_COLOR)
        time.sleep(NEWLINE_DELAY)

        if len(guessed) == ideal_tries:
            clear()
            click.echo("")
            print_slow("ALERT: SYSTEM DETECTED HACKING ACTIVITY. RESETTING PASSWORD...", fg='red')
            click.echo("")
            time.sleep(1)

            print_slow("You tried too many times. The system has changed the password.")
            print_slow(f"Please retry. You have {ideal_tries} guesses.")
            click.echo("")
            answer = random.randint(low_bound, high_bound + 1)
            guessed = []
            guess = click.prompt("Please enter the password", type=int)
            guessed.append(guess)
            break
        
        print_slow("Previous Guesses: ", nl=False)
        for i in range(len(guessed)):
            print_slow(f"{guessed[i]} ", nl=False)
            if guessed[i] > answer:
                print_slow("(TOO LARGE)", fg=HIGH_COLOR, nl=False)
            else:
                print_slow("(TOO SMALL)", fg=LOW_COLOR, nl=False)
            if i != len(guessed) - 1:
                print_slow(", ", nl=False)
        time.sleep(NEWLINE_DELAY)
        click.echo("\n")

        guess = click.prompt("Please enter the password", type=int)
        guessed.append(guess)

    game_end(level, len(guessed), ideal_tries)




if __name__ == '__main__':
    game_init(0)

