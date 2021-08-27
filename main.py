import locale
from tkinter import *
from os.path import abspath
from contextlib import suppress
from tkinter.ttk import Combobox
from time import sleep, localtime
from datetime import date, timedelta
import tkinter.messagebox as messagebox
from tkcalendar import Calendar, DateEntry


locale.setlocale(locale.LC_TIME, "pt_BR")

cor = {'white': '#ffffff',
       'black': '#000000',
       'gray20': '#202020',
       'ice': '#EBEBEB',
       'gray54': '#545454', }


def size(window: tuple[int, int, int]) -> None:
    x = app.winfo_screenwidth() // 2 - window[0] // 2
    y = app.winfo_screenheight() // 2 - window[1] // 2
    app.geometry(f'{window[0]}x{window[1]}+{x}+{y}')
    app.resizable(window[2], window[2])


def search(*files: str) -> str:
    path = []
    for file in files:
        path.append(file)
    return str(abspath('/'.join(path)))


def _bt_main_click(event, close: bool = None) -> None:
    if close == None:
        app.geometry(f'+{event.x_root}+{event.y_root}')
    if close:
        app.destroy()
    else:
        app.overrideredirect(False)
        app.iconify()


def _bt_main_effects(event, button: int, effect: bool) -> None:
    if button == 1:
        if effect:
            sleep(0.1)
            bt_next.place(x=422, y=296)
        else:
            bt_next.place(x=422, y=298)
    elif button == 2:
        if effect:
            sleep(0.1)
            bt_not_know.place(x=284, y=296)
        else:
            bt_not_know.place(x=284, y=298)
    elif button == 3:
        with suppress(BaseException):
            app.deiconify()
            app.overrideredirect(True)


def _get_pos(event):
    xwin = app.winfo_x()
    ywin = app.winfo_y()
    startx = event.x_root
    starty = event.y_root

    xwin -= startx
    ywin -= starty

    def move_window(event):
        app.configure(cursor="fleur")
        app.geometry(f'+{event.x_root + xwin}+{event.y_root + ywin}')

    def release_window(event):
        app.config(cursor="arrow")

    frame.bind('<B1-Motion>', move_window)
    frame.bind('<ButtonRelease-1>', release_window)
    lb_title.bind('<B1-Motion>', move_window)
    lb_title.bind('<ButtonRelease-1>', release_window)


def _entry_click(event) -> None:
    global open_window

    def click(event=None) -> None:
        global open_window, birth
        open_window = False
        lb_date = cal.get_date()
        birth = lb_date
        lb_cal.configure(text=lb_date)
        window.destroy()

    if not open_window:
        open_window = True
        window = Frame(app)
        window.configure(background=cor['black'],
                         highlightbackground=cor['gray20'])
        window.place(x=12, y=50, width=250, height=250)

        cal = Calendar(
            window, background=cor['black'], foreground=cor['white'], maxdate=date.today(), locale='pt_BR')
        cal.pack(expand=1, fill=BOTH)

        bt_cal = Button(window, text='Pronto', background=cor['gray20'], foreground=cor['white'],
                        font='Arial 10 bold', border=0, relief='flat', command=click)
        bt_cal.pack(fill=X, padx=2, pady=2)


def _bt_calc(event) -> None:
    global open_window, birth

    def click(event=None) -> None:
        global open_window, birth
        open_window = False
        lb_cal['text'] = ''
        birth = None
        window.destroy()

    if not open_window:
        try:
            open_window = True

            birthx = str(birth).replace('/', ' ').split()
            dia, mes, ano = int(birthx[0]), int(birthx[1]), int(birthx[2])

            if mes > 3:
                mes -= 3
                ano += 1

            else:
                mes += 9

            d = date(ano, mes, dia)
            d += timedelta(days=7)
            d = d.strftime('\n%A\n\n%d/%m/%Y')

            msg = f'Resultado:\n\n{d}'

            window = Frame(app)
            window.configure(background=cor['black'],
                             highlightbackground=cor['gray20'])
            window.place(x=12, y=50, width=250, height=250)

            lb_result = Label(
                window, text=msg, background=cor['ice'], foreground=cor['gray20'], font='Arial 12 bold', justify='center')
            lb_result.pack(expand=1, fill=BOTH)

            bt_cal = Button(window, text='Fechar', background=cor['gray20'], foreground=cor['white'],
                            font='Arial 10 bold', border=0, relief='flat', command=click)
            bt_cal.pack(fill=X, padx=2, pady=2)
        except:
            open_window = False


