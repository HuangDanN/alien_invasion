import pygame.font


# 按钮类
class Button:
    # 初始化
    def __init__(self, ai_setting, screen, msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        # 设置按钮长宽
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        # 指定默认字体渲染  字号
        self.font = pygame.font.SysFont(None, 48)
        # 创建按钮的rect 对象，并居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        # 按钮标签只需创建一次
        self.preg_msg(msg)

    # 将msg渲染为图像，并居中
    def preg_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    # 绘制按钮，填充文本
    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
