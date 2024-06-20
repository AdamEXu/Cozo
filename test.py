code = '''
def sum_two_numbers_efficient(a, b):
    if a == 0:
        return b
    elif b == 0:
        return a
    else:
        return a + b
'''

from generation import generate_explanation
print(generate_explanation(code))