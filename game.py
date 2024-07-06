from pygame import *
# init, display, time, image, mouse, Surface, sprite, font, event, mixer, QUIT, quit
from random import randint
from datetime import datetime
from sys import exit
from screeninfo import get_monitors


rabbit = None
resolutions_preset = ((426, 240), (640, 360), (854, 480), (1280, 720), (1920, 1080), (2560, 1440), (3840, 2160))
framerate = 45
last_edit_difficult_s = last_edit_difficult_m = last_del_save_s = last_del_save_m = 0
check_mouse_on_button = check_mouse_click_button = check_maximized = to_fullscreen = is_fullscreen = resolutions_menu_check = False
last_coords_mouse = last_coords_click_but = [0, 0, 0, 0]

rabbit_pick_up = 'rabbit_pick_up.wav'
on_button = 'on_button.wav'
click_button = 'click_button.wav'
game_over_sound = 'game_over.mp3'
menu_music = 'menu_music.mp3'
game_music = 'game_music.mp3'


class Button:
    global check_mouse_on_button

    def __init__(self, width, height = 40, left_indent = 0, top_indent = 5):
        self.width = int(width * scale)
        self.height = int(height * scale)
        self.left_indent = left_indent
        self.top_indent = top_indent
        self.fone = Surface((self.width, self.height))
        self.fone.fill((255, 255, 255))
        self.fone.set_alpha(0)

    def draw(self, x, y, text, command = None, dat = None):
        global check_mouse_on_button, last_coords_mouse, check_mouse_click_button, last_coords_click_but

        x, y = int(x * scale), int(y * scale)
        cursor = mouse.get_pos()
        click = mouse.get_pressed()

        if x < cursor[0] < x + self.width:
            if y < cursor[1] < y + self.height:
                self.fone.set_alpha(150)
                if not check_mouse_on_button:
                    check_mouse_on_button = True
                    play_sound(on_button, 0)
                    last_coords_mouse = [x, y, self.width, self.height]

                if click[0] and command != None and (not check_mouse_click_button):
                    play_sound(click_button, 0)
                    check_mouse_click_button = True
                    last_coords_click_but = [x, y, self.width, self.height]

                    if dat != None:
                        command(dat)
                    else:
                        command()

        if not (last_coords_mouse[0] < cursor[0] < last_coords_mouse[0] + last_coords_mouse[2] and\
                last_coords_mouse[1] < cursor[1] < last_coords_mouse[1] + last_coords_mouse[3]):
            check_mouse_on_button = False
        
        if (not (last_coords_click_but[0] < cursor[0] < last_coords_click_but[0] + last_coords_click_but[2] and\
        last_coords_click_but[1] < cursor[1] < last_coords_click_but[1] + last_coords_click_but[3])) or (not click[0]):
            check_mouse_click_button = False

        self.rect = self.fone.get_rect()
        self.rect.center = ((x, y))
        window.blit(self.fone, (x, y))
        print_text(text, int(x / scale) + self.top_indent, int(y / scale) + self.left_indent)


