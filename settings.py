class Settings():
    '''存储外星人入侵中所有的设置'''

    def __init__(self):
        '''初始化设置'''
        self.screen_width = 900
        self.screen_height = 600
        self.bg_color = (230, 230, 230)    # 设置背景色  灰色

        self.ship_speed_factor = 2   # 飞船移动速度
        self.ship_limit = 3            # 飞船数量
        self.zombie_speed_factor = 0.5   # 外星人移动速度
        self.fleet_drop_speed = 10
        self.fleet_direction = 1       # 1表示右移

        self.bullet_speed_factor = 0.5  # 子弹移动速度
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 8        # 允许屏幕中出现子弹的数量

        self.speedup_scale = 1.2      # 以什么样的速度加快游戏节奏
        self.score_scale = 1.5

        self.initialize_dynamic_settings()      # 初始化随游戏进行而变化的设置

        self.ship_image_path = 'images/dog.bmp'    # 飞船图片路径
        self.zombie_image_path = 'images/zombie.jpg'

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed_factor = 1.8
        self.bullet_speed_factor = 0.5
        self.zombie_speed_factor = 0.5

        self.fleet_direction = 1

        self.zombie_points = 50  # 记分

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.zombie_speed_factor *= self.speedup_scale
        self.zombie_points = int(self.zombie_points * self.score_scale)


