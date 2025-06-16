import random

import numpy as np
import torch
from torch import nn

from game_mechanics import load_network, play_the_market, train_network

# Enter your team name here!
TEAM_NAME = ""  # It's what'll show up in the competition!

# Do you want to train your network or test
# it out on the stock market?
# i_want_to = "train"
i_want_to = "test"


# Adjust the number of days you play the market for (when testing your already-trained neural network) here!
NUMBER_OF_FORECASTS = 100


def train(previous_5_days: torch.Tensor, next_days: torch.Tensor) -> nn.Module:
    """Write the code to train your network here!

    Args:
        previous_5_days: Tensor of shape (1000, 5). 200
            training examples of 5 day periods
        next_days: Tensor of shape (1000, 1). 1000 training
            examples of the day following the corresponding
            previous 5 days.

    Returns:
        A trained pytorch neural network.
    """
    neural_network = ...
    return neural_network


def predict_price(previous_5_days: torch.Tensor) -> float:
    """Write the code to test your network here!

    Args:
        previous_5_days: Tensor of shape (1,). The previous 5
            days of stock price that you will use to make
            your prediction
    Returns:
        A float that is your forecast for the next day's
            stock price.
    """
    network = load_network(TEAM_NAME)
    return float(network(previous_5_days)[0])


#### Leave this code alone ####
if __name__ == "__main__":
    import replit

    replit.clear()

    if i_want_to == "train":
        train_network(train, TEAM_NAME)
    elif i_want_to == "test":
        play_the_market(predict_price, NUMBER_OF_FORECASTS)
    else:
        raise ValueError(f"i_want_to = {i_want_to}, please set it to 'train' or 'test'!")
