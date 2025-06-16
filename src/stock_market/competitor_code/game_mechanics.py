import random
from pathlib import Path
from typing import Callable, Tuple

import numpy as np
import torch
import torch.nn as nn

ONE_MILLION = 1_000_000.00

HERE = Path(__file__).parent.resolve()


def save_network(network: nn.Module, team_name: str) -> None:
    assert isinstance(network, nn.Module), f"train() function outputs an invalid network: {network}"
    assert "/" not in team_name, "Invalid TEAM_NAME. '/' are illegal in TEAM_NAME"
    torch.save(network, f"{team_name}_network")


def load_network(team_name: str) -> nn.Module:
    net_path = HERE / f"{team_name}_network"
    assert (
        net_path.exists()
    ), f"Network saved using TEAM_NAME='{team_name}' doesn't exist! ({net_path})"
    model = torch.load(net_path)
    model.eval()
    return model


def training_data_from_stock(stock: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    x, y = [], []
    for start_chunk, end_chunk in enumerate(range(5, len(stock))):
        x.append(stock[start_chunk:end_chunk])
        y.append(stock[end_chunk])
    return np.array(x), np.array(y)


def train_network(train: Callable, team_name: str) -> None:
    stock_price = np.load(f"{HERE}/data/stock_price_train.npy")
    previous_5_days, next_days = training_data_from_stock(stock_price)
    previous_5_days = torch.tensor(previous_5_days).float()
    next_days = torch.unsqueeze(torch.tensor(next_days), dim=1).float()
    print("Starting network training!")
    neural_network = train(previous_5_days, next_days)
    print("Network training completed!, Saving network.")
    save_network(neural_network, team_name)


def play_the_market(take_action: Callable, number_of_forecasts: int) -> None:
    market = StockMarket("", 1, number_of_forecasts=number_of_forecasts)

    returns = market.play_standalone_game(take_action)
    if returns > 0:
        print(f"Congratulations! You made ${round(returns, 2)}!")
    else:
        print(f"Oh No! You lost ${-round(returns, 2)}!. You're fired!")


class TradingGame:
    def __init__(self, initial_stock_price: float, verbose: bool = True) -> None:
        self.starting_money = self.current_money = ONE_MILLION
        self.starting_stocks = self.stocks_held = 1000
        # How many stocks to buy or sell in each trade
        self.n_stocks_trade = 100
        self.intial_cost = initial_stock_price * self.starting_stocks
        self.current_position = "none"

        self.verbose = verbose
        if self.verbose:
            print(
                f"\nStarting Trading with £{self.starting_money}\nThe initial stock price is £{round(initial_stock_price, 2)} per share \n"
            )

    def open_position(self, forecast: float, today_closing: float) -> None:
        if self.verbose:
            print(f"You predict that the stock price will open tomorrow at £{round(forecast, 2)}")

        if forecast < today_closing:
            self.go_short(today_closing)
        elif forecast > today_closing:
            self.go_long(today_closing)
        else:
            self.no_position()

    def close_position(self, previous_close: float, open: float) -> None:
        if self.verbose:
            print(
                f"The market opened at £{round(open, 2)}!\nClosing {self.current_position} position"
            )

        if self.current_position == "long":
            money_change = (open - previous_close) * self.n_stocks_trade
        elif self.current_position == "short":
            money_change = (open - previous_close) * self.n_stocks_trade * -1
        else:
            money_change = 0

        if self.verbose:
            if money_change > 0:
                print(f"You made £{round(money_change, 2)}!\n")
            elif money_change < 0:
                print(f"You lost £{-round(money_change, 2)}!\n")
            else:
                print("You broke even!\n")
        self.current_money += money_change

    def go_long(self, today_closing: float) -> None:
        self.current_position = "long"
        if self.verbose:
            print(f"Going long {self.n_stocks_trade} stocks at £{round(today_closing, 2)} each")

    def go_short(self, today_closing: float) -> None:
        self.current_position = "short"
        if self.verbose:
            print(f"Going short {self.n_stocks_trade} stocks at £{round(today_closing, 2)} each")

    def no_position(self) -> None:
        self.current_position = "none"
        if self.verbose:
            print("Taking no position")

    def get_final_return(self) -> float:
        return self.current_money - self.starting_money


class StockMarket:
    def __init__(
        self,
        team_name: str,
        game_speed_multiplier: float,
        number_of_forecasts: int,
    ) -> None:
        self.team_name = team_name
        self.game_speed_multiplier = game_speed_multiplier
        self.number_of_forecasts = number_of_forecasts
        self.visualisation_controller = None
        self.forecasts_done = 0
        self.game_over = False
        self.total_error = 0
        self._stock_price = np.load(f"{HERE}/data/stock_price_test.npy")
        assert (
            self._stock_price.shape[0] - 5 >= number_of_forecasts
        ), f"Number of forecasts requested ({number_of_forecasts}) exceeds the maximum number of forecasts in test set: {self._stock_price.shape[0] - 5}"

        self.trading_game = TradingGame(self.current_ticker[-1], False)

    @property
    def steps_from_end(self) -> int:
        return self.number_of_forecasts - self.forecasts_done

    @property
    def current_ticker(self) -> np.ndarray:
        return self._stock_price[: len(self._stock_price) - self.steps_from_end]

    def reset(self) -> None:
        self.game_over = False
        self.forecasts_done = 0
        self.total_error = 0

    def play_standalone_game(self, take_action: Callable[[np.ndarray], float]) -> float:
        while self.forecasts_done < self.number_of_forecasts:
            self.update(take_action)
        return self.trading_game.get_final_return()

    def update(self, take_action: Callable[[np.ndarray], float]) -> None:
        data = torch.unsqueeze(torch.tensor(self.current_ticker[-5:]), dim=1).T.float()

        try:
            forecast = take_action(data)
            assert isinstance(forecast, float), "You must return a float!"
        except Exception as e:
            print(e)
            forecast = float(random.choice(data[0]))
            print(self.team_name, "chose randomly because of broken torch files")
        error = np.abs(forecast - self._stock_price[-self.steps_from_end])
        self.total_error += error
        self.trading_game.open_position(forecast, self.current_ticker[-1])
        self.forecasts_done += 1
        self.trading_game.close_position(self.current_ticker[-2], self.current_ticker[-1])
