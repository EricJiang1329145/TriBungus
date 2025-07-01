import pyxel
import random

class Fungus:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 100  # 初始生命力
        self.color = 8 + (self.health // 25)  # 根据生命力选择8-11号红色系
        self.reproduction_cooldown = 0

    def update(self):
        # 自然消耗
        self.health = max(0, self.health - 1)
        
        # 繁殖逻辑
        if self.health > 80 and self.reproduction_cooldown <= 0:
            # 寻找相邻空位
            new_x = self.x + random.choice([-10, 0, 10])
            new_y = self.y + random.choice([-10, 0, 10])
            
            # 检查新位置是否在边界内
            if 0 <= new_x <= pyxel.width and 0 <= new_y <= pyxel.height:
                self.reproduction_cooldown = 30  # 繁殖冷却时间
                return Fungus(new_x, new_y)
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
        self.fungi = [Fungus(random.randint(0, pyxel.width), random.randint(0, pyxel.height)) for _ in range(3)]
        pyxel.mouse(True)
        
        self.fungi = [Fungus(random.randint(0,384), random.randint(0,384)) 
                     for _ in range(3)]
        
        pyxel.run(self.update, self.draw)

    def update(self):
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
            color_index = 8 + (fungus.health // 25)  # 8深红 -> 11浅红
            pyxel.rect(fungus.x, fungus.y, 10, 10, color_index)
        
        # 调整UI元素位置
        pyxel.text(10, 10, f"菌群数量: {len(self.fungi)}", 0)
        pyxel.text(10, 25, f"FPS: {pyxel.frame_count%60}", 0)
        # 显示当前分辨率
        pyxel.text(5, 5, f'分辨率: {self.size}x{self.size}', 0)

if __name__ == "__main__":
    TribUngus()