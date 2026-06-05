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
pygame.display.set_caption("Catch or Crash 接不可失")

clock = pygame.time.Clock()

# =========================
# 顏色
# =========================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (90, 170, 255)
DARK_BLUE = (30, 30, 60)
GOLD = (255, 215, 0)
ORANGE = (255, 165, 0)
BROWN = (150, 80, 30)
GRAY = (120, 120, 120)
DARK_GRAY = (80, 80, 80)
RED = (220, 50, 50)
PURPLE = (150, 80, 200)
GREEN = (80, 220, 120)

# =========================
# 字型
# =========================
try:
    font_path = "C:/Windows/Fonts/msjh.ttc"
    font = pygame.font.Font(font_path, 28)
    big_font = pygame.font.Font(font_path, 60)
    title_font = pygame.font.Font(font_path, 54)
    subtitle_font = pygame.font.Font(font_path, 36)
    button_font = pygame.font.Font(font_path, 28)
    text_font = pygame.font.Font(font_path, 24)
    small_font = pygame.font.Font(font_path, 20)
except:
    font = pygame.font.SysFont("arial", 28)
    big_font = pygame.font.SysFont("arial", 60)
    title_font = pygame.font.SysFont("arial", 54)
    subtitle_font = pygame.font.SysFont("arial", 36)
    button_font = pygame.font.SysFont("arial", 28)
    text_font = pygame.font.SysFont("arial", 24)
    small_font = pygame.font.SysFont("arial", 20)

# =========================
# 畫面狀態
# =========================
current_screen = "main_menu"
# main_menu / how_to_play / settings / game
def go_game_settings():
    global current_screen
    current_screen = "game_settings"


def resume_game():
    global current_screen
    current_screen = "game"


def restart_current_game():
    reset_game()
    resume_game()
# =========================
# 主選單設定狀態
# =========================
sound_on = True
music_on = True

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
word_list = [
    "GAME",
    "COIN",
    "STAR",
    "CODE",
    "PLAY",
    "GOLD",
    "HERO",
    "MOON",
    "FIRE",
    "WIND"
]

word_goal = 5
target_words = random.sample(word_list, word_goal)
word_number = 0
target_word = target_words[word_number]
current_index = 0
collected_word = ""


# =========================
# 按鈕類別
# =========================
class Button:
    def __init__(self, text, x, y, width, height, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            color = BLUE
        else:
            color = DARK_GRAY

        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=12)

        text_surface = button_font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()


# =========================
# 文字輔助函式
# =========================
def draw_center_text(text, font_obj, color, x, y):
    text_surface = font_obj.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


def draw_left_text(text, font_obj, color, x, y):
    text_surface = font_obj.render(text, True, color)
    screen.blit(text_surface, (x, y))


# =========================
# 畫面切換函式
# =========================
def go_main_menu():
    global current_screen
    current_screen = "main_menu"


def go_how_to_play():
    global current_screen
    current_screen = "how_to_play"


def go_settings():
    global current_screen
    current_screen = "settings"


def quit_game():
    pygame.quit()
    sys.exit()


# =========================
# 設定切換
# =========================
def toggle_sound():
    global sound_on
    sound_on = not sound_on
    print("音效：開" if sound_on else "音效：關")


def toggle_music():
    global music_on
    music_on = not music_on
    print("背景音樂：開" if music_on else "背景音樂：關")


# =========================
# 開始遊戲：重點在這裡
# =========================
def start_game():
    global current_screen

    reset_game()
    current_screen = "game"


# =========================
# 重設遊戲資料：讓遊戲從第一關開始
# =========================
def reset_game():
    global player_x
    global score, life, level
    global falling_objects, spawn_timer
    global game_state, transition_timer, transition_text
    global target_words, word_number, target_word, current_index, collected_word

    player_x = WIDTH // 2 - player_width // 2

    score = 0
    life = 3
    level = 1

    falling_objects = []
    spawn_timer = 0

    game_state = "playing"
    transition_timer = 0
    transition_text = ""

    target_words = random.sample(word_list, word_goal)
    word_number = 0
    target_word = target_words[word_number]
    current_index = 0
    collected_word = ""


