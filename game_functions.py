import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


# 响应鼠标事件
def check_event(ship, ai_setting, screen, bullets, stats, play_button, aliens, sb):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship, ai_setting, screen, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, aliens, bullets, ai_setting, screen, ship, sb)


# 点击按钮事件
def check_play_button(stats, play_button, mouse_x, mouse_y, aliens, bullets, ai_setting, screen, ship, sb):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    # 点击按钮后需重置游戏信息
    if button_clicked and not stats.game_active:
        stats.game_active = True
        stats.reset_stats()
        aliens.empty()
        bullets.empty()
        # 创建新的外星人
        create_fleet(ai_setting, screen, aliens, ship)
        ship.center_ship()
        # 隐藏光标
        pygame.mouse.set_visible(False)
        ai_setting.initialize_dynamic_settings()
        sb.prep_level()
        sb.prep_high_score()
        sb.prep_score()
        sb.prep_ships()


# 响应按键
def check_keydown_events(event, ship, ai_setting, screen, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    # elif event.key == pygame.K_UP:
    #     ship.moving_up = True
    # elif event.key == pygame.K_DOWN:
    #     ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ship, ai_setting, screen, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


# 松开按键
def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


# 更新子弹信息
def update_bullets(bullets, aliens, ai_setting, screen, ship, sb, stats):
    bullets.update()
    # for 删除元素 应该使用副本
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_setting, screen, ship, aliens, bullets, sb, stats)


# 删除碰撞子弹和外星人
def check_bullet_alien_collisions(ai_setting, screen, ship, aliens, bullets, sb, stats):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_setting.alien_points
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        bullets.empty()
        ai_setting.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_setting, screen, aliens, ship)


# 发射子弹
def fire_bullet(ship, ai_setting, screen, bullets):
    if len(bullets) < ai_setting.bullets_allowed:
        new_bullet = Bullet(ai_setting, screen, ship)
        bullets.add(new_bullet)


# 计算每行容纳多少个
def get_number_aliens_x(ai_setting, alien_width):
    available_space_x = ai_setting.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


# 计算垂直 容纳多少行外星人
def get_number_rows(ai_setting, ship_height, alien_height):
    available_space_y = (ai_setting.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


# 创建单个外星人
def create_alien(ai_setting, screen, aliens, alien_number, row_number):
    alien = Alien(ai_setting, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


# 创建外星人群
def create_fleet(ai_setting, screen, aliens, ship):
    alien = Alien(ai_setting, screen)
    number_aliens_x = get_number_aliens_x(ai_setting, alien.rect.width)
    number_rows = get_number_rows(ai_setting, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_setting, screen, aliens, alien_number, row_number)


# 更新外星人位置
def update_aliens(ai_setting, aliens, ship, screen, bullets, stats, sb):
    check_fleet_edges(ai_setting, aliens)
    aliens.update()
    check_aliens_bottom(ai_setting, aliens, ship, screen, bullets, stats, sb)
    # 检测外星人与飞船之间碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_setting, aliens, ship, screen, bullets, stats, sb)


# 处理外星人到边缘
def check_fleet_edges(ai_setting, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_setting, aliens)
            break


# 修改外星人方向
def change_fleet_direction(ai_setting, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_setting.fleet_drop_speed
    ai_setting.fleet_direction *= -1


# 外星人到底屏幕底部
def check_aliens_bottom(ai_setting, aliens, ship, screen, bullets, stats, sb):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        # 当外星人到达底部 当作 碰撞到飞船处理
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_setting, aliens, ship, screen, bullets, stats, sb)
            break


# 外星人碰撞飞船
def ship_hit(ai_setting, aliens, ship, screen, bullets, stats, sb):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_setting, screen, aliens, ship)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


# 判断最高分
def check_high_score(state, sb):
    if state.score > state.high_score:
        state.high_score = state.score
        sb.prep_high_score()


# 刷新屏幕
def update_screen(ai_setting, screen, ship, bullets, aliens, play_button, stats, sb):
    # 渲染屏幕背景色
    screen.fill(ai_setting.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # 绘制飞船
    ship.blitme()
    # 绘制外星人
    aliens.draw(screen)
    # 游戏开始 按钮隐藏
    if not stats.game_active:
        # 绘制按钮
        play_button.draw_button()
    # 显示得分
    sb.show_score()
    # 刷新屏幕内容
    pygame.display.flip()
