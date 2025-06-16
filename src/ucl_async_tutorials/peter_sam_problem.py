"""Someone picks 2 random integers between 0 and 99, Sam gets told the sum and Peter gets told the
product.

They're asked to sequentially guess the two integers.

This is all they know, as well as what the other has said about whether they know the numbers.

Both Sam and Peter are perfectly logical and know the other is too.

1. Peter says "I don't know what the numbers are"
   Sam says "I don't know what the numbers are"
2. Peter says "I don't know what the numbers are"
   Sam says "I don't know what the numbers are"
3. Peter says "I don't know what the numbers are"
   Sam says "I don't know what the numbers are"
4. Peter says "I don't know what the numbers are"
   Sam says "I don't know what the numbers are"
5. Peter says "I don't know what the numbers are"
   Sam says "I don't know what the numbers are"
6. Peter says "I don't know what the numbers are"
   Sam says "I don't know what the numbers are"
7. Peter says "I don't know what the numbers are"
   Sam says "I don't know what the numbers are"

8. Peter says "I know what the numbers are now"

What are the numbers?
"""
from typing import Dict, List, Tuple

# BELOW IS THE CORRECT SOLUTION!

num_incorrect_guesses = 7

possible_number_a = list(range(100))[1:]

peter_possible_numbers: Dict[int, List[Tuple[int, int]]] = {}
sam_possible_numbers: Dict[int, List[Tuple[int, int]]] = {}

for a in possible_number_a:
    for b in range(a, 100):
        peter_possible_numbers[a * b] = peter_possible_numbers.get(a * b, []) + [(a, b)]
        sam_possible_numbers[a + b] = sam_possible_numbers.get(a + b, []) + [(a, b)]

guess = "peter"
nobody_knows_the_answer = True

for _ in range(num_incorrect_guesses * 2):
    guesser_poss_numbers = peter_possible_numbers if guess == "peter" else sam_possible_numbers
    other_poss_numbers = sam_possible_numbers if guess == "peter" else peter_possible_numbers
    print(guess, "guesses:")
    for number in guesser_poss_numbers.copy():
        if len(guesser_poss_numbers[number]) == 1:
            print(number)
            [(poss_a, poss_b)] = guesser_poss_numbers.pop(number)
            for other_num, value in other_poss_numbers.items():
                if (poss_a, poss_b) in other_poss_numbers[other_num]:
                    value.remove((poss_a, poss_b))

    guess = "sam" if guess == "peter" else "peter"

print({num: options for num, options in peter_possible_numbers.items() if len(options) == 1})
