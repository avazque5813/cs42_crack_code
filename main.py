
import click
import sys, time 
import math
import random
import os
import numpy as np
from pyfiglet import Figlet

HIGH_COLOR = 'blue'
LOW_COLOR = 'magenta'
NEWLINE_DELAY = 0.5
EXTRA_TRIES = 0


KEYCOMBO = [3,4,80] # Level 1, 2 and 3 answers 
# Index 0 contains the digit of first slot in lock 
# Index 1 contains the digit of second slot in lock
# Index 2 contains the digits of slots three and four in lock 

F_ASCII_ART = Figlet(font='doh') # TEXT to ASCII ART
# More info: http://www.jave.de/figlet/fonts.html
# Fonts examples:  http://www.jave.de/figlet/fonts/overview.html 

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
                np.random.exponential(np.random.choice([0.005, 0.01, 0.015]))
            )

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Checks if input is w/in bound
def check_bound(user_input, high, low):
    if user_input not in range(low, high +1):
        print_slow(f"Number needs to be within {low} and {high}")
        return False
    return True

def levels(level, hard):
    if level == 0:
        return (1, 10)
    elif level == 1:
        if hard: 
            return (1, 100)
        return (1, 10)
    else:
        if hard: 
            return (1, 1000)
        return (1, 99)



############# commands ###################

@click.command()
@click.option('-s', '--start_level', default=0, 
              help="Set the start level. Possible levels are 0, 1, and 2.\n"+"Default is 0.\n")
@click.option('-e', '--extra_guess', default=0,
              help="You can increase the guess limit for each of the levels.\n"
              +"Default is 0 extra guesses.")
@click.option('-r', '--randomize', default=False,
              help="Enable randomization of password for each level.\n" + 
              "Default password for each level is same as keycombo password.\n")
@click.option('-w', '--warn', default=True, 
              help="Gives players warning message when they have 2 guesses left.\n"+ "Default is warnings are on.")
@click.option('-hd', '--hard', default=False, 
              help="Enables hard mode. Changes bounds for levels to: "+
              "1-10, 1-100, 1-1000\n" + "Default this is off.\n" +
              "Note: Recommend you turn on random if hard mode is turned on.\n")
def game_init(start_level, extra_guess, randomize, warn, hard):   
    clear()
    click.secho('\n\n\n')
    click.secho('Crack the Code\n'.center(50), fg='green', blink=True, bold=True)
    click.secho('WELCOME Detective!\n',fg='green')
    click.secho('Mission:\n',fg='green')

    print_slow('Our intel tells us that the computer holds the password.')
    print_slow('We need your help to crack the password.')
    time.sleep(NEWLINE_DELAY)
    print_slow("The password is a list of numbers. For each number, we will let you know the smallest and largest possible number.")
    click.echo("")
    time.sleep(NEWLINE_DELAY)
    print_slow("Try to guess the password, but be careful, too many guesses and the system will reset!")
    print_slow("Make sure to pay attention to whether your guess was too high or low!")
    time.sleep(NEWLINE_DELAY)
    click.echo("")

    time.sleep(1)
    game_loop(start_level, extra_guess, randomize, warn, hard)
    print_slow("Feel free to come back and try later!")

def final_end(level):
    """
    This is called in two cases:
    1. All levels passed
    2. Failed to pass level and not trying again
    """
    print_slow(f"Great job you passed {level + 1} levels!")

    if (level==2):
        print_slow("You figured out the password for the lock!!")
    else:
        print_slow("Try again and see if you can pass all the levels!")
    print_slow("You learned how 'binary searches' work. :)")
    exit()

def level_end(level, guess_tries, ideal_tries, extra_guess, randomize, warn, hard):
    """
        This is called at the end of each level. 
    """
    print_slow(f"Congrats!! You guessed the password in {guess_tries} tries.")    
    if guess_tries <= ideal_tries - extra_guess:
        print_slow("You were able to get it within the ideal number of tries.")
    click.echo("")

    if level == 2:
        print_slow(f"The password for entries 3 and 4 in the lock is {KEYCOMBO[level]}!", fg='red')
        print(F_ASCII_ART.renderText(f"{KEYCOMBO[level]}").rstrip())
    else:
        print_slow(f"The password for entry {level+1} in the lock is {KEYCOMBO[level]}. ", fg='red')
        print(F_ASCII_ART.renderText(f"{KEYCOMBO[level]}").rstrip())

    click.echo("")

    time.sleep(1)

    if level == 2:
        final_end(level)

    print_slow("Starting up the next level...")
    time.sleep(1)
    game_loop(level+1, extra_guess, randomize, warn, hard)
    final_end(level)

def game_loop(level, extra_guess, randomize, warn, hard):
    click.echo("")
    print_slow(f"###### LEVEL {level + 1} ######")
    click.echo("")
    low_bound, high_bound = levels(level, hard)
    print_slow("We know the password is between the numbers "+ str(low_bound) +" and " + str(high_bound) + ".")


    # Calculating the ideal number of tries by taking ceiling of log base 2 of upper bound + 1
    ideal_tries = math.ceil(math.log2(high_bound+1))
    #ideal_tries = ideal_tries + extra_guess # Adding Extra tries to make it easier
    if level == 2:
        ideal_tries += 2 #added two more tries for the last level
    print_slow("Try to get it in " + str(ideal_tries) + " or less guesses.")
    click.echo("")
    
    
    if randomize:
        answer = random.randint(low_bound, high_bound + 1)
    else:
        answer = KEYCOMBO[level]
    guess = -1
    while(not check_bound(guess, high_bound, low_bound)):
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

        if len(guessed) == ideal_tries - 2 and warn:
            click.echo("")
            print_slow("Detecting potential suspicious activity. Tightening security...", fg='red')
            click.echo("")
            time.sleep(1)
            print_slow("The system is onto you. You have 2 more tries before the system acts.")
            click.echo("")

        if len(guessed) == ideal_tries:
            clear()
            click.echo("")
            print_slow("ALERT: SYSTEM DETECTED HACKING ACTIVITY. RESETTING...", fg='red')
            click.echo("")
            time.sleep(1)

            if randomize:
                print_slow("You tried too many times. The system has changed the password.")
                print_slow(f"Please retry. You have {ideal_tries} guesses.")
                click.echo("")
                answer = random.randint(low_bound, high_bound + 1)
            else:
                # answer = KEYCOMBO[level]
                print_slow("You tried too many times. The system has restarted and you will need to start from stage 1.")
                click.echo("")
                game_loop(0, extra_guess, randomize, warn, hard)
                return
            guessed = []
            guess = click.prompt("Please enter the password", type=int)
            while(not check_bound(guess, high_bound, low_bound)):
                guess = click.prompt("Please enter the password", type=int)
            guessed.append(guess)
            continue
        
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
        while(not check_bound(guess, high_bound, low_bound)):
            guess = click.prompt("Please enter the password", type=int)
        guessed.append(guess)

    level_end(level, len(guessed), ideal_tries, extra_guess, randomize, warn, hard)




if __name__ == '__main__':
    game_init()

