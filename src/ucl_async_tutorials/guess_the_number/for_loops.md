## For Loops

For the final 2 exercises, it'll help to know how to use `for` loops.

Here's an example `for` loop. They're useful to run some code with many possible values.
We'll dissect the different parts once we understand what it's useful for.

```python3
for item in range(5):
    print(item)
```

Outputs the following (try it - you'll need to hit enter twice in the console for this to run):
```python3
0
1
2
3
4
```

So what happens there?

The code runs the 2nd line, `print(item)`, **5 times**.
In general, all the indented code below the colon is run
(for multiple lines being run in a `for` loop, look at the examples).

Each time, `item` is a different number in the range `0` to `4`.

So, this is equivalent to running:
```python
item = 0
print(item)
item = 1
print(item)
item = 2
print(item)
item = 3
print(item)
item = 4
print(item)
```

### `for` syntax

5 key points on the syntax for writing `for` loops!

1. `for` and `in` are keywords and are necessary for **any** `for` loop.


2. `item` is the variable you're assigning the value of the current iteration
to. You can give it any valid variable name.


3. `range(INTEGER)` gives you a list of sequential integer from `0` -> `INTEGER` to iterate through.


4. DON'T FORGET THE COLON `:` AT THE END OF THE LINE!


5. You have to indent (with a `TAB`) the code to run every iteration
which is below the `for` line.


> Why `0` first? Surely it should be `1` -> `5`, not `0` -> `4`?

Afraid not. Starting with 0 is convention in Python. Just the way it is.
So `range(66)` has `66` elements, but the highest is `65`.

### MOAR EXAMPLES

#### 1 - Triangle Number
```python3
triangle_number = 0
for x in range(6):
    triangle_number = triangle_number + x

print(triangle_number)
```

Sums the numbers from `0` -> `5` to get the 5th triangle number.

So it outputs:

```python3
15
```

#### 2 - Checking a number

```python3
for i in range(10):
    print(i)
    print(x == i)
```

Checks the value of `x` and prints out each number and if it's
equal to `x`.

If `x == 7`, it outputs:

```python3
0
False
1
False
2
False
3
False
4
False
5
False
6
False
7
True
8
False
9
False
```

#### 3 - Checking if a Number is Prime (complicated)

```python3
number_to_check = 2937

# Check if any number 2 -> number_to_check - 1 is a factor
for x in range(2, number_to_check):
    if (number_to_check // x) == (number_to_check / x):
        print("Is not prime!")
        break
```
Since 2937 is divisble by 3, this outputs:

```
Is not prime!
```

This time `range()` gets 2 arguments:
- `2` - the number to start the range at
- `number_to_check` - 1 more than the highest number in the range (highest number checked is  `2938`)

These combine to make `range(2, number_to_check)` to give a number range
from `2` -> `number_to_check - 1` (including both `2` and `number_to_check - 1`).

The `break` keyword is used too, which stops iterating through the loop
when it's reached. This stops us from printing `Is not prime!` multiple times,
since it runs right after the first time it's reached.

We also use an `if` statement here.
This means the code indented below `if` only runs if `(number_to_check // x) == (number_to_check / x)`,
which simply checks whether dividing gives a whole number or not.
Check out `if_else.md` if you like.


Still confused by `for` loops? Learn up to here on the roadmap: (https://app.learney.me/maps/PythonCurriculum?concept=33)
