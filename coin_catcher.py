import pygame
import random
import sys

# =========================
# 初始化
# =========================
pygame.init()
pygame.mixer.init()
# =========================
# 讀取設定檔
# =========================
try:
    with open("settings.txt", "r") as f:
        lines = f.readlines()

    sound_on = lines[0].strip() == "True"
    menu_music_on = lines[1].strip() == "True"
    game_music_on = lines[2].strip() == "True"

except:
    sound_on = True
    menu_music_on = True
    game_music_on = True
# =========================
# 遊戲背景音樂
# =========================
if game_music_on:
    pygame.mixer.music.load("assets/game_bgm.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

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

# 復古像素城市配色
RETRO_DARK = (68, 62, 70)        # 443E46
RETRO_CREAM = (246, 222, 184)    # F6DEB8
RETRO_LAVENDER = (144, 140, 164) # 908CA4
RETRO_BLUE = (87, 101, 158)      # 57659E
RETRO_PINK = (197, 114, 132)     # C57284
RETRO_CORAL = (255, 91, 96)      # FF5B60

# =========================
# 字型
# =========================
font = pygame.font.SysFont("Microsoft JhengHei", 28)
ui_font = pygame.font.SysFont("Arial Black",25)
big_font = pygame.font.SysFont(  "Arial Black", 72)

# =========================
# 圖片
# =========================
coin_img = pygame.image.load("assets/coin.png").convert_alpha()
heart_img = pygame.image.load("assets/heart.png").convert_alpha()
rock_img = pygame.image.load("assets/rock.png").convert_alpha()
fake_coin_img = pygame.image.load("assets/fake_coin.png").convert_alpha()
basket_img = pygame.image.load("assets/basket.png").convert_alpha()
# =========================
# 音效
# =========================
coin_sound = pygame.mixer.Sound(
    "assets/coin.mp3"
)

rock_sound = pygame.mixer.Sound(
    "assets/hit.mp3"
)

fake_coin_sound = pygame.mixer.Sound(
    "assets/fake_coin.mp3"
)

level_up_sound = pygame.mixer.Sound(
    "assets/level_up.mp3"
)

game_over_sound = pygame.mixer.Sound(
    "assets/game_over.mp3"
)

win_sound = pygame.mixer.Sound(
    "assets/win.mp3"
)

letter_correct_sound = pygame.mixer.Sound(
    "assets/letter_correct.mp3"
)

letter_wrong_sound = pygame.mixer.Sound(
    "assets/letter_wrong.mp3"
)
button_click_sound = pygame.mixer.Sound(
    "assets/button.mp3"
)

button_click_sound.set_volume(0.6)
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

#//// 測試       level = 1
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
            "fall_speed": 5,
            "coin_size": 40,
            "spawn_interval": 35,
            "bad_rate": 0.25
        }

    elif level == 3:
        return {
            "target_score": 50,
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
    basket_scaled = pygame.transform.scale(
        basket_img,
        (player_width, 55)
    )
    screen.blit(basket_scaled, (player_x, player_y - 25))

    # # 籃子上緣
    # pygame.draw.rect(
    #     screen,
    #     ORANGE,
    #     (player_x - 5, player_y - 5, player_width + 10, 8)
    # )


# =========================
# 畫掉落物
# =========================
def draw_falling_objects():
    for obj in falling_objects:
        x = obj["x"]
        y = obj["y"]
        size = obj["size"]

        if obj["type"] == "coin":
            img = pygame.transform.scale(coin_img, (size, size))
            screen.blit(img, (x, y))

        elif obj["type"] == "rock":
            img = pygame.transform.scale(rock_img, (size, size))
            screen.blit(img, (x, y))

        elif obj["type"] == "fake_coin":
            img = pygame.transform.scale(fake_coin_img, (size, size))
            screen.blit(img, (x, y))

        elif obj["type"] == "letter":
            letter_text = big_font.render(obj["letter"], True, RETRO_CREAM)
            letter_font = pygame.font.SysFont("Arial Black",50)
            letter_text = letter_font.render(obj["letter"],True,RETRO_CREAM)
            screen.blit(letter_text, (x, y))


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
        coin_sound.play()

    elif obj["type"] == "rock":
        life -= 1
        rock_sound.play()

    elif obj["type"] == "fake_coin":
        score -= 1
        fake_coin_sound.play()

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
        letter_correct_sound.play()
        collected_word += obj["letter"]
        current_index += 1
        score += 2

        if current_index >= len(target_word):
            if word_number + 1 >= word_goal:
                pygame.mixer.music.stop()
                win_sound.play()
                game_state = "clear"
            else:
                start_next_word()

            return True

    else:
        letter_wrong_sound.play()
        # 接到不是目前需要的字母會扣血
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
        level_up_sound.play()
        falling_objects.clear()

        game_state = "transition"
        transition_timer = FPS * 2
        transition_text = f"LEVEL {level}"

# =========================
# 畫背景函式
# =========================
def draw_arcade_game_background():
    if level == 1:
        bg_color = RETRO_BLUE
        grid_color = RETRO_CREAM

    elif level == 2:
        bg_color = RETRO_LAVENDER
        grid_color =RETRO_CREAM

    else:
        bg_color = RETRO_PINK
        grid_color = RETRO_CREAM

    screen.fill(bg_color)

    for x in range(0, WIDTH, 40):
        pygame.draw.line(screen, grid_color, (x, 0), (x, HEIGHT), 1)

    for y in range(0, HEIGHT, 40):
        pygame.draw.line(screen, grid_color, (0, y), (WIDTH, y), 1)

# =========================
# 畫轉場背景函式
# =========================
def draw_transition_background():
    screen.fill(RETRO_DARK)

    # for x in range(0, WIDTH, 40):
    #     pygame.draw.line(screen, RETRO_LAVENDER, (x, 0), (x, HEIGHT), 1)

    # for y in range(0, HEIGHT, 40):
    #     pygame.draw.line(screen, RETRO_LAVENDER, (0, y), (WIDTH, y), 1)


def draw_gameover_background():
    screen.fill(RETRO_DARK)

    # for x in range(0, WIDTH, 40):
    #     pygame.draw.line(screen, RETRO_CORAL, (x, 0), (x, HEIGHT), 1)

    # for y in range(0, HEIGHT, 40):
    #     pygame.draw.line(screen, RETRO_CORAL, (0, y), (WIDTH, y), 1)


def draw_win_background():
    screen.fill(RETRO_BLUE)

    # for x in range(0, WIDTH, 40):
    #     pygame.draw.line(screen, RETRO_CREAM, (x, 0), (x, HEIGHT), 1)

    # for y in range(0, HEIGHT, 40):
    #     pygame.draw.line(screen, RETRO_CREAM, (0, y), (WIDTH, y), 1)
# =========================
# 畫 UI
# =========================
def draw_ui():

    # =========================
    # 左上角：分數
    # =========================
    score_text = ui_font.render(
        f"SCORE : {score}",
        True,
        RETRO_CORAL
    )
    screen.blit(score_text, (25, 15))

    # =========================
    # 左上角：生命值
    # =========================
    for i in range(life):
        heart_scaled = pygame.transform.scale(
            heart_img,
            (30, 30)
        )
        screen.blit(
            heart_scaled,
            (25 + i * 35, 50)
        )

    # =========================
    # 右上角：關卡
    # =========================
    level_text = ui_font.render(
        f"LEVEL {level}",
        True,
        RETRO_DARK
    )
    # 右側資訊區固定起點
    info_x = WIDTH - 280

    level_text = ui_font.render(f"LEVEL {level}",True,RETRO_DARK)
    screen.blit(level_text, (info_x, 15))

    # =========================
    # 第三關
    # =========================
    if level == 3:

        word_text = ui_font.render(
            f"WORD : {word_number + 1}/{word_goal}",
            True,
            RETRO_DARK
        )
        screen.blit(word_text, (info_x, 50))

        progress_word = (
            collected_word +
            "_" * (len(target_word) - len(collected_word))
        )

        target_text = ui_font.render(f"TARGET : {target_word}", True, RETRO_DARK)

        progress_text = ui_font.render(
            f"PROGRESS : {progress_word}",
            True,
            RETRO_DARK
        )
        screen.blit(word_text, (info_x, 50))
        screen.blit(target_text, (info_x, 85))
        screen.blit(progress_text, (info_x, 120))

    # =========================
    # 第一、二關
    # =========================
    else:

        setting = get_level_setting(level)

        target_text = ui_font.render(
            f"TARGET SCORE : {setting['target_score']}",
            True,
            RETRO_DARK
        )

        screen.blit(target_text, (info_x, 50))
# =========================
# 畫轉場
# =========================
def draw_transition():
    draw_transition_background()

    title = big_font.render(
        transition_text,
        True,
        RETRO_CREAM
    )

    if level == 2:
        hint_text = "WARNING : NEW ENEMIES"
    elif level == 3:
        hint_text = "WORD CHALLENGE"
    else:
        hint_text = "GET READY!"

    hint = font.render(
        hint_text,
        True,
        RETRO_CORAL
    )

    screen.blit(
    title,
    (WIDTH // 2 - title.get_width() // 2,
     HEIGHT // 2 - 100)
    )

    screen.blit(
    hint,
    (WIDTH // 2 - hint.get_width() // 2,
     HEIGHT // 2 + 30)
    )

# =========================
# 新增兩個按鈕函式
# =========================
def restart_game():
    global score, life, level
    global game_state, spawn_timer
    global falling_objects
    global word_number, current_index
    global collected_word, target_words, target_word
    global player_x
    global game_over_played
    game_over_played = False

    score = 0
    life = 3
    level = 1

    player_x = WIDTH // 2 - player_width // 2

    spawn_timer = 0
    falling_objects.clear()


    target_words = random.sample(word_list, word_goal)
    word_number = 0
    target_word = target_words[word_number]
    current_index = 0
    collected_word = ""

    game_state = "playing"
    if game_music_on:
       pygame.mixer.music.load("assets/game_bgm.mp3")
       pygame.mixer.music.set_volume(0.4)
       pygame.mixer.music.play(-1)
    else:
       pygame.mixer.music.stop()


def return_to_menu():
    pygame.quit()
    import subprocess
    import sys

    subprocess.Popen([sys.executable, "main_menu.py"])

    # running = False

    pygame.quit()
    sys.exit()


class Button:
    def __init__(self, text, x, y, width, height, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        hover = self.rect.collidepoint(mouse_pos)

         # 按鈕
        fill_color = RETRO_CREAM if not hover else RETRO_CORAL
        border_color = RETRO_DARK
        text_color = RETRO_DARK if not hover else RETRO_CREAM
        
         # 按鈕底色
        pygame.draw.rect(surface, fill_color, self.rect, border_radius=8)
        pygame.draw.rect(surface, border_color, self.rect, 3, border_radius=8)

        text_surface = font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
           if self.rect.collidepoint(event.pos):

            if sound_on:
                button_click_sound.play()

            pygame.time.delay(250)

            if self.action:
                self.action()

            return True

        return False
# 畫失敗畫面
# =========================
def draw_game_over():

    draw_gameover_background()


    title = big_font.render(
        "GAME OVER",
        True,
        RETRO_CORAL
    )

    score_text = font.render(
        f"FINAL SCORE {score}",
        True,
         RETRO_CREAM
    )

    screen.blit(
    title,
    title.get_rect(center=(WIDTH//2, 145))
    )

    screen.blit(
        score_text,
        score_text.get_rect(center=(WIDTH//2,280))
    )

    restart_btn = Button(
        "重新開始",
        300,
        360,
        200,
        50,
        restart_game
    )

    menu_btn = Button(
        "返回主選單",
        300,
        440,
        200,
        50,
        return_to_menu
    )

    restart_btn.draw(screen)
    menu_btn.draw(screen)

    return [restart_btn, menu_btn]

# =========================
# 畫勝利畫面
# =========================
def draw_clear():
    draw_win_background()

    text = big_font.render("YOU WIN!", True, RETRO_CORAL)
    score_text = font.render(f"Final Score : {score}", True, RETRO_CREAM)

    screen.blit(
        text,
        text.get_rect(center=(WIDTH // 2, 160))
    )

    screen.blit(
        score_text,
        score_text.get_rect(center=(WIDTH // 2, 280))
    )

    restart_btn = Button(
        "重新開始",
        300,
        360,
        200,
        50,
        restart_game
    )

    menu_btn = Button(
        "返回主選單",
        300,
        440,
        200,
        50,
        return_to_menu
    )

    restart_btn.draw(screen)
    menu_btn.draw(screen)

    return [restart_btn, menu_btn]


# =========================
# 主迴圈
# =========================\
game_over_played = False
running = True

while running:
    clock.tick(FPS)
    buttons = []

    
    # 遊戲失敗判定
    if life <= 0 and game_state == "playing":
        pygame.mixer.music.stop()
        game_state = "game_over"
        if not game_over_played:
           game_over_sound.play()
           game_over_played = True

      # 畫面更新
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

        draw_arcade_game_background()
        draw_player()
        draw_falling_objects()
        draw_ui()

    elif game_state == "transition":
        draw_transition()

        transition_timer -= 1
        if transition_timer <= 0:
            game_state = "playing"

    elif game_state == "game_over":
        buttons = draw_game_over()

    elif game_state == "clear":
        buttons = draw_clear()

    # 事件處理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        for button in buttons:
             if button.check_click(event):
              break

    pygame.display.update()

    

    # # =========================
    # # 遊戲進行中
    # # =========================
    # if game_state == "playing":
    #     keys = pygame.key.get_pressed()

    #     if keys[pygame.K_LEFT]:
    #         player_x -= player_speed

    #     if keys[pygame.K_RIGHT]:
    #         player_x += player_speed

    #     # 限制角色不超出畫面
    #     if player_x < 0:
    #         player_x = 0

    #     if player_x + player_width > WIDTH:
    #         player_x = WIDTH - player_width

    #     # 生成掉落物
    #     spawn_timer += 1
    #     setting = get_level_setting(level)

    #     if spawn_timer >= setting["spawn_interval"]:
    #         create_falling_object()
    #         spawn_timer = 0

    #     update_falling_objects()
    #     check_level_progress()

    #     # 畫面更新
    #     draw_arcade_game_background()
    #     draw_player()
    #     draw_falling_objects()
    #     draw_ui()

    # =========================
    # 關卡轉場
    # =========================
    #   elif game_state == "transition":
    #       draw_transition()

    #     transition_timer -= 1
    #     if transition_timer <= 0:
    #         game_state = "playing"

    # # =========================
    # # 遊戲失敗
    # # =========================
    # elif game_state == "game_over":
    #      buttons = draw_game_over()

    # # =========================
    # # 遊戲完成
    # # =========================
    # elif game_state == "clear":
    #     draw_clear()

    # pygame.display.update()

pygame.quit()
sys.exit()