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
