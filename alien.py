import pygame
from pygame.sprite import Sprite


# 外星人类
class Alien(Sprite):
    def __init__(self, ai_setting, screen):
        super().__init__()
        self.screen = screen
        self.ai_setting = ai_setting
        # 加载外星人图像
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        # 初始化外星人最初位置
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # 外星人实际位置
        self.x = float(self.rect.x)

    # 绘制外星人
    def blitme(self):
        self.screen.blit(self.image, self.rect)

    # 更新位置
    def update(self):
        self.x += (self.ai_setting.alien_speed_factor * self.ai_setting.fleet_direction)
        self.rect.x = self.x

    # 判断外星人位置，位于边缘，返回true
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
