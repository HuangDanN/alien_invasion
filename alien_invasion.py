import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from game_stats import GameStats
import game_functions as gf
from button import Button
from scoredboard import Scoreboard


def run_game():
    # 初始化游戏   创建一个屏幕对象
    pygame.init()
    # 获取配置信息
    ai_setting = Settings()
    # 设置显示窗
    screen = pygame.display.set_mode((ai_setting.screen_width, ai_setting.screen_height))
    # 设置标题
    pygame.display.set_caption("Alien invasion")
    # 创建统计信息
    stats = GameStats(ai_setting)
    # 获取飞船
    ship = Ship(ai_setting, screen)
    # 创建存储子弹编组
    bullets = Group()
    #  创建外星人群
    aliens = Group()
    gf.create_fleet(ai_setting, screen, aliens, ship)
    # 创建PLAY按钮
    play_button = Button(ai_setting, screen, "Play")
    # 创建计分牌
    sb = Scoreboard(ai_setting, screen, stats)
    while True:
        # 监听键盘输入
        gf.check_event(ship, ai_setting, screen, bullets, stats, play_button, aliens, sb)
        if stats.game_active:
            ship.update()
            gf.update_bullets(bullets, aliens, ai_setting, screen, ship, sb, stats)
            gf.update_aliens(ai_setting, aliens, ship, screen, bullets, stats, sb)
        # 刷新屏幕
        gf.update_screen(ai_setting, screen, ship, bullets, aliens, play_button, stats, sb)


run_game()
