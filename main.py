#numpy makes the program much faster
import numpy as np
import math
import json 
import os

Guesses = []
Targets = []

with open('dictionary_5_letter.json', 'r') as file:
    Guesses = json.load(file)

with open('targets_5_letter.json', 'r') as file:
    Targets = json.load(file)

G = len(Guesses)
A = len(Targets)

Guesses = np.array(Guesses)
Targets = np.array(Targets)

# uint8 is used to save memory, this is an 8-bit integer to store the values in the matrix, as the largest value is 242, which is less than 255=(2**8).
# we could have used np.zeros ,but np.empty is much faster.

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
    ## moved the matrix initialization here to avoid creating an empty one if it's already was saved before
    M = np.empty((G,A), dtype = np.uint8)
    #we used enumerate because it is better than accessing the element i in the Guesses array(much faster) and less exposure to mistakes.
    for i, guess in enumerate(Guesses):
        for j, target in enumerate(Targets):
            M[i,j] = pattern_to_code(get_feedback(guess, target))
    return M

#we have to save the matrix in a file, because we do not need to calcuate it everytime we start the game(it will be calculated once).

#loading the matrix file at the first of the game
if os.path.exists('pattern_matrix.npy'):
    M = np.load('pattern_matrix.npy')
else:
    M = build_pattern_matrix(Guesses, Targets)
    np.save('pattern_matrix.npy', M)

def computing_best_guess(C):
    ## changed the initialization of them for safety
    best_indx = -1
    best_entropy = -1
    #C is the array of targets' indices, which will be changed after each round 
    # by filteration as we will minimize it by removing all words 
    # that if we have used in the guess instead of the word we have used 
    # they will not give us the same pattern/feedback

    ## an array of all candidate words 
    candidate_words = [Targets[j] for j in C]
    for i, guess in enumerate(Guesses):
        Entropy = 0
        patterns = M[i, C]
        unique_patterns, counts = np.unique(patterns, return_counts=True)
        probabilities = counts / len(C)
        for p in probabilities:
            Entropy += - p * math.log2(p)
        ## updated the condition to handle an edge case
        if (Entropy > best_entropy) or ((Entropy == best_entropy) and (guess in candidate_words)):
                best_entropy = Entropy 
                best_indx = i
    return best_indx, best_entropy


## list of indices to easily filter it out       
C = list(range(A))
## the game loop
while True:

    best_indx, best_entropy = computing_best_guess(C)
    prior_entropy = math.log2(len(C)) if len(C) > 1 else 0

    print(f"remaining candidates:  {len(C)}")
    print(f"H(W) (prior entropy) = {prior_entropy: .3f} bits")
    print(f"H(Y) (best guess's entropy) = {best_entropy: .3f} bits")
    print(f"H(W|Y) (posterior entropy) = {prior_entropy - best_entropy : .3f} bits")
    print(f"I(W;Y) information gain = {best_entropy: .3f} bits")
    print("BEST=" + Guesses[best_indx])

    guess = input()
    if guess not in Guesses:
        print("invalid word, try again")
        continue

    feedback = input()

    feedback_code = pattern_to_code(feedback)
        
    if(feedback_code == 242):
        print("solved")
        break
    ## gets the index of the input guess (Guesses == guess -> returns an array of true or false -> np.where -> gets the index of true in the form of a tuple -> [0][0] convert it into an array and get the first element)    
    guess_idx = np.where(Guesses == guess)[0][0]
    ## filters out the list of indices keeping the ones matching the patterns by a "list comprehension"  
    C = [j for j in C if feedback_code == M[guess_idx, j]]