import sys
import pygame
from os.path import join
from settings import Settings
from ship import Ship
from meteor import Meteor
from interface import Scoreboard, Stats, Message
from explosion import Explosion

class SpaceShooter:
    def __init__(self) -> None:
        pygame.init()
        self.settings = Settings()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_frect()
        self.background = pygame.image.load(join('assets','background.png')).convert_alpha()
        self.background = pygame.transform.scale(self.background,
                                                 (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Space Shooter")
        self.sprites = pygame.sprite.Group()
        self.meteor_sprites = pygame.sprite.Group()
        self.laser_sprites = pygame.sprite.Group()
        self._register_meteor_event()
        self.settings.create_surfaces()
        self.settings.import_sounds()
        self._new_game()

        self.ship_collided = False
        self.running = True

    def _new_game(self) -> None:
        self.settings.game_music.play(loops=-1)
        self.stats = Stats()
        self.scoreboard = Scoreboard(self.screen, self.stats)
        self.ship = Ship(self.screen, self.settings, self.sprites, self.laser_sprites)
        Meteor(self.screen, self.settings.meteor_surface, self.settings, self.stats, (self.sprites, self.meteor_sprites))
        self.settings.meteor_speed = self.settings.DEFAULT_METEOR_SPEED

    def _register_meteor_event(self) -> None:
        self.METEOR_EVENT = pygame.event.custom_type()
        pygame.time.set_timer(self.METEOR_EVENT, 500)

    def _check_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._process_keydowns(event)
            elif event.type == pygame.KEYUP:
                self._process_keyups(event)
            elif event.type == self.METEOR_EVENT and not self.ship_collided:
                Meteor(self.screen, self.settings.meteor_surface, self.settings, self.stats, (self.sprites, self.meteor_sprites))

    def _process_keydowns(self, event: pygame.event) -> None:
        if event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_ESCAPE:
            self.running = False

    def _process_keyups(self, event: pygame.event) -> None:
        if event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

    def _clear_sprites(self) -> None:
        self.sprites.empty()
        self.meteor_sprites.empty()
        self.laser_sprites.empty()

    def _end_of_game_options(self) -> None:
        self.settings.game_music.stop()
        self._clear_sprites()
        msg = Message(self.screen, self.stats)
        msg.show_message()
        if pygame.mouse.get_just_pressed()[0]:
            click_pos = pygame.mouse.get_pos()
            if msg.continue_rect.collidepoint(click_pos):
                self.ship_collided = False
                self._new_game()
            elif msg.end_game_rect.collidepoint(click_pos):
                self.running = False

    def _update_window(self) -> None:
        self.screen.blit(self.background, (0, 0))
        if self.ship_collided:
            self._end_of_game_options()
        else:
            self.sprites.draw(self.screen)
            self.scoreboard.show_scoreboard()
        pygame.display.flip()

    def _check_collisions(self) -> None:
        if pygame.sprite.spritecollide(self.ship, self.meteor_sprites, True, pygame.sprite.collide_mask):
            self.ship_collided = True

        for laser in self.laser_sprites:
            laser_hits = pygame.sprite.spritecollide(laser, self.meteor_sprites, True, pygame.sprite.collide_mask)
            if laser_hits:
                laser.kill()
                self.stats.score += self.stats.destroy_meteor_award * len(laser_hits)
                Explosion(self.settings.explosion_frames, laser.rect.midright, self.screen, self.sprites)
                self.settings.explosion_sound.play()

    def run_game(self) -> None:
        while self.running:
            dt = self.clock.tick(120) / 1000
            self._check_events()
            self.sprites.update(dt)
            self._check_collisions()
            if self.stats.check_level_up():
                self.settings.meteor_speed += 50
            self._update_window()

if __name__ == '__main__':
    game = SpaceShooter()
    game.run_game()
    pygame.quit()
    sys.exit()
