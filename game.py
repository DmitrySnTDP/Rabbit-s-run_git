from random import randint
from tkinter import Tk, Canvas, PhotoImage, Button, Radiobutton, StringVar
from datetime import datetime

window = Tk()
window.geometry('1280x720')
window.title('Кроличий побег')
window.resizable(width = False,height = False)
width = window.winfo_screenwidth()
height= window.winfo_screenheight()
canvas = Canvas(window,width = width,height = height,highlightthickness = 0)
canvas.place(x = 0,y = 0,width = width,height = height)

fone = PhotoImage(file = 'image/foneHD.png')
fone_menu = PhotoImage(file = 'image/foneHD_blur.png')
small_run = PhotoImage(file = 'image/little_game1.png')
average_run = PhotoImage(file = 'image/average_game1.png')
long_run = PhotoImage(file = 'image/long_game1.png')
regulat = PhotoImage(file = 'image/reg1.png')
v_menu = PhotoImage(file = 'image/v_menu1.png')
v_set = PhotoImage(file = 'image/settings.png')
default_img = PhotoImage(file = 'image/default.png')
easy_img = PhotoImage(file = 'image/easy.png')
medium_img = PhotoImage(file = 'image/medium.png')
hard_img = PhotoImage(file = 'image/hard.png')
save_set_img = PhotoImage(file = 'image/save_set.png')
reset_save_img = PhotoImage(file = 'image/reset_save.png')

class Rabbit:
    def __init__(self,canvas):
        global diff_coef
        self.canvas = canvas
        self.speed = randint(10,15)*diff_coef

        self.x =- 50
        self.y = 525 + randint(0,95)
        self.photo = PhotoImage(file = 'image/rabbit1.png')

def kurs(event):
    global k_x,k_y
    k_x = event.x
    k_y = event.y

def menu():
    global old_r_s, old_r_a, old_r_l,saves_old
    canvas.delete('all')
    saves_old = []

    with open('save_records.txt') as saves:
        for i in range(4):
            save_old = []
            for ii in range(3):
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

    canvas.create_image(640,360,image=fone_menu)
    canvas.create_text(640,50,text = 'Кроличий побег',font = ('Arial',30),fill = 'yellow')

    small_g = Button(image = small_run,highlightthickness = 0,command = small_G)
    canvas.create_window((315, 150), anchor = "nw", window = small_g)

    canvas.create_text(790,180,text = 'Рекорд: ',font = ('Arial',25),fill = 'yellow')
    canvas.create_text(885,180,text = old_r_s,font = ('Arial',25),fill = 'yellow')
   
    average_g = Button(image = average_run,highlightthickness = 0,command = average_G)
    canvas.create_window((333, 225), anchor = "nw", window = average_g)

    canvas.create_text(790,255,text = 'Рекорд: ',font = ('Arial',25),fill = 'yellow')
    canvas.create_text(885,255,text = old_r_a,font = ('Arial',25),fill = 'yellow')

    long_g = Button(image = long_run,highlightthickness = 0,command = long_G)
    canvas.create_window((330, 300),anchor = "nw", window = long_g)

    canvas.create_text(790,330,text = 'Рекорд: ',font = ('Arial',25),fill = 'yellow')
    canvas.create_text(885,330,text = old_r_l,font = ('Arial',25),fill = 'yellow')

    regulations = Button(image = regulat,highlightthickness = 0,command = regulation)
    canvas.create_window((575, 375), anchor = "nw", window = regulations)

    settings = Button(image = v_set,highlightthickness = 0,command = setting)
    canvas.create_window((575, 450), anchor = "nw", window = settings)

def small_G():
    go_game(25)

def average_G():
    go_game(50)

def long_G():
    go_game(75)

def go_game(lenn):
    global rabb,n,s,start
    rabb = [Rabbit(canvas) for i in range(lenn)]
    print(len(rabb))
    n = 0
    s = 0
    start = datetime.now().strftime('%S.%f')
    game()

def regulation():
    canvas.delete('all')
    canvas.create_image(640,360,image=fone_menu)
    canvas.create_text(640,400,text='Суть игры в том, чтобы поймать как можно больше сбегающих с фермы кроликов. Они бегут друг за другом. За каждого пойманного кролика вы получаете от 5 до 150 очков, в зависимоти от времени, за которе вы его поймали. Во время небольшого побега сбегает 25 кроликов, во время среднего 50 кроликов, а во время большого 75 кроликов.',width=800,font=('Arial',25),fill='yellow')
    
    Vmenu = Button(highlightthickness = 0,image = v_menu,command = menu)
    canvas.create_window((10,10), anchor = "nw", window=Vmenu)

