import sys
import pygame

from time import sleep

from bullet import *
from zombiefile import Zombie

def check_events(ai_settings, screen, stats, score, play_button,  ship, zombies, bullets, ):
    # 监视键盘和鼠标事件
    for event in pygame.event.get():

        if event.type == pygame.QUIT:  # 关闭窗口退出
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets,)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, score, play_button, ship, zombies, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, score,  play_button, ship, zombies, bullets, mouse_x, mouse_y):

    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)  # 隐藏光标
        if play_button.rect.collidepoint(mouse_x, mouse_y):
            stats.reset_stats()
            stats.game_active = True

            score.prep_score()      # 重置记分牌和等级
            score.prep_high_score()
            score.prep_level()
            score.prep_ships()

            zombies.empty()
            bullets.empty()

            creat_fleet(ai_settings, screen, ship, zombies)
            ship.center_ship()


def update_screen(ai_settings, screen, stats, score, ship, zombies, bullets, play_button):
    '''更新屏幕上的图片，并切换到新屏幕'''
    screen.fill(ai_settings.bg_color)  # 设置背景颜色
    ship.blitme()  # 绘制飞船
    zombies.draw(screen)
    score.show_score()

    # 循环子弹组里面的元素，进行绘制 为空时不执行
    for bullet in bullets.sprites():
        bullet.draw_bullet()    # 绘制子弹

    if not stats.game_active:
        play_button.draw_button()

    # 显示最新屏幕，擦拭旧屏幕
    pygame.display.flip()
    # print('1')

def check_keydown_events(event, ai_settings, screen, ship, bullets, ):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False

def update_bullets(ai_settings, screen, stats, score, ship, bullets, zombies):
    '''更新子弹位置，删除子弹'''
    bullets.update()     # 子弹组每个成员执行self.update()操作
    for bullet in bullets.sprites():
        if bullet.rect.bottom <= 0:  # 子弹出界 删除
            bullets.remove(bullet)

    check_bullet_zombie_collisions(ai_settings, screen, stats, score, ship, zombies, bullets)

def check_bullet_zombie_collisions(ai_settings, screen, stats, score, ship, zombies, bullets):
    collisions = pygame.sprite.groupcollide(bullets, zombies, True, True)

    if collisions:
        for zombies in collisions.values():
            stats.score += ai_settings.zombie_points * len(zombies)
            score.prep_score()
        check_high_score(stats, score)
    if len(zombies) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        score.prep_level()
        creat_fleet(ai_settings, screen, ship, zombies)

def update_ship(ship):
    ship.update()

def fire_bullet(ai_settings,screen,ship,bullets):
    # 创建一个子弹对象 加入到子弹组
    if len(bullets) < ai_settings.bullets_allowed:  # 子弹少于允许值时再生成
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_zombies_x(ai_settings, zombie_width):
    available_space_x = ai_settings.screen_width - 2 * zombie_width
    number_zombie_x = int(available_space_x / (2 * zombie_width))
    return number_zombie_x

def get_number_rows(ai_settings, ship_height, zombie_height):
    available_space_y = (ai_settings.screen_height - (3 * zombie_height)
                         - ship_height)
    number_rows = int(available_space_y / (2 * zombie_height))
    return number_rows

def creat_zombie(ai_settings, screen, zombies, zombie_number, row_number):
    zombie = Zombie(ai_settings, screen)
    zombie_width = zombie.rect.width
    zombie.x = zombie_width + 2 * zombie_number * zombie_width
    zombie.rect.x = zombie.x
    zombie.rect.y = zombie.rect.height + 2 * zombie.rect.height * row_number
    zombies.add(zombie)

def creat_fleet(ai_settings, screen, ship,  zombies, ):
    zombie = Zombie(ai_settings, screen)
    number_zombies_x = get_number_zombies_x(ai_settings, zombie.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, zombie.rect.height)

    for row_number in range(number_rows):
        for zombie_number in range(number_zombies_x):
            creat_zombie(ai_settings, screen, zombies, zombie_number, row_number)

def check_fleet_edges(ai_settings, zombies):
    """有外星人达到边缘时的措施"""
    for zombie in zombies.sprites():
        if zombie.check_edges():
            change_fleet_direction(ai_settings, zombies)
            break

def change_fleet_direction(ai_settings, zombies):
    """将整群外星人下移，并改变方向"""
    for zombie in zombies.sprites():
        zombie.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def update_zombies(ai_settings, stats, screen, score, ship, zombies, bullets):
    """检查是否有外星人位于屏幕边缘，并更新外星人位置"""
    check_fleet_edges(ai_settings, zombies)
    zombies.update()

    check_zombies_bottom(ai_settings, stats, screen, score, ship, zombies, bullets )
    if pygame.sprite.spritecollideany(ship, zombies):
        # print('ship hit!!!')
        ship_hit(ai_settings, stats, screen, score, ship, zombies, bullets)

def ship_hit(ai_settings, stats, screen, score, ship, zombies, bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        stats.ships_left -= 1

        score.prep_ships()

        zombies.empty()
        bullets.empty()

        creat_fleet(ai_settings, screen, ship, zombies)
        ship.center_ship()

        sleep(0.9)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_zombies_bottom(ai_settings, stats, screen, score, ship, zombies, bullets):
    """检查是否有外星人到达屏幕底端"""
    screen_rect = screen.get_rect()
    for zombie in zombies.sprites():
        if zombie.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, score, ship, zombies, bullets)
            break

def check_high_score(stats, score):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        score.prep_high_score()




