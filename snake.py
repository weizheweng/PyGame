import pygame
import random
import json
from sys import exit

class RPS:
    def __init__(self, game, snake, fruits):
        self.game = game
        self.snake = snake
        self.fruits = fruits  # 接收多個水果的列表
        self.pos = []
        self.spawn()

    def spawn(self):
        # 確保 RPS 點不與蛇的身體和所有水果的位置重疊
        valid_position = False
        while not valid_position:
            x = random.randrange(0, self.game.canvas_x, self.game.unit)
            y = random.randrange(0, self.game.canvas_y, self.game.unit)
            self.pos = [x, y]

            # 檢查位置是否與蛇身體重疊
            is_not_on_snake = all(self.pos != body for body in self.snake.body)

            # 檢查位置是否與任何水果的點重疊
            is_not_on_fruit = all(
                self.pos != fruit_pos for fruit in self.fruits for fruit_pos in fruit.pos
            )

            # 只有當兩者都有效時，才接受這個位置
            valid_position = is_not_on_snake and is_not_on_fruit

class Text:
    def __init__(self, game, txt, size, color, font):
        self.game = game
        font = pygame.font.SysFont(font, size)
        self.surface = font.render(txt, True, color)
        self.rect = self.surface.get_rect()

    def midleft(self, x, y):
        self.rect.midleft = (x, y)
        self.game.window.blit(self.surface, self.rect)
        
class Game:
    def __init__(self):
        # 遊戲設定
        self.canvas_x = 720
        self.canvas_y = 630
        self.unit = 30
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
        self.mini_game = pygame.image.load("resources/mini_game.png").convert_alpha()
        # 音效
        pygame.mixer.init()
        self.bgm = pygame.mixer.Sound("resources/bgm.wav")
        self.fruit_sfx = pygame.mixer.Sound("resources/fruit.wav")
        self.game_over_sfx = pygame.mixer.Sound("resources/game_over.wav")
        self.bgm.play(-1)
        # 暫停
        self.paused = False
        # 重新開始
        self.restart = False
        # 關閉
        self.quit = False
        
    def toggle_pause(self):
        """切換暫停狀態"""
        self.paused = not self.paused
        
    def toggle_restart(self):
        """切換重新開始狀態"""
        self.restart = not self.restart
        
    def toggle_quit(self):
        """切換關閉狀態"""
        self.quit = not self.quit

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
        self.score = 0  # 初始化分數屬性
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
                self.score = 15  # size 1 的水果得 15 分
            elif self.size == 2:
                # 水平或垂直的兩個unit
                if random.choice([True, False]):  # 隨機決定是水平方向還是垂直方向
                    # 確保水平水果不會超過邊界
                    if base_x + self.game.unit < self.game.canvas_x:
                        self.pos = [[base_x, base_y], [base_x + self.game.unit, base_y]]
                        self.score = 10  # size 2 的水果得 10 分
                    else:
                        continue  # 超過邊界就重新生成
                else:
                    # 確保垂直水果不會超過邊界
                    if base_y + self.game.unit < self.game.canvas_y:
                        self.pos = [[base_x, base_y], [base_x, base_y + self.game.unit]]
                        self.score = 10  # size 2 的水果得 10 分
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
                    self.score = 5  # size 4 的水果得 5 分
                else:
                    continue  # 超過邊界就重新生成

            # 檢查水果是否與蛇身體重疊
            valid_position = True
            for body in self.snake.body:  # 使用snake物件中的body
                if any(pos == body for pos in self.pos):  # 檢查水果的每個位置是否與蛇身體重疊
                    valid_position = False  # 如果水果與蛇身體重疊，標記為無效位置，並重新生成
                    break

