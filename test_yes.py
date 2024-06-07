'''
Add 2 numbers code
Step 1: get variable a from input
Step 2: get variable b from input
Step 3: add a and b
Step 4: print the result
'''

def step1():
    a = input("Enter the first number: ")
    return a

def step2():
    b = input("Enter the second number: ")
    return b

def step3(a, b):
    sum = a + b
    return sum

def step4(sum):
    print("The sum of the two numbers is: ", sum)

def step2_5(a, b):
    return int(a), int(b)

def main():
    a = step1()
    b = step2()
    a, b = step2_5(a, b)
    sum = step3(a, b)
    step4(sum)

main()