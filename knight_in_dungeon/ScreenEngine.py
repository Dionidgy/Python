import pygame
import collections

pygame.init()
user_dim = pygame.display.list_modes()[0][1] // 600
pygame.quit()

colors = {
    "black": (0, 0, 0, 255),
    "white": (255, 255, 255, 255),
    "red": (255, 0, 0, 255),
    "green": (0, 255, 0, 255),
    "blue": (0, 0, 255, 255),
    "wooden": (153, 92, 0, 255),
}

class ScreenHandle(pygame.Surface):

    def __init__(self, *args, **kwargs):
        if len(args) > 1:
            self.successor = args[-1]
            self.next_coord = args[-2]
            args = args[:-2]
        else:
            self.successor = None
            self.next_coord = (0, 0)
        super().__init__(*args, **kwargs)
        self.fill(colors["wooden"])

    def draw(self, canvas):
        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            self.successor.draw(canvas)

    def connect_engine(self, engine):
        if self.successor is not None:
            return self.successor.connect_engine(engine)


class GameSurface(ScreenHandle):

    def connect_engine(self, engine):
        self.game_engine = engine
        if self.successor is not None:
            return self.successor.connect_engine(engine)

    def draw_hero(self):
        self.game_engine.hero.draw(self)

    def draw_map(self):

        min_x = 0
        min_y = 0

        min_x, min_y = self.calculate(min_x, min_y)


        if self.game_engine.map:
            for i in range(len(self.game_engine.map[0]) - min_x):
                for j in range(len(self.game_engine.map) - min_y):
                    self.blit(self.game_engine.map[min_y + j][min_x + i][
                              0], (i * self.game_engine.sprite_size, j * self.game_engine.sprite_size))
        else:
            self.fill(colors["white"])

    def draw_object(self, sprite, coord):
        size = self.game_engine.sprite_size

        min_x = 0
        min_y = 0

        min_x, min_y = self.calculate(min_x, min_y)

        self.blit(sprite, ((coord[0] - min_x) * self.game_engine.sprite_size,
                           (coord[1] - min_y) * self.game_engine.sprite_size))

    def draw(self, canvas):
        size = self.game_engine.sprite_size

        min_x = 0
        min_y = 0

        min_x, min_y = self.calculate(min_x, min_y)

        self.draw_map()
        for obj in self.game_engine.objects:
            self.blit(obj.sprite[0], ((obj.position[0] - min_x) * self.game_engine.sprite_size,
                                      (obj.position[1] - min_y) * self.game_engine.sprite_size))
        self.draw_hero()

        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            return self.successor.draw(canvas)

    def calculate(self, min_x, min_y):
        screen_size = list(self.get_size())
        screen_size[0] /= self.game_engine.sprite_size
        screen_size[1] /= self.game_engine.sprite_size
        hero_pos = self.game_engine.hero.position
        min_x = int(max(0, hero_pos[0] - screen_size[0] + 3))
        min_y = int(max(0, hero_pos[1] - screen_size[1] + 3))
        return (min_x, min_y)


