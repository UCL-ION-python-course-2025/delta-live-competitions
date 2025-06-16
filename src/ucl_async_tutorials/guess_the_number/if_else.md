## If-Else

To do the extension exercise, it'll help to know how to use `if` and `else` statements.

Here's an example `if`. They're useful to run different code based on the outcome
of an expression. An example is useful here. We'll dissect how it works once we understand what it's useful for.

```python3
if x == 7:
    x = x + 4
```

This adds `4` to `x` if `x == 7` (`==` means 'is equal to').

Otherwise, it doesn't do anything.

`if`'s can be followed by `else` statements which run when the `if` is `False`.

```python3
if x < 7:
    x = x + 4
else:
    x = x - 4
```

This adds `4` to `x` if `x` is less than `7` and subtracts `4` from `x` otherwise.

### `if`-`else` syntax

1. `if` statements start with `if`


2. They're followed by an *expression* which is evaluated to `True` or `False`.
E.g. `x < 7`


3. They end with a colon `:`


4. You must indent the code that optionally runs in the `if` and `else` statements.


### MOAR EXAMPLES

#### 1 - Check if divisible by 2

```python3
if x % 2 == 0:
    print("x is even!")
```

This uses the modulus operator to check if the number is divisible by 2.

If it is, it prints `x is even!`.

We can optionally add an `else` statement here too.

```python3
if x % 2 == 0:
    print("x is even!")
else:
    print("x is odd!")
```

This will print `x is even!` or `x is odd!` depending on whether it's odd or even.

#### 2 - Checking if a Number is Prime

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

We also use a `for` loop here with `break`, which stops iterating through the loop
when it's reached. This stops us from printing `Is not prime!` multiple times.

#### 3 - Running all the rounds of Guess The Number

```python3
for round_num in range(1, 14):  # Iterate through 1 -> 14 inclusive
    hidden_num = HiddenNumber(round_num)

    if hidden_num == 1:
        ...
    elif hidden_num == 2:
        ...
    elif hidden_num == 3:
        ...
    ...
    else:
        ...
```

Above uses `elif` which is a mix between `else` and `if` and allows
you to chain together several mutually exclusive conditions.

Here it only checks if `hidden_num == 2` once it's checked that
`hidden_num == 1` is `False`. More than anything else, this makes
it easier for others to understand your code.

Still confused by `if` statements? Learn up to here on the roadmap: (https://app.learney.me/maps/PythonCurriculum?concept=28)
