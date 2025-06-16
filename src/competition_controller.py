import json
from datetime import datetime
from pathlib import Path
from time import sleep
from typing import Dict, List, Optional, Type

import pygame

from events import Event
from game_parent import Game, HeadToHeadGame, MultiPlayerGame, PointsGame
from knockout_competition import KnockoutCompetition, remove_robots
from multiplayer_competition import MultiplayerCompetition
from observation import Observable
from points_competition import PointsCompetition
from team import Team


class CompetitionController(Observable):
    def __init__(
        self,
        name: str,
        teams: List[Team],
        game: Type[Game],
        min_time_per_step: float = 1,
        moves_per_state_change: int = 1,
        plate_enabled: bool = True,
        run_in_series: bool = True,
        speed_increase_factor: float = 1,
        wait_for_click_end_of_round: bool = True,
    ):
        """Drives the competition. Sets up new rounds and runs each game by calling game.step().

        Args:
            name: name of the game
            teams: teams competing in the game
            game: Inherits from game_parent/Game
            min_time_per_step: Each step will take at least this
                               long. Controller will sleep if each
                               team's choose_move takes less time.
            moves_per_state_change: After how many steps should each game be drawn
                                    (usually 1)
            plate_enabled: Should first round losers go into their own tournament?
            run_in_series: Should games be run one after another
                           (rather than simultaneously)?
            speed_increase_factor: Speed of the game will increase by this factor
                                   after each step
        """

        # remove when other game types are added
        assert issubclass(game, (HeadToHeadGame, PointsGame, MultiPlayerGame))

        super().__init__(name)
        assert teams, "No teams given to Competition Controller!"
        self.teams = teams
        self.game = game
        self.plate_enabled = plate_enabled
        self.run_in_series = run_in_series

        # This is for the live competition - if all the moves happen instantaneously, then it's no fun!
        self.min_time_per_step = self.original_time_per_step = min_time_per_step
        self.moves_per_state_change = moves_per_state_change
        self.speed_increase_factor = speed_increase_factor

        # Start with overall competition
        comp_type = (
            KnockoutCompetition
            if issubclass(game, HeadToHeadGame)
            else (
                PointsCompetition
                if issubclass(game, PointsGame)
                else (
                    MultiplayerCompetition
                    if issubclass(game, MultiPlayerGame)
                    else None
                )
            )
        )
        assert comp_type is not None
        self.competitions = [comp_type(teams, f"Overall {game.NAME} Cup", game)]
        self.rounds_of_games = [self.get_new_round_of_games()]

        self.plate_created = False
        self.wait_for_click_end_of_round = wait_for_click_end_of_round

    @property
    def round_num(self) -> int:
        return len(self.rounds_of_games)

    def run_round_of_games(self) -> None:
        if self.run_in_series:
            self.run_round_of_games_series()
        else:
            self.run_round_of_games_parallel()

    def run_round_of_games_parallel(self) -> None:
        move_num = 0
        while any(not game.completed for game in self.current_round_of_games()):
            move_num += 1
            time_start = datetime.now()
            # .step() steps the game forward in time
            [game.step() for game in self.current_round_of_games()]

            # Redraw the matches in progress
            if (
                move_num % self.moves_per_state_change
                == self.moves_per_state_change - 1
            ):
                self.redraw()

            self.wait_until_next_move(time_start)

        self.redraw()

    def run_round_of_games_series(self) -> None:
        for game in self.current_round_of_games():
            move_num = 0
            while not game.completed:
                move_num += 1
                time_start = datetime.now()
                # .step() steps the game forward in time
                game.step()

                # Redraw the matches in progress
                if (
                    move_num % self.moves_per_state_change
                    == self.moves_per_state_change - 1
                ):
                    self.redraw()

                self.wait_until_next_move(time_start)

            self.min_time_per_step = self.original_time_per_step

            if self.wait_for_click_end_of_round:
                wait_for_click()

        self.redraw()

    def wait_until_next_move(self, time_start: datetime) -> None:
        """Wait in case it doesn't take long enough."""

        self.min_time_per_step /= self.speed_increase_factor
        time_since_start = (datetime.now() - time_start).total_seconds()
        if time_since_start < self.min_time_per_step:
            sleep(self.min_time_per_step - time_since_start)

    def current_round_of_games(self) -> List[Game]:
        return self.rounds_of_games[-1]

    def current_round_over(self) -> bool:
        return all(game.completed for game in self.current_round_of_games())

    def get_new_round_of_games(self) -> List[Game]:
        if issubclass(self.game, PointsGame):
            return self.competitions[0].live_games
        elif issubclass(self.game, MultiPlayerGame):
            return [self.competitions[0].game]
        elif issubclass(self.game, HeadToHeadGame):
            # Not including robot_v_robot games here causes issues
            competition_games = [
                game for comp in self.competitions for game in comp.live_games
            ]

            if len(competition_games) != 1:  # Not the overall final
                # Remove the overall final - wait until the end to play that!
                competition_games = [
                    game
                    for game in competition_games
                    if not ("Overall" in game.name and game.name.startswith("Final"))
                ]

            return competition_games
        else:
            raise NotImplementedError("Unknown game type")

    def teams_not_in_competition(self, competition_games: List[Game]) -> List[Team]:
        return [
            team
            for team in self.teams
            if all(team not in game.teams for game in competition_games)
        ]

    def new_round(self) -> None:
        if not self.competitions_over:
            main_comp_losing_teams = self.competitions[0].rounds[-1].losers
            [comp.complete_round() for comp in self.competitions]

            # Make plate if more than 4 teams knocked out and no plate yet
            if (
                len(main_comp_losing_teams) >= 4
                and self.plate_enabled
                and not self.plate_created
            ):
                self.competitions += [
                    KnockoutCompetition(
                        main_comp_losing_teams,
                        f"{self.game.NAME} Plate",
                        self.game,
                        is_third_playoff=False,
                    )
                ]
                self.plate_created = True

            self.rounds_of_games.append(self.get_new_round_of_games())
            self.notify(Event.GAME_RESET)

    @property
    def competitions_over(self) -> bool:
        return all(comp.winner is not None for comp in self.competitions)

    @property
    def ranking(self) -> Dict[int, List[Team]]:
        """Get the ranking of teams as a dictionary, not including robots."""
        if not self.competitions_over:
            return {}

        if issubclass(self.game, PointsGame):
            return self.competitions[0].ranking

        ranking: Dict[int, List[Team]] = {}
        # Add those in competition
        for comp in self.competitions:
            assert comp.ranking is not None

            # Remove the highest rank if there are already rankings (2 tournaments, 2nd contains
            #  1st round losers from 1st tournament)
            if ranking:
                ranking.pop(max(ranking))

            # Add all the teams from each competition's ranking
            for comp_rank, comp_teams in sorted(
                comp.ranking.items(), key=lambda x: x[0]
            ):
                # Remove all robots
                comp_teams = remove_robots(comp_teams, self.game.ROBOT_PLAYER)

                # If there are no other teams, skip to next ranking level
                if not comp_teams:
                    continue

                # Ranking of these teams is 1 + number of teams in ranking so far
                ranking[sum(len(teams) for teams in ranking.values()) + 1] = comp_teams

        ranking_dir = Path("./rankings")
        # Ensure the rankings directory exists
        ranking_dir.mkdir(parents=True, exist_ok=True)

        # Save the json of the rankings in the rankings dir
        with (ranking_dir / f"{self.game.NAME}_ranking.json".replace(" ", "_")).open(
            "w"
        ) as file:
            json.dump(
                {key: [team.name for team in val] for key, val in ranking.items()}, file
            )

        return ranking

    def get_competition_to_draw(self) -> Optional[KnockoutCompetition]:
        """Get the competition to draw the tournament tree of."""
        if not issubclass(self.game, HeadToHeadGame):
            return None
        for comp in self.competitions:
            if not comp.tournament_tree_visualised:
                return comp
        return None


def wait_for_click() -> None:
    # If pygame is not initialised, dont wait
    if not pygame.get_init():
        return
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
