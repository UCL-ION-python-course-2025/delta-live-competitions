# Recap: Feature Vectors

They were introduced through [Tutorial 6](https://replit.com/team/delta-academy-RL/6-Da-Vincis-Vengence),
with the final exercise in that tutorial required you to build a set of features that can be used by
an RL algorithm to learn to play Tic-Tac-Toe.

![Flow diagram showing feature vectors fitting into the value function and state relationship](./images/feature_vector_connect_4.png)

Feature vectors are useful to:
1. **Reduce the effective state space size** (number of possible states) of a problem
2. **Reduce the time spent training** by reducing the number of parameters that need
to be learned

It does both of these by sharing value estimates between similar states.
How is **similar** defined? It's defined by the designer. In this case,
that's you.

### How do I design a feature vector?

First, think about what the **value of a state** would be in the MDP you're trying to solve.
For example, **in a game of chess**, a state where you've taken their queen would be higher value
than the identical state where they still have their queen.

So **whether their queen has been taken** (could be represented by a 0 or a 1) could be a feature.

Another feature could be **whether you have your opponent in checkmate**. You need to identify
this so your 1-step lookahead greedy function can identify states where it wins and choose those.

In general, ask yourself: **what are the key features that affect how valuable a state is in
this game?**

The feature state doesn't actually have to be a consistent length, although it's recommended that
it is, otherwise you may get 2 feature vectors that refer to different features looking
identical to the value function.
