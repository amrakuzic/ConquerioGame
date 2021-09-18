import tkinter as tk
from tkinter.constants import ANCHOR, BOTH, UNDERLINE
from PIL import ImageTk, Image
import pygame
import random


class PrikazPocetne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.can = tk.Canvas(self, bg="black", height=800, width=1000)
        self.can.pack(expand=True, fill=BOTH)
        self.createWidgets(self.master)

    def createWidgets(self, master):
        bgImg = Image.open(
            'images\\bg6.png')
        self.can.image = ImageTk.PhotoImage(bgImg)
        self.can.create_image(100, 200, image=self.can.image)
        # can.update()
        self.can.update_idletasks()
        lbl_naslov = tk.Label(self.can, text="Conquerio", bg='#071268', fg='white', borderwidth=2, relief="solid")
        lbl_naslov.config(font=("Courier", 72), borderwidth=10, relief="raised")
        lbl_naslov.place(relx=.48, rely=.2, anchor="c")
        # text_canvas = can.create_text(450,100,anchor="c",font=("Courier", 72, "bold"),fill="white")
        # can.itemconfig(text_canvas, text="Conquerio")
        okvir = tk.Frame(self.can, height=250, width=200, background="#071268", borderwidth=10, relief="raised")
        okvir.place(relx=.48, rely=.6, anchor="c")
        btn_igraj = tk.Button(okvir,
                              text="Igraj", font=("Courier", 20),
                              bg='#071268', fg='white',
                              borderwidth=0, activebackground='#071268',
                              command=lambda: master.promijeni_prikaz(PrikazIgre))
        btn_igraj.place(relx=.5, rely=.10, anchor="c")

        btn_info = tk.Button(okvir, text="Info", font=("Courier", 20), bg='#071268', fg='white', borderwidth=0,
                             activebackground='#071268', command=lambda: master.promijeni_prikaz(PrikazInfo))
        btn_info.place(relx=.5, rely=.64, anchor="c")
        btn_postavke = tk.Button(okvir, text="Postavke", font=("Courier", 20), bg='#071268', fg='white', borderwidth=0,
                                 activebackground='#071268', command=lambda: master.promijeni_prikaz(PrikazPostavke))
        btn_postavke.place(relx=.5, rely=.46, anchor="c")
        btn_najboljiRez = tk.Button(okvir, text="Rezultati", font=("Courier", 20), bg='#071268', fg='white',
                                    borderwidth=0, activebackground='#071268',
                                    command=lambda: master.promijeni_prikaz(PrikazRezultati))
        btn_najboljiRez.place(relx=.5, rely=.28, anchor="c")
        btn_quit = tk.Button(okvir, text="Izlaz", font=("Courier", 20), bg='#071268', fg='white', borderwidth=0,
                             command=self.master.quit, activebackground='#071268')
        btn_quit.place(relx=.5, rely=.82, anchor="c")
        buttons = [btn_igraj, btn_info, btn_postavke, btn_najboljiRez, btn_quit]

        def on_enter(e):
            e.widget['foreground'] = 'green'
            prvi = pygame.mixer.Channel(0)
            prvi.set_volume(0.1)
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds\\beep.wav'), maxtime=600)

        def on_leave(e):
            e.widget['foreground'] = 'SystemButtonFace'

        for b in buttons:
            b.bind("<Enter>", on_enter)
            b.bind("<Leave>", on_leave)


