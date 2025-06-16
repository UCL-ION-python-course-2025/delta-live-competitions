from game_parent import Game
from observation import Observer


class TemplateTournament(Observer):
    """Templating an ABC is slightly weird."""

    def draw_game(self, game: Game) -> None:
        pass

    def draw_win_message(self, game: Game) -> None:
        """Displays win message on top of the board."""
        pass