def _bt_not_know(event) -> None:
    global open_window

    def click_calc():
        dia = 7
        mes = int(sb_month.get())
        ano = int(sb_year.get())

        if mes > 3:
            mes -= 3
            ano += 1
        else:
            mes += 9

        d = date(ano, mes, dia)

        if cb.get() == 'Início':
            d += timedelta(days=5)
        elif cb.get() == 'Meiado':
            d += timedelta(days=15)
        else:
            d += timedelta(days=25)

        d = d.strftime('\n%A\n\n%d/%m/%Y')
        msg = f'Resultado:\n\n{d}'
        lb_result['text'] = msg

    def click_back():
        global open_window
        open_window = False
        window.destroy()

    if not open_window:
        open_window = True
        lb_cal['text'] = ''

        window = Frame(app)
        window.configure(background=cor['white'],
                         highlightbackground=cor['gray20'])
        window.place(x=12, y=50, width=250, height=250)

        # Período
        lb_not_0 = Label(window, text='Período',
                         background=cor['white'], font='Arial 8 bold')
        lb_not_0.place(x=25, y=5)

        cb = Combobox(window, justify='center', values=[
                      'Início', 'Meiado', 'Final'], width=10)
        cb.place(x=25, y=25)

        # Mês
        lb_not_1 = Label(window, text='Mês',
                         background=cor['white'], font='Arial 8 bold')
        lb_not_1.place(x=115, y=5)

        sb_month = Spinbox(
            window, background=cor['white'], relief='solid', justify='center', from_=1, to=12, width=5)
        sb_month.place(x=115, y=25, height=21)

        # Ano
        lb_not_2 = Label(window, text='Ano',
                         background=cor['white'], font='Arial 8 bold')
        lb_not_2.place(x=170, y=5)

        sb_year = Spinbox(window, background=cor['white'], relief='solid', justify='center', from_=int(
            localtime()[0])-150, to=int(localtime()[0]), width=5)
        sb_year.place(x=170, y=25, height=21)

        # Button calc
        bt_not_calc = Button(window, text='Calcular', background=cor['gray20'], foreground=cor[
                             'white'], font='Arial 10 bold', border=0, relief='flat', command=click_calc)
        bt_not_calc.place(x=75, y=55, width=100)

        # Result
        lb_result = Label(
            window, background=cor['white'], font='Arial 12 bold', justify='center', border=1, relief='solid')
        lb_result.place(x=25, y=85, width=190, height=130)

        # Button back
        bt_back = Button(window, text='Voltar', background=cor['gray20'], foreground=cor['white'],
                         font='Arial 10 bold', border=0, relief='flat', command=click_back)
        bt_back.place(x=5, y=220, width=240, height=25)


# --> Begin's configuration

# Create object
app = Tk()
app.title('')
app.configure(background=cor['white'])
app.bind('<Enter>', lambda event, button=3,
         effect=None: _bt_main_effects(event, button, effect))

# Variable's controls
open_window = False
birth = None


# --> Layout

# Satus bar
app.overrideredirect(True)
frame = Frame(app, background=cor['gray20'])
frame.place(x=0, y=0, width=550, height=20)
frame.bind('<1>', _get_pos)

# icon
icon = PhotoImage(file=search('img', 'icon.png'))
lb_icon = Label(frame, image=icon,
                background=cor['gray20'], border=0, relief='flat')
lb_icon.place(x=0, y=0)

# Title
lb_title = Label(frame, text='Data Provável do Parto',
                 background=cor['gray20'], foreground=cor['white'], font='Arial 8 bold')
lb_title.place(x=210, y=1)
lb_title.bind('<1>', _get_pos)

# Button Minimized
img_min = PhotoImage(file=search('img', 'img4.png'))
lbx0 = Label(frame, image=img_min, border=0, highlightthickness=0)
lbx0.place(x=514, y=3.5, width=12, height=12)
lbx0.bind('<1>', lambda event, close=False: _bt_main_click(event, close))

# Buttons Close
img_close = PhotoImage(file=search('img', 'img3.png'))
lbx1 = Label(frame, image=img_close, border=0, highlightthickness=0)
lbx1.place(x=531, y=3.5, width=12, height=12)
lbx1.bind('<1>', lambda event, close=True: _bt_main_click(event, close))

# Entry Date
img1 = PhotoImage(file=search('img', 'img_textBox0.png'))
entry = Label(app, image=img1, border=0,
              highlightthickness=0, background=cor['white'])
entry.place(x=320, y=170)
entry.bind('<1>', _entry_click)

# Button Next
img2 = PhotoImage(file=search('img', 'img0.png'))
bt_next = Label(app, image=img2, border=0, relief='flat')
bt_next.place(x=422, y=298)
bt_next.bind('<1>', _bt_calc)
bt_next.bind('<Enter>', lambda event, button=1,
             effect=True: _bt_main_effects(event, button, effect))
bt_next.bind('<Leave>', lambda event, button=1,
             effect=False: _bt_main_effects(event, button, effect))

# Button Not Know
img3 = PhotoImage(file=search('img', 'img1.png'))
bt_not_know = Label(app, image=img3, border=0, relief='flat')
bt_not_know.place(x=284, y=298)
bt_not_know.bind('<1>', _bt_not_know)
bt_not_know.bind('<Enter>', lambda event, button=2,
                 effect=True: _bt_main_effects(event, button, effect))
bt_not_know.bind('<Leave>', lambda event, button=2,
                 effect=False: _bt_main_effects(event, button, effect))


# --> Background

# Image
img0 = PhotoImage(file=search('img', 'img2.png'))
lb0 = Label(app, image=img0, border=0, highlightthickness=0)
lb0.place(x=0, y=20)

# Title
lb_info = Label(app, text='Vamos descobrir\nJuntos ?',
                background=cor['white'], foreground=cor['black'], font='Arial 18 bold', justify='center')
lb_info.place(x=315, y=43)

# Entry info
entry_info = Label(app, text='Data da última mestruação',
                   background=cor['white'], foreground=cor['gray54'], font='Arial 8 bold')
entry_info.place(x=330, y=150)

lb_cal = Label(app, background=cor['ice'],
               foreground=cor['gray54'], font='Arial 12 bold')
lb_cal.place(x=335, y=177)
lb_cal.bind('<1>', _entry_click)


# --> END

# Dimension and loop
size((550, 340, 0))
app.mainloop()