# =========================
# 主選單畫面
# =========================
def draw_main_menu():
    screen.fill(BLACK)

    draw_center_text("Catch or Crash", title_font, GOLD, WIDTH // 2, 90)
    draw_center_text("接不可失", subtitle_font, WHITE, WIDTH // 2, 150)

    buttons = [
        Button("開始遊戲", 275, 230, 250, 55, start_game),
        Button("遊戲說明", 275, 305, 250, 55, go_how_to_play),
        Button("設定", 275, 380, 250, 55, go_settings),
        Button("離開遊戲", 275, 455, 250, 55, quit_game),
    ]

    for button in buttons:
        button.draw(screen)

    return buttons


# =========================
# 遊戲說明畫面
# =========================
def draw_how_to_play():
    screen.fill(BLACK)

    draw_center_text("遊戲說明", title_font, GOLD, WIDTH // 2, 80)

    rules = [
        "遊戲目標：操作角色接住從上方掉落的金幣來累積分數。",
        "操作方式：使用鍵盤 ← / → 控制角色左右移動。",
        "第一關：基礎接金幣玩法，達到指定分數即可進入下一關。",
        "第二關：加入石頭與假金幣，考驗反應與判斷能力。",
        "第三關：拼字挑戰，依序接取正確英文字母完成單字。",
        "漏接金幣或接到錯誤物件會扣生命值。",
        "生命值歸零時遊戲結束。"
    ]

    y = 140
    for rule in rules:
        draw_left_text(rule, text_font, WHITE, 70, y)
        y += 42

    buttons = [
        Button("返回主選單", 275, 510, 250, 55, go_main_menu),
    ]

    for button in buttons:
        button.draw(screen)

    return buttons


# =========================
# 主選單設定畫面
# =========================
def draw_settings():
    screen.fill(BLACK)

    draw_center_text("設定", title_font, GOLD, WIDTH // 2, 100)

    sound_text = "音效：開" if sound_on else "音效：關"
    music_text = "背景音樂：開" if music_on else "背景音樂：關"

    buttons = [
        Button(sound_text, 275, 210, 250, 55, toggle_sound),
        Button(music_text, 275, 290, 250, 55, toggle_music),
        Button("返回主選單", 275, 400, 250, 55, go_main_menu),
    ]

    for button in buttons:
        button.draw(screen)

    return buttons

# =========================
# 遊戲中設定 / 暫停選單畫面
# =========================
def draw_game_settings():
    screen.fill(BLACK)

    draw_center_text("遊戲暫停", title_font, GOLD, WIDTH // 2, 90)

    sound_text = "音效：開" if sound_on else "音效：關"

    buttons = [
        Button("繼續遊戲", 275, 170, 250, 55, resume_game),
        Button("重新開始", 275, 245, 250, 55, restart_current_game),
        Button(sound_text, 275, 320, 250, 55, toggle_sound),
        Button("返回主選單", 275, 395, 250, 55, go_main_menu),
        Button("離開遊戲", 275, 470, 250, 55, quit_game),
    ]

    for button in buttons:
        button.draw(screen)

    return buttons

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

        if random.random() < 0.5:
            letter = correct_letter
        else:
            wrong_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".replace(correct_letter, "")
            letter = random.choice(wrong_letters)

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

        if player_rect.colliderect(obj_rect):
            word_finished = False

            if level == 3:
                word_finished = handle_letter_catch(obj)
            else:
                handle_normal_catch(obj)

            if obj in falling_objects:
                falling_objects.remove(obj)

            if word_finished:
                falling_objects.clear()
                break

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
def start_next_word():
    global word_number, target_word, current_index, collected_word

    word_number += 1
    target_word = target_words[word_number]
    current_index = 0
    collected_word = ""


def handle_letter_catch(obj):
    global score, life, current_index, collected_word, game_state

    correct_letter = target_word[current_index]

    if obj["letter"] == correct_letter:
        collected_word += obj["letter"]
        current_index += 1
        score += 2

        if current_index >= len(target_word):
            if word_number + 1 >= word_goal:
                game_state = "clear"
            else:
                start_next_word()

            return True

    else:
        life -= 1

    return False


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
        ui = f"Score: {score}   Life: {life}   Level: {level}   Word: {word_number + 1}/{word_goal} {target_word}   Current: {collected_word}"
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
    restart_text = small_font.render("按 R 重新開始，按 M 返回主選單", True, WHITE)

    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 20))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 40))


# =========================
# 畫勝利畫面
# =========================
def draw_clear():
    screen.fill(BLACK)

    text = big_font.render("YOU WIN!", True, GOLD)
    word_text = font.render(f"Completed Words: {word_goal}", True, WHITE)
    words_text = font.render("Words: " + " / ".join(target_words), True, WHITE)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = small_font.render("按 R 重新開始，按 M 返回主選單", True, WHITE)

    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 130))
    screen.blit(word_text, (WIDTH // 2 - word_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(words_text, (WIDTH // 2 - words_text.get_width() // 2, HEIGHT // 2))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 45))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 95))


# =========================
# 遊戲主畫面更新
# =========================
# =========================
# 遊戲主畫面更新
# =========================
def update_game():
    global player_x, spawn_timer, game_state

    game_buttons = []

    if life <= 0 and game_state == "playing":
        game_state = "game_over"

    if game_state == "playing":
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player_x -= player_speed

        if keys[pygame.K_RIGHT]:
            player_x += player_speed

        if player_x < 0:
            player_x = 0

        if player_x + player_width > WIDTH:
            player_x = WIDTH - player_width

        spawn_timer += 1
        setting = get_level_setting(level)

        if spawn_timer >= setting["spawn_interval"]:
            create_falling_object()
            spawn_timer = 0

        update_falling_objects()
        check_level_progress()

        screen.fill(BLUE)
        draw_player()
        draw_falling_objects()
        draw_ui()

        # 遊戲畫面右上角設定按鈕
        game_buttons = [
            Button("設定", 690, 15, 90, 40, go_game_settings)
        ]

        for button in game_buttons:
            button.draw(screen)

    elif game_state == "transition":
        draw_transition()
        transition_timer_update()

    elif game_state == "game_over":
        draw_game_over()

    elif game_state == "clear":
        draw_clear()

    return game_buttons

def transition_timer_update():
    global transition_timer, game_state

    transition_timer -= 1
    if transition_timer <= 0:
        game_state = "playing"


# =========================
# 主迴圈
# =========================
# =========================
# 主迴圈
# =========================
running = True

while running:
    clock.tick(FPS)

    buttons = []

    # =========================
    # 畫面繪製
    # =========================
    if current_screen == "main_menu":
        buttons = draw_main_menu()

    elif current_screen == "how_to_play":
        buttons = draw_how_to_play()

    elif current_screen == "settings":
        buttons = draw_settings()

    elif current_screen == "game":
        buttons = update_game()

    elif current_screen == "game_settings":
        buttons = draw_game_settings()

    # =========================
    # 事件處理
    # =========================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 只有 KEYDOWN 才能使用 event.key
        if event.type == pygame.KEYDOWN:

            if current_screen == "how_to_play":
                if event.key == pygame.K_ESCAPE:
                    go_main_menu()

            elif current_screen == "settings":
                if event.key == pygame.K_ESCAPE:
                    go_main_menu()

            elif current_screen == "game":
                if event.key == pygame.K_ESCAPE and game_state == "playing":
                    go_game_settings()

                elif game_state in ["game_over", "clear"]:
                    if event.key == pygame.K_r:
                        start_game()

                    elif event.key == pygame.K_m:
                        go_main_menu()

            elif current_screen == "game_settings":
                if event.key == pygame.K_ESCAPE:
                    resume_game()

        # 滑鼠點擊按鈕
        for button in buttons:
            button.check_click(event)

    pygame.display.update()

pygame.quit()
sys.exit()