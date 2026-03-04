#numpy makes the program much faster
import numpy as np
import math
import json 
import os

Guesses = []
Targets = []

with open('dictionary_5_letter.json', 'r') as file:
    Guesses = json.load(file)

with open('targets_5_letters.json', 'r') as file:
    Targets = json.load(file)

G = len(Guesses)
A = len(Targets)

Guesses = np.array(Guesses)
Targets = np.array(Targets)

# uint8 is used to save memory, this is an 8-bit integer to store the values in the matrix, as the largest value is 242, which is less than 255=(2**8).
# we could have used np.zeros ,but np.empty is much faster.
M = np.empty((G,A), dtype = np.uint8)

def get_feedback(guess, target):
    feedback = ['r'] * 5
    target_left = list(target)

    for i in range(5):
        if guess[i] == target[i]:
            feedback[i] = 'g'
            target_left[i] = None

    for i in range(5):
        if feedback[i] == 'g':
            continue
        if guess[i] in target_left:
            feedback[i] = 'y'
            target_left[target_left.index(guess[i])] = None

    return ''.join(feedback)

CHAR_TO_DIGIT = {'r': 0, 'y': 1, 'g': 2}
DIGIT_TO_CHAR = {0: 'r', 1: 'y', 2: 'g'}

def pattern_to_code(pattern_str):
    code = 0
    for i in range(5):
       code += CHAR_TO_DIGIT[pattern_str[i]] * 3**i
    return code


def code_to_pattern(code):
    result = []
    for i in range(5):
        result.append(DIGIT_TO_CHAR[code % 3])
        code //= 3
    return ''.join(result)

def build_pattern_matrix(Guesses, Targets):
    #we used enumerate because it is better than accessing the element i in the Guesses array(much faster) and less exposure to mistakes.
    for i, guess in enumerate(Guesses):
        for j, target in enumerate(Targets):
            M[i,j] = pattern_to_code(get_feedback(guess, target))

#we have to save the matrix in a file, because we do not need to calcuate it everytime we start the game(it will be calculated once).
np.save('pattern_matrix.npy', M)

#loading the matrix file at the first of the game
if os.path.exists('pattern_matrix.npy'):
    M = np.load('pattern_matrix.npy')
else:
    M = build_pattern_matrix(Guesses, Targets)
    np.save('pattern_matrix.npy', M)

def computing_best_guess(Guesses, C):
    best_guess = ""
    best_entropy = 0
    #C is the array of targets' indices, which will be changed after each round 
    # by filteration as we will minimize it by removing all words 
    # that if we have used in the guess instead of the word we have used 
    # they will not give us the same pattern/feedback
    for i, guess in enumerate(Guesses):
        Entropy = 0
        patterns = M[i, C]
        unique_patterns, counts = np.unique(patterns, return_counts=True)
        probabilities = counts / len(C)
        for p in probabilities:
            Entropy += - p * math.log(p, 2)
            if Entropy > best_entropy:
                best_entropy = Entropy 
                best_guess = guess
    return best_guess
        
    

 
