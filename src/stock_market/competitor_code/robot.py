import random

import numpy as np

import torch
from torch import nn

from .game_mechanics import load_network, play_the_market, train_network

# Enter your team name here!
TEAM_NAME = "robot"

# Do you want to train your network or try
# it out on the stock market?
# i_want_to = "train"
i_want_to = "test"


def train(previous_5_days: torch.Tensor, next_days: torch.Tensor) -> nn.Module:
    """Write the code to train your network here!

    Args:
        previous_5_days: Tensor of shape [200x5]. 200 training examples of 5
                         day periods
        next_days: Tensor of shape [200x1]. 200 training examples of the day
                   following the corresponding previous 5 days.

    Returns:
        A trained pytorch neural network.
    """

    neural_network = nn.Linear(5, 1, bias=False)
    return neural_network


def predict_price(previous_5_days: torch.Tensor) -> float:
    """WE MIGHT NOT NEED THIS IN MAIN? Write the code to test your network here!

    Args:
        previous_5_days: Tensor of shape [1]. The previous 5 days of stock price
                         that you will use to make your prediction
    Returns:
        A float that is your forecast for the next day's stock price.
    """
    network = load_network(TEAM_NAME)
    return float(network(previous_5_days)[0])


if __name__ == "__main__":

    if i_want_to == "train":
        train_network(train, TEAM_NAME)
    elif i_want_to == "test":
        play_the_market(predict_price, 100)
    else:
        raise ValueError(f"i_want_to = {i_want_to}, please set it to 'train' or 'test'!")
