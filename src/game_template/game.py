from competitor_code.game_mechanics import TemplateMechanics
from game_parent import HeadToHeadGame, PointsGame


class GameTemplate(TemplateMechanics, PointsGame):
    """Inherit from PointsGame or HeadToHeadGame."""

    pass
