from pygame import init, display, time, image, mouse, Surface, sprite, font, event, mixer, QUIT, quit
from random import randint
from datetime import datetime

width = 1280
height = 720
framerate = 30
diff_coef = indexx = 1 
last_edit_difficult = last_del_save = k_x = k_y = 0
init()
# mixer.init() #звук
window = display.set_mode((width, height))
check_bar_list = ['', '•', '', '']
display.set_caption('Кроличий побег')
clock = time.Clock()

fone = image.load('image/foneHD.png')
fone_menu = image.load('image/foneHD_blur.png')
rabbit_img = image.load('image/rabbit1.png')


class Button:
    def __init__(self, width, height = 40, left_indent = 0, top_ident = 5):
        self.width = width
        self.height = height
        self.left_indent = left_indent
        self.top_indent = top_ident
        self.fone = Surface((self.width, self.height))
        self.fone.fill((255,255,255))
        self.fone.set_alpha(0)

    def draw(self, x, y, text, command = None, dat = None):
        cursor = mouse.get_pos()
        click = mouse.get_pressed()

        if x < cursor[0] < x + self.width:
            if y < cursor[1] < y + self.height:
                self.fone.set_alpha(150)

                if click[0] and command != None:
                    if dat != None:
                        command(dat)
                    else:
                        command()

        self.rect = self.fone.get_rect()
        self.rect.center = ((x, y))
        window.blit(self.fone, (x, y))
        print_text(text, x + self.top_indent, y + self.left_indent)