class Rabbit(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        global diff_coef

        self.speed = randint(22, 30) * diff_coef * scale
        self.image = rabbit_img
        self.rect = self.image.get_rect()
        self.rect.center = (-50 * scale, (525 + randint(0, 95)) * scale)
    
    def resize(self):
        self.image = transform.scale(image.load('image/rabbit1.png'), (int(100 * scale), int(95 * scale)))
        rabbit.speed = rabbit.speed / last_scale * scale
        rabbit.rect.x = rabbit.rect.x / last_scale * scale
        rabbit.rect.y = rabbit.rect.y / last_scale * scale

    def update(self):
        self.rect.x += self.speed


def play_sound(sound, channel):
    mixer.Channel(channel).play(mixer.Sound(f'sounds/{sound}'))
    

def print_text(message, x , y, font_color = (255, 255, 0), font_type = 'Arial', font_size = 30, bold = False):
    font_type = font.SysFont(font_type, int(font_size * scale), bold = bold)
    text = font_type.render(message, True, font_color)
    window.blit(text, (int(x * scale), int(y * scale)))


def fullscreen():
    global scale, window, is_fullscreen, last_scale, to_fullscreen, on_fullscreen
    
    if (not is_fullscreen):
        to_fullscreen = is_fullscreen = on_fullscreen = True
        last_scale = scale
        scale = size_monitor[0] / 1280
        window = display.set_mode((int(1280 * scale), int(720 * scale)), FULLSCREEN)
    else:
        scale = last_scale
        is_fullscreen = on_fullscreen = False
        window = display.set_mode((int(1280 * scale), int(720 * scale)), RESIZABLE)
    write_save()
    transform_img()


def resize_window(size = (1280, 720), vres = False):
    global window, scale, last_scale
    last_scale = scale
    if size[0] / 1280 < scale and size[1] / 720 < scale:
        scale = min(size[0] / 1280, size[1] / 720)
    elif size[0] / 1280 > scale and size[1] / 720 > scale:
        scale = max(size[0] / 1280, size[1] / 720)
    else:
        scale = size[0] / 1280

    if not vres:
        window = display.set_mode((1280 * scale, 720 * scale), RESIZABLE)
    transform_img()


def transform_img():
    global fone, fone_menu, rabbit_img, rabbit
    
    fone = transform.scale(image.load('image/foneHD.png'), (int(1280 * scale), int(720 * scale)))
    fone_menu = transform.scale(image.load('image/foneHD_blur.png'), (int(1280 * scale), int(720 * scale)))
    rabbit_img =  transform.scale(image.load('image/rabbit1.png'), (int(100 * scale), int(95 * scale)))

    if rabbit != None:
        rabbit.resize()


def counter_resolutions_presets():
    global resolutions_count

    resolutions_count = 1
    while resolutions_count < len(resolutions_preset) and size_monitor[0] > resolutions_preset[resolutions_count - 1][0]:
        resolutions_count += 1


def gets_monitors():
    global size_monitor
    monitors = get_monitors()
    for i in range(len(monitors)):
        if monitors[i].is_primary:
            size_monitor = [monitors[i].width, monitors[i].height]
            break


def resolutions_menu_on():
    global resolutions_menu_check
    resolutions_menu_check = True
    counter_resolutions_presets()


def resolutions_menu_off(size = None):
    global resolutions_menu_check, is_fullscreen, on_fullscreen
    resolutions_menu_check = False
    if size != None:
        resize_window(size)
        is_fullscreen = on_fullscreen = False


def edit_volume(s):
    global volume, interface_volume, game_volume, music_volume
    num_volume, resize_volume = s
    
    if num_volume == 0:
        volume = round(volume + resize_volume, 1)
    elif num_volume == 1:
        interface_volume = round(interface_volume + resize_volume, 1)
    elif num_volume == 2:
        game_volume = round(game_volume + resize_volume, 1)
    elif num_volume == 3:
        music_volume = round(music_volume + resize_volume, 1)


def go_exit():
    write_save()
    quit()
    exit()


def menu(run_s = None):
    check_run(run_s)
    window.blit(fone_menu, (0, 0))
    Button(217).draw(210, 150,'Небольшой побег', go_game, 25)
    Button(185).draw(225, 225, 'Средний побег', go_game, 50)
    Button(187).draw(225, 300, 'Большой побег', go_game, 75)
    Button(110).draw(902, 188, 'Правила', regulation, 'regulation')
    Button(132).draw(892, 265, 'Настройки', settings, 'settings')
    Button(85).draw(575, 450, 'Выход', go_exit)
    print_text('Кроличий побег', 545, 50)
    print_text(f'Рекорд: {saves_old[indexx][0]}', 565, 150)
    print_text(f'Рекорд: {saves_old[indexx][1]}', 565, 225)
    print_text(f'Рекорд: {saves_old[indexx][2]}', 565, 300)
    print_text('v2.2.0', 10, 695, (255, 255, 255), font_size = 12)


def regulation(run_s = None):
    check_run(run_s)
    window.blit(fone_menu, (0, 0))
    Button(95).draw(10, 10, 'В меню', menu, 'menu')
    print_text('Суть игры в том, чтобы поймать как можно больше сбегающих с фермы кроликов.', 150, 285)
    print_text('Они бегут друг за другом. За каждого пойманного кролика вы получаете от 10 до 150 очков,', 105, 335)
    print_text(' в зависимоти от времени, за которе вы его поймали. Во время небольшого побега сбегает', 100, 385)
    print_text('25 кроликов, во время среднего 50 кроликов, а во время большого 75 кроликов.', 167, 435)


def settings(run_s = None):
    global last_change

    check_run(run_s, indexx)
    window.blit(fone_menu, (0, 0))
    Button(95).draw(10, 10, 'В меню', menu, 'menu')
    Button(75).draw(283, 100, 'Легко', change,  0.75)
    Button(180).draw(227, 175, 'По умолчанию', change, 1)
    Button(100).draw(268, 250, 'Средне', change, 1.25)
    Button(100).draw(270, 325, 'Сложно', change, 1.5)
    print_text(check_bar_list[0], 265, 90, font_size = 50)
    print_text(check_bar_list[1], 210, 165, font_size = 50)
    print_text(check_bar_list[2], 250, 240, font_size = 50)
    print_text(check_bar_list[3], 250, 315, font_size = 50)

    if resolutions_menu_check:
        resolutions_menu_fone = Surface((180 * scale, 40 * (resolutions_count + 1) * scale))
        resolutions_menu_fone.fill((255, 255, 255))
        resolutions_menu_fone.set_alpha(100)
        window.blit(resolutions_menu_fone, (500 * scale, 175 * scale))
        Button(180).draw(500, 175, f'▲разрешение', resolutions_menu_off)
        for c in range(resolutions_count):
            Button(180).draw(500, 215 + c * 40, f'{resolutions_preset[c][0]}x{resolutions_preset[c][1]}', resolutions_menu_off, resolutions_preset[c])
    else:
        Button(180).draw(500, 175, f'▼разрешение', resolutions_menu_on)

    if volume > 0:
        Button(25).draw(800, 150, '-', edit_volume, (0, -0.1))
    if volume < 1:
        Button(25).draw(1200, 150, '+', edit_volume, (0, 0.1))
    if interface_volume > 0:
        Button(25).draw(800, 275, '-', edit_volume, (1, -0.1))
    if interface_volume < 1:
        Button(25).draw(1200, 275, '+', edit_volume, (1, 0.1))
    if game_volume > 0:
        Button(25).draw(800, 400, '-', edit_volume, (2, -0.1))
    if game_volume < 1:
        Button(25).draw(1200, 400, '+', edit_volume, (2, 0.1))
    if music_volume > 0:
        Button(25).draw(800, 525, '-', edit_volume, (3, -0.1))
    if music_volume < 1:
        Button(25).draw(1200, 525, '+', edit_volume, (3, 0.1))

    print_text('общая громкость:', 900, 100)
    print_text('•', 845 + (33 * volume * 10), 148, font_size = 50, bold = True)
    print_text('——————————', 850, 150, font_size = 40, bold = True)
    print_text('громкость интерфейса:', 900, 225)
    print_text('•', 845 + (33 * interface_volume * 10), 273, font_size = 50, bold = True)
    print_text('——————————', 850, 275, font_size = 40, bold = True)
    print_text('громкость игры:', 900, 350)
    print_text('•', 845 + (33 * game_volume * 10), 398, font_size = 50, bold = True)
    print_text('——————————', 850, 400, font_size = 40, bold = True)
    print_text('громкость музыки:', 900, 475)
    print_text('•', 845 + (33 * music_volume * 10), 523, font_size = 50, bold = True)
    print_text('——————————', 850, 525, font_size = 40, bold = True)

    Button(175).draw(510, 100, 'Полный экран', fullscreen)
    Button(262).draw(185, 400, 'Сбросить сохранения', del_save)

    if is_fullscreen:
        print_text('•', 490, 90, font_size = 50)
    now_s = float(datetime.now().strftime('%S.%f'))
    now_m = float(datetime.now().strftime('%H.%M'))

    if last_change != indexx and (now_s - last_edit_difficult_s) < 1.0 and now_m == last_edit_difficult_m:
        print_text('Сложность изменена!', 190, 475)
    elif now_s - last_del_save_s < 1 and now_m == last_del_save_m:
        print_text('Сохранения сброшены!', 179, 475)
    elif last_change != indexx:
        last_change = indexx


def check_run(run_s, last_c = None):
    global run_status, last_change

    if run_s != None:
        run_status = run_s
        if last_c != None:
            last_change = last_c


def del_save():
    global saves_old, last_del_save_s, last_del_save_m

    saves_old = [[0,0,0], [0,0,0], [0,0,0], [0,0,0]]
    last_del_save_s = float(datetime.now().strftime('%S.%f'))
    last_del_save_m = float(datetime.now().strftime('%H.%M'))

    with open('save.txt','w') as saves_w:
        for i in range(4):
            saves_w.write(f'0|0|0\n')

        saves_w.write(f'{(diff_coef)}\n')
        saves_w.write(f'{int(on_fullscreen)}\n')
        saves_w.write(f'{scale}\n')
        saves_w.write(f'{volume}|{interface_volume}|{game_volume}|{music_volume}\n')


def write_save():
    with open('save.txt', 'w') as saves1:
        for saves_new in saves_old:
            saves1.write(f'{saves_new[0]}|{saves_new[1]}|{saves_new[2]}\n')

        saves1.write(f'{diff_coef}\n')
        saves1.write(f'{int(on_fullscreen)}\n')
        saves1.write(f'{scale}\n')
        saves1.write(f'{volume}|{interface_volume}|{game_volume}|{music_volume}\n')


def change(k):
    global diff_coef, indexx, last_edit_difficult_s, last_edit_difficult_m, check_bar_list

    diff_coef = k
    check_bar_list = ['', '', '', '']
    if k == 0.75:
        indexx = 0
    elif k == 1:
        indexx = 1
    elif k == 1.25:
        indexx = 2
    elif k == 1.5:
        indexx = 3

    write_save()
    check_bar_list[indexx] = '•'
    last_edit_difficult_s = float(datetime.now().strftime('%S.%f'))
    last_edit_difficult_m = float(datetime.now().strftime('%H.%M'))


def go_game(lenn):
    global n, s, start, all_sprites, run_status, max_n, rabbit

    rabbit = Rabbit()
    all_sprites = sprite.Group()
    all_sprites.add(rabbit)
    n = s = 0
    max_n = lenn
    run_status = 'game'
    mixer.Channel(2).fadeout(500)
    start = datetime.now().strftime('%S.%f')


def game():
    global n, s, start, all_sprites, run_status, rabbit, old_r, k_y, k_x

    window.blit(fone, (0,0))
    print_text(str(s), 612, 25, font_size = 40)
    window.blit(font.SysFont("Arial", 40).render(str(s) , True, (255,165,0)), (display.get_window_size()[0], 25))
    check_catch_rabb = False

    if rabbit.rect.x >= 1330 * scale:
        check_catch_rabb = True
        start = datetime.now().strftime('%S.%f')

    elif rabbit.rect.x <= k_x and rabbit.rect.x + (100 * scale) >= k_x and rabbit.rect.y <= k_y and rabbit.rect.y + (100 * scale) >= k_y:
        check_catch_rabb = True
        play_sound(rabbit_pick_up, 1)
        end = datetime.now().strftime('%S.%f')
        times = (float(end) - float(start)) * diff_coef
        start = end

        if times <= 0.1: s += 150
        elif times <= 0.25: s += 100
        elif times <= 0.5: s += 75
        elif times <= 0.75: s += 50
        elif times <= 1.0: s += 25
        else: s += 10
    
    if check_catch_rabb:
        if n < max_n:
            n += 1
            rabbit = Rabbit()
            all_sprites = sprite.Group()
            all_sprites.add(rabbit)
        else:
            run_status = 'game_over'
            play_sound(game_over_sound, 1)

            old_r = saves_old[indexx][(n // 25) - 1]
            if s >= saves_old[indexx][(n // 25) - 1]:
                saves_old[indexx][(n // 25 - 1)] = s
            write_save()

    k_x = k_y = 0


def game_over():
    window.blit(fone_menu, (0, 0))
    print_text('Игра окончена', 555, 50)
    print_text(f'Рекорд: {str(old_r)}', 570, 125)
    print_text(f'Очки: {str(s)}', 580, 175)
    Button(95).draw(10, 10, 'В меню', menu, 'menu')


with open('save.txt') as f:
    saves_old = [list(map(int, f.readline().split('|'))) for i in range(4)]
    diff_coef = float(f.readline())
    on_fullscreen = int(f.readline())
    scale = float(f.readline())
    volume, interface_volume, game_volume, music_volume = map(float, f.readline().split('|'))


gets_monitors()
init()
mixer.init()
mixer.set_num_channels(3)
window = display.set_mode((int(1280 * scale), int(720 * scale)), RESIZABLE)
display.set_caption('Кроличий побег')
display.set_icon(image.load('image/rab.png'))
clock = time.Clock()
all_sprites = sprite.Group()

if on_fullscreen:
    fullscreen()
else:
    transform_img()

change(diff_coef)
menu('menu')


while True:
    clock.tick(framerate)

    for even_t in event.get():
        if WINDOWMAXIMIZED == even_t.type:
            check_maximized = True
        if WINDOWRESIZED == even_t.type:
            check_maximized = False
            if not is_fullscreen:
                to_fullscreen = False
            
        if even_t.type == QUIT:
            go_exit()
        elif even_t.type == VIDEORESIZE and not check_maximized and not to_fullscreen:
            resize_window(even_t.size)
        elif even_t.type == VIDEORESIZE and check_maximized:
            resize_window(even_t.size, True)
        elif even_t.type == KEYDOWN:
            if key.get_pressed()[K_f]:
                fullscreen()
        elif even_t.type == MOUSEBUTTONDOWN:
            if mouse.get_pressed()[0]:
                k_x, k_y = mouse.get_pos()
        elif even_t.type == WINDOWMOVED:
            gets_monitors()

    mixer.Channel(0).set_volume(interface_volume * volume)
    mixer.Channel(1).set_volume(game_volume * volume)
    mixer.Channel(2).set_volume(music_volume * volume)

    if run_status == 'menu':
        if not mixer.Channel(2).get_busy():
            play_sound(menu_music, 2)
        menu()
    elif run_status == 'game':
        if not mixer.Channel(2).get_busy():
            play_sound(game_music, 2)
        game()
        all_sprites.update()
        all_sprites.draw(window)
    elif run_status == 'game_over':
        if mixer.Channel(2).get_busy():
            mixer.Channel(2).fadeout(500)
        game_over()
    elif run_status == 'regulation':
        if not mixer.Channel(2).get_busy():
            play_sound(menu_music, 2)
        regulation()
    elif run_status == 'settings':
        if not mixer.Channel(2).get_busy():
            play_sound(menu_music, 2)
        settings()
    
    display.flip()