class ProgressBar(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fill(colors["wooden"])

    def connect_engine(self, engine):
        self.engine = engine
        if self.successor is not None:
            return self.successor.connect_engine(engine)

    def draw(self, canvas):
        self.fill(colors["wooden"])
        pygame.draw.rect(self, colors["black"], (user_dim*50, user_dim*30, user_dim*200, user_dim*30), user_dim*2)
        pygame.draw.rect(self, colors["black"], (user_dim*50, user_dim*70, user_dim*200, user_dim*30), user_dim*2)

        pygame.draw.rect(self, colors[
                         "red"], (user_dim*50, user_dim*30, user_dim*200 * self.engine.hero.hp / self.engine.hero.max_hp, user_dim*30))
        pygame.draw.rect(self, colors["green"], (user_dim*50, user_dim*70,
                                                 user_dim*200 * self.engine.hero.exp / (100 * (2**(self.engine.hero.level - 1))), user_dim*30))

        font = pygame.font.SysFont("comicsansms", user_dim*20)
        self.blit(font.render(f'Hero at {self.engine.hero.position}', True, colors["black"]),
                  (user_dim*250, 0))

        self.blit(font.render(f'{self.engine.level} floor', True, colors["black"]),
                  (user_dim*10, 0))

        self.blit(font.render(f'HP', True, colors["black"]),
                  (user_dim*10, user_dim*30))
        self.blit(font.render(f'Exp', True, colors["black"]),
                  (user_dim*10, user_dim*70))

        self.blit(font.render(f'{self.engine.hero.hp}/{self.engine.hero.max_hp}', True, colors["black"]),
                  (user_dim*60, user_dim*30))
        self.blit(font.render(f'{self.engine.hero.exp}/{(100*(2**(self.engine.hero.level-1)))}', True, colors["black"]),
                  (user_dim*60, user_dim*70))

        self.blit(font.render(f'Level', True, colors["black"]),
                  (user_dim*300, user_dim*30))
        self.blit(font.render(f'Gold', True, colors["black"]),
                  (user_dim*300, user_dim*70))

        self.blit(font.render(f'{self.engine.hero.level}', True, colors["black"]),
                  (user_dim*360, user_dim*30))
        self.blit(font.render(f'{self.engine.hero.gold}', True, colors["black"]),
                  (user_dim*360, user_dim*70))

        self.blit(font.render(f'Str', True, colors["black"]),
                  (user_dim*420, user_dim*30))
        self.blit(font.render(f'Luck', True, colors["black"]),
                  (user_dim*420, user_dim*70))

        self.blit(font.render(f'{self.engine.hero.stats["strength"]}', True, colors["black"]),
                  (user_dim*480, user_dim*30))
        self.blit(font.render(f'{self.engine.hero.stats["luck"]}', True, colors["black"]),
                  (user_dim*480, user_dim*70))

        self.blit(font.render(f'SCORE', True, colors["black"]),
                  (user_dim*550, user_dim*30))
        self.blit(font.render(f'{self.engine.score:.4f}', True, colors["black"]),
                  (user_dim*550, user_dim*70))

        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            return self.successor.draw(canvas)


class InfoWindow(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.len = 30
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)

    def update(self, value):
        self.data.append(f"> {str(value)}")

    def draw(self, canvas):
        self.fill(colors["wooden"])
        size = self.get_size()

        font = pygame.font.SysFont("comicsansms", user_dim*20)
        for i, text in enumerate(self.data):
            self.blit(font.render(text, True, colors["black"]),
                      (user_dim*5, user_dim*20 + user_dim*18 * i))

        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            return self.successor.draw(canvas)

    def connect_engine(self, engine):
        self.engine = engine
        engine.subscribe(self)
        if self.successor is not None:
            return self.successor.connect_engine(engine)


class HelpWindow(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.len = 30
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)
        self.data.append([" →", "Move Right"])
        self.data.append([" ←", "Move Left"])
        self.data.append([" ↑ ", "Move Top"])
        self.data.append([" ↓ ", "Move Bottom"])
        self.data.append([" H ", "Show Help"])
        self.data.append(["Num+", "Zoom +"])
        self.data.append(["Num-", "Zoom -"])
        self.data.append([" R ", "Restart Game"])
        self.data.append(["Coursera", "OOP final project"])

    def connect_engine(self, engine):
        self.engine = engine
        if self.successor is not None:
            return self.successor.connect_engine(engine)

    def draw(self, canvas):
        alpha = 0
        if self.engine.show_help:
            alpha = 128
        self.fill((0, 0, 0, alpha))
        size = self.get_size()
        font1 = pygame.font.SysFont("courier", user_dim*24)
        font2 = pygame.font.SysFont("serif", user_dim*24)
        if self.engine.show_help:
            pygame.draw.lines(self, (255, 0, 0, 255), True, [
                              (0, 0), (user_dim*700, 0), (user_dim*700, user_dim*500), (0, user_dim*500)], user_dim*5)
            for i, text in enumerate(self.data):
                self.blit(font1.render(text[0], True, ((128, 128, 255))),
                          (user_dim*50, user_dim*50 + user_dim*30 * i))
                self.blit(font2.render(text[1], True, ((128, 128, 255))),
                          (user_dim*200, user_dim*50 + user_dim*30 * i))

        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            return self.successor.draw(canvas)