class Rabbit(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        global diff_coef
        self.speed = randint(10, 15) * diff_coef
        self.image = rabbit_img
        self.rect = self.image.get_rect()
        self.rect.center = (-50, 525 + randint(0, 95))

    def update(self):
        self.rect.x += self.speed
        

def print_text(message, x , y, font_color = (255, 255, 0), font_type = 'Arial', font_size = 30):
    font_type = font.SysFont(font_type, font_size)
    text = font_type.render(message, True, font_color)
    window.blit(text, (x, y))


def menu():    
    window.blit(fone_menu, (0, 0))
    Button(217).draw(210, 150,'Небольшой побег', small_G)
    Button(185).draw(225, 225, 'Средний побег', average_G)
    Button(187).draw(225, 300, 'Большой побег', long_G)
    Button(110).draw(902, 188, 'Правила', to_regulation)
    Button(132).draw(892, 265, 'Настройки', to_settings)
    print_text('Кроличий побег', 545, 50)
    print_text(f'Рекорд: {old_r_s}', 565, 150)
    print_text(f'Рекорд: {old_r_a}', 565, 225)
    print_text(f'Рекорд: {old_r_l}', 565, 300)    


def regulation():
    window.blit(fone_menu, (0, 0))
    Button(95).draw(10, 10, 'В меню', to_menu)
    print_text('Суть игры в том, чтобы поймать как можно больше сбегающих с фермы кроликов.', 150, 285)
    print_text('Они бегут друг за другом. За каждого пойманного кролика вы получаете от 5 до 150 очков,', 105, 335)
    print_text(' в зависимоти от времени, за которе вы его поймали. Во время небольшого побега сбегает', 100, 385)
    print_text('25 кроликов, во время среднего 50 кроликов, а во время большого 75 кроликов.', 167, 435)


def settings():
    global last_change
    window.blit(fone_menu, (0, 0))
    Button(95).draw(10, 10, 'В меню', to_menu)
    Button(75).draw(283, 100, 'Легко', change,  '0.75')
    Button(180).draw(227, 175, 'По умолчанию', change, '1')
    Button(100).draw(268, 250, 'Средне', change, '1.25')
    Button(100).draw(270, 325, 'Сложно', change, '1.5')
    Button(262).draw(185, 400, 'Сбросить сохранения', del_save)
    print_text(check_bar_list[0], 265, 90, font_size = 50)
    print_text(check_bar_list[1], 210, 165, font_size = 50)
    print_text(check_bar_list[2], 250, 240, font_size = 50)
    print_text(check_bar_list[3], 250, 315, font_size = 50)
    now = int(datetime.now().strftime('%S'))
    if last_change != indexx and (now - int(last_edit_difficult)) < 1:
        print_text('Сложность изменена!', 190, 475)
    elif now - int(last_del_save) < 1:
        print_text('Сохранения сброшены!', 179, 475)
    elif last_change != indexx:
        last_change = indexx

    

def del_save():
    global saves_old, last_del_save
    saves_old = [[0,0,0], [0,0,0], [0,0,0], [0,0,0]]
    last_del_save = datetime.now().strftime('%S')
    with open('save_records.txt','w') as saves_w:
        for i in range(4):
            saves_w.write(f'0|0|0\n')
    

def change(n):
    global diff_coef, indexx, last_edit_difficult, check_bar_list
    diff_coef = float(n)
    check_bar_list = ['', '', '', '']
    if n == '0.75':
        indexx = 0
    elif n == '1':
        indexx = 1
    elif n == '1.25':
        indexx = 2
    elif n == '1.5':
        indexx = 3
    check_bar_list[indexx] = '•'
    last_edit_difficult = datetime.now().strftime('%S')


def small_G():
    go_game(25)

def average_G():
    go_game(50)

def long_G():
    go_game(75)


def go_game(lenn):
    global n, s, start, all_sprites, run_status, max_n, rabbit, framerate

    rabbit = Rabbit()
    all_sprites = sprite.Group()
    all_sprites.add(rabbit)
    n = s = 0
    max_n = lenn
    run_status = 'game'
    framerate = 60
    start = datetime.now().strftime('%S.%f')


def game():
    global n, s, start, all_sprites, run_status, rabbit, old_r, framerate, k_y, k_x

    window.blit(fone, (0,0))
    window.blit(font.SysFont("Arial", 40).render(str(s) , True, (255,165,0)), (612, 25))

    if rabbit.rect.x >= 1330:
        n += 1

        if n < max_n:
            rabbit = Rabbit()
            all_sprites.add(rabbit)

        start = datetime.now().strftime('%S.%f')

    elif rabbit.rect.x <= k_x and rabbit.rect.x + 100 >= k_x and rabbit.rect.y <= k_y and rabbit.rect.y + 100 >= k_y:
        n += 1
        if n < max_n:
            rabbit = Rabbit()
            all_sprites = sprite.Group()
            all_sprites.add(rabbit)

        k_x = k_y = 0
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
        framerate = 30
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
                    saves1.write(f'{saves_new[0]}|{saves_new[1]}|{saves_new[2]}\n')

    
    else:
        k_x = k_y = 0


def to_menu():
    global run_status, old_r_a, old_r_l, old_r_s
    old_r_s, old_r_a, old_r_l = saves_old[indexx]
    run_status = 'menu'

def to_regulation():
    global run_status
    run_status = 'regulation'

def to_settings():
    global run_status, last_change
    last_change = indexx
    run_status = 'settings'


def game_over():
    window.blit(fone_menu, (0, 0))
    window.blit(font.SysFont("Arial", 30).render('Игра окончена', True, (255,255,0)), (555, 50))
    window.blit(font.SysFont("Arial", 30).render(f'Рекорд: {str(old_r)}', True, (255,255,0)), (570, 125))
    window.blit(font.SysFont("Arial", 30).render(f'Очки: {str(s)}', True, (255,255,0)), (580, 175))
    
    Button(95).draw(10, 10, 'В меню', to_menu)
    

all_sprites = sprite.Group()
with open('save_records.txt') as f:
    saves_old = [list(map(int, f.readline().split('|'))) for i in range(4)]

to_menu()

while True:
    clock.tick(framerate)
    for even_t in event.get():
        if even_t.type == QUIT:
            quit()        

    if mouse.get_pressed()[0]:
        k_x, k_y = mouse.get_pos()

    event.get()

    if run_status == 'menu':
        menu()
    elif run_status == 'game':
        framerate = 60
        game()
        all_sprites.update()
        all_sprites.draw(window)
    elif run_status == 'game_over':
        game_over()
    elif run_status == 'regulation':
        regulation()
    elif run_status == 'settings':
        settings()
    
    display.flip()