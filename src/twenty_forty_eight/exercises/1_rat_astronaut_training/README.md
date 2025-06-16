## Rat astronaut training
You are an unwitting rat stuck in an astronaut training program. Elon Musk and Jeff Bezos plan to launch you to space to make sure it's safe for them to go Mars.

But first, they test you in a super hi-tech astronaut training facility where they can control gravity.

To start with, the room has no gravity, and so objects float around.

Then Mr. Musk flicks the gravity switch, but flicks it the wrong way! All the objects go directly up to the ceiling.

To survive, you must predict where the objects will go so you can position yourself safely.

### Instructions

You are given a numpy array `room`. The array takes a random size, with the number of rows and columns taking random values between 5 and 10.

The array is full of zeros, other than the 'objects', which are signified by different numbers from 1 -> n. There are a random number of objects in the room.

Row '0' is the top of the room. Column '0' is the left hand side.

Here's a simplified 3 x 3 version:

![Non-gravity room (passed into your function)](./nongravity-room.png
)

You must write code that takes the array 'room' and returns where the objects will be after the reverse gravity is switched on. (Note: the objects can stack on top of each other! See the example below).

Your code, when applied to the example above, should return:


![Non-gravity room (passed into your function)](./gravity-room.png
)


You should write your code inside the `room_after_upsidedown_gravity()` function. The code below that is used to run the tests to see if you got it right, no need to edit there!
