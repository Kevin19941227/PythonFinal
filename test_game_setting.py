import pygame
import sys

pygame.init()

# =========================
# 視窗設定
# =========================
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch or Crash 接不可失 - 遊戲中設定測試")

# =========================
# 顏色設定
# =========================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 210, 80)
BLUE = (80, 160, 255)
DARK_BLUE = (30, 30, 60)
GRAY = (90, 90, 90)
LIGHT_GRAY = (180, 180, 180)
RED = (255, 100, 100)

# =========================
# 中文字型
# =========================
font_path = "C:/Windows/Fonts/msjh.ttc"

title_font = pygame.font.Font(font_path, 46)
button_font = pygame.font.Font(font_path, 28)
text_font = pygame.font.Font(font_path, 24)
small_font = pygame.font.Font(font_path, 20)

# =========================
# 遊戲狀態
# =========================
current_screen = "game"
sound_on = True


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
            color = GRAY

        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=10)

        text_surface = button_font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()


# =========================
# 功能函式
# =========================
def go_game():
    global current_screen
    current_screen = "game"


def go_game_settings():
    global current_screen
    current_screen = "game_settings"


def go_main_menu():
    global current_screen
    current_screen = "main_menu"


def toggle_sound():
    global sound_on
    sound_on = not sound_on


def quit_game():
    pygame.quit()
    sys.exit()


# =========================
# 假遊戲畫面
# =========================
def draw_game_screen():
    screen.fill(DARK_BLUE)

    # 上方資訊列
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 70))

    score_text = text_font.render("分數：0", True, WHITE)
    screen.blit(score_text, (30, 22))

    life_text = text_font.render("生命：3", True, WHITE)
    screen.blit(life_text, (600, 22))

    # 設定按鈕
    buttons = [
        Button("設定", 690, 15, 90, 40, go_game_settings)
    ]

    # 畫出假金幣
    pygame.draw.circle(screen, YELLOW, (400, 220), 35)
    coin_text = small_font.render("金幣", True, BLACK)
    coin_rect = coin_text.get_rect(center=(400, 220))
    screen.blit(coin_text, coin_rect)

    # 畫出假炸彈
    pygame.draw.circle(screen, RED, (250, 180), 28)
    bomb_text = small_font.render("炸彈", True, WHITE)
    bomb_rect = bomb_text.get_rect(center=(250, 180))
    screen.blit(bomb_text, bomb_rect)

    # 畫出假玩家
    pygame.draw.rect(screen, BLUE, (350, 480, 100, 45), border_radius=12)
    player_text = small_font.render("玩家", True, WHITE)
    player_rect = player_text.get_rect(center=(400, 502))
    screen.blit(player_text, player_rect)

    # 提示文字
    hint = small_font.render("這是暫時的遊戲畫面，之後可接上正式接金幣玩法", True, LIGHT_GRAY)
    hint_rect = hint.get_rect(center=(WIDTH // 2, 560))
    screen.blit(hint, hint_rect)

    for button in buttons:
        button.draw(screen)

    return buttons


# =========================
# 遊戲中設定畫面
# =========================
def draw_game_settings():
    screen.fill(BLACK)

    title = title_font.render("遊戲設定", True, YELLOW)
    title_rect = title.get_rect(center=(WIDTH // 2, 100))
    screen.blit(title, title_rect)

    sound_text = "音效：開" if sound_on else "音效：關"

    buttons = [
        Button(sound_text, 275, 190, 250, 55, toggle_sound),
        Button("返回遊戲", 275, 270, 250, 55, go_game),
        Button("返回主選單", 275, 350, 250, 55, go_main_menu),
        Button("離開遊戲", 275, 430, 250, 55, quit_game),
    ]

    for button in buttons:
        button.draw(screen)

    return buttons


# =========================
# 假主選單
# =========================
def draw_main_menu():
    screen.fill(BLACK)

    title = title_font.render("Catch or Crash", True, YELLOW)
    title_rect = title.get_rect(center=(WIDTH // 2, 90))
    screen.blit(title, title_rect)

    subtitle = text_font.render("接不可失", True, WHITE)
    subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, 145))
    screen.blit(subtitle, subtitle_rect)

    buttons = [
        Button("開始遊戲", 275, 220, 250, 55, go_game),
        Button("遊戲說明", 275, 295, 250, 55, go_how_to_play),
        Button("設定", 275, 370, 250, 55, go_main_settings),
        Button("離開遊戲", 275, 445, 250, 55, quit_game),
    ]

    for button in buttons:
        button.draw(screen)

    return buttons

def go_how_to_play():
    global current_screen
    current_screen = "how_to_play"


def go_main_settings():
    global current_screen
    current_screen = "main_settings"
# =========================
# 主迴圈
# =========================
clock = pygame.time.Clock()

while True:
    buttons = []

    if current_screen == "game":
        buttons = draw_game_screen()
    elif current_screen == "game_settings":
        buttons = draw_game_settings()
    elif current_screen == "main_menu":
        buttons = draw_main_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if current_screen == "game":
                    go_game_settings()
                elif current_screen == "game_settings":
                    go_game()

        for button in buttons:
            button.check_click(event)

    pygame.display.update()
    clock.tick(60)