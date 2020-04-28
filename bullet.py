import pygame
from pygame.sprite import Sprite


#  子弹类
class Bullet(Sprite):
    def __init__(self, ai_setting, screen, ship):
        # 在飞船位置创建子弹对象
        super().__init__()
        self.screen = screen
        # 在（0，0）创建一个表示子弹的矩形，在设置位置
        self.rect = pygame.Rect(0, 0, ai_setting.bullet_width, ai_setting.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        # 存储子弹位置
        self.y = float(self.rect.y)
        self.color = ai_setting.bullet_color
        self.speed_factor = ai_setting.bullet_speed_factor

    # 向上移动子弹
    def update(self):
        # 更新子弹位置数值
        self.y -= self.speed_factor
        # 更新子弹rect的位置
        self.rect.y = self.y

    # 绘制子弹
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
