import pygame
import sys

# =========================
# 初始化 pygame
# =========================
pygame.init()
pygame.mixer.init()
# =========================
# 視窗設定
# =========================
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch or Crash 接不可失")

# =========================
# 顏色設定
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

ARCADE_BG = RETRO_BLUE
BUTTON_DARK = RETRO_DARK

# =========================
# 字型設定
# =========================
title_font = pygame.font.SysFont("arial", 56, bold=True)
subtitle_font = pygame.font.SysFont("Microsoft JhengHei", 36, bold=True)
button_font = pygame.font.SysFont("Microsoft JhengHei", 30)
text_font = pygame.font.SysFont("Microsoft JhengHei", 24)

# =========================
# 音樂設定
# =========================
pygame.mixer.music.load("assets/menu_bgm.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

button_click_sound = pygame.mixer.Sound("assets/button.mp3")
button_click_sound.set_volume(0.6)

# =========================
# 遊戲狀態
# =========================
current_screen = "main_menu"

# =========================
# 設定狀態
# =========================
sound_on = True
music_on = True
game_music_on = True


# =========================
# Button 類別
# =========================
class Button:
    def __init__(self, text, x, y, width, height, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        hover = self.rect.collidepoint(mouse_pos)

        fill_color = (255, 230, 190) if hover else RETRO_CREAM
        border_color = RETRO_CORAL if hover else RETRO_DARK
        text_color = RETRO_DARK

        # glow_rect = self.rect.inflate(8, 8)
        # pygame.draw.rect(surface, border_color, glow_rect, 2, border_radius=4)

        pygame.draw.rect(surface, fill_color, self.rect, border_radius=4)
        pygame.draw.rect(surface, border_color, self.rect, 3, border_radius=4)

        if hover:
           arrow = button_font.render(">", True, RETRO_CORAL)
           surface.blit(arrow, (self.rect.x - 35, self.rect.y + 4))

        text_surface = button_font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    if sound_on:
                       button_click_sound.play()
                    pygame.time.delay(250)

                    if self.action:
                        self.action()


# =========================
# 功能函式
# =========================
def go_main_menu():
    global current_screen
    current_screen = "main_menu"


def start_game():
    import subprocess
    import sys
    
    with open("settings.txt", "w") as f:
       f.write(f"{sound_on}\n")
       f.write(f"{music_on}\n")
       f.write(f"{game_music_on}\n")

    pygame.mixer.music.stop()
    pygame.quit()

    subprocess.Popen([
        sys.executable,
        "coin_catcher.py"
    ])

    sys.exit()


def go_how_to_play():
    global current_screen
    current_screen = "how_to_play"


def go_settings():
    global current_screen
    current_screen = "settings"


def go_pause():
    global current_screen
    current_screen = "pause"


def resume_game():
    global current_screen
    current_screen = "game"


def restart_game():
    global current_screen
    current_screen = "game"
    print("重新開始遊戲")


def quit_game():
    pygame.quit()
    sys.exit()


def toggle_sound():
    global sound_on
    sound_on = not sound_on
    if sound_on:
        button_click_sound.set_volume(0.4)
    else:
        button_click_sound.set_volume(0)


def toggle_music():
    global music_on
    music_on = not music_on
    if music_on:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()

def toggle_game_music():
    global game_music_on
    game_music_on = not game_music_on
# =========================
# 畫面繪製復古背景函式
# =========================

def draw_arcade_background():
    screen.fill(RETRO_BLUE)

    for x in range(0, WIDTH, 40):
        pygame.draw.line(screen, RETRO_LAVENDER, (x, 0), (x, HEIGHT), 1)

    for y in range(0, HEIGHT, 40):
        pygame.draw.line(screen, RETRO_LAVENDER, (0, y), (WIDTH, y), 1)

    pygame.draw.rect(screen, RETRO_CREAM, (20, 20, WIDTH - 40, HEIGHT - 40), 3)
    pygame.draw.rect(screen, RETRO_PINK, (28, 28, WIDTH - 56, HEIGHT - 56), 2)
# =========================
# 畫面繪製函式
# =========================
def draw_main_menu():
    draw_arcade_background()

    # 標題陰影
    title_shadow = title_font.render("Catch or Crash", True, RETRO_CORAL)
    title_shadow_rect = title_shadow.get_rect(center=(WIDTH // 2 + 4, 120 + 4))
    screen.blit(title_shadow, title_shadow_rect)

    title = title_font.render("Catch or Crash", True, RETRO_CREAM)
    title_rect = title.get_rect(center=(WIDTH // 2, 120))
    screen.blit(title, title_rect)

    subtitle = subtitle_font.render("接不可失", True, RETRO_CREAM)
    subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, 180))
    screen.blit(subtitle, subtitle_rect)


    buttons = [
        Button("開始遊戲", 300, 245, 200, 50, start_game),
        Button("遊戲說明", 300, 320, 200, 50, go_how_to_play),
        Button("設定", 300, 395, 200, 50, go_settings),
        Button("離開遊戲", 300, 470, 200, 50, quit_game),
    ]

    for button in buttons:
        button.draw(screen)

    # footer = text_font.render("CATCH THE COINS  |  DODGE THE DANGER", True, RETRO_CREAM)
    # footer_rect = footer.get_rect(center=(WIDTH // 2, 550))
    # screen.blit(footer, footer_rect)

    return buttons


def draw_how_to_play():
    draw_arcade_background()

    title = subtitle_font.render("HOW TO PLAY", True, RETRO_CREAM)
    title_rect = title.get_rect(center=(WIDTH // 2, 75))
    screen.blit(title, title_rect)

    subtitle = text_font.render("遊戲說明", True, RETRO_CREAM)
    screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, 120)))

    rules = [
        "1. 使用 ← / → 控制角色左右移動",
        "2. 接住金幣可以獲得分數",
        "3. 漏接金幣或接到障礙物會扣生命",
        "4. 生命值歸零時遊戲結束",
        "5. 達到指定分數即可進入下一關",
        "6. 第三關要依照順序接正確英文字母",
    ]

    y = 170
    for rule in rules:
        text = text_font.render(rule, True, WHITE)
        screen.blit(text, (120, y))
        y += 42

    buttons = [
        Button("返回主選單", 275, 500, 250, 50, go_main_menu),
    ]

    for button in buttons:
        button.draw(screen)

    return buttons


def draw_settings():
    draw_arcade_background()

    title = subtitle_font.render("SETTINGS", True, RETRO_CREAM)
    title_rect = title.get_rect(center=(WIDTH // 2, 90))
    screen.blit(title, title_rect)

    subtitle = text_font.render("設定", True, RETRO_CREAM)
    screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, 135)))

    sound_text = "音效：開" if sound_on else "音效：關"
    music_text = "背景音樂：開" if music_on else "背景音樂：關"
    game_music_text = ( "遊戲音樂：開"if game_music_on else "遊戲音樂：關")
    buttons = [
        Button(sound_text, 275, 210, 250, 50, toggle_sound),
        Button(music_text, 275, 290, 250, 50, toggle_music),
        Button(game_music_text, 275, 370, 250, 50, toggle_game_music),
        Button("返回主選單", 275, 450, 250, 50, go_main_menu),
    ]

    for button in buttons:
        button.draw(screen)

    return buttons


# def draw_game():
#     draw_arcade_background()

#     title = subtitle_font.render("GAME START", True, RETRO_CREAM)
#     title_rect = title.get_rect(center=(WIDTH // 2, 100))
#     screen.blit(title, title_rect)

#     info = text_font.render("這裡之後會放正式的接金幣遊戲內容", True, WHITE)
#     info_rect = info.get_rect(center=(WIDTH // 2, 180))
#     screen.blit(info, info_rect)

#     hint = text_font.render("按 ESC 開啟暫停選單", True, RETRO_CREAM)
#     hint_rect = hint.get_rect(center=(WIDTH // 2, 240))
#     screen.blit(hint, hint_rect)

#     # 玩家
#     pygame.draw.rect(screen, RETRO_CREAM, (360, 470, 80, 40), border_radius=4)

#     # 金幣
#     pygame.draw.circle(screen, RETRO_CREAM, (400, 330), 25)
#     pygame.draw.circle(screen, (255, 150, 40), (400, 330), 25, 3)

#     return []


def draw_pause_menu():
    draw_arcade_background()

    title = subtitle_font.render("PAUSE", True, RETRO_CREAM)
    title_rect = title.get_rect(center=(WIDTH // 2, 90))
    screen.blit(title, title_rect)

    subtitle = text_font.render("遊戲暫停", True, RETRO_CREAM)
    screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, 135)))

    sound_text = "音效：開" if sound_on else "音效：關"

    buttons = [
        Button("繼續遊戲", 275, 180, 250, 50, resume_game),
        Button("重新開始", 275, 250, 250, 50, restart_game),
        Button(sound_text, 275, 320, 250, 50, toggle_sound),
        Button("返回主選單", 275, 390, 250, 50, go_main_menu),
        Button("離開遊戲", 275, 460, 250, 50, quit_game),
    ]

    for button in buttons:
        button.draw(screen)

    return buttons

# def go_main_settings():
#     global current_screen
#     current_screen = "main_settings"
# =========================
# 主迴圈
# =========================
clock = pygame.time.Clock()

while True:
    buttons = []

    if current_screen == "main_menu":
        buttons = draw_main_menu()
    elif current_screen == "how_to_play":
        buttons = draw_how_to_play()
    elif current_screen == "settings":
        buttons = draw_settings()
    elif current_screen == "pause":
        buttons = draw_pause_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
               if current_screen == "pause":
                  resume_game()
               elif current_screen in ["how_to_play", "settings"]:
                  go_main_menu()

        for button in buttons:
            button.check_click(event)

    pygame.display.update()
    clock.tick(60)