def rps_game(game, color):
    choices = ["Rock", "Paper", "Scissors"]
    player_choice = None
    com_choice = random.choice(choices)

    # 繪製 RPS 選擇界面
    while player_choice is None:
        game.window.fill(color.black)
        Text(game, "Choose: [R] ock, [P] aper, [S] cissors", 40, color.white, "impact").midleft(100, 300)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    player_choice = "Rock"
                elif event.key == pygame.K_p:
                    player_choice = "Paper"
                elif event.key == pygame.K_s:
                    player_choice = "Scissors"

    # 判斷結果
    if player_choice == com_choice:
        result = "Draw"
        score_change = 0
    elif (player_choice == "Rock" and com_choice == "Scissors") or \
         (player_choice == "Paper" and com_choice == "Rock") or \
         (player_choice == "Scissors" and com_choice == "Paper"):
        result = "You Win! (+10)"
        score_change = 10
    else:
        result = "You Lose! (-2)"
        score_change = -2

    # 倒數計時顯示
    countdown_time = 5  # 倒數 5 秒
    start_time = pygame.time.get_ticks()  # 紀錄開始時間

    while True:
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # 計算經過的時間
        remaining_time = max(0, countdown_time - elapsed_time)  # 計算剩餘時間

        # 更新畫面
        game.window.fill((0, 0, 0))
        Text(game, f"You chose {player_choice}, AI chose {com_choice}.", 40, color.white, "impact").midleft(100, 300)
        Text(game, result, 50, color.red if score_change < 0 else color.green, "impact").midleft(100, 400)
        Text(game, f"Returning in {int(remaining_time)} seconds...", 30, color.white, "impact").midleft(100, 500)
        pygame.display.update()

        # 倒數結束後退出
        if remaining_time <= 0:
            break

    return score_change

def handle_key_events(game, snake, score):
    """處理方向按鍵事件"""
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
                
            # 暫停/繼續遊戲
            elif event.key == pygame.K_k:
                game.toggle_pause()
            
            # 離開遊戲並儲存狀態
            elif event.key == pygame.K_f:
               game.toggle_quit()

            # 重新開始遊戲
            elif event.key == pygame.K_r:
                game.toggle_restart()

def update_snake_direction(snake):
    """更新蛇的移動方向，避免掉頭"""
    if snake.new_direction == "RIGHT" and snake.direction != "LEFT":
        snake.direction = "RIGHT"
    elif snake.new_direction == "LEFT" and snake.direction != "RIGHT":
        snake.direction = "LEFT"
    elif snake.new_direction == "DOWN" and snake.direction != "UP":
        snake.direction = "DOWN"
    elif snake.new_direction == "UP" and snake.direction != "DOWN":
        snake.direction = "UP"

def move_snake(snake, unit):
    """依據方向移動蛇"""
    if snake.direction == "RIGHT":
        snake.head[0] += unit
    elif snake.direction == "LEFT":
        snake.head[0] -= unit
    elif snake.direction == "DOWN":
        snake.head[1] += unit
    elif snake.direction == "UP":
        snake.head[1] -= unit

def save_score_to_json(score, file_path="game_state.json"):
    data = {"score": score}
    with open(file_path, "w") as file:
        json.dump(data, file)

def load_score_from_json(file_path="game_state.json"):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            return data.get("score", 0)  # 如果沒有找到分數，預設為 0
    except FileNotFoundError:
        return 0

