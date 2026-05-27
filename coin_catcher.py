import pygame
import random
import sys

# =========================
# 初始化
# =========================
pygame.init()

WIDTH = 800
HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("接金幣遊戲")

clock = pygame.time.Clock()

# =========================
# 顏色
# =========================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (90, 170, 255)
GOLD = (255, 215, 0)
ORANGE = (255, 165, 0)
BROWN = (150, 80, 30)
GRAY = (120, 120, 120)
RED = (220, 50, 50)
PURPLE = (150, 80, 200)
GREEN = (80, 220, 120)

# =========================
# 字型
# =========================
font = pygame.font.SysFont("arial", 28)
big_font = pygame.font.SysFont("arial", 60)

# =========================
# 玩家設定
# =========================
player_width = 110
player_height = 25
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 70
player_speed = 8

# =========================
# 遊戲資料
# =========================
score = 0
life = 3
level = 1
max_level = 3

falling_objects = []
spawn_timer = 0

game_state = "playing"
# playing / transition / game_over / clear

transition_timer = 0
transition_text = ""

# 第三關拼字
target_word = "GAME"
current_index = 0
collected_word = ""


# =========================
# 關卡設定
# =========================
def get_level_setting(level):
    if level == 1:
        return {
            "target_score": 10,
            "fall_speed": 4,
            "coin_size": 32,
            "spawn_interval": 45,
            "bad_rate": 0.0
        }

    elif level == 2:
        return {
            "target_score": 25,
            "fall_speed": 6,
            "coin_size": 28,
            "spawn_interval": 35,
            "bad_rate": 0.35
        }

    elif level == 3:
        return {
            "target_score": 999,
            "fall_speed": 6,
            "coin_size": 34,
            "spawn_interval": 40,
            "bad_rate": 0.3
        }


# =========================
# 產生掉落物
# =========================
def create_falling_object():
    global current_index

    setting = get_level_setting(level)
    size = setting["coin_size"]

    x = random.randint(0, WIDTH - size)
    y = -size

    # 第三關：拼字模式
    if level == 3:
        obj_type = "letter"

        correct_letter = target_word[current_index]

        # 50% 機率生成正確字母，其餘生成干擾字母
        if random.random() < 0.5:
            letter = correct_letter
        else:
            letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

        obj = {
            "x": x,
            "y": y,
            "size": size,
            "speed": setting["fall_speed"],
            "type": obj_type,
            "letter": letter
        }

    # 第一、二關：金幣、石頭、假金幣
    else:
        if random.random() < setting["bad_rate"]:
            obj_type = random.choice(["rock", "fake_coin"])
        else:
            obj_type = "coin"

        obj = {
            "x": x,
            "y": y,
            "size": size,
            "speed": setting["fall_speed"],
            "type": obj_type
        }

    falling_objects.append(obj)


# =========================
# 畫玩家
# =========================
def draw_player():
    pygame.draw.rect(
        screen,
        BROWN,
        (player_x, player_y, player_width, player_height)
    )

    # 籃子上緣
    pygame.draw.rect(
        screen,
        ORANGE,
        (player_x - 5, player_y - 5, player_width + 10, 8)
    )


