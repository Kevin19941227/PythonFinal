import pygame
import sys

# =========================
# 初始化 pygame
# =========================
pygame.init()

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
GRAY = (180, 180, 180)
DARK_GRAY = (80, 80, 80)
YELLOW = (255, 210, 80)
BLUE = (80, 160, 255)
RED = (255, 100, 100)

# =========================
# 字型設定
# =========================
title_font = pygame.font.SysFont("arial", 56, bold=True)
subtitle_font = pygame.font.SysFont("Microsoft JhengHei", 36, bold=True)
button_font = pygame.font.SysFont("Microsoft JhengHei", 30)
text_font = pygame.font.SysFont("Microsoft JhengHei", 24)

# =========================
# 遊戲狀態
# =========================
current_screen = "main_menu"

# =========================
# 設定狀態
# =========================
sound_on = True
music_on = True

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
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    if self.action:
                        self.action()


# =========================
# 功能函式
# =========================
def go_main_menu():
    global current_screen
    current_screen = "main_menu"


def start_game():
    global current_screen
    current_screen = "game"


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


def toggle_music():
    global music_on
    music_on = not music_on


# =========================
# 畫面繪製函式
# =========================
def draw_main_menu():
    screen.fill(BLACK)

    title = title_font.render("Catch or Crash", True, YELLOW)
    title_rect = title.get_rect(center=(WIDTH // 2, 100))
    screen.blit(title, title_rect)

    subtitle = subtitle_font.render("接不可失", True, WHITE)
    subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, 155))
    screen.blit(subtitle, subtitle_rect)

    buttons = [
        Button("開始遊戲", 300, 230, 200, 50, start_game),
        Button("遊戲說明", 300, 300, 200, 50, go_how_to_play),
        Button("設定", 300, 370, 200, 50, go_settings),
        Button("離開遊戲", 300, 440, 200, 50, quit_game),
    ]

    for button in buttons:
        button.draw(screen)

    return buttons


def draw_how_to_play():
    screen.fill(BLACK)

    title = subtitle_font.render("遊戲說明", True, YELLOW)
    title_rect = title.get_rect(center=(WIDTH // 2, 70))
    screen.blit(title, title_rect)

    rules = [
        "玩家需要操作角色左右移動，接住從上方掉落的金幣。",
        "← / →：控制角色移動",
        "接到金幣可以加分。",
        "漏接金幣或接到障礙物會扣生命值。",
        "生命值歸零時遊戲結束。",
        "達到關卡指定分數即可進入下一關。",
    ]

    y = 140
    for rule in rules:
        text = text_font.render(rule, True, WHITE)
        screen.blit(text, (100, y))
        y += 40

    buttons = [
        Button("返回主選單", 300, 500, 200, 50, go_main_menu),
    ]

    for button in buttons:
        button.draw(screen)

    return buttons


def draw_settings():
    screen.fill(BLACK)

    title = subtitle_font.render("設定", True, YELLOW)
    title_rect = title.get_rect(center=(WIDTH // 2, 90))
    screen.blit(title, title_rect)

    sound_text = "音效：開" if sound_on else "音效：關"
    music_text = "背景音樂：開" if music_on else "背景音樂：關"

    buttons = [
        Button(sound_text, 275, 190, 250, 50, toggle_sound),
        Button(music_text, 275, 270, 250, 50, toggle_music),
        Button("返回主選單", 275, 400, 250, 50, go_main_menu),
    ]

    for button in buttons:
        button.draw(screen)

    return buttons


def draw_game():
    screen.fill((30, 30, 50))

    title = subtitle_font.render("遊戲畫面測試", True, WHITE)
    title_rect = title.get_rect(center=(WIDTH // 2, 100))
    screen.blit(title, title_rect)

    info = text_font.render("這裡之後會放正式的接金幣遊戲內容", True, WHITE)
    info_rect = info.get_rect(center=(WIDTH // 2, 180))
    screen.blit(info, info_rect)

    hint = text_font.render("按 ESC 開啟暫停選單", True, YELLOW)
    hint_rect = hint.get_rect(center=(WIDTH // 2, 240))
    screen.blit(hint, hint_rect)

    # 先畫一個簡單角色示意
    pygame.draw.rect(screen, BLUE, (360, 470, 80, 40), border_radius=8)

    # 先畫一個金幣示意
    pygame.draw.circle(screen, YELLOW, (400, 330), 25)

    return []


def draw_pause_menu():
    screen.fill(BLACK)

    title = subtitle_font.render("遊戲暫停", True, YELLOW)
    title_rect = title.get_rect(center=(WIDTH // 2, 90))
    screen.blit(title, title_rect)

    sound_text = "音效：開" if sound_on else "音效：關"

    buttons = [
        Button("繼續遊戲", 275, 170, 250, 50, resume_game),
        Button("重新開始", 275, 240, 250, 50, restart_game),
        Button(sound_text, 275, 310, 250, 50, toggle_sound),
        Button("返回主選單", 275, 380, 250, 50, go_main_menu),
        Button("離開遊戲", 275, 450, 250, 50, quit_game),
    ]

    for button in buttons:
        button.draw(screen)

    return buttons

def go_main_settings():
    global current_screen
    current_screen = "main_settings"
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
    elif current_screen == "game":
        buttons = draw_game()
    elif current_screen == "pause":
        buttons = draw_pause_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if current_screen == "game":
                    go_pause()
                elif current_screen == "pause":
                    resume_game()
                elif current_screen in ["how_to_play", "settings"]:
                    go_main_menu()

        for button in buttons:
            button.check_click(event)

    pygame.display.update()
    clock.tick(60)
