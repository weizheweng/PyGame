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
        self.blue = (0, 0, 255)
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
    def __init__(self, game, snake, size=1):
        self.game = game
        self.snake = snake  # 這裡接收並儲存snake物件
        self.size = size  # 水果的大小
        self.pos = []
        self.spawn()

    def spawn(self):
        # 確保水果不與蛇的身體重疊，且不會超過畫布的邊界
        valid_position = False
        while not valid_position:
            base_x = random.randrange(0, self.game.canvas_x, self.game.unit)  # 隨機生成水果的起始位置
            base_y = random.randrange(0, self.game.canvas_y, self.game.unit)
            
            # 根據水果大小來確保位置不會超過邊界
            if self.size == 1:
                self.pos = [[base_x, base_y]]  # 預設水果為一個unit
            elif self.size == 2:
                # 水平或垂直的兩個unit
                if random.choice([True, False]):  # 隨機決定是水平方向還是垂直方向
                    # 確保水平水果不會超過邊界
                    if base_x + self.game.unit < self.game.canvas_x:
                        self.pos = [[base_x, base_y], [base_x + self.game.unit, base_y]]
                    else:
                        continue  # 超過邊界就重新生成
                else:
                    # 確保垂直水果不會超過邊界
                    if base_y + self.game.unit < self.game.canvas_y:
                        self.pos = [[base_x, base_y], [base_x, base_y + self.game.unit]]
                    else:
                        continue  # 超過邊界就重新生成
            elif self.size == 4:
                # 四個unit組成的正方形
                if (base_x + self.game.unit < self.game.canvas_x and 
                    base_y + self.game.unit < self.game.canvas_y):
                    self.pos = [
                        [base_x, base_y],
                        [base_x + self.game.unit, base_y],
                        [base_x, base_y + self.game.unit],
                        [base_x + self.game.unit, base_y + self.game.unit],
                    ]
                else:
                    continue  # 超過邊界就重新生成

            # 檢查水果是否與蛇身體重疊
            valid_position = True
            for body in self.snake.body:  # 使用snake物件中的body
                if any(pos == body for pos in self.pos):  # 檢查水果的每個位置是否與蛇身體重疊
                    valid_position = False  # 如果水果與蛇身體重疊，標記為無效位置，並重新生成
                    break




def main():
    game = Game()  # 創建遊戲對象
    color = Color()  # 創建顏色對象
    score = 0  # 初始化分數
    snake = Snake(game, color)  # 創建蛇對象
    fruits = [
        Fruit(game, snake, size=1),  # 一個unit的水果
        Fruit(game, snake, size=1),  
        Fruit(game, snake, size=1),  
        Fruit(game, snake, size=2),  # 兩個水平或垂直unit的水果
        Fruit(game, snake, size=2),  
        Fruit(game, snake, size=4),  # 四個unit的正方形水果
    ]

    while True:
        start_time = pygame.time.get_ticks()  # 記錄時間，用於控制遊戲速度
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

        # 判斷蛇是否吃到水果
        if any(snake.head == pos for fruit in fruits for pos in fruit.pos):
            game.fruit_sfx.play()
            for fruit in fruits:
                if snake.head in fruit.pos:  # 如果蛇的頭部位置碰到水果的任何位置
                    fruit.spawn()  # 生成新的水果
                    score += 1  # 分數加1
        else:
            snake.body.pop()

        # 判斷是否碰撞牆壁或自己
        if not (0 <= snake.head[0] < game.canvas_x):
            break
        if not (0 <= snake.head[1] < game.canvas_y):
            break
        if snake.head in snake.body[1:]:
            break

        game.canvas.blit(game.background, (0, 0))

        # 畫蛇
        pygame.draw.rect(game.canvas, color.grey, (snake.head[0], snake.head[1], game.unit + 2, game.unit + 2))
        for body in snake.body[1:]:
            pygame.draw.rect(game.canvas, color.grey, (body[0], body[1], game.unit + 2, game.unit + 2))

        pygame.draw.rect(game.canvas, snake.color1, (snake.head[0] - 1, snake.head[1] - 1, game.unit + 2, game.unit + 2))
        pygame.draw.rect(game.canvas, snake.color2, (snake.head[0] - 1, snake.head[1] - 1, game.unit + 2, game.unit + 2), 2)

        for body in snake.body[1:]:
            pygame.draw.rect(game.canvas, snake.color1, (body[0], body[1], game.unit, game.unit))
            pygame.draw.rect(game.canvas, snake.color2, (body[0], body[1], game.unit, game.unit), 2)

        game.canvas.blit(game.face, snake.head)

        # 畫水果
        for fruit in fruits:
            for pos in fruit.pos:
                if fruit.size == 1:
                    temp_color = color.red  # 紅色
                elif fruit.size == 2:
                    temp_color = color.blue  # 藍色
                elif fruit.size == 4:
                    temp_color = color.grey  # 灰色
                pygame.draw.rect(game.canvas, temp_color, (pos[0], pos[1], game.unit - 4, game.unit - 4), 0, 3)

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
