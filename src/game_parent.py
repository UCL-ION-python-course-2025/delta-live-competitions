import enum
import random
from abc import ABC
from typing import List, Optional, Tuple

from team import Team


class PlayState(enum.Enum):
    YET_TO_START = 0
    IN_PROGRESS = 1
    COMPLETED = 2


class GameType(enum.Enum):
    HEAD_TO_HEAD = 0
    LAST_TEAM_STANDING = 1
    FREE_FOR_ALL = 2


def no_robot_action_set():
    raise NotImplementedError("No robot action set - override ROBOT_PLAYER to do so!")


class Game(ABC):
    NAME = None
    ROBOT_PLAYER = Team("Robot", no_robot_action_set)

    def __init__(self, name: str, *args):
        self.name = name
        self.game_type = None
        self.play_state: PlayState = PlayState.YET_TO_START

    def __repr__(self):
        return self.name

    def step(self) -> None:
        """Performs a step in the game."""
        raise NotImplementedError

    def reset_game(self) -> None:
        """Resets the game state."""
        self.play_state = PlayState.YET_TO_START

    @property
    def winner(self) -> Team:
        """Returns the winning team."""
        raise NotImplementedError

    def complete(self) -> None:
        self.play_state = PlayState.COMPLETED

    @property
    def completed(self) -> bool:
        return self.play_state == PlayState.COMPLETED

    @property
    def teams(self) -> List[Team]:
        raise NotImplementedError


YELLOW_COLOR = (255, 240, 0)
RED_COLOR = (255, 0, 0)


class HeadToHeadGame(Game, ABC):
    def __init__(
        self,
        team_a: Team,
        team_b: Team,
        name: str,
        team_a_color: Tuple[int, int, int] = YELLOW_COLOR,
        team_b_color: Tuple[int, int, int] = RED_COLOR,
        both_teams_progress_on_draw: bool = False,
    ):
        super().__init__(name)
        self.team_a = team_a
        self.team_b = team_b
        self.team_a_score = 0
        self.team_b_score = 0
        self.player_turn: int = random.choice([-1, 1])
        self.went_first: int = self.player_turn
        self.team_a_color = team_a_color
        self.team_b_color = team_b_color
        self.both_teams_progress_on_draw = both_teams_progress_on_draw

    def reset_game(self) -> None:
        super(HeadToHeadGame, self).reset_game()
        if self.is_robot_vs_robot_game:
            self.team_a_score += 1  # Doesn't matter who wins
            self.complete()

    @property
    def is_robot_vs_robot_game(self) -> bool:
        return self.team_a == self.team_b

    @property
    def both_teams_progressing(self) -> bool:
        return (
            self.completed
            and self.both_teams_progress_on_draw
            and self.team_a_score == self.team_b_score
        )

    @property
    def winner(self) -> Optional[Team]:
        if not self.completed:
            return None
        return (
            self.team_a
            if self.team_a_score > self.team_b_score
            else (
                self.team_b
                if self.team_a_score < self.team_b_score
                else (
                    self.team_a
                    if self.team_a_score == self.team_b_score
                    and self.both_teams_progress_on_draw
                    else None
                )
            )
        )

    @property
    def winner_color(self) -> Optional[Tuple[int, int, int]]:
        if not self.completed:
            return None
        return (
            self.team_a_color
            if self.team_a_score > self.team_b_score
            else self.team_b_color if self.team_a_score < self.team_b_score else None
        )

    @property
    def loser(self) -> Optional[Team]:
        if not self.completed:
            return None
        return (
            self.team_b
            if self.team_a_score > self.team_b_score
            else (
                self.team_a
                if self.team_a_score < self.team_b_score
                else (
                    self.team_b
                    if self.team_a_score == self.team_b_score
                    and self.both_teams_progress_on_draw
                    else None
                )
            )
        )

    @property
    def teams(self) -> List[Team]:
        return [self.team_a, self.team_b]

    @property
    def next_to_play(self) -> Team:
        return self.team_a if self.player_turn == 1 else self.team_b

    def complete(self) -> None:
        super().complete()
        if self.both_teams_progressing:
            self.team_a.name = f"{self.team_a.name} & {self.team_b.name}"


class PointsGame(Game, ABC):
    def __init__(self, name: str, team: Team):
        super().__init__(name)
        self._team = team
        self.score = 0

    @property
    def teams(self) -> List[Team]:
        return [self._team]


class MultiPlayerGame(Game, ABC):
    def __init__(
        self,
        teams: List[Team],
        name: str,
    ):
        """Parent class for a game when all players play on the same board at the same time."""
        super().__init__(name)
        self._teams = teams
        self.team_scores = [0] * len(self.teams)

    @property
    def teams(self) -> List[Team]:
        return self._teams
