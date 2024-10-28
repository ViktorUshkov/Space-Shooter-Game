import pygame
from os.path import join
from settings import Settings

class Stats:
    BASE_DODGE_AWARD = 1
    BASE_DESTROY_AWARD = 5
    LVL_UP_MULTIPLIER = 1.5
    POINTS_TO_LVL_UP = 100

    def __init__(self) -> None:
        self.score = None
        self.dodge_meteor_award = None
        self.destroy_meteor_award = None
        self.reset_score()
        self.level = 1
        self.multiplier = self.LVL_UP_MULTIPLIER
        self.points_to_level_up = self.POINTS_TO_LVL_UP

    def reset_score(self) -> None:
        self.score = 0
        self.dodge_meteor_award = self.BASE_DODGE_AWARD
        self.destroy_meteor_award = self.BASE_DESTROY_AWARD

    def _increase_award(self) -> None:
        self.level += 1
        self.destroy_meteor_award *= self.multiplier
        self.dodge_meteor_award *= self.multiplier
        self.points_to_level_up += self.points_to_level_up * self.multiplier

    def check_level_up(self) -> bool:
        if self.score >= self.points_to_level_up:
            self._increase_award()
            return True
        return False


class Scoreboard:
    def __init__(self, screen: pygame.Surface, stats: Stats) -> None:
        self.screen = screen
        self.screen_rect = screen.get_frect()
        self.stats = stats
        self.font = pygame.font.Font(join('assets','font','Oxanium-Bold.ttf'), 36)
        self.fontcolor = (200, 200, 200)

    def show_scoreboard(self) -> None:
        score_surface = self.font.render(f'SCORE: {round(self.stats.score)}', True, self.fontcolor)
        score_rect = score_surface.get_frect(midtop=self.screen_rect.midtop)
        self.screen.blit(score_surface, score_rect)

        level_surface = self.font.render(f'LEVEL: {round(self.stats.level)}', True, self.fontcolor)
        level_rect = level_surface.get_frect(topleft=self.screen_rect.topleft)
        self.screen.blit(level_surface, level_rect)

        target_surface = self.font.render(f'TARGET: {round(self.stats.points_to_level_up)}', True, self.fontcolor)
        target_rect = target_surface.get_frect(topleft=level_rect.bottomleft)
        self.screen.blit(target_surface, target_rect)


class Message:
    def __init__(self, screen: pygame.Surface, stats: Stats) -> None:
        self.screen = screen
        self.screen_rect = screen.get_frect()
        self.stats = stats
        self.color = (255, 255, 255)
        self.font = pygame.font.Font(join('assets','font','Oxanium-Bold.ttf'), 40)
        self.fontcolor = (0, 0, 0)
        self.width = self.screen_rect.width / 2 + 200
        self.height = self.screen_rect.height - 300
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.continue_rect = None
        self.end_game_rect = None

    def show_message(self) -> None:
        pygame.draw.rect(self.screen, self.color, self.rect, border_radius=30)
        pygame.draw.rect(self.screen, self.fontcolor, self.rect, width=5, border_radius=30)

        you_lost_surface = self.font.render(f'YOU DIED', True, self.fontcolor)
        you_lost_rect = you_lost_surface.get_frect(midtop=(self.rect.midtop[0], self.rect.midtop[1] + 30))
        self.screen.blit(you_lost_surface, you_lost_rect)

        final_score_surface = self.font.render(f'YOUR FINAL SCORE IS {round(self.stats.score)}', True, self.fontcolor)
        final_score_rect = final_score_surface.get_frect(midtop=you_lost_rect.midbottom)
        self.screen.blit(final_score_surface, final_score_rect)

        replay_surface = self.font.render(f'WANT TO PLAY AGAIN?', True, self.fontcolor)
        replay_rect = replay_surface.get_frect(midtop=final_score_rect.midbottom)
        self.screen.blit(replay_surface, replay_rect)

        continue_surface = self.font.render(f'YES', True, 'green')
        self.continue_rect = continue_surface.get_frect(bottomleft=(self.rect.bottomleft[0] + 150, self.rect.bottomleft[1] - 50))
        self.screen.blit(continue_surface, self.continue_rect)

        end_game_surface = self.font.render(f'NO', True, 'red')
        self.end_game_rect = end_game_surface.get_frect(bottomright=(self.rect.bottomright[0] - 150, self.rect.bottomright[1] - 50))
        self.screen.blit(end_game_surface, self.end_game_rect)