import pygame
import random
from sys import exit


class Game:
    def __init__(self):
        # 遊戲設定
        self.canvas_x = 720
        self.canvas_y = 630
        self.unit = 30
        self.game_speed = 10
        # 初始化 Pygame
        pygame.init()
        self.window = pygame.display.set_mode((780, 780))
        pygame.display.set_caption("貪食蛇")
        self.canvas = pygame.Surface((self.canvas_x, self.canvas_y))
        # 載入資源
        self.background = pygame.image.load("resources/background.png").convert()
        self.border = pygame.image.load("resources/border.png").convert()
        self.face = pygame.image.load("resources/face.png").convert_alpha()
        self.game_over = pygame.image.load("resources/game_over.png").convert_alpha()
        # 音效
        pygame.mixer.init()
        self.bgm = pygame.mixer.Sound("resources/bgm.wav")
        self.fruit_sfx = pygame.mixer.Sound("resources/fruit.wav")
        self.game_over_sfx = pygame.mixer.Sound("resources/game_over.wav")
        self.bgm.play(-1)

class Color:
    def __init__(self):
        self.black = (0, 0, 0)
        self.grey = (85, 85, 85)
        self.white = (255, 255, 255)
        self.red = (229, 46, 8)
        self.darkRed = (157, 31, 6)
        self.green = (64, 201, 73)
        self.darkGreen = (36, 127, 42)

class Text:
    def __init__(self, game, txt, size, color, font):
        self.game = game
        font = pygame.font.SysFont(font, size)
        self.surface = font.render(txt, True, color)
        self.rect = self.surface.get_rect()

    def midleft(self, x, y):
        self.rect.midleft = (x, y)
        self.game.window.blit(self.surface, self.rect)


class Snake:
    def __init__(self, game, color):
        self.game = game
        self.color1 = color.green
        self.color2 = color.darkGreen
        self.head = [0, 0]
        self.body = [self.head]
        self.direction = "RIGHT"
        self.new_direction = "RIGHT"
        length = 4
        for i in range(length - 1):
            self.head[0] += game.unit
            self.body.insert(0, list(self.head))


class Fruit:
    def __init__(self, game):
        self.game = game
        self.pos = [0, 0]
        self.spawn()

    def spawn(self):
        self.pos = [
            random.randrange(0, self.game.canvas_x, self.game.unit),
            random.randrange(0, self.game.canvas_y, self.game.unit),
        ]


def main():
    game = Game()
    while True:
        score = 0
        color = Color()
        snake = Snake(game, color)
        fruit = Fruit(game)

        while True:
            start_time = pygame.time.get_ticks()
            while pygame.time.get_ticks() - start_time < 1000 // game.game_speed:
                pygame.event.pump()

            # 偵測鍵盤事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_d, pygame.K_RIGHT]:
                        snake.new_direction = "RIGHT"
                    elif event.key in [pygame.K_a, pygame.K_LEFT]:
                        snake.new_direction = "LEFT"
                    elif event.key in [pygame.K_s, pygame.K_DOWN]:
                        snake.new_direction = "DOWN"
                    elif event.key in [pygame.K_w, pygame.K_UP]:
                        snake.new_direction = "UP"
                        
            # 判斷轉彎方向是否合理
            if snake.new_direction == "RIGHT" and snake.direction != "LEFT":
                snake.direction = "RIGHT"
            elif snake.new_direction == "LEFT" and snake.direction != "RIGHT":
                snake.direction = "LEFT"
            elif snake.new_direction == "DOWN" and snake.direction != "UP":
                snake.direction = "DOWN"
            elif snake.new_direction == "UP" and snake.direction != "DOWN":
                snake.direction = "UP"

            if snake.direction == "RIGHT":
                snake.head[0] += game.unit
            elif snake.direction == "LEFT":
                snake.head[0] -= game.unit
            elif snake.direction == "DOWN":
                snake.head[1] += game.unit
            elif snake.direction == "UP":
                snake.head[1] -= game.unit

            snake.body.insert(0, list(snake.head))

            if snake.head == fruit.pos:
                game.fruit_sfx.play()
                fruit.spawn()
                score += 1
            else:
                snake.body.pop()
                
            # 碰撞判定
            if not (0 <= snake.head[0] < game.canvas_x):
                break
            if not (0 <= snake.head[1] < game.canvas_y):
                break
            if snake.head in snake.body[1:]:
                break

            game.canvas.blit(game.background, (0, 0))
            
            pygame.draw.rect(game.canvas, color.grey, (snake.head[0], snake.head[1], game.unit + 2, game.unit + 2))
            for body in snake.body[1:]:
                pygame.draw.rect(game.canvas, color.grey, (body[0], body[1], game.unit + 2, game.unit + 2))
                
            pygame.draw.rect(game.canvas, snake.color1, (snake.head[0] - 1, snake.head[1] - 1, game.unit + 2, game.unit + 2))
            pygame.draw.rect(game.canvas, snake.color2, (snake.head[0] - 1, snake.head[1] - 1, game.unit + 2, game.unit + 2), 2)

            for body in snake.body[1:]:
                pygame.draw.rect(game.canvas, snake.color1, (body[0], body[1], game.unit, game.unit))
                pygame.draw.rect(game.canvas, snake.color2, (body[0], body[1], game.unit, game.unit), 2)

            game.canvas.blit(game.face, snake.head)

            pygame.draw.rect(game.canvas, color.grey, (fruit.pos[0] + 3, fruit.pos[1] + 3, game.unit - 4, game.unit - 4), 0, 3)
            pygame.draw.rect(game.canvas, color.red, (fruit.pos[0] + 2, fruit.pos[1] + 2, game.unit - 4, game.unit - 4), 0, 3)
            pygame.draw.rect(game.canvas, color.darkRed, (fruit.pos[0] + 2, fruit.pos[1] + 2, game.unit - 4, game.unit - 4), 2, 3)

            game.window.blit(game.border, (0, 0))
            game.window.blit(game.canvas, (30, 120))
            Text(game, str(score), 45, color.white, "impact").midleft(90, 45)

            pygame.display.update()

        game.game_over_sfx.play()
        game.window.blit(game.game_over, (0, 0))
        pygame.display.update()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False


if __name__ == "__main__":
    main()
