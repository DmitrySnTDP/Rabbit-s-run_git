from pygame import * 
from random import randint
from datetime import datetime
import sys


width = 1280
height = 720
default_framerate = 60
diff_coef = 1
indexx = 0
n = 0
k_x = 0
k_y = 0
n = 0
init()
# mixer.init() #звук
window = display.set_mode((width, height))
display.set_caption('Кроличий побег')
clock = time.Clock()

fone = image.load('image/foneHD.png')
fone_menu = image.load('image/foneHD_blur.png')
small_run_status = image.load('image/little_game1.png')
average_run_status = image.load('image/average_game1.png')
long_run_status = image.load('image/long_game1.png')
regulat = image.load('image/reg1.png')
v_menu = image.load('image/v_menu1.png')
v_set = image.load('image/settings.png')
default_img = image.load('image/default.png')
easy_img = image.load('image/easy.png')
medium_img = image.load('image/medium.png')
hard_img = image.load('image/hard.png')
save_set_img = image.load('image/save_set.png')
reset_save_img = image.load('image/reset_save.png')


# class Button:
#     def __init__(self, x, y, width, height, color, text):
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.color = color
#         self.text = text
    
#     def draw(self, window):
#         pass
#     def update_button(self):
#         pass
    
#     def draw_button():
#         if button_press:



class Rabbit(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        global diff_coef
        self.speed = randint(5, 10) * diff_coef
        self.image = image.load('image/rabbit1.png')
        self.rect = self.image.get_rect()
        self.rect.center = (50, 525 + randint(0, 95))

    def update(self):
        self.rect.x += self.speed
        

# текст: window.blit(font.SysFont("Arial", 30).render('', True, (255,255,0)), (100, 100))

# def kurs(event):
#     global k_x,k_y
#     k_x = event.x
#     k_y = event.y


def menu():
    global old_r_s, old_r_a, old_r_l,saves_old, run_status
    saves_old = []

    with open('save_records.txt') as saves:
        for i in range(4):
            save_old = []
            for j in range(3):
                save_old.append(int(saves.readline()))
            saves_old.append(save_old)

    if diff_coef == 1:
        old_r_s,old_r_a,old_r_l = saves_old[0]
    elif diff_coef == 0.75:
        old_r_s,old_r_a,old_r_l = saves_old[1]
    elif diff_coef == 1.25:
        old_r_s,old_r_a,old_r_l = saves_old[2]
    elif diff_coef == 1.5:
        old_r_s,old_r_a,old_r_l = saves_old[3]

    window.blit(fone_menu, (0,0))
    run_status = 'go_game'

def go_game(lenn):
    global n, s, start, all_sprites, run_status, max_n, rabbit
    all_sprites = sprite.Group()
    rabbit = Rabbit()
    all_sprites.add(rabbit)
    n = s = 0
    max_n = lenn
    start = datetime.now().strftime('%S.%f')
    run_status = 'game'


def game():
    global k_x, k_y, n, s, start, all_sprites, run_status, rabbit, old_r

    window.blit(fone, (0,0))
    window.blit(font.SysFont("Arial", 35).render(str(s) , True, (255,165,0)), (610, 25))

    if rabbit.rect.x >= 1330:
        n += 1

        if n < max_n:
            rabbit = Rabbit()
            all_sprites.add(rabbit)


        start = datetime.now().strftime('%S.%f')
    elif rabbit.rect.x - 50 <= k_x and rabbit.rect.x + 50 >= k_x and rabbit.rect.y - 50 <= k_y and rabbit.rect.y + 50 >= k_y:
        n += 1
        if n < max_n:
            rabbit = Rabbit()
            all_sprites.add(rabbit)

        # k_x = 0
        # k_y = 0
        end = datetime.now().strftime('%S.%f')
        times = (float(end) - float(start)) * diff_coef
        start = end

        if times <= 0.1:
            s += 150
        elif times <= 0.25:
            s += 100
        elif times <= 0.36:
            s += 75
        elif times <= 0.5:
            s += 50
        elif times <= 0.75:
            s += 25
        elif times <= 1.0:
            s += 10
        else:
            s += 5
    
    if n == max_n:
        run_status = 'game_over'
        if n == 25:
            old_r = old_r_s
        elif n == 50:
            old_r = old_r_a
        else:
            old_r = old_r_l

        with open('save_records.txt','w') as saves1:
            if s >= old_r and n == 25:
                saves_old[indexx][0] = s
            elif s >= old_r and n == 50:
                saves_old[indexx][1] = s
            elif s >= old_r and n == 75:
                saves_old[indexx][2] = s
                
            for saves_new in saves_old:
                for save_new in saves_new:
                    saves1.write(str(save_new) + '\n')

    
    # else:
    #     None
        # k_x = 0
        # k_y = 0


def to_menu():
    global run_status
    run_status = 'menu'


def game_over():
    window.blit(fone_menu,(0, 0))
    window.blit(font.SysFont("Arial", 30).render('Рекорд:', True, (255,255,0)), (575, 125))
    window.blit(font.SysFont("Arial", 30).render(str(old_r), True, (255,255,0)), (735, 125))
    window.blit(font.SysFont("Arial", 30).render('Очки:', True, (255,255,0)), (595, 175))
    window.blit(font.SysFont("Arial", 30).render(str(s), True, (255,255,0)), (735, 175))
    window.blit(font.SysFont("Arial", 30).render('Игра окончена', True, (255,255,0)), (int(width*0.45), 50))

    rectt = Rect(50,50,100,100)
    surf = Surface(rectt.size, SRCALPHA)
    draw.rect(surf, (100,0,0), rectt)
    # Vmenu = Button(image = v_menu,highlightthickness = 0,command = to_menu)
    # canvas.create_window((10,10), anchor = "nw", window = Vmenu)
    

all_sprites = sprite.Group()
button_sprites = sprite.Group()
run_status = 'menu'
while True:
    clock.tick(default_framerate)
    for even_t in event.get():
        if even_t.type == QUIT:
            pass
            quit()
            sys.exit()

    if run_status == 'menu':
        menu()
    elif run_status == 'go_game':
        go_game(1)
    elif run_status == 'game':
        game()
        all_sprites.update()
        all_sprites.draw(window)
    elif run_status == 'game_over':
        game_over()


    
    
    
    display.flip()
    