class PrikazIgre(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.bgcan = tk.Canvas(self, bg="black", height=800, width=1000)
        self.bgcan.pack(expand=True, fill=BOTH)
        bgImg = Image.open(
            'images\\bg6.png')
        self.bgcan.image = ImageTk.PhotoImage(bgImg)
        self.bgcan.create_image(100, 200, image=self.bgcan.image)
        self.__can = tk.Canvas(self, bg="black", height=600, width=800, cursor="sb_h_double_arrow",
                               highlightthickness=0)
        self.createWidgets(self.master)

    @property
    def can(self):
        return self.__can

    def createWidgets(self, master):
        self.can.place(relx=0.1, rely=0.174)
        self.can.update_idletasks()

        okvir = tk.Frame(self, width=800, height=100, bd=2, background="blue", highlightbackground="#000C69",
                         highlightthickness=10)
        okvir.place(relx=0.1, rely=0.05)

        self.lblLvl = tk.Label(okvir, text="L1", bg="blue", font=("Fixedsys", 40), fg="white")
        self.lblLvl.place(relx=0.01, rely=0.05)
        self.lblOsvojenProstor = tk.Label(okvir, text="Osvojeni Prostor: ", bg="blue", font=("Fixedsys", 14),
                                          fg="white")
        self.lblOsvojenProstor.place(relx=0.7, rely=0.2)
        self.lblBodovi = tk.Label(okvir, text="0", bg="blue", font=("Fixedsys", 40), fg="white")
        self.lblBodovi.place(relx=0.45, rely=0.05)

        self.lblBrZivIgrac = tk.Label(okvir, text="Preostalo života: ", bg="blue", font=("Fixedsys", 14), fg="white")
        self.lblBrZivIgrac.place(relx=0.7, rely=0.6)
        btnRestart = tk.Button(self.bgcan, text="Restart", font=("Courier", 20), bg='#071268', fg='white',
                               borderwidth=0, activebackground='#071268',
                               command=lambda: master.restart_igru())
        btnRestart.place(relx=.5, rely=.95, anchor="c")

    def update_labels(self, preostalo_zivota, osvojen_prostor, lvl, bodovi):
        self.lblBrZivIgrac.configure(text='Preostalo života: {0}'.format(preostalo_zivota))
        self.lblOsvojenProstor.configure(text='Osvojeno Prostora: {0}%'.format(osvojen_prostor))
        self.lblLvl.configure(text='L{0}'.format(lvl))
        self.lblBodovi.configure(text='{0}'.format(bodovi))


class PrikazPostavke(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        can = tk.Canvas(self, bg="black", height=800, width=1000)
        can.pack(expand=True, fill=BOTH)
        bgImg = Image.open(
            'images\\bg6.png')
        can.image = ImageTk.PhotoImage(bgImg)
        can.create_image(100, 200, image=can.image)
        can.update()

        naslov = tk.Label(can, text="Postavke", borderwidth=10, relief="raised")
        naslov.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        naslov.config(font=("Courier", 72), background="#071268", fg="#d98600")

        okvir = tk.Frame(can, height=500, width=530, background="#071268", borderwidth=2, relief="solid")
        okvir.place(relx=.5, rely=.5, anchor="c")

        self.lbl_zvuk = tk.Label(okvir, font=("Courier", 20), text="Zvuk   0", anchor="w")
        self.lbl_zvuk.place(relx=0.05, rely=0.1, width=170, height=30)

        self.lbl_glazba = tk.Label(okvir, font=("Courier", 20), text="Glazba 0", anchor="w")
        self.lbl_glazba.place(relx=0.05, rely=0.2, width=170, height=30)

        btnZvukP = tk.Button(okvir, text="Pojacaj", font=("Courier", 12), bg='#071268', fg='white', borderwidth=1,
                             activebackground='#071268',
                             command=master.pojacaj_zvuk)

        btnZvukS = tk.Button(okvir, text="Smanji", font=("Courier", 12), bg='#071268', fg='white', borderwidth=1,
                             activebackground='#071268',
                             command=master.stisaj_zvuk)

        btnGlazbaP = tk.Button(okvir, text="Pojacaj", font=("Courier", 12), bg='#071268', fg='white', borderwidth=1,
                               activebackground='#071268',
                               command=master.pojacaj_glazbu)

        btnGlazbaS = tk.Button(okvir, text="Smanji", font=("Courier", 12), bg='#071268', fg='white', borderwidth=1,
                               activebackground='#071268',
                               command=master.smanji_glazbu)

        btn_vratiSe = tk.Button(can, text="<Nazad", font=("Courier", 20), bg='#071268', fg='white', borderwidth=0,
                                activebackground='#071268',
                                command=lambda: master.promijeni_prikaz(PrikazPocetne))

        btnZvukP.place(relx=.5, rely=.13, anchor="c")
        btnZvukS.place(relx=.7, rely=.13, anchor="c")
        btnGlazbaP.place(relx=.5, rely=.23, anchor="c")
        btnGlazbaS.place(relx=.7, rely=.23, anchor="c")

        btn_vratiSe.place(relx=.5, rely=.9, anchor="c")

    def update_zvuk(self, glasnoca):
        glasnocaZvuk = int(glasnoca * 100)
        self.lbl_zvuk.configure(text='Zvuk  {0}'.format(glasnocaZvuk))

    def update_glazba(self, glasnoca):
        glasnocaGlazba = int(glasnoca * 100)
        self.lbl_glazba.configure(text='Glazba {0}'.format(glasnocaGlazba))


class PrikazRezultati(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        can = tk.Canvas(self, bg="black", height=800, width=1000)
        can.pack(expand=True, fill=BOTH)
        bgImg = Image.open(
            'images\\bg6.png')
        can.image = ImageTk.PhotoImage(bgImg)
        can.create_image(100, 200, image=can.image)
        can.update()

        naslov = tk.Label(can, text="Rezultati", borderwidth=10, relief="raised")
        naslov.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        naslov.config(font=("Courier", 72), fg="#d98600", background="#071268")

        self.okvir = tk.Frame(can, height=500, width=530, background="#071268", borderwidth=2, relief="solid")
        self.okvir.place(relx=.5, rely=.5, anchor="c")
        btn_vratiSe = tk.Button(can, text="<Nazad", font=("Courier", 20), bg='#071268', fg='white', borderwidth=0,
                                activebackground='#071268',
                                command=lambda: master.promijeni_prikaz(PrikazPocetne))
        btn_vratiSe.place(relx=.5, rely=.9, anchor="c")

    def ucitaj_rezultate(self, redniBroj, ime, bodovi, yPozicija):
        lbl = tk.Label(self.okvir, text=redniBroj, fg="white", bg="#071268", font=("Fixedsys", 18))
        lbl.place(relx=0.2, rely=yPozicija)
        lblIme = tk.Label(self.okvir, text=ime, fg="white", bg="#071268", font=("Fixedsys", 18))
        lblIme.place(relx=0.4, rely=yPozicija)
        lblBodovi = tk.Label(self.okvir, text=bodovi, fg="white", bg="#071268", font=("Fixedsys", 18))
        lblBodovi.place(relx=0.7, rely=yPozicija)


class PrikazInfo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        can = tk.Canvas(self, bg="black", height=800, width=1000)
        can.pack(expand=True, fill=BOTH)
        bgImg = Image.open(
            'images\\bg6.png')
        can.image = ImageTk.PhotoImage(bgImg)
        can.create_image(100, 200, image=can.image)
        can.update()
        naslov = tk.Label(can, text="Info", borderwidth=10, relief="raised")
        naslov.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        naslov.config(font=("Courier", 72), fg="#d98600", background="#071268")

        okvir = tk.Frame(can, height=400, width=550, background="#071268", borderwidth=2, relief="solid")
        okvir.place(relx=.5, rely=.5, anchor="c")
        self.lblIspis = tk.Label(okvir, text="", background="#071268", fg='white', font=("Courier", 12))
        self.lblIspis.place(relx=0.5, rely=0.5, anchor="c")
        btn_vratiSe = tk.Button(can, text="<Nazad", font=("Courier", 20), bg='#071268', fg='white', borderwidth=0,
                                activebackground='#071268',
                                command=lambda: master.promijeni_prikaz(PrikazPocetne))
        btn_vratiSe.place(relx=.5, rely=.9, anchor="c")

    def ucitaj_info(self):
        self.lblIspis.configure(text='__________________________________________________\n\n'
                                     'KAKO IGRATI CONQUERIO\n'
                                     '__________________________________________________\n\n'
                                     'Lijevi klik miša --> GRADNJA ZIDA                 \n'
                                     'Desni klik miša --> PROMJENA SMJERA ZIDA          \n'
                                     'Pomicanje miša --> ODABIR LOKACIJE ZA GRADNJU ZIDA\n'
                                     '\n'
                                     '__________________________________________________\n'
                                     '\n'
                                     'CILJ IGRE\n'
                                     '__________________________________________________\n\n'
                                     'Osvojiti što više prostora gradnjom zida.         \n'
                                     'Zid je izgrađen ako dodirne neaktivan rub okvira  \n'
                                     'bez da ga pritom dotakne neka loptica.            \n'
                                     'Osvajanjem minimalno 75% okvira igrač             \n'
                                     'prelazi na sljedeći lvl.                          \n'
                                     'Igra završava kad igrač ostane bez života.        \n'
                                .format())


class PrikazGameOver(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        can = tk.Canvas(self, bg="black", height=800, width=1000)
        can.pack(expand=True, fill=BOTH)
        bgImg = Image.open(
            'images\\game_over.png')
        can.image = ImageTk.PhotoImage(bgImg)
        can.create_image(500, 250, image=can.image)
        can.update()
        self.lblIme = tk.Label(can, text="Ime   ", background="#424141", fg='white', font=("Courier", 20))
        self.lblIme.place(relx=0.4, rely=0.6, anchor="c")
        self.entIme = tk.Entry(can, background="#424141", fg='white', font=("Courier", 20))
        self.entIme.place(relx=0.6, rely=0.6, width=100, anchor="c")
        self.lblBodovi = tk.Label(can, text="Bodovi", background="#424141", fg='white', font=("Courier", 20))
        self.lblBodovi.place(relx=0.4, rely=0.7, anchor="c")
        self.lblBodoviIgrac = tk.Label(can, text="0", background="#424141", fg='white', font=("Courier", 20))
        self.lblBodoviIgrac.place(relx=0.6, rely=0.7, anchor="c")
        self.btnOk = tk.Button(can, text="Ok", background="#424141", fg='white', font=("Courier", 20),
                               command=lambda: self.master.upisi_rezultat(self.entIme.get()))
        self.btnOk.place(relx=0.45, rely=0.8)

    def ispisi_bodove(self, bodovi):
        self.lblBodoviIgrac.configure(text=bodovi)
