import datetime
import random


class HiddenNumber:
    TIME_TO_HINT = 3 * 60  # secs
    INTRO_TEXT = {
        0: "Welcome to the Hidden Number game!\n\n"
        "MAKE SURE YOU'VE READ THE README!\n\n"
        "This is the practice round - you can play around here.\n\n"
        "Enter the hidden number's variable name to see what it is!\n\n"
        "In future rounds this is disabled. You have to work out the number by performing operations on it.\n\n"
        "To guess the number use `hidden_num.guess(YOUR_GUESS)`.\n\n"
        "To move to exercise #1, do `hidden_num = HiddenNumber(1)`. Good luck :)",
        1: "Round 1: Addition\n\n"
        "Starting off easy - you've been doing this since you were 4 years old!\n\n"
        "Shockingly, `+` means addition in Python.\n\n"
        "To guess the number use `hidden_num.guess(YOUR_GUESS)`",
        2: "Round 2: Subtraction\n\n"
        "Be warned, this one is a lot harder than the previous one... subtraction is the opposite of addition!! :O\n\n"
        "And to top it off, `-` means subtract in Python!\n\n"
        "Last reminder that to guess a number, use `hidden_num.guess(YOUR_GUESS)`.",
        3: "Round 3: Multiplication\n\n"
        "`*` is the multiplication symbol, just like you are (a star :D)",
        4: "Round 4: Division as Numerator\n\n"
        "`/` is the division symbol. It's like drawing a fraction as `1/2` in maths.\n\n"
        "(You can only use the hidden number as the numerator, for now, e.g. `hidden_num / 23`)",
        5: "Round 5: Division as Denominator\n\n"
        "`/` is the division symbol. It's like drawing a fraction as `1/2` in maths.\n\n"
        "(You can only use the hidden number as the denominator, e.g. `23 / hidden_num`)",
        6: "Round 6: Exponents\n\n"
        "`**` is the exponent symbol... don't tell me you've forgotten what an exponent is!\n\n"
        "It's raising a number to a power! So 2 squared is `2 ** 2`. 2 cubed is `2 ** 3`",
        7: "Round 7: Floor Division as Numerator\n\n"
        "`//` is the floor division symbol. What's floor division??\n\n"
        "Division where you round DOWN the answer to the nearest integer.\n"
        "E.g. 14 // 3 = 4 as 14 / 3 = 4.67\n"
        "Or 15 // 2 = 7 as 15 / 2 = 7.5\n\n"
        "Hopefully this is the first operator that's new to you!",
        8: "Round 8: Floor Division as Denominator\n\n"
        "Time to use floor division with the hidden number as the denominator!\n\n"
        "Bet you didn't see this coming...\n"
        "(This one is really tricky!!)",
        9: "Round 9: Modulus as Numerator\n\n"
        "`%` is the modulus symbol (percent symbol). It's the remainder of a division.\n\n"
        "Have a play with it with a few numbers first to get to grips with it.\n\n"
        "E.g. 5 % 3 = 2, since 5 / 3 = 1 with a remainder of 2.\n"
        "(For now, you can only use the hidden number as the numerator, e.g. `hidden_num % 42`)",
        10: "Round 10: Modulus as Denominator\n\n"
        "In the shock of the century, we're now going use the hidden number as the denominator of the modulus!\n\n"
        "So now you can do `42 % hidden_num`. Unbelievable scenes.",
        11: "Round 11: Less Than & Greater Than\n\n"
        "This is the first expression you're seeing. This means it outputs `True` or `False`.\n\n"
        "I know what you're thinking: 'Hold your horses, you want to teach 2 operators in one exercise??'\n\n"
        "Well, you're right. We're taking liberties. It's what we do.\n\n"
        "`<` is the less than operator. E.g. `5 < 6` returns True and `5 < 4` returns False.\n\n"
        "And... hold on to your hats, you can use `>` too!",
        12: "Round 12: Less Than or Equal To & Greater Than or Equal To\n\n"
        "`<=` is the less than or equal to operator and `>=` greater than or equal to.\n\n"
        "They work just like the `<` and `>` operators, but they're inclusive.",
        13: "Round 13: Comparisons - Is Equal To\n\n"
        "This is denoted `==`. You use this to compare this number to other numbers.\n\n"
        "It's used like this: `hidden_num == 6`.\n"
        "If `hidden_num` is 6, this will return `True`, otherwise it will return False.\n\n"
        "HINT: Use a `for` loop! Read `for_loops.md` (and switch to Markdown) for an explanation.\n\n"
        "You'd have to check all 100 numbers to get this one right without it...\n\n"
        "So how can we use `for` loops to help figure out what the hidden number is?",
        14: "Round 14: Not Equals To\n\n"
        "This is the last exercise. It's okay. Stop crying...\n\n"
        "Really...\n\n"
        "This is the opposite of the previous one. `!=` means 'not equal to'.\n\n"
        "E.g. `hidden_num != 6`.\n"
        "Here if `hidden_num` is 6, this will return `False`, otherwise it will return `True`.\n\n"
        "It's worth thinking along the same lines as your previous solution!",
    }

    def __init__(self, exercise_number: int):
        self._hidden_number = random.randint(1, 100)
        self.exercise_number = exercise_number
        self.time_started = datetime.datetime.now()
        print(("-" * 16) + "\n\n", self.INTRO_TEXT[exercise_number], "\n")
        self.hint_given = False

    def hint(self) -> None:
        print(self.EXERCISE_HINTS[self.exercise_number])

    def hint_if_necessary(self) -> None:
        if (
            not self.hint_given
            and (self.time_started - datetime.datetime.now()).total_seconds()
            > self.TIME_TO_HINT
        ):
            self.hint()
            self.hint_given = True

    def __repr__(self):
        """Allow printing the number if exercise 0."""
        return str(self._hidden_number) if self.exercise_number == 0 else ""

    def __add__(self, other):
        """Exercise 1 - Addition"""
        if self.exercise_number in [0, 1]:
            return self._hidden_number + other
        else:
            raise ValueError("Can't add in this exercise")

    def __sub__(self, other):
        """Exercise 2 - Subtraction"""
        if self.exercise_number in [0, 2]:
            return self._hidden_number - other
        else:
            raise ValueError("Can't subtract in this exercise")

    def __mul__(self, other):
        """Exercise 3 - Multiplication"""
        if self.exercise_number != 3:
            raise ValueError("Can't multiply in this exercise")
        if other < 0.5 or other > 2:
            return self._hidden_number * other
        else:
            raise ValueError("Can't multiply by a number too close to 1!")

    # __mul__ only covers self * 3, while __rmul__ covers 3 * self
    __rmul__ = __mul__

    def __truediv__(self, other):
        """Exercise 4 - Division"""
        if self.exercise_number in [0, 4]:
            return self._hidden_number / other
        else:
            raise ValueError("Can't divide in this exercise")

    def __rtruediv__(self, other):
        """Exercise 5 - Right division"""
        if self.exercise_number in [0, 5]:
            return other / self._hidden_number
        else:
            raise ValueError("Can't divide in this exercise")

    def __pow__(self, power, modulo=None):
        """Exercise 6 - Exponentiation"""
        if self.exercise_number in [0, 6]:
            return self._hidden_number**power
        else:
            raise ValueError("Can't exponentiate in this exercise")

    def __floordiv__(self, other):
        """Exercise 7 - Floor division"""
        if self.exercise_number in [0, 7]:
            return self._hidden_number // other
        else:
            raise ValueError("Can't divide in this exercise")

    def __rfloordiv__(self, other):
        """Exercise 8 - Floor division as denominator"""
        if self.exercise_number in [0, 8]:
            return other // self._hidden_number
        else:
            raise ValueError("Can't divide in this exercise")

    def __mod__(self, other):
        """Exercise 9 - Modulus"""
        if self.exercise_number in [0, 9]:
            return self._hidden_number % other
        else:
            raise ValueError("Can't modulus in this exercise")

    def __rmod__(self, other):
        """Exercise 10 - Right modulus"""
        if self.exercise_number in [0, 10]:
            return other % self._hidden_number
        else:
            raise ValueError("Can't modulus in this exercise")

    def __gt__(self, other):
        """Exercise 11 - Greater than"""
        if self.exercise_number in [0, 11]:
            return self._hidden_number > other
        else:
            raise ValueError("Can't use `>` or `<` in this exercise")

    def __lt__(self, other):
        """Exercise 11 - Less than"""
        if self.exercise_number in [0, 11]:
            return self._hidden_number < other
        else:
            raise ValueError("Can't use `>` or `<` in this exercise")

    def __ge__(self, other):
        """Exercise 12 - Greater than or equal to"""
        if self.exercise_number in [0, 12]:
            return self._hidden_number >= other
        else:
            raise ValueError("Can't use `>=` or `<=` in this exercise")

    def __le__(self, other):
        """Exercise 12 - Less than or equal to"""
        if self.exercise_number in [0, 12]:
            return self._hidden_number <= other
        else:
            raise ValueError("Can't use `>=` or `<=` in this exercise")

    def __eq__(self, other):
        """Exercise 13 - Equal to"""
        if self.exercise_number in [0, 13]:
            return self._hidden_number == other
        else:
            raise ValueError("Can't use 'equals to' operator `==` in this exercise")

    def __ne__(self, other):
        """Exercise 14 - Not Equal to"""
        if self.exercise_number in [0, 14]:
            return self._hidden_number != other
        else:
            raise ValueError("Can't use 'not equals to' operator `!=` in this exercise")

    EXERCISE_HINTS = {
        0: "HINT: You should probably move onto exercise 1 soon!",
        1: "HINT: Try adding a number to this hidden number `num` and storing it in a variable.\n\n"
        "For example, `num = hidden_num + 1`"
        "Then print out that variable's value. This should give you 1 more than the hidden number.",
        2: "HINT: Try subtracting a number from this hidden number `num` and storing it in a variable.\n\n"
        "For example, `num = hidden_num - 1`\n\n"
        "Then print out that variable's value.",
        3: "HINT: Try multiplying this hidden number `num` by another number and storing it in a variable.\n\n"
        "If this is the third hint you've seen, hopefully you're starting to notice a pattern :)",
        4: "HINT: `hidden_num / 10` gives you 1/10th of the hidden number.\n\n"
        "Store this in a variable and print it out. If this is a 10th of the hidden number, then what is the hidden number?",
        5: "HINT: `1 / hidden_num` gives you 1 divided by the hidden number.\n\n"
        "Store this in a variable and print it out. We'll need to transform this to be able to guess the number...",
        6: "HINT: Since `hidden_num ** 2` squares the hidden number, how can we invert this?\n\n"
        "(square roots exist)\n\n"
        "What's the square root as an exponent? 0.5, right?",
        7: "HINT: Given `//` gives the rounded down answer to division, what is `hidden_num // 1`?",
        8: "HINT: This one is tricky!\n\n"
        "If you do `small_number // hidden_number`, then you'll probably get 0.\n\n"
        "That's not very useful. What about doing a big number? Like 100000?\n\n"
        "Then you can store the answer in a variable (let's call it x) and do `1/x`\n to figure out the original number!",
        9: "HINT: What's the remainder of `hidden_num` divided by 100? Ie `hidden_num % 100`? ;)",
        10: "HINT: What's the remainder of 100 divided by any number from 1 -> 100?\n\n",
        11: "HINT: Keep trying `hidden_num > another_num`, changing `another_num` to something else each time to narrow it down!",
        12: "HINT: Keep trying `hidden_num >= another_num`, changing `another_num` to something else each time to narrow it down!",
        13: "HINT: Those `for` loops are pretty handy here!\n\n"
        "You'll want to use them to iterate over the numbers in the range of 1 to 100 "
        "(`for number in range(100):`) to check each number with `==`",
        14: "HINT: Another one where `for` loops are handy!\n\n"
        "You'll want to use them to iterate over the numbers in the range of 1 to 100 to check each number with `!=`",
    }

    def guess(self, guess):
        if guess == self._hidden_number:
            message = "Congrats, you're correct!! You guessed right!"
            if self.exercise_number < 14:
                message += (
                    f"\n\nEnter: `hidden_num = HiddenNumber({self.exercise_number + 1})` "
                    f"to the console to play exercise {self.exercise_number + 1}."
                )
            else:
                message += (
                    f"\n\nCongrats! You've finished all the exercises! Now an extension activity - write a program"
                    f" that solves these problems!\n\n"
                    f"All the Python you've been writing in the console can be written into a file and then you can run that file.\n\n"
                    f"Write the code in `main.py`, then click `Run` at the top to run it.\n\n"
                    f"You'll now only see output from `print()` statements in the console. (try just adding `print(22)` to the file and running it)\n\n"
                    f"Use a `for` loop to change the exercise number and `if` statements"
                    f"to change what code you run based on which exercise it is!\n"
                    f"To learn about these, either read `for_loops.md` and `if_else.md` or look at https://app.learney.me/maps/PythonCurriculum?concept=28"
                )
            print(message)
        elif self.exercise_number == 0:
            if guess > self._hidden_number:
                print("Too high!")
            else:
                print("Too low!")
            self.hint_if_necessary()
        else:
            print("Incorrect! Try again! :)")
            self.hint_if_necessary()


hidden_num = HiddenNumber(0)

hidden_num.guess(1)
