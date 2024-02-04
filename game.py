from random import randint
from tkinter import Tk, Canvas, PhotoImage, Button
from datetime import datetime

window = Tk()
window.geometry('1280x720')
window.title('Кроличий побег')
window.resizable(width=False,height=False)
width = window.winfo_screenwidth()
height= window.winfo_screenheight()
canvas=Canvas(window,width=width,height=height,highlightthickness=0)
canvas.place(x=0,y=0,width=width,height=height)

fone=PhotoImage(file='image/foneHD.png')
fone_menu=PhotoImage(file='image/foneHD_blur.png')
small_run=PhotoImage(file='image/little_game1.png')
average_run=PhotoImage(file='image/average_game1.png')
long_run=PhotoImage(file='image/long_game1.png')
regulat=PhotoImage(file='image/reg1.png')
v_menu=PhotoImage(file='image/v_menu1.png')

class Rabbit:
    def __init__(self,canvas):
        self.canvas=canvas
        self.speed=randint(10,15)
        self.x=-50
        self.y=525+randint(0,95)
        self.photo=PhotoImage(file='image/rabbit1.png')

def kurs(event):
    global k_x,k_y
    k_x=event.x
    k_y=event.y

def menu():
    global old_r_s,old_r_a,old_r_l
    canvas.delete('all')

    with open('save_records.txt') as saves:
        old_r_s = int(saves.readline())
        old_r_a=int(saves.readline())
        old_r_l=int(saves.readline())
    # saves.close()
    canvas.create_image(640,360,image=fone_menu)
    canvas.create_text(640,50,text='Кроличий побег',font=('Arial',30),fill='yellow')
    small_g=Button(image=small_run,highlightthickness=0,command=small_G)
    canvas.create_window((315, 150), anchor="nw", window=small_g)

    canvas.create_text(790,180,text='Рекорд: ',font=('Arial',25),fill='yellow')
    canvas.create_text(885,180,text=old_r_s,font=('Arial',25),fill='yellow')
   
    average_g=Button(image=average_run,highlightthickness=0,command=average_G)
    canvas.create_window((333, 225), anchor="nw", window=average_g)

    canvas.create_text(790,255,text='Рекорд: ',font=('Arial',25),fill='yellow')
    canvas.create_text(885,255,text=old_r_a,font=('Arial',25),fill='yellow')

    long_g=Button(image=long_run,highlightthickness=0,command=long_G)
    canvas.create_window((330, 300),anchor="nw", window=long_g)

    canvas.create_text(790,330,text='Рекорд: ',font=('Arial',25),fill='yellow')
    canvas.create_text(885,330,text=old_r_l,font=('Arial',25),fill='yellow')

    regulations = Button(image=regulat,highlightthickness=0,command=regulation)
    canvas.create_window((575, 375), anchor="nw", window=regulations)

def small_G():
    global rabb,n,s,start
    rabb=[Rabbit(canvas) for i in range(25)]
    n=0
    s=0
    start=datetime.now().strftime('%S.%f')
    game()

def average_G():
    global rabb,n,s,start
    rabb=[Rabbit(canvas) for i in range(50)]
    n=0
    s=0
    start=datetime.now().strftime('%S.%f')
    game()

def long_G():
    global rabb,n,s,start
    rabb=[Rabbit(canvas) for i in range(75)]
    n=0
    s=0
    start=datetime.now().strftime('%S.%f')
    game()

def regulation():
    canvas.delete('all')
    canvas.create_image(640,360,image=fone_menu)
    canvas.create_text(640,400,text='Суть игры в том, чтобы поймать как можно больше сбегающих с фермы кроликов. Они бегут друг за другом. За каждого пойманного кролика вы получаете от 5 до 150 очков, в зависимоти от времени, за которе вы его поймали. Во время небольшого побега сбегает 25 кроликов, во время среднего 50 кроликов, а во время большого 75 кроликов.',width=800,font=('Arial',25),fill='yellow')
    
    Vmenu = Button(highlightthickness=0,image=v_menu,command=menu)
    canvas.create_window((10,10), anchor="nw", window=Vmenu)

def game():
    global k_x,k_y,n,s,start
    canvas.delete('all')
    canvas.create_image(640,360,image=fone)
    canvas.create_image(rabb[n].x,rabb[n].y,image=rabb[n].photo)
    canvas.create_text(610,25,text=s,fill='orange',font=('Arial',35))
    rabb[n].x+=rabb[n].speed

    if rabb[n].x>=1330:
        n+=1
        start=datetime.now().strftime('%S.%f')
    elif rabb[n].x-50<=k_x and rabb[n].x+50>=k_x and rabb[n].y-50<=k_y and rabb[n].y+50>=k_y:
        n+=1
        k_x=0
        k_y=0
        end=datetime.now().strftime('%S.%f')
        times=float(end)-float(start)
        start=datetime.now().strftime('%S.%f')

        if times<=0.1:
            s+=150
        elif times<=0.25:
            s+=100
        elif times<=0.36:
            s+=75
        elif times<=0.5:
            s+=50
        elif times<=0.75:
            s+=25
        elif times<=1.0:
            s+=10
        else:
            s+=5

    if n==len(rabb):
        if n==25:
            old_r=old_r_s
        elif n==50:
            old_r=old_r_a
        else:
            old_r=old_r_l

        canvas.delete('all')
        canvas.create_image(640,360,image=fone_menu)
        canvas.create_text(575,125,text='Рекорд: ',font=('Arial',30),fill='yellow')
        canvas.create_text(735,125,text=old_r,font=('Arial',30),fill='yellow')
        canvas.create_text(595,175,text='Очки: ',font=('Arial',30),fill='yellow')
        canvas.create_text(735,175,text=s,font=('Arial',30),fill='yellow')
        canvas.create_text(640,50,text='Игра окончена',font=('Arial',30),fill='yellow')

        Vmenu = Button(image=v_menu,highlightthickness=0,command=menu)
        canvas.create_window((10,10), anchor="nw", window=Vmenu)

        saves1=open('save_records.txt','w')
        if s>=old_r and n==25:
            records = [str(s),str(old_r_a),str(old_r_l)]
        elif s>=old_r and n==50:
            records = [str(old_r_s),str(s),str(old_r_l)]
        elif s>=old_r and n==75:
            records = [str(old_r_s),str(old_r_a),str(s)]
        else:
            records=[str(old_r_s),str(old_r_a),str(old_r_l)]
        for i in records:
            saves1.write(i+'\n')
        saves1.close()
    else:
        k_x=0
        k_y=0
        window.after(10, game)

n=0
k_x=0
k_y=0
menu()

window.bind('<Button-1>',kurs)
window.mainloop()