import time

import pygame

from competition_controller import CompetitionController
from observation import Observer


def play_competition(controller: CompetitionController, view: Observer) -> None:

    podia_shown, games_shown = False, False
    clock = pygame.time.Clock()
    pygame_running = True
    rules_shown = False
    while pygame_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame_running = False
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if not rules_shown:
                    view.show_rules()
                    rules_shown = True
                    continue
                if controller.current_round_over():
                    if not controller.competitions_over:
                        print("New round")
                        controller.new_round()

                    elif not podia_shown:
                        print("Showing podia")
                        view.draw_podium_and_leaderboard(controller.ranking)
                        podia_shown = True
                    else:
                        pygame_running = False
                        break
                else:
                    comp_to_draw = controller.get_competition_to_draw()
                    if comp_to_draw is not None:
                        view.draw_knockout_tournament_tree(comp_to_draw)
                        games_shown = False
                    elif not games_shown:
                        view.draw_all_games()
                        games_shown = True
                    else:
                        print("Running games")
                        controller.run_round_of_games()
                clock.tick(30)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                view.draw_all_games()

    pygame.quit()
