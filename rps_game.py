import pygame
import random

# 初始化 Pygame
pygame.init()

# 畫布大小和顏色
WIDTH, HEIGHT = 600, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 設定 Pygame 視窗
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock-Paper-Scissors Game")

# 字型設定
font = pygame.font.Font(None, 36)
result_font = pygame.font.Font(None, 48)

# 圖片載入
rock_img = pygame.image.load("resources/mini_game/rock.png")

paper_img = pygame.image.load("resources/mini_game/paper.png")
scissors_img = pygame.image.load("resources/mini_game/scissors.png")

# 圖片縮放
rock_img = pygame.transform.scale(rock_img, (100, 100))
paper_img = pygame.transform.scale(paper_img, (100, 100))
scissors_img = pygame.transform.scale(scissors_img, (120, 120))

# 玩家與電腦選項
options = ["rock", "paper", "scissors"]
images = {"rock": rock_img, "paper": paper_img, "scissors": scissors_img}

# 遊戲狀態
score = 0
game_result = ""
computer_choice = None  # 電腦的選擇圖案初始化

# 判斷勝負邏輯
def determine_winner(player_choice, computer_choice):
    if player_choice == computer_choice:
        return "Draw"
    elif (player_choice == "rock" and computer_choice == "scissors") or \
         (player_choice == "paper" and computer_choice == "rock") or \
         (player_choice == "scissors" and computer_choice == "paper"):
        return "Win"
    else:
        return "Lose"

# 主遊戲循環
running = True
while running:
    screen.fill(WHITE)
    
    # 顯示分數
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    
    # 顯示遊戲結果
    result_text = result_font.render(game_result, True, BLACK)
    screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, 50))
    
    # 顯示玩家選項
    screen.blit(rock_img, (100, HEIGHT - 150))
    screen.blit(paper_img, (250, HEIGHT - 150))
    screen.blit(scissors_img, (400, HEIGHT - 150))
    
    # 顯示提示文字
    prompt_text = font.render("Choose: Rock, Paper, or Scissors", True, BLACK)
    screen.blit(prompt_text, (WIDTH // 2 - prompt_text.get_width() // 2, HEIGHT - 200))
    
    # 顯示電腦選擇（若有）
    if computer_choice:
        computer_text = font.render("Computer chose:", True, BLACK)
        screen.blit(computer_text, (WIDTH // 2 - computer_text.get_width() // 2, 120))
        screen.blit(images[computer_choice], (WIDTH // 2 - 50, 150))  # 電腦選擇圖案置中顯示
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 獲取玩家選擇
            mouse_x, mouse_y = event.pos
            if 100 < mouse_x < 200 and HEIGHT - 150 < mouse_y < HEIGHT - 50:
                player_choice = "rock"
            elif 250 < mouse_x < 350 and HEIGHT - 150 < mouse_y < HEIGHT - 50:
                player_choice = "paper"
            elif 400 < mouse_x < 500 and HEIGHT - 150 < mouse_y < HEIGHT - 50:
                player_choice = "scissors"
            else:
                player_choice = None
            
            if player_choice:
                # 電腦隨機選擇
                computer_choice = random.choice(options)
                result = determine_winner(player_choice, computer_choice)
                
                # 更新結果和分數
                if result == "Win":
                    game_result = f"You Win! ({player_choice} vs {computer_choice})"
                    score += 10
                elif result == "Lose":
                    game_result = f"You Lose! ({player_choice} vs {computer_choice})"
                    score -= 2
                else:
                    game_result = f"Tie! ({player_choice} vs {computer_choice})"

    pygame.display.flip()

# 結束遊戲
pygame.quit()