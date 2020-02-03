import pygame

from settings import Settings
from ship import Ship
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from pygame.sprite import Group
import game_functions as gf


def run_game():
    pygame.init()       # 初始化背景设置
    ai_settings = Settings()        # 全局设置

    screen = pygame.display.set_mode(           # 创建screen显示窗口
        (ai_settings.screen_width,ai_settings.screen_height)
    )
    pygame.display.set_caption('Alien Invasion')    # 标题

    stats = GameStats(ai_settings)   # 创建一个用于储存游戏统计信息的实例
    score = Scoreboard(ai_settings, screen, stats)
    play_button = Button(ai_settings, screen, "play")

    # 创建飞船
    ship = Ship(ai_settings,screen)
    # 创建外星人组
    zombies = Group()
    # 创建子弹编组
    bullets = Group()
    gf.creat_fleet(ai_settings, screen, ship, zombies)

    # 开始游戏主循环
    while True:
        # 监视键盘和鼠标事件
        gf.check_events(ai_settings, screen, stats, score, play_button, ship, zombies,  bullets, )

        if stats.game_active:
            # 移动飞船
            gf.update_ship(ship)
            # 更新外星人位置
            gf.update_zombies(ai_settings, stats, screen, score, ship, zombies, bullets)
            # 碰撞更新
            gf.update_bullets(ai_settings, screen, stats, score, ship, bullets, zombies)
        # 更新屏幕
        gf.update_screen(ai_settings, screen, stats, score,  ship, zombies, bullets, play_button)

run_game()
