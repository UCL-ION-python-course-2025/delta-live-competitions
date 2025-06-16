# For learney eyes only

from typing import List

import numpy as np
from matplotlib import pyplot as plt


class GenerateDataAR:
    """Sample generator for autoregressive (AR) signals.

    Generates time series with an autogressive lag defined by the number of parameters in ar_param.

    Parameters
    ----------
    ar_param : list (default [None])
        Parameter of the AR(p) process
        [phi_1, phi_2, phi_3, .... phi_p]
    sigma : float (default 1.0)
        Standard deviation of the signal
    start_value : list (default [None])
        Starting value of the AR(p) process

    NOTE: Adapted from: https://github.com/TimeSynth/TimeSynth
    TODO: The structure of the code is kinda trash, could be refactored easily and can be vectorised
    """

    def __init__(self, ar_params: List[float], start_values: List[float], sigma: float = 0) -> None:
        self.ar_params = ar_params.copy()[::-1]
        self.sigma = sigma
        self.data = start_values.copy()
        self.previous_value = start_values.copy()
        if len(start_values) != len(ar_params):
            raise ValueError(
                f"ar_params length = {len(ar_params)}. start_values length = {len(start_values)}. Need to be the same length"
            )

    def sample_next(self):
        """Sample the next value of the signal.

        Returns
        -------
        ar_value : float
            sampled signal for time t

        TODO: This can be vectorized
        """
        ar_value = [self.previous_value[i] * self.ar_params[i] for i in range(len(self.ar_params))]
        noise = np.random.normal(loc=0.0, scale=self.sigma)
        ar_value = np.sum(ar_value) + noise
        self.previous_value = self.previous_value[1:] + [ar_value]
        return ar_value

    def sample_n_values(self, number_of_samples: int) -> None:
        for _ in range(number_of_samples):
            self.data.append(self.sample_next())


def test_is_ar(ar_phi: List, data: np.ndarray) -> None:
    """Passes if data is an AR(ar_phi) process with no noise."""
    n_params = len(ar_phi)
    for i in range(len(data) - n_params):
        assert data[n_params + i] == np.dot(data[0 + i : n_params + i], np.array(ar_phi)[::-1])


def generate_stock_price(sigma: float = 10, length: int = 1000, plot: bool = False) -> np.ndarray:
    """
    Get a vector of a stock price over time.
    Parameters
    ----------
    sigma : float (default 0.0)
        Standard deviation of the signal
    length : int (default 1000)
        Length of the stock price vector
    """

    # Need to be slightly unstable dynamics otherwise noise dominates
    # This in conjuction with a sigma of 10 and a length of 200 gives
    # a vector that looks like a stock, but is dominated by the AR dynamics,
    # not the noise. A cheater than knows the weights will win every time with this.
    # ar_phi = [0.7, 0.1, 0.6, -0.3, -0.3]
    ar_phi = [0.7, 0.1, 0.6, -0.3, -0.2]
    data = list(np.random.randint(90, 110, size=len(ar_phi)))

    ar = GenerateDataAR(ar_params=ar_phi, sigma=sigma, start_values=data)
    ar.sample_n_values(length)
    return_data = np.array(ar.data)
    return_data = return_data - min(return_data) + 10  # Min the stock at 10

    if sigma == 0.0:
        test_is_ar(ar_phi, return_data)
    if plot:
        plt.plot(return_data)
        plt.ylabel("Stock price")
        plt.xlabel("Days")
        plt.show()
    return return_data


if __name__ == "__main__":
    stock = generate_stock_price(plot=True)
    with open("stock_price_train2.npy", "wb") as f:
        np.save(f, stock)