# =========================
# 畫掉落物
# =========================
def draw_falling_objects():
    for obj in falling_objects:
        x = obj["x"]
        y = obj["y"]
        size = obj["size"]

        if obj["type"] == "coin":
            pygame.draw.circle(
                screen,
                GOLD,
                (x + size // 2, y + size // 2),
                size // 2
            )
            pygame.draw.circle(
                screen,
                ORANGE,
                (x + size // 2, y + size // 2),
                size // 2,
                3
            )

        elif obj["type"] == "rock":
            pygame.draw.rect(
                screen,
                GRAY,
                (x, y, size, size)
            )

        elif obj["type"] == "fake_coin":
            pygame.draw.circle(
                screen,
                PURPLE,
                (x + size // 2, y + size // 2),
                size // 2
            )

        elif obj["type"] == "letter":
            letter_text = big_font.render(obj["letter"], True, GOLD)
            screen.blit(
                letter_text,
                (x, y)
            )


# =========================
# 更新掉落物
# =========================
def update_falling_objects():
    global score, life, current_index, collected_word, game_state

    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    for obj in falling_objects[:]:
        obj["y"] += obj["speed"]

        obj_rect = pygame.Rect(obj["x"], obj["y"], obj["size"], obj["size"])

        # 接到物件
        if player_rect.colliderect(obj_rect):
            if level == 3:
                handle_letter_catch(obj)
            else:
                handle_normal_catch(obj)

            falling_objects.remove(obj)

        # 物件掉出畫面
        elif obj["y"] > HEIGHT:
            handle_miss(obj)
            falling_objects.remove(obj)


# =========================
# 第一、二關接到物件
# =========================
def handle_normal_catch(obj):
    global score, life

    if obj["type"] == "coin":
        score += 1

    elif obj["type"] == "rock":
        life -= 1

    elif obj["type"] == "fake_coin":
        score -= 1
        if score < 0:
            score = 0


# =========================
# 第三關接到字母
# =========================
def handle_letter_catch(obj):
    global score, life, current_index, collected_word, game_state

    correct_letter = target_word[current_index]

    if obj["letter"] == correct_letter:
        collected_word += obj["letter"]
        current_index += 1
        score += 2

        if current_index >= len(target_word):
            game_state = "clear"

    else:
        life -= 1


# =========================
# 漏接處理
# =========================
def handle_miss(obj):
    global life

    if level in [1, 2]:
        if obj["type"] == "coin":
            life -= 1

    elif level == 3:
        correct_letter = target_word[current_index]

        if obj["type"] == "letter" and obj["letter"] == correct_letter:
            life -= 1


# =========================
# 關卡判定
# =========================
def check_level_progress():
    global level, game_state, transition_timer, transition_text

    setting = get_level_setting(level)

    if level in [1, 2] and score >= setting["target_score"]:
        level += 1
        falling_objects.clear()

        game_state = "transition"
        transition_timer = FPS * 2
        transition_text = f"LEVEL {level}"


# =========================
# 畫 UI
# =========================
def draw_ui():
    if level == 3:
        ui = f"Score: {score}   Life: {life}   Level: {level}   Word: {target_word}   Current: {collected_word}"
    else:
        setting = get_level_setting(level)
        ui = f"Score: {score}   Life: {life}   Level: {level}   Target: {setting['target_score']}"

    text = font.render(ui, True, WHITE)
    screen.blit(text, (20, 20))


# =========================
# 畫轉場
# =========================
def draw_transition():
    screen.fill(BLACK)

    text = big_font.render(transition_text, True, WHITE)
    hint = font.render("Get Ready!", True, WHITE)

    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 60))
    screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 20))


# =========================
# 畫失敗畫面
# =========================
def draw_game_over():
    screen.fill(BLACK)

    text = big_font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)

    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 80))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))


# =========================
# 畫勝利畫面
# =========================
def draw_clear():
    screen.fill(BLACK)

    text = big_font.render("YOU WIN!", True, GOLD)
    word_text = font.render(f"Completed Word: {target_word}", True, WHITE)
    score_text = font.render(f"Final Score: {score}", True, WHITE)

    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(word_text, (WIDTH // 2 - word_text.get_width() // 2, HEIGHT // 2 - 20))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 25))


# =========================
# 主迴圈
# =========================
running = True

while running:
    clock.tick(FPS)

    # 事件處理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 遊戲失敗判定
    if life <= 0 and game_state == "playing":
        game_state = "game_over"

    # =========================
    # 遊戲進行中
    # =========================
    if game_state == "playing":
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player_x -= player_speed

        if keys[pygame.K_RIGHT]:
            player_x += player_speed

        # 限制角色不超出畫面
        if player_x < 0:
            player_x = 0

        if player_x + player_width > WIDTH:
            player_x = WIDTH - player_width

        # 生成掉落物
        spawn_timer += 1
        setting = get_level_setting(level)

        if spawn_timer >= setting["spawn_interval"]:
            create_falling_object()
            spawn_timer = 0

        update_falling_objects()
        check_level_progress()

        # 畫面更新
        screen.fill(BLUE)
        draw_player()
        draw_falling_objects()
        draw_ui()

    # =========================
    # 關卡轉場
    # =========================
    elif game_state == "transition":
        draw_transition()

        transition_timer -= 1
        if transition_timer <= 0:
            game_state = "playing"

    # =========================
    # 遊戲失敗
    # =========================
    elif game_state == "game_over":
        draw_game_over()

    # =========================
    # 遊戲完成
    # =========================
    elif game_state == "clear":
        draw_clear()

    pygame.display.update()

pygame.quit()
sys.exit()