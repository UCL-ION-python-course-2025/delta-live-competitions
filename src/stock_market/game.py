import os

import pygame
from pygame import Surface

from game_parent import PointsGame
from stock_market.competitor_code.game_mechanics import ONE_MILLION, StockMarket
from stock_market.competitor_code.robot import predict_price as robot_choose_move
from team import Team

ASSET_PATH = "src/stock_market/assets"


class StockGame(PointsGame, StockMarket):
    NAME = "stock_market"
    ROBOT_PLAYER = Team("Robot", robot_choose_move)
    GAME_SPEED_MULTIPLIER = 100
    TOTAL_ROUNDS = 100

    def __init__(
        self,
        name: str,
        team: Team,
    ):
        PointsGame.__init__(
            self,
            name,
            team,
        )
        self.n_rounds = 0
        StockMarket.__init__(
            self, team.name, StockGame.GAME_SPEED_MULTIPLIER, number_of_forecasts=10
        )
        self.n_total_guesses = 0
        self.n_rounds_solved = 0
        self.score = 100
        self.timeout = 1

    def draw_game(self, screen: Surface, scale: float) -> None:
        self.screen = screen
        self.scale = scale
        pygame.font.init()
        self.font = pygame.font.Font(os.path.join(ASSET_PATH, "FreeSansBold.otf"), int(10 / scale))
        self.display_current_money(self.trading_game.current_money)

    def set_starting_position(self, x: float, y: float) -> None:
        self.x_starting_pos = x
        self.y_starting_pos = y

    def display_team_name(self) -> None:
        text = self.font.render(self.team_name, True, "black")
        team_name_rect = text.get_rect(
            center=(
                self.x_starting_pos,
                self.y_starting_pos - 30 / self.scale,
            )
        )
        self.screen.blit(text, team_name_rect)

    def display_current_money(self, money: float) -> None:
        txt = f"${'{:,}'.format(round(money, 2))}"
        text = self.font.render(txt, True, "green" if money >= ONE_MILLION else "red", "black")
        money_rect = text.get_rect(
            center=(
                self.x_starting_pos,
                self.y_starting_pos,
            )
        )
        self.screen.blit(text, money_rect)

        made_money = money >= ONE_MILLION
        change_text = (
            f"+${'{:,}'.format(round(money - ONE_MILLION, 2))}"
            if made_money
            else f"-${'{:,}'.format(round(ONE_MILLION - money, 2))}"
        )
        text = self.font.render(change_text, True, "green" if made_money else "red", "black")
        money_rect = text.get_rect(
            center=(
                self.x_starting_pos,
                self.y_starting_pos + self.font.get_linesize(),
            )
        )
        self.screen.blit(text, money_rect)

    def step(self) -> None:
        self.n_rounds += 1
        self.update(self._team.choose_move)
        self.display_current_money(self.trading_game.current_money)

        if self.n_rounds == self.TOTAL_ROUNDS:
            self.score = self.trading_game.current_money
            self.complete()
