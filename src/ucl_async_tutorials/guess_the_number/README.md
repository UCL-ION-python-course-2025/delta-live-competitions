## Instructions

Work out the hidden number using Python *operators*
(such as `+`, `-` and `*`) in the Console. The hidden number is
chosen randomly between 1 and 100 (inclusive) each round.

**In each exercise you only have some operators available to use!**

To start exercise `1`: (change the number in brackets to change the exercise)

```python
hidden_num = HiddenNumber(1)
```

Here, `hidden_num` (you can call this variable what you like!) is a hidden number
between `1` and `100`, which you have to work out in the console and guess! :)

To make a guess at `hidden_num` (we're guessing it's `77` below), run:
```python
hidden_num.guess(77)
```

You don't want to guess randomly - that'll take forever! So for each exercise we're enabling certain operators (e.g. addition `+`, subtraction `-` etc) which you can use to work out what it is!

E.g. this will print out the number 5 higher than the hidden number ;)
```python
new_num = hidden_num + 5
new_num
```

**Struggling??** Use this to get a hint!

```python
hidden_num.hint()
```

## General Basics of Code

To set a variable:
```python
x = 7
```

To see the value of a variable:
```python
x
```
or in a file
```python
print(x)
```


You can practice with exercise `0`, where you can see the
hidden number with the 2nd line below:

```python
hidden_num = HiddenNumber(0)
print(hidden_num)
```

N.B. Lines starting with a `#` are **comments** - these aren't code and **don't run**! E.g.
```python
# Comments are useful to explain code to others in files :)
```
