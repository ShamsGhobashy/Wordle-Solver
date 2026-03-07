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

length_of_guesses = len(Guesses)
length_of_Targets = len(Targets)

Guesses = np.array(Guesses)
Targets = np.array(Targets)

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
    M = np.empty((length_of_guesses, length_of_Targets), dtype = np.uint8)
    for i, guess in enumerate(Guesses):
        for j, target in enumerate(Targets):
            M[i,j] = pattern_to_code(get_feedback(guess, target))
    return M

if os.path.exists('pattern_matrix.npy'):
    M = np.load('pattern_matrix.npy')
else:
    M = build_pattern_matrix(Guesses, Targets)
    np.save('pattern_matrix.npy', M)

def computing_best_guess(list_of_indices):
    best_words = []
    candidate_words = [Targets[j] for j in list_of_indices]
    for i, guess in enumerate(Guesses):
        Entropy = 0
        patterns = M[i, list_of_indices]
        unique_patterns, counts = np.unique(patterns, return_counts=True)
        probabilities = counts / len(list_of_indices)
        for p in probabilities:
            Entropy += - p * math.log2(p)
        is_candidate = 1 if guess in candidate_words else 0
        best_words.append((Entropy, is_candidate, i))
                
    return best_words
      
list_of_indices = list(range(length_of_Targets))

rounds = 0

while rounds < 6:

    if len(list_of_indices) == 1:
        print(f"BEST={Targets[list_of_indices[0]]}")
        guess = input()
        feedback = input()
        if pattern_to_code(feedback) == 242:
            print("solved")
            break
        continue

    best_words = computing_best_guess(list_of_indices)
    best_words.sort(reverse=True)
    top_20 = best_words[:20]
    best_entropy, is_candidate, best_indx = top_20[0] 
    prior_entropy = math.log2(len(list_of_indices)) if len(list_of_indices) > 1 else 0

    print(f"remaining candidates:  {len(list_of_indices)}")
    print(f"H(W) (prior entropy) = {prior_entropy: .3f} bits")
    print(f"H(Y) (best guess's entropy) = {best_entropy: .3f} bits")
    print(f"H(W|Y) (posterior entropy) = {prior_entropy - best_entropy : .3f} bits")
    print(f"I(W;Y) information gain = {best_entropy: .3f} bits")

    for entropy, is_candidate, idx in top_20:
        print(f"  {Guesses[idx]} — H(Y)={entropy:.3f} bits")

    print("BEST=" + Guesses[best_indx])

    guess = input()
    if guess not in Guesses:
        print("invalid word, try again")
        continue

    feedback = input()
    if len(feedback) != 5 or not all(c in {'r', 'y', 'g'} for c in feedback):
        print("invalid feedback, try again")
        continue

    feedback_code = pattern_to_code(feedback)
        
    if(feedback_code == 242):
        print("solved")
        break   
    guess_idx = np.where(Guesses == guess)[0][0] 
    list_of_indices = [j for j in list_of_indices if feedback_code == M[guess_idx, j]]
    
    if len(list_of_indices) == 0 :
        print("Error, some pattern was wrong")
        break

    rounds += 1
else:
    print("failed to solve")