def setting():
    canvas.delete('all')
    canvas.create_image(640,360,image = fone_menu)

    Vmenu = Button(highlightthickness = 0,image = v_menu,command = menu)
    canvas.create_window((10,10), anchor = "nw", window = Vmenu)

    difficult_default = Radiobutton(highlightthickness = 0,image = default_img,variable = var,value = 'default')
    canvas.create_window((320,100), anchor = "nw", window=difficult_default)

    difficult_easy = Radiobutton(highlightthickness = 0,image = easy_img,variable = var,value = 'easy')
    canvas.create_window((320,175), anchor = "nw", window = difficult_easy)

    difficult_medium = Radiobutton(highlightthickness = 0,image = medium_img,variable = var,value = 'medium')
    canvas.create_window((320,250), anchor = "nw", window = difficult_medium)

    difficult_hard = Radiobutton(highlightthickness = 0,image = hard_img,variable = var,value = 'hard')
    canvas.create_window((320,325), anchor = "nw", window = difficult_hard)

    save_setting = Button(highlightthickness = 0,image = save_set_img,command = change)
    canvas.create_window((320,400), anchor = "nw", window = save_setting)

    reset_saves = Button(highlightthickness = 0,image = reset_save_img,command = del_save)
    canvas.create_window((750,100), anchor = "nw", window = reset_saves)

def del_save():
    global saves_old
    saves_old = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    with open('save_records.txt','w') as saves_w:
        for saves in saves_old:
            for save in saves:
                saves_w.write(str(save) + '\n')

def change():
    global diff_coef, indexx
    if var.get() == 'default':
        diff_coef = 1
        indexx = 0
    elif var.get() == 'easy':
        diff_coef = 0.75
        indexx = 1
    elif var.get() == 'medium':
        diff_coef = 1.25
        indexx = 2
    elif var.get() == 'hard':
        diff_coef = 1.5
        indexx = 3

def game():
    global k_x,k_y,n,s,start
    canvas.delete('all')
    canvas.create_image(640,360,image = fone)
    canvas.create_image(rabb[n].x,rabb[n].y,image = rabb[n].photo)
    canvas.create_text(610,25,text=s,fill = 'orange',font = ('Arial',35))
    rabb[n].x += rabb[n].speed

    if rabb[n].x >= 1330:
        n += 1
        start = datetime.now().strftime('%S.%f')
    elif rabb[n].x - 50 <= k_x and rabb[n].x + 50 >= k_x and rabb[n].y - 50 <= k_y and rabb[n].y + 50 >= k_y:
        n += 1
        k_x = 0
        k_y = 0
        end = datetime.now().strftime('%S.%f')
        times = (float(end) - float(start)) * diff_coef
        start = datetime.now().strftime('%S.%f')

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

    if n == len(rabb):
        if n == 25:
            old_r = old_r_s
        elif n == 50:
            old_r = old_r_a
        else:
            old_r = old_r_l
    

        canvas.delete('all')
        canvas.create_image(640,360,image = fone_menu)
        canvas.create_text(575,125,text = 'Рекорд: ',font = ('Arial',30),fill = 'yellow')
        canvas.create_text(735,125,text = old_r,font = ('Arial',30),fill = 'yellow')
        canvas.create_text(595,175,text = 'Очки: ',font = ('Arial',30),fill = 'yellow')
        canvas.create_text(735,175,text = s,font = ('Arial',30),fill = 'yellow')
        canvas.create_text(640,50,text = 'Игра окончена',font = ('Arial',30),fill = 'yellow')

        Vmenu = Button(image = v_menu,highlightthickness = 0,command = menu)
        canvas.create_window((10,10), anchor = "nw", window = Vmenu)

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
    else:
        k_x = 0
        k_y = 0
        window.after(10, game)

var = StringVar()
var.set('default')
diff_coef = 1
indexx = 0
n = 0
k_x = 0
k_y = 0
menu()

window.bind('<Button-1>',kurs)
window.mainloop()