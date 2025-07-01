import pyxel
import random

class Fungus:
    class ColorPalette:
        RED = 8
        GREEN = 3
        BLUE = 1
        ORANGE = 9
        PURPLE = 5
        MIKU = 2
        CHINA_RED = 4

    COLOR_PALETTE = [
        ColorPalette.RED,
        ColorPalette.GREEN,
        ColorPalette.BLUE,
        ColorPalette.ORANGE,
        ColorPalette.PURPLE,
        ColorPalette.MIKU,
        ColorPalette.CHINA_RED
    ]

    def __init__(self, x, y, color=None):
        self.x = x
        self.y = y
        self.health = 100
        self.color = color if color else random.choice(self.COLOR_PALETTE)
        self.reproduction_cooldown = 0

    def reproduce(self):
        # 繁殖时继承颜色
        return Fungus(new_x, new_y, self.color)

    def update(self):
        # 自然消耗
        self.health = max(0, self.health - 1)
        
        # 繁殖逻辑
        if self.health > 80 and self.reproduction_cooldown <= 0:
            # 生成有效坐标
            new_x = self.x + random.choice([-10,0,10])
            new_y = self.y + random.choice([-10,0,10])
            
            if 0 <= new_x <= pyxel.width and 0 <= new_y <= pyxel.height:
                self.reproduction_cooldown = 30
                return Fungus(new_x, new_y, self.color)  # 传递坐标和颜色
        return None

class TribUngus:
    def __init__(self):
        # 获取用户输入
        while True:
            try:
                self.size = int(input('请输入像素尺寸（128-1024）：') or 512)
                if 128 <= self.size <= 1024:
                    break
                print('请输入128-1024之间的整数')
            except ValueError:
                print('请输入有效数字')
        
        pyxel.init(self.size, self.size, title="菌类战争", fps=24)
        # 配置调色板RGB值
        pyxel.colors[8] = 0xFF0000   # 红色
        pyxel.colors[3] = 0x00FF00   # 绿色
        pyxel.colors[1] = 0x0000FF   # 蓝色
        pyxel.colors[9] = 0xFFA500   # 橙色
        pyxel.colors[5] = 0x800080   # 紫色
        
        # 新增经典颜色
        pyxel.colors[2] = 0x39C5BB   # 初音绿
        pyxel.colors[4] = 0xCD071E   # 中国红
        self.fungi = [Fungus(random.randint(0, pyxel.width), random.randint(0, pyxel.height))]
        pyxel.mouse(True)
        
        self.fungi = [Fungus(random.randint(0,384), random.randint(0,384)) 
                     for _ in range(3)]
        
        pyxel.run(self.update, self.draw)

    def update(self):
        # 添加鼠标点击生成
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            if 0 <= mx <= pyxel.width and 0 <= my <= pyxel.height:
                self.fungi.append(Fungus(mx, my))
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        # 更新所有菌类
        new_fungi = []
        for fungus in self.fungi:
            fungus.reproduction_cooldown -= 1
            offspring = fungus.update()
            if offspring:
                new_fungi.append(offspring)
        self.fungi += new_fungi

    def draw(self):
        pyxel.cls(7)
        
        # 增大菌类显示尺寸为8x8像素
        for fungus in self.fungi:
            # 绘制时使用颜色属性
            pyxel.rect(fungus.x, fungus.y, 10, 10, fungus.color)
        
        # 调整UI元素位置
        # 动态UI布局
        base_size = self.size // 32
        line_height = base_size * 10
        
        # 分辨率显示（左上角）
        pyxel.text(base_size, base_size, f'分辨率: {self.size}x{self.size}', 7 if self.size < 256 else 0)
        
        # 游戏数据（右上角）
        stats_x = self.size - 12*base_size
        pyxel.text(stats_x, base_size, f'菌群数量: {len(self.fungi)}', 0)
        pyxel.text(stats_x, base_size + line_height, f'FPS: {pyxel.frame_count%60}', 0)

if __name__ == "__main__":
    TribUngus()