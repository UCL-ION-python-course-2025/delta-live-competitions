import math
from copy import copy
from typing import Dict, List, Optional, Type
from warnings import warn

import numpy as np

from competition import Competition
from game_parent import Game, HeadToHeadGame
from team import Team


class KnockoutCompetition(Competition):
    def __init__(
        self,
        teams: List[Team],
        name: str,
        game: Type[HeadToHeadGame],
        is_third_playoff: bool = True,
    ):
        if all(team == game.ROBOT_PLAYER for team in teams):
            warn(f"All competitors in {game.NAME} game are robots!")

        # Randomly draw the matchups
        np.random.shuffle(teams)
        teams = self.add_robot_teams(teams, game)
        self.original_draw_names = [team.name for team in teams]
        self.tournament_tree_visualised = False
        self.is_third_playoff = is_third_playoff

        super(KnockoutCompetition, self).__init__(teams, name, game)

        self.rounds = [
            KnockoutCompetitionRound(
                teams,
                get_competition_round_name(self.name, 1, len(self.teams)),
                game,
            )
        ]

    def __repr__(self) -> str:
        return f"Knockout Competition: '{self.name}'"

    @staticmethod
    def add_robot_teams(teams: List[Team], game: Type[HeadToHeadGame]) -> List[Team]:
        num_rounds = math.ceil(math.log2(len(teams)))
        round_size = 2**num_rounds
        num_to_add = round_size - len(teams)
        for count in range(num_to_add):
            # Add non-players in alternate slots (so they aren't next to one another and thus playing each other)
            teams.insert(2 * count + 1, copy(game.ROBOT_PLAYER))

        return teams

    @property
    def live_games(self) -> List[Game]:
        games = []
        for active_round in self.live_rounds:
            games += active_round.games
        return games

    @property
    def live_rounds(self) -> List["KnockoutCompetitionRound"]:
        return [comp_round for comp_round in self.rounds if comp_round.live]

    def complete_round(self) -> bool:
        # Nothing to do if it was the final
        if not self.rounds[-1].name.startswith("Final"):
            if len(self.teams) == 4:
                # If the semi-final has just finished, make another 'round' which is the 3rd/4th playoff
                semi_winners = self.rounds[-1].winners
                semi_losers = self.rounds[-1].losers
                if self.is_third_playoff:  # Plates don't need 3rd/4th playoffs
                    self.rounds.append(
                        KnockoutCompetitionRound(
                            semi_losers,
                            f"3rd/4th Play-Off of {self.name}",
                            self.game,
                        ),
                    )
                self.rounds.append(
                    KnockoutCompetitionRound(
                        semi_winners,
                        get_competition_round_name(self.name, len(self.rounds) + 1, 2),
                        self.game,
                    )
                )
            else:
                # Otherwise, remove all losers
                for comp_round in self.live_rounds:
                    for loser in comp_round.losers:
                        self.teams.remove(loser)

                self.rounds.append(
                    KnockoutCompetitionRound(
                        self.teams,
                        get_competition_round_name(
                            self.name, len(self.rounds) + 1, len(self.teams)
                        ),
                        self.game,
                    )
                )
        for comp_round in self.live_rounds:
            comp_round.live = not comp_round.completed()
            print(comp_round.name, "is", "" if comp_round.live else "not", "live")
        self.tournament_tree_visualised = False
        return True

    def get_team_names(self) -> List[List[str]]:
        team_names = [
            comp_round.team_names
            for comp_round in self.rounds
            if comp_round is not self.third_fourth_playoff
        ]
        while len(team_names[-1]) > 2:
            team_names.append([""] * (len(team_names[-1]) // 2))
        return team_names + [[self.winner.name if self.winner is not None else ""]]

    def get_round_names(self) -> List[str]:
        return [
            comp_round.name
            for comp_round in self.rounds
            if comp_round is not self.third_fourth_playoff
        ]

    @property
    def third_fourth_playoff(self) -> Optional["KnockoutCompetitionRound"]:
        for comp_round in self.rounds:
            if comp_round.name.startswith("3rd/4th Play-Off of"):
                return comp_round
        return None

    @property
    def final(self) -> Optional["KnockoutCompetitionRound"]:
        for comp_round in self.rounds:
            if comp_round.name.startswith("Final"):
                return comp_round
        return None

    @property
    def winner(self) -> Optional[Team]:
        if (
            all(comp_round.completed() for comp_round in self.rounds)
            and self.final is not None
        ):
            return self.final.winners[0]
        elif all(team == self.game.ROBOT_PLAYER for team in self.teams):
            # If only robots are left in the competition, a robot is the winner
            return self.game.ROBOT_PLAYER
        return None

    @property
    def ranking(self) -> Optional[Dict[int, List[Team]]]:
        if self.winner is None:
            return None

        ranking: Dict[int, List[Team]] = {}
        # reversed() so final first, then 3rd/4th playoff, ...
        for comp_round in reversed(self.rounds):
            # Add winners when no rounds follow for winner (e.g. final & 3rd/4th)
            if comp_round in [self.final, self.third_fourth_playoff]:
                teams_added = [team for teams in ranking.values() for team in teams]
                rank = len(teams_added) + 1
                winners = remove_robots(comp_round.winners, self.game.ROBOT_PLAYER)
                # Want to remove copy of a team if a draw occurred & they're in there twice
                ranking[rank] = [
                    w for w in winners if all(w.name not in t.name for t in teams_added)
                ]

            # Add losers from round
            non_robot_losers = remove_robots(comp_round.losers, self.game.ROBOT_PLAYER)
            teams_added = [team for teams in ranking.values() for team in teams]
            rank = len(teams_added) + 1
            # Want to remove copy of a team if a draw occurred & they're in there twice
            non_draw_losers = [
                l
                for l in non_robot_losers
                if all(l.name not in t.name for t in teams_added)
            ]
            ranking[rank] = [t for t in non_draw_losers if t not in teams_added]

        # Remove if teams empty (no teams in a round)
        return {rank: teams for rank, teams in ranking.items() if teams}


class KnockoutCompetitionRound:
    def __init__(self, teams: List[Team], name: str, game: Type[HeadToHeadGame]):
        self.teams = teams
        self.games = [
            game(teams[i], teams[i + 1], name) for i in range(0, len(teams) - 1, 2)
        ]
        self.name = name
        self.robot_v_robot = all(team == game.ROBOT_PLAYER for team in teams)
        self.live = True

    def __repr__(self) -> str:
        return f"Knockout Round: '{self.name}'"

    def completed(self) -> bool:
        return all(
            game.winner is not None or game.both_teams_progressing
            for game in self.games
        )

    @property
    def winners(self) -> List[Team]:
        return [game.winner for game in self.games if game.winner is not None]

    @property
    def losers(self) -> List[Team]:
        return [game.loser for game in self.games if game.loser is not None]

    @property
    def team_names(self) -> List[str]:
        return [team.name for game in self.games for team in game.teams]


def remove_robots(teams: List[Team], robot: Team) -> List[Team]:
    """Removes the robots from a team."""
    return [team for team in teams if team.name != robot.name]


def get_competition_round_name(
    comp_name: str, round_num: int, players_left: int
) -> str:
    return f"{get_round_name(round_num, players_left)} of {comp_name}"


def get_round_name(round_num: int, players_left: int) -> str:
    if players_left == 2:
        return "Final"
    elif players_left == 4:
        return "Semi-Final"
    else:
        th_or_otherwise = (
            "st"
            if round_num == 1
            else "nd" if round_num == 2 else "rd" if round_num == 3 else "th"
        )
        return f"{round_num}{th_or_otherwise} Round"
