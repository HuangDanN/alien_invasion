# 游戏统计信息
class GameStats:
    # 初始化信息
    def __init__(self, ai_setting):
        self.ai_setting = ai_setting
        self.reset_stats()
        # 游戏活动状态标志
        self.game_active = False

        self.high_score = 0

    # 重置信息
    def reset_stats(self):
        self.ships_left = self.ai_setting.ship_limit
        self.score = 0
        self.level = 1
