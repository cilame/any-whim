import pygame
from pygame.locals import *

# 主要处理框架问题，实现普通的各类默认配置
# 让coding更方便，开发更简单


# 注意 pygame.event.get() 函数不会将当前event作为queue数据形式脱出
# 所以 pygame.event.get() 函数只是获取当前循环中的



class artist:
    '''
    #==============================================
    # 所有表演资源的存储
    #==============================================
    '''
    def __init__(self,
                 screen,
                 background,
                 ticks):
        self.screen     = screen
        self.screen_pos = (0,0)
        self.background = background
        self.ticks      = ticks
        self.group      = pygame.sprite.Group()
        self.framerate  = pygame.time.Clock()

    def blit_bg(self):
        # 背景
        if self.background:
            self.screen.blit(self.background, self.screen_pos)# 默认
        else:
            self.screen.fill((0,0,100))

    def update(self,ticks=None):
        self.blit_bg()

        ticks = ticks if ticks is not None else self.ticks
        self.framerate.tick(ticks)
        ticks = pygame.time.get_ticks()

        self.group.update(ticks)
        self.group.draw(self.screen)

        if pygame.key.get_pressed()[K_ESCAPE]: exit()
        for event in pygame.event.get():
            if event.type == QUIT: exit()

        pygame.display.update()


class actor(pygame.sprite.Sprite):
    '''
    #==============================================
    # 行为对象，主要用于加载各类对象图片
    #==============================================
    '''
    def __init__(self,
                 img=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.load_img(img)
        self.rect = self.image.get_rect() if self.image else None

    def load_img(self,img):
        try:
            image = pygame.image.load(img).convert_alpha()
        except:
            print("无法加载图片.",img)
            image = None
        return image

    def update(self,ticks):
        x, y = pygame.mouse.get_pos()
        x-= self.image.get_width() // 2
        y-= self.image.get_height() // 2
        self.rect[0] = x
        self.rect[1] = y

        # 测试删除对象本身
        if pygame.key.get_pressed()[K_s]:
            self.kill()


class initer:
    '''
    #==============================================
    # 处理许多默认值的初始化工作
    #==============================================
    '''
    def __init__(self,
                 bg_filename    = None,
                 size           = (640, 480),    # screen
                 flag           = 0,
                 depth          = 32,
                 title          = 'vslg',        # title
                 ticks          = 32
                 ):
        
        self.ticks      = ticks
        self.screen     = pygame.display.set_mode(size,flag,depth)
        self.background = self.create_background(bg_filename)
        self.artist     = artist(self.screen, self.background, self.ticks)
        pygame.display.set_caption(title)

    def create_background(self,bg_filename):
        try:
            background = pygame.image.load(bg_filename).convert()
        except:
            print("无法加载bg_filename，使用默认背景。")
            background = None
        return background

    def regist(self,filename):
        # 将组件注册进整体循环里面
        a = actor(filename)
        self.artist.group.add(a)

    def run(self):
        while True:
            self.artist.update()



if __name__ == "__main__":
    bg = './sushiplate.jpg'
    tk = 120 # 帧率

    cur = 'fugu.png'
    
    s = initer(bg,ticks=tk)
    s.regist(cur)
    s.run()








