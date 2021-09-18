import os
from prikaz import *
from model import *
import random


class Conquerio(tk.Tk):
    def __init__(self, prikaz):
        tk.Tk.__init__(self)
        self.postavi_prozor()

        # za kontroliranje PrikazIgre
        self.igrac = Igrac()
        self.lvl = 1
        self.misKoord = [0, 0]
        self.smjerGradnje = -1
        self.dopustenaGradnja = True
        self.mis_kliknut = False
        self.zidKreiran = False
        self.osvojenProstor = 0
        self.povrsinaOkvira = 800 * 600
        self.presaoLvl = False
        # ucitaj pocetni okvir(view)
        self._prikaz = None
        # self.createBindings()

        # za manipulaciju view-a
        self.aktivna = "PrikazPocetne"
        self.ucitaj_glazbu()
        self.cursors = ["sb_h_double_arrow", "sb_v_double_arrow"]
        # self.zid = Zid(self.frame.can, "blue", -20, -20, -20, -20, 2)
        self.promijeni_prikaz(prikaz)

    @property
    def prikaz(self):
        return self._prikaz

    @prikaz.setter
    def prikaz(self, value):
        self._prikaz = value

    def postavi_prozor(self):
        WIDTH, HEIGHT = 1000, 800

        # sirina i visina ekrana
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()

        # za polozaj prozora
        x = (ws / 2) - (WIDTH / 2)
        y = (hs / 2) - (HEIGHT / 2)

        self.geometry('%dx%d+%d+%d' % (WIDTH, HEIGHT, x, y))

        self.title("Conquerio")
        self.resizable(width=False, height=False)

    @staticmethod
    def ucitaj_glazbu():
        pygame.mixer.pre_init()
        pygame.mixer.init()
        pygame.init()
        pygame.mixer.music.load(os.path.join(os.getcwd(), 'music', 'song.wav'))
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(loops=-1)

    def restart_igru(self):
        Koordinate.izbrisi_sve_zidove()
        self.destroy()
        appl = Conquerio(PrikazPocetne)
        appl.mainloop()

    def promijeni_prikaz(self, prikaz):
        # unistava postojeci prikaz i postavlja drugi
        novi_prikaz = prikaz(self)
        ime = prikaz(self).__class__.__name__
        self.aktivna = ime
        if self.prikaz is not None:
            self.prikaz.destroy()
        self.prikaz = novi_prikaz
        self.prikaz.pack(expand=True, fill=BOTH)

        if self.aktivna == "PrikazIgre":
            # kontroliraj prikaz igre
            loptice = self.ucitaj_loptice(self.lvl)

            self.tijek_igre(loptice)
        if self.aktivna == "PrikazRezultati":
            # kontroliraj prikaz rezultata
            with open("rezultati.txt", "r") as file:
                tekst = file.readlines()
                sviRez = {}
                for linija in tekst:
                    ime = linija.split(":")
                    sviRez[ime[0]] = ime[1]
            sortirani = dict(sorted(sviRez.items(), key=lambda x: int(x[1]), reverse=True))
            yPoz = 0.02
            brojac = 0
            for i in sortirani:
                self.prikaz.ucitaj_rezultate(str(brojac + 1), i, sortirani[i], yPoz)
                yPoz += 0.1
                brojac += 1
                if brojac == 10:
                    break

        if self.aktivna == "PrikazInfo":
            # kontrolira prikaz info
            self.prikaz.ucitaj_info()

        if self.aktivna == "PrikazGameOver":
            # kontrolira prikaz game over
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds\\game_over.wav'), maxtime=2000)
            pygame.mixer.Channel(1).set_volume(0.1)
            self.ispisi_bodove()

    # za kontrolu PrikazIgre
    def ucitaj_loptice(self, lvl):
        rKLop = []
        for i in range(lvl + 2):
            x0L = random.randint(100, 700)
            y0L = random.randint(100, 500)
            rKLop.append((x0L, y0L))
        boje = ["green", "blue", "white", "yellow", "purple"]
        loptice = []
        for i in range(lvl + 2):
            broj = random.randint(0, len(boje) - 1)
            boja = boje[broj]
            prviSmjer = 0
            drugiSmjer = 0

            # sve dok brzine loptica nisu -2 ili 2
            while -2 < prviSmjer < 2:
                prviSmjer = random.randint(-2, 2)
            while -2 < drugiSmjer < 2:
                drugiSmjer = random.randint(-2, 2)

            lopta = Lopta(self.prikaz.can, rKLop[i][0], rKLop[i][1], rKLop[i][0] + 40, rKLop[i][1] + 40, prviSmjer,
                          drugiSmjer, boja)
            loptice.append(lopta)
        return loptice

    def tijek_igre(self, loptice, spremljeniBodovi=0):
        zid = Zid(self.prikaz.can, "orange", -10, -10, -10, -10, self.smjerGradnje)
        self.zidKreiran = True
        while self.aktivna == "PrikazIgre":
            if not self.zidKreiran:
                zid = Zid(self.prikaz.can, "orange", -10, -10, -10, -10, self.smjerGradnje)
                self.zidKreiran = True


            # ako je gradnja dozvoljena postavi mogućnost pritiskanja lijevog i desnog klika miša
            if self.dopustenaGradnja is True:
                self.prikaz.can.bind('<ButtonRelease-3>', self.promijeni_smjer)
                self.prikaz.can.bind('<ButtonRelease-1>', self.pocetakGradnje)
            else:
                self.prikaz.can.unbind('<ButtonRelease-1>')
                self.prikaz.can.unbind('<ButtonRelease-3>')

            # ako je igrač započeo gradnju zida
            if self.mis_kliknut is True:
                # dohvacanje koordinata za gradnju zida
                abs_coord_x = self.winfo_pointerx() - self.prikaz.can.winfo_rootx()
                abs_coord_y = self.winfo_pointery() - self.prikaz.can.winfo_rooty()
                koord = [abs_coord_x, abs_coord_y]
                # ako su koordinate slobodne za gradnju
                if Koordinate.koordinate_slobodne(koord) is True:
                    zid.uIzgradnji = True
                    zid.smjer = self.smjerGradnje
                    self.prikaz.can.coords(zid.image, abs_coord_x, abs_coord_y, abs_coord_x + 10, abs_coord_y + 10)
                # ako koordinate nisu slobode
                else:
                    zid.uIzgradnji = False
                    self.dopustenaGradnja = True
                self.mis_kliknut = False

            self.kretnjaLoptica(loptice)
            x0Z, y0Z, x1Z, y1Z = self.prikaz.can.coords(zid.image)
            # ako se zid gradi i zid nije izgradjen
            if zid.uIzgradnji is True and zid.izgradjen() is False:
                # napravi korak gradnje zida
                zid.gradiSe()
                # ako postoji prazan prostor proširi zid, inače dodaj zid u listu zidova
            if zid.izgradjen():
                if zid.prazanProstorDesno() is True or zid.prazanProstorLijevo() is True \
                        or zid.prazanProstorGore() is True or zid.prazanProstorDolje() is True:
                    zid.prosiri()
                else:
                    Koordinate.dodajZid(x0Z, y0Z, x1Z, y1Z, zid.smjer)
                self.dopustenaGradnja = True
                self.zidKreiran = False
                self.racunaj_osvojeni_prostor()
                self.igrac.bodovi = int(self.osvojenProstor * 15 + spremljeniBodovi)

                # sve dok igrač nije osvojio 75% računaj osvojenu površinu
                if self.osvojenProstor >= 75:
                    # ucitaj novi lvl
                    self.ucitaj_novi_lvl()
                    return 0
            # provjera dira li koja loptica zid u gradnji
            # ako dira onda smanji igracu zivot
            for i in range(len(Koordinate.loptice())):
                x0L = int(Koordinate.loptice()[i][0])
                y0L = int(Koordinate.loptice()[i][1])
                x1L = int(Koordinate.loptice()[i][2])
                y1L = int(Koordinate.loptice()[i][3])
                # ako loptica dira zid u gradnji
                if y1Z >= y1L >= y0Z and x1Z >= x1L >= x0Z or y1Z >= y0L >= y0Z and x1Z >= x0L >= x0Z:
                    self.igrac.brojZivota -= 1
                    self.dopustenaGradnja = True
                    zid.uIzgradnji = False
                    self.prikaz.can.coords(zid.image, -10, -10, -10, -10)

            # ako je igrač izgubio
            if self.igrac.brojZivota == 0:
                self.aktivna = "PrikazGameOver"
                self.promijeni_prikaz(PrikazGameOver)
                return 0

            self.prikaz.update_labels(self.igrac.brojZivota, self.osvojenProstor, self.lvl, self.igrac.bodovi)
            self.update()
            self.update_idletasks()


            self.prikaz.update_idletasks()
            self.prikaz.update()
            self.after(6)

    def kretnjaLoptica(self, listaLoptica):
        noveKoord = []
        for lopta in listaLoptica:
            lopta.kretnja()
            try:
                x0, y0, x1, y1 = self.prikaz.can.coords(lopta.image)
                koords = [x0, y0, x1, y1]
                noveKoord.append(koords)
                Koordinate.updateLoptice(noveKoord)
            except:
                print("nema koordinata")

        for lopta in listaLoptica:
            if lopta.diraZid() is True or lopta.diraOkvir():
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds\\ball_hit.wav'), maxtime=600)
                pygame.mixer.Channel(0).set_volume(0.1)
                lopta.promijeni_smjer()

    def pocetakGradnje(self, zid):
        self.mis_kliknut = True
        self.dopustenaGradnja = False

    def promijeni_smjer(self, event):
        self.smjerGradnje *= (-1)
        self.cursors.reverse()
        # update cursor na prikazu
        self.prikaz.can.configure(cursor=self.cursors[0])

    def ucitaj_novi_lvl(self):
        # print("ucitan novi lvl")
        Koordinate.izbrisi_sve_zidove()
        Koordinate.izbrisi_sve_loptice()
        self.lvl += 1
        spremljeniBodovi = self.igrac.bodovi
        self.igrac.bodovi = int(self.osvojenProstor * 15 + spremljeniBodovi)
        self.osvojenProstor = 0
        self.update()
        self.after(400)
        self.prikaz.can.delete("all")
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('sounds\\success.wav'), maxtime=2000)
        pygame.mixer.Channel(1).set_volume(0.1)
        loptice = self.ucitaj_loptice(self.lvl)
        self.after(5, lambda: self.tijek_igre(loptice, spremljeniBodovi))

    def racunaj_osvojeni_prostor(self):
        # print("racunaj osvojeni prostor")
        ukupnaPovrsina = 0
        for i in range(len(Koordinate.zidovi())):
            x0 = int(Koordinate.zidovi()[i][0])
            y0 = int(Koordinate.zidovi()[i][1])
            x1 = int(Koordinate.zidovi()[i][2])
            y1 = int(Koordinate.zidovi()[i][3])
            povrsinaZida = (x1 - x0) * (y1 - y0)
            ukupnaPovrsina += povrsinaZida
        self.osvojenProstor = int(ukupnaPovrsina / self.povrsinaOkvira * 100)

    #za kontrolu PrikazPostavke
    def pojacaj_zvuk(self):
        glasnoca = pygame.mixer.Channel(0).get_volume()
        glasnoca2 = pygame.mixer.Channel(1).get_volume()
        pygame.mixer.Channel(0).set_volume(glasnoca + 0.1)
        pygame.mixer.Channel(1).set_volume(glasnoca2 + 0.1)
        self.prikaz.update_zvuk(glasnoca)

    def stisaj_zvuk(self):
        glasnoca = pygame.mixer.Channel(0).get_volume()
        glasnoca2 = pygame.mixer.Channel(1).get_volume()
        pygame.mixer.Channel(0).set_volume(glasnoca - 0.1)
        pygame.mixer.Channel(1).set_volume(glasnoca2 - 0.1)
        self.prikaz.update_zvuk(glasnoca)

    def pojacaj_glazbu(self):
        glasnoca = pygame.mixer.music.get_volume()
        novaGlasnoca = glasnoca + 0.1
        if novaGlasnoca > 1:
            novaGlasnoca = 1
        pygame.mixer.music.set_volume(novaGlasnoca)

        self.prikaz.update_glazba(novaGlasnoca)

    def smanji_glazbu(self):
        glasnoca = pygame.mixer.music.get_volume()
        novaGlasnoca = glasnoca - 0.1
        if novaGlasnoca < 0:
            novaGlasnoca = 0
        pygame.mixer.music.set_volume(novaGlasnoca)
        self.prikaz.update_glazba(novaGlasnoca)

    # za kontroliranje PrikazGameOver
    def upisi_rezultat(self, ime):
        bodovi = str(self.igrac.bodovi)
        f = open("rezultati.txt", "a")
        rez = ime + ":" + bodovi + ":"
        f.write(rez + "\n")
        f.close()
        self.after(10, self.restart_igru)

    def ispisi_bodove(self):
        self.prikaz.ispisi_bodove(self.igrac.bodovi)


if __name__ == "__main__":
    app = Conquerio(PrikazPocetne)
    app.mainloop()
