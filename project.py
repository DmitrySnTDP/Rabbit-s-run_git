import random
from tkinter import*

window = Tk()
window.geometry('1280x720')
window.title('Кроличий побег')
width = window.winfo_screenwidth()
height= window.winfo_screenheight()

def menu():
    global old_r_s,old_r_a,old_r_l
    saves = open('save_records.txt')
    old_r_s = int(saves.readline())
    old_r_a=int(saves.readline())
    old_r_l=int(saves.readline())
    saves.close()

    fone = Label(bg='white')
    fone.place(width=1280,height=720)

    name_g=Label(text='Кроличьи побег',bg='white',font=('Arial',30))
    name_g.place(x=525,y=15)

    small_g=Button(text='Небольшой побег',bg='white',font=('Arial',25),command=small_G)
    small_g.place(x=315,y=150)
    small_r=Label(text='Рекорд: ',bg='white',font=('Arial',25))
    small_r.place(x=725,y=165)

    record_s=Label(text=old_r_s,bg='white',font=('Arial',25))
    record_s.place(x=855,y=165)

    average_g=Button(text='Средний побег',bg='white',font=('Arial',25),command=average_G)
    average_g.place(x=333,y=225)
    average_r=Label(text='Рекорд: ',bg='white',font=('Arial',25))
    average_r.place(x=725,y=240)

    record_a=Label(text=old_r_a,bg='white',font=('Arial',25))
    record_a.place(x=855,y=240)

    long_g=Button(text='Большой побег',bg='white',font=('Arial',25),command=long_G)
    long_g.place(x=330,y=300)
    long_r=Label(text='Рекорд: ',bg='white',font=('Arial',25))
    long_r.place(x=725,y=315)

    record_l=Label(text=old_r_l,bg='white',font=('Arial',25))
    record_l.place(x=855,y=315)

    regulations = Button(text='Правила',bg='white',font=('Arial',25),command=regulation)
    regulations.place(x=575,y=375)

def small_G():
    global l
    l=25
    start()

def average_G():
    global l
    l=50
    start()

def long_G():
    global l
    l=75
    start()

def regulation():
    fone=Label(bg='white')
    fone.place(width=1280,height=720)

    texts=Message(text='Суть игры в том, чтобы поймать как можно больше сбегающих с фермы кроликов. Они бегут друг за другом. Учитывайте, что чем больше кроликов вы поймали, тем больше боятся остальные и быстрее бегут. За каждого пойманного кролика вы получаете 25 очков. Во время небольшого побега сбегает 25 кроликов, во время среднего 50 кроликов, а во время большого 75 кроликов.',bg='white',font=('Arial',25))
    texts.place(x=240,y=125,width=800)

    Vmenu = Button(text='В меню',bg='white',font=('Arial',25),command=menu)
    Vmenu.place(x=10,y=10)

def start():
    global s,xR,n
    
    n=0
    s=0
    xR = 5   
    photo = PhotoImage(file="foneHD.png")
    label = Label(image = photo)
    label.image = photo
    label.place(width=1280,height=720)
    run()

def dop():
    global s,xR,n
    s+=25
    xR = 5
    n+=1
    run()
    
def run():
    global xR,s,n,l,old_r_s,old_r_a,old_r_l
    old_r=0
    if xR<=1050 and n<l:
        xR=xR+random.randint(50,100)
        window.after(1000+s*4,run)

        photo = PhotoImage(file="foneHD_bottom.png")
        label = Label(image = photo)
        label.image = photo
        label.place(width=1280,height=147,y=530)

        schot =Label(text=s,fg='orange',bg='lightskyblue',font=('Arial',34))
        schot.place(x=600,y=10)

        rabbit = PhotoImage(file="rabbit1.png")
        rabbit_l = Button(image = rabbit,bg='khaki',command=dop)
        rabbit_l.image = rabbit
        rabbit_l.place(width=100,height=95, x=xR,y=565)

    elif n<50:
        n+=1
        photo = PhotoImage(file="foneHD_bottom.png")
        label = Label(image = photo)
        label.image = photo
        label.place(width=1280,height=147,y=530)

        schot =Label(text=s,fg='orange',bg='lightskyblue',font=('Arial',34))
        schot.place(x=600,y=10)

        xR=5
        run()
    else:
        if l==25:
            old_r=old_r_s
        elif l==50:
            old_r=old_r_a
        else:
            old_r=old_r_l
        
        endL=Label(bg='white')
        endL.place(width=1280,height=720)

        Vmenu = Button(text='В меню',bg='white',font=('Arial',25),command=menu)
        Vmenu.place(x=10,y=10)

        old_record=Label(text='Рекорд: ',bg='white',font=('Arial',30))
        old_record.place(x=550,y=125)
        old_record_n=Label(text=old_r,bg='white',font=('Arial',30))
        old_record_n.place(x=710,y=125)

        result=Label(text='Очки: ',bg='white',font=('Arial',30))
        result.place(x=570,y=175)
        result_n=Label(text=s,bg='white',font=('Arial',30))
        result_n.place(x=710,y=175)

        TheEnd= Label(text='Игра окончена',bg='white',font=('Arial',30))
        TheEnd.place(x=530,y=50)

        
        if s>=old_r and l==25:
            saves1=open('save_records.txt','w')
            records = [str(s),str(old_r_a),str(old_r_l)]
            for i in records:
                saves1.write(i +'\n')
            saves1.close()
        elif s>=old_r and l==50:
            saves1=open('save_records.txt','w')
            records = [str(old_r_s),str(s),str(old_r_l)]
            for i in records:
                saves1.write(i +'\n')
            saves1.close()
        elif s>=old_r and l==75:
            saves1=open('save_records.txt','w')
            records = [str(old_r_s),str(old_r_a),str(s)]
            for i in records:
                saves1.write(i+ '\n')
            saves1.close()

menu()

window.mainloop()