def display_pause_message(game, color):
    # 創建暫停與繼續文字
    pause_text = Text(game, "Paused", 48, color=color.white, font="impact")
    continue_text = Text(game, "Press 'K' to continue", 32, color=color.white, font="impact")

    # 計算文字的顯示位置，讓它們在畫面中央
    pause_text.midleft(game.canvas_x // 2 - pause_text.rect.width // 2, game.canvas_y // 2 - 40)
    continue_text.midleft(game.canvas_x // 2 - continue_text.rect.width // 2, game.canvas_y // 2 + 10)

    # 更新畫面
    pygame.display.flip()
    
def display_restart_message(game, color):
    # 創建暫停與繼續文字
    pause_text = Text(game, "Restarting...", 48, color=color.white, font="impact")
    continue_text = Text(game, "Press 'R' to restart", 32, color=color.white, font="impact")

    # 計算文字的顯示位置，讓它們在畫面中央
    pause_text.midleft(game.canvas_x // 2 - pause_text.rect.width // 2, game.canvas_y // 2 - 40)
    continue_text.midleft(game.canvas_x // 2 - continue_text.rect.width // 2, game.canvas_y // 2 + 10)

    # 更新畫面
    pygame.display.flip()
    
    # 等待玩家按下 'R' 鍵來重新開始
    waiting_for_restart = True
    while waiting_for_restart:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # 按下 'R' 鍵重新開始
                    waiting_for_restart = False
                    break  

def display_quit_message(game, color):
    # 創建暫停與繼續文字
    pause_text = Text(game, "Quitting...", 48, color=color.white, font="impact")
    continue_text = Text(game, "Press 'F' to quit", 32, color=color.white, font="impact")

    # 計算文字的顯示位置，讓它們在畫面中央
    pause_text.midleft(game.canvas_x // 2 - pause_text.rect.width // 2, game.canvas_y // 2 - 40)
    continue_text.midleft(game.canvas_x // 2 - continue_text.rect.width // 2, game.canvas_y // 2 + 10)

    # 更新畫面
    pygame.display.flip()
    
    # 等待玩家按下 'F' 鍵來關閉
    waiting_for_quit = True
    while waiting_for_quit:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    waiting_for_quit = False
                    break  

def play_game(game, color):
    score = load_score_from_json()
    base_speed = 10  # 初始速度
    max_speed = 30   # 最大速度限制
    speed_increment = 2  # 每次提升速度的增量
    points_per_speed_increase = 100  # 每 100 分提升一次速度

    game_speed = base_speed
    snake = Snake(game, color)  # 新增 Snake 點
    fruits = [  # 新增 Fruit 點
        Fruit(game, snake, size=1),
        Fruit(game, snake, size=1),  
        Fruit(game, snake, size=1),  
        Fruit(game, snake, size=2),  
        Fruit(game, snake, size=2),
        Fruit(game, snake, size=4),
    ]
    
    rps = RPS(game, snake, fruits)  # 新增 RPS 點

    # 遊戲邏輯循環
    while True:
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < 1000 // game_speed:
            pygame.event.pump()

        # 處理事件
        handle_key_events(game, snake, score)
        
        if game.paused:
            display_pause_message(game, color)
            continue  # 跳過當前循環，保持暫停狀態
        
        if game.restart:
            display_restart_message(game, color)
            break  # 終止遊戲
        
        if game.quit:
            display_quit_message(game, color)
            save_score_to_json(score)
            pygame.quit()
            exit()
        
        # 更新蛇的方向
        update_snake_direction(snake)

        # 移動蛇
        move_snake(snake, game.unit)

        snake.body.insert(0, list(snake.head))

        # 判斷蛇是否吃到水果
        if any(snake.head == pos for fruit in fruits for pos in fruit.pos):
            game.fruit_sfx.play()  # 播放水果音效
            for fruit in fruits:
                if snake.head in fruit.pos:
                    fruit.spawn()
                    score += fruit.score
        # 判斷蛇是否吃到 RPS 點
        elif snake.head == rps.pos:
            score_change = rps_game(game, color)
            score += score_change
            rps.spawn()  # 重新生成 RPS 點
        else:
            snake.body.pop()
        
        # 提高速度
        if score % points_per_speed_increase == 0:  # 每累積特定分數
            game_speed = min(max_speed, base_speed + (score // points_per_speed_increase) * speed_increment)

        # 判斷是否碰撞牆壁或自己
        if not (0 <= snake.head[0] < game.canvas_x) or not (0 <= snake.head[1] < game.canvas_y) or snake.head in snake.body[1:]:
            break

        # 繪製遊戲畫面
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
                temp_color = color.red if fruit.size == 1 else color.blue if fruit.size == 2 else color.grey
                pygame.draw.rect(game.canvas, temp_color, (pos[0], pos[1], game.unit - 4, game.unit - 4), 0, 3)
                
        # 畫 RPS 點
        icon = pygame.transform.scale(game.mini_game, (game.unit, game.unit))
        game.canvas.blit(icon, (rps.pos[0], rps.pos[1]))

        game.window.blit(game.border, (0, 0))
        game.window.blit(game.canvas, (30, 120))
        Text(game, f"Score: {score}", 45, color.white, "impact").midleft(90, 45)

        pygame.display.update()

def main():
    pygame.init()  # 只初始化一次
    game = Game()
    color = Color()

    while True:  # 外層循環，控制多輪遊戲
        # 顯示開始畫面
        game.restart = False
        game.window.fill(color.black)  # 使用黑色背景清屏
        start_text = Text(game, "Press ENTER to start", 40, color.white, "impact")
        text_width = start_text.rect.width
        start_text.midleft(game.canvas_x // 2 - text_width // 2, game.canvas_y // 2)
        pygame.display.update()

        waiting_for_start = True
        while waiting_for_start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting_for_start = False

        # 開始遊戲
        play_game(game, color)

        if game.restart:
            continue
            
        # 顯示遊戲結束畫面
        game.game_over_sfx.play()
        game.window.fill((0, 0, 0))  # 使用黑色背景代替關閉視窗
        game.window.blit(game.game_over, (0, 0))  # 顯示遊戲結束畫面
        pygame.display.update()

        # 等待按下 Enter 鍵重新開始
        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting_for_restart = False

if __name__ == "__main__":
    main()