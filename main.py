import pyxel
import random
import json
import os

# 加载颜色配置文件
def load_colors():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'colors.json'), 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载颜色配置文件失败: {e}")
        return None

# 全局颜色配置
color_config = load_colors()

class Fungus:
    # 动态加载颜色调色板
    @staticmethod
    def get_color_palette():
        if color_config and 'colors' in color_config:
            return [int(color['hex'], 16) for color in color_config['colors']]
        else:
            # 默认颜色，以防配置文件加载失败
            return [0xFF004D, 0x00E436, 0x29ADFF, 0xFFA300, 0x83769C, 0x39C5BB]

    def __init__(self, x, y, color=None):
        self.x = x
        self.y = y
        self.health = 100
        self.color = color if color else random.choice(self.get_color_palette())
        self.reproduction_cooldown = 0

    def reproduce(self):
        return Fungus(new_x, new_y, self.color)

    def update(self):
        self.health = max(0, self.health - 1)
        if self.health > 80 and self.reproduction_cooldown <= 0:
            new_x = self.x + random.choice([-10,0,10])
            new_y = self.y + random.choice([-10,0,10])
            if 0 <= new_x <= pyxel.width and 0 <= new_y <= pyxel.height:
                self.reproduction_cooldown = 30
                return Fungus(new_x, new_y, self.color)
        return None

class TribUngus:
    def __init__(self):
        while True:
            try:
                self.size = int(input('请输入像素尺寸（128-1024）：') or 512)
                if 128 <= self.size <= 1024:
                    break
                print('请输入128-1024之间的整数')
            except ValueError:
                print('请输入有效数字')
        pyxel.init(self.size, self.size, title="菌类战争", fps=24)
        
        # 设置自定义颜色
        if color_config:
            # 加载默认调色板
            if 'default_palette' in color_config:
                default_colors = [int(color, 16) for color in color_config['default_palette']]
                pyxel.colors = default_colors.copy()
            
            # 应用自定义颜色
            if 'custom_colors' in color_config:
                for index, hex_color in color_config['custom_colors'].items():
                    pyxel.colors[int(index)] = int(hex_color, 16)
        
        self.fungi = [Fungus(random.randint(0, pyxel.width), random.randint(0, pyxel.height))]
        pyxel.mouse(True)
        self.fungi = [Fungus(random.randint(0,384), random.randint(0,384)) for _ in range(3)]
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            if 0 <= mx <= pyxel.width and 0 <= my <= pyxel.height:
                self.fungi.append(Fungus(mx, my))
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        new_fungi = []
        for fungus in self.fungi:
            fungus.reproduction_cooldown -= 1
            offspring = fungus.update()
            if offspring:
                new_fungi.append(offspring)
        self.fungi += new_fungi

    def draw(self):
        pyxel.cls(7)
        for fungus in self.fungi:
            # 将16进制颜色映射回索引
            color_index = self._get_color_index(fungus.color)
            pyxel.rect(fungus.x, fungus.y, 10, 10, color_index)
        base_size = self.size // 32
        line_height = base_size * 10
        pyxel.text(base_size, base_size, f'分辨率: {self.size}x{self.size}', 7 if self.size < 256 else 0)
        stats_x = self.size - 12*base_size
        pyxel.text(stats_x, base_size, f'菌群数量: {len(self.fungi)}', 0)
        pyxel.text(stats_x, base_size + line_height, f'FPS: {pyxel.frame_count%60}', 0)
    
    def _get_color_index(self, hex_color):
        # 从配置文件中获取颜色映射
        if color_config and 'colors' in color_config:
            for color in color_config['colors']:
                if int(color['hex'], 16) == hex_color:
                    return color['index']
        
        # 默认颜色映射，以防配置文件加载失败
        color_map = {
            0xFF004D: 8,  # RED
            0x00E436: 11, # GREEN
            0x29ADFF: 12, # BLUE
            0xFFA300: 9,  # ORANGE
            0x83769C: 13, # PURPLE
            0x39C5BB: 3,  # MIKU
        }
        return color_map.get(hex_color, 8)  # 默认返回红色索引

if __name__ == "__main__":
    TribUngus()