# 飞船模块
import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_setting, screen):
        super().__init__()
        self.screen = screen
        self.ai_setting = ai_setting
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)
        # 移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """根据标志 移动飞船位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_setting.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_setting.ship_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.rect.bottom -= self.ai_setting.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.rect.bottom += self.ai_setting.ship_speed_factor
        # 根据self.center 更新rect
        self.rect.centerx = self.center

    def blitme(self):
        """指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    # 初始化飞船位置
    def center_ship(self):
        self.center = self.screen_rect.centerx