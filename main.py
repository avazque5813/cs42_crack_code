
import click
import sys, time 
import math
import random


"""
    print_slow:
        - simulates typed print output 
        - outputs in green 
"""
def print_slow(str):
    for letter in str:
        click.secho(letter, fg='green', nl=False)
        time.sleep(0.1)
    click.echo("") # New line


# Checks if input is w/in bound
def check_bound(user_input, high, low):
    if user_input not in range(low, high +1):
        print_slow(f"Number needs to be within {low} and {high}")
        return False
    return True

# Check if answer is correct
def check_answer(user_input, answer):
    if user_input > answer:
        return 2
    elif user_input < answer:
        return 1
    else:
        return 0

def levels(level):
    if level == 0:
        return (0, 10)
    elif level == 1:
        return (0, 20)
    elif level == 2:
        return (0, 50)
    else:
        return (0, 100)



def game_init(start_level):   
    click.secho('Crack the Code\n', fg='green', blink=True, bold=True)
    click.secho('WELCOME Detective!\n',fg='green')
    click.secho('Mission:\n',fg='green')
    print_slow('We need your help to crack the password.')
    print_slow("At the beginning of the level we will let you know what the smallest and largest numbers that the password can be are.")
    print_slow("Try to figure out the password in the smallest, number of guess possible!")
    if click.confirm("Ready to start?"):
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

    if click.confirm("Do you want to try the next level?"):
        if level == 2:
            final_end(level)
        game_loop(level+1)
    final_end(level)

def game_loop(level):
    low_bound, high_bound = levels(level)
    print_slow("We know the password is between the numbers "+ str(low_bound) +" and " + str(high_bound) + ".")

    ideal_tries = math.ceil(math.log2(high_bound+1))

    print_slow("Try to get it in " + str(ideal_tries) + " or less guesses.")
    
    answer = random.randint(low_bound, high_bound)
    guess = click.prompt("Please enter the password: ", type=int)
    guessed = []
    guessed.append(str(guess))
    while guess != answer:
        if guess > answer:
            print_slow(f"Try again, {guess} was larger than the actual password.")
        else:
            print_slow(f"Try again, {guess} was smaller than the actual password.")
        print_slow("Previous Guesses: "+ ' '.join(guessed) + ".")
        guess = click.prompt("Please enter the password: ", type=int)
        guessed.append(str(guess))

    game_end(level, len(guessed), ideal_tries)




if __name__ == '__main__':
    game_init(0)

