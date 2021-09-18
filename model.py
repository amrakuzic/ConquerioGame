from tkinter import *


class Lopta(object):
    def __init__(self, canvas, xPozicija, yPozicija, promjerX, promjerY, xBrzina, yBrzina, boja):
        self.__canvas = canvas
        self.__boja = boja
        self.__image = canvas.create_oval(xPozicija, yPozicija, promjerX, promjerY, fill=boja, outline='')
        self.__xBrzina = xBrzina
        self.__yBrzina = yBrzina
        self.__promjer = promjerX - xPozicija

    @property
    def image(self):
        return self.__image

    @property
    def promjer(self):
        return self.__promjer

    @property
    def xBrzina(self):
        return self.__xBrzina

    @property
    def yBrzina(self):
        return self.__yBrzina

    @xBrzina.setter
    def xBrzina(self, value):
        self.__xBrzina = value

    @yBrzina.setter
    def yBrzina(self, value):
        self.__yBrzina = value

    def promijeni_smjer_x(self):
        self.xBrzina = -self.xBrzina

    def promijeni_smjer_y(self):
        self.yBrzina = -self.yBrzina

    def diraGore(self):
        dira = False
        try:
            x0, y0, x1, y1 = self.__canvas.coords(self.__image)
        except:
            x0, y0, x1, y1 = [-10, -10, -10, -10]
        # Za okvir
        for i in range(len(Koordinate.zidovi())):
            x0Z = int(Koordinate.zidovi()[i][0])
            y0Z = int(Koordinate.zidovi()[i][1])
            x1Z = int(Koordinate.zidovi()[i][2])
            y1Z = int(Koordinate.zidovi()[i][3])
            if self.promjer <= y1 - y1Z <= self.promjer + 2 and (x0Z <= x0 <= x1Z):
                # zanemari vertikalne zidove
                # ako je horizontalni zid zanemari
                if y0 == 0 or y1 == 600:
                    continue
                # print("Dira Zid Lijevo")
                dira = True
                return dira
        return dira

    def diraDolje(self):
        # loptica   O
        #          |
        #  (ide dolje i udara u gornji dio zida)
        #       _______
        dira = False

        try:
            x0, y0, x1, y1 = self.__canvas.coords(self.__image)
        except:
            x0, y0, x1, y1 = [-10, -10, -10, -10]
        for i in range(len(Koordinate.zidovi())):
            x0Z = int(Koordinate.zidovi()[i][0])
            y0Z = int(Koordinate.zidovi()[i][1])
            x1Z = int(Koordinate.zidovi()[i][2])
            y1Z = int(Koordinate.zidovi()[i][3])
            smjerZ = int(Koordinate.zidovi()[i][4])
            if self.promjer <= y0Z - y0 <= self.promjer + 2 and (x0Z <= x0 <= x1Z):
                y1 = y1 + (y0Z - y1 - 2)
                self.__canvas.coords(self.__image, x0, y0, x1, y1)
                # print("Dira doljeeeee")
                if y0 == 0 or y1 == 600:
                    continue
                dira = True
                return dira

                # Za okvir
        return dira

    def diraDesno(self):
        dira = False
        try:
            x0, y0, x1, y1 = self.__canvas.coords(self.__image)
        except:
            x0, y0, x1, y1 = [-10, -10, -10, -10]

        for i in range(len(Koordinate.zidovi())):
            x0Z = int(Koordinate.zidovi()[i][0])
            y0Z = int(Koordinate.zidovi()[i][1])
            x1Z = int(Koordinate.zidovi()[i][2])
            y1Z = int(Koordinate.zidovi()[i][3])
            smjerZ = int(Koordinate.zidovi()[i][4])
            if x0Z - x0 <= self.promjer and 1 > x0Z - x1 > -5 and (y0Z <= y0 <= y1Z) and smjerZ == 1:
                x1 = x1 + (x0Z - x1)
                # x0 = x0 + (koordinata-x1-1)
                self.__canvas.coords(self.__image, x0, y0, x1, y1)
                # ako je horizontalni zid zanemari
                if x0 == 0 or x1 == 800:
                    continue
                # print("Dira Zid Lijevo")
                dira = True
                return dira
        return dira

    def diraOkvirDesno(self):
        dira = False
        try:
            x0, y0, x1, y1 = self.__canvas.coords(self.__image)
        except:
            x0, y0, x1, y1 = [-10, -10, -10, -10]
        if 794 < x1 < 800:
            dira = True
        return dira

    def diraOkvirGore(self):
        dira = False
        try:
            x0, y0, x1, y1 = self.__canvas.coords(self.__image)
        except:
            x0, y0, x1, y1 = [-10, -10, -10, -10]
        if 0 < y0 < 6:
            dira = True
        return dira

    def diraOkvirDolje(self):
        dira = False
        try:
            x0, y0, x1, y1 = self.__canvas.coords(self.__image)
        except:
            x0, y0, x1, y1 = [-10, -10, -10, -10]
        if 594 < y1 < 600:
            dira = True
        return dira

    def diraOkvirLijevo(self):
        dira = False
        try:
            x0, y0, x1, y1 = self.__canvas.coords(self.__image)
        except:
            x0, y0, x1, y1 = [-10, -10, -10, -10]
        if 0 < x0 < 6:
            dira = True
        return dira

    def diraOkvir(self):
        dira = False
        diraDesniOkvir = self.diraOkvirDesno()
        diraLijeviOkvir = self.diraOkvirLijevo()
        diraGornjiOkvir = self.diraOkvirGore()
        diraDonjiOkvir = self.diraOkvirDolje()
        if diraLijeviOkvir is True or diraDesniOkvir is True or diraGornjiOkvir is True or diraDonjiOkvir is True:
            dira = True
        return dira

    def diraLijevo(self):
        # | <- O
        dira = False
        # dira = ""
        try:
            x0, y0, x1, y1 = self.__canvas.coords(self.__image)
        except:
            x0, y0, x1, y1 = [0, 0, 0, 0]

        if x0 == Koordinate.okvir_xPocetak():
            # print(f'pocetna lopte {x0} ++++ pocetna zida{Koordinate.okvir_xPocetak()}')
            dira = True
            # print("Dira Okvir Lijevo")
            # self.__canvas.coords(self.__image, x0+100,y0,x1+100,y1)
            return dira
        # listaSvihZidova = Koordinate.zidovi()
        for i in range(len(Koordinate.zidovi())):
            x0Z = int(Koordinate.zidovi()[i][0])
            y0Z = int(Koordinate.zidovi()[i][1])
            x1Z = int(Koordinate.zidovi()[i][2])
            y1Z = int(Koordinate.zidovi()[i][3])
            smjerZ = int(Koordinate.zidovi()[i][4])
            if x1 - x1Z <= self.promjer and 1 > x0 - x1Z > -5 and (y0Z <= y0 <= y1Z) and smjerZ == 1:
                # print("lijevooo")
                x1 = x1 + (x1Z - x1)
                # ako je horizontalni zid zanemari
                if x0 == 0 or x1 == 800:
                    continue
                # print(f'LKL{x0} DKZ{koordinata}  DKL{x1}')
                # print("Dira Zid Lijevo")
                dira = True
                # dira = "l"
                return dira
        return dira

    def diraZid(self):
        # print("IzvrSava se diraZidFunk")
        diraLijevo = self.diraLijevo()
        diraDesno = self.diraDesno()
        diraGore = self.diraGore()
        diraDolje = self.diraDolje()
        if diraGore is True or diraLijevo is True or diraDesno is True or diraDolje is True:
            return True
        return False

    def promijeni_smjer(self):
        if self.diraGore() is True or self.diraOkvirDolje() is True:
            # Ako loptica dira s gornjim svojim dijelom nešto
            self.promijeni_smjer_y()
        if self.diraDolje() is True or self.diraOkvirGore() is True:
            self.promijeni_smjer_y()
        if self.diraOkvirDesno() is True or self.diraDesno() is True:
            self.promijeni_smjer_x()
        if self.diraLijevo() is True or self.diraOkvirLijevo() is True:
            self.promijeni_smjer_x()

    def kretnja(self):
        self.__canvas.move(self.__image, self.xBrzina, self.yBrzina)


class Zid(object):
    def __init__(self, prikaz, boja, xPocetak=0, yPocetak=0, xKraj=0, yKraj=0, smjer=-1):
        self.__prikaz = prikaz
        self.__boja = "orange"
        self.__koordinate = [xPocetak, yPocetak, xKraj, yKraj]
        # self.__prikaz.coords = koord
        self.__image = self.prikaz.create_rectangle(self.koordinate[0], self.koordinate[1], self.koordinate[2],
                                                    self.koordinate[3], fill=boja, outline="white")
        self.__uIzgradnji = False
        self.__gradnjaDozvoljena = True
        self.gotovaGradnjaGore = False
        self.gotovaGradnjaDolje = False
        self.gotovaGradnjaLijevo = False
        self.gotovaGradnjaDesno = False
        self.dodanUListuZidova = False
        self.__smjer = smjer

    @property
    def prikaz(self):
        return self.__prikaz

    @prikaz.setter
    def prikaz(self, value):
        self.__prikaz = value

    @property
    def smjer(self):
        return self.__smjer

    @smjer.setter
    def smjer(self, value):
        self.__smjer = value

    @property
    def uIzgradnji(self):
        return self.__uIzgradnji

    @property
    def gradnjaDozvoljena(self):
        return self.__gradnjaDozvoljena

    @gradnjaDozvoljena.setter
    def gradnjaDozvoljena(self, value):
        self.__gradnjaDozvoljena = value

    @property
    def koordinate(self):
        return self.__koordinate

    @koordinate.setter
    def koordinate(self, value):
        self.__koordinate = value

    @property
    def image(self):
        return self.__image

    @uIzgradnji.setter
    def uIzgradnji(self, value):
        self.__uIzgradnji = value

    def gradiSe(self):
        # self.nijeUGradnji = False
        x0, y0, x1, y1 = self.prikaz.coords(self.__image)
        # print(f'Koordinate novog zida: {x0} {y0} {x1} {y1}')
        # print("Korak zida se napravio")
        if self.smjer == 1:
            if self.gotovaGradnjaGore is False:
                y0 = y0 - 3
                # print("Gradi se gore")
            if self.gotovaGradnjaDolje is False:
                y1 += 3
                # print("Gradi se dole")
            # gradi jednu vrstu zida
        if self.smjer == -1:
            if self.gotovaGradnjaLijevo is False:
                # print("Gradi se lijevo")
                x0 -= 3
            # gradi drugu vrstu zida
            if self.gotovaGradnjaDesno is False:
                # print("Gradi se desno")
                x1 += 3

        # y1 +=5

        self.prikaz.coords(self.__image, x0, y0, x1, y1)

    # def zidIzgradjenLijevo
    def izgradjen(self):
        # nije dotaknuo oba ruba okvira
        izgradjen = False
        self.gotovaGradnjaGore = False
        self.gotovaGradnjaDolje = False
        self.gotovaGradnjaLijevo = False
        self.gotovaGradnjaDesno = False
        try:
            x0, y0, x1, y1 = self.prikaz.coords(self.__image)
        except:
            print("nema koord za dohvatiti")
            x0, y0, x1, y1 = [0, 0, 0, 0]

        # x provjera
        if y0 < Koordinate.okvir_yPocetak():
            self.gotovaGradnjaGore = True
        if y1 > Koordinate.okvir_yKraj():
            self.gotovaGradnjaDolje = True
        if x0 < Koordinate.okvir_xPocetak():
            self.gotovaGradnjaLijevo = True
        if x1 > Koordinate.okvir_xKraj():
            self.gotovaGradnjaDesno = True
        # svi napravljeni zidovio

        listaSvihZidova = Koordinate.zidovi()
        izgradjenX0 = False
        izgradjenY0 = False
        izgradjenX1 = False
        izgradjenY1 = False
        for i in range(len(listaSvihZidova)):
            x0Z = int(listaSvihZidova[i][0])
            y0Z = int(listaSvihZidova[i][1])
            x1Z = int(listaSvihZidova[i][2])
            y1Z = int(listaSvihZidova[i][3])
            if -2 <= x0 - x1Z <= 6 and y0Z <= y0 <= y1Z and self.smjer == -1:
                # lijevo je izgradjeno
                izgradjenX0 = True
                self.gotovaGradnjaLijevo = True
                x0 = x1Z
            if -2 <= x0Z - x1 <= 6 and y0Z <= y0 <= y1Z and x0Z > 0 and self.smjer == -1:
                # print(f'x0Z-x1{x0Z - x1}')
                self.gotovaGradnjaDesno = True
                izgradjenX1 = True
                x1 = x0Z
            if -2 <= y0 - y1Z <= 6 and x0Z <= x0 <= x1Z and self.smjer == 1:
                # print("testaaa")
                izgradjenY0 = True
                self.gotovaGradnjaGore = True
                # print(self.gotovaGradnjaGore)
                y0 = y1Z
            if -2 < y0Z - y1 <= 6 and x0Z <= x0 <= x1Z and self.smjer == 1:
                izgradjenY1 = True
                self.gotovaGradnjaDolje = True
                y1 = y0Z
        self.prikaz.coords(self.__image, x0, y0, x1, y1)

        if (self.gotovaGradnjaGore is True and self.gotovaGradnjaDolje is True or
                (self.gotovaGradnjaDesno is True and self.gotovaGradnjaLijevo is True) or
                (izgradjenX0 is True and izgradjenX1 is True) or
                (izgradjenY0 is True and izgradjenY1 is True)):
            self.uIzgradnji = False
            izgradjen = True
            self.__gradnjaDozvoljena = True
            # Zid je napravljen, moze se ponovno inicirati rad zida

        return izgradjen

    def prazanProstorDesno(self):
        prazan = False
        koordSvihLoptica = Koordinate.loptice()
        x0, y0, x1, y1 = self.prikaz.coords(self.image)
        for loptica in koordSvihLoptica:
            # print(koordinata)
            if loptica[0] < x0 or (loptica[0] >= x0 and (loptica[3] < y0 or loptica[1] > y1)) and self.smjer == 1:
                prazan = True
            else:
                prazan = False
                break
        # gledamo ima li loptica desno od zida tj je li bilo koji x0 loptice veći od x0 zida
        # Ako nema loptica desno od zida koji se izgradio vrati True
        # Za svaku loptu u listi loptica: ako je x1 koordinata loptice veca od x0 zida
        return prazan

    def prazanProstorLijevo(self):
        prazan = False
        koordSvihLoptica = Koordinate.loptice()
        # koordinateZida
        x0, y0, x1, y1 = self.prikaz.coords(self.image)
        for loptica in koordSvihLoptica:
            # print(koordinata)
            # ako je vertikalni
            if loptica[0] > x1 or (loptica[0] <= x1 and (loptica[3] < y0 or loptica[1] > y1)) and self.smjer == 1:
                prazan = True
            else:
                prazan = False
                break
        # Ako nema loptica lijevo od zida vrati True
        return prazan

    def prazanProstorGore(self):
        prazan = False
        koordSvihLoptica = Koordinate.loptice()
        # koordinateZida
        x0, y0, x1, y1 = self.prikaz.coords(self.image)
        for loptica in koordSvihLoptica:
            # print(koordinata)
            # ako je vertikalni
            if (loptica[1] > y0 or (loptica[1] <= y1 and (loptica[2] < x0 or loptica[0] > x1))) and self.smjer == -1:
                prazan = True
            else:
                prazan = False
                break
        # Ako nema loptica lijevo od zida vrati True
        return prazan

    def prazanProstorDolje(self):
        # Ako nema loptica dolje od zida vrati True
        prazan = False
        koordSvihLoptica = Koordinate.loptice()
        # koordinateZida
        x0, y0, x1, y1 = self.prikaz.coords(self.image)
        for loptica in koordSvihLoptica:
            # print(koordinata)
            # ako je vertikalni
            if (loptica[3] < y0 or (loptica[3] >= y0 and (loptica[2] < x0 or loptica[0] > x1))) and self.smjer == -1:
                prazan = True
            else:
                prazan = False
                break
        # Ako nema loptica lijevo od zida vrati True
        return prazan

    def prosiri(self):
        if self.prazanProstorDesno() is True:
            # proširi desno
            # print("PRazan desno")
            x0, y0, x1, y1 = self.prikaz.coords(self.__image)
            # pronaci ce x0 od prvog sljedeceg desnog zida (ili okvira) i izgraditi ga do tamo
            listaSvihZidova = Koordinate.zidovi()
            listax0KoordSvihZ = [int(zidKoordinate[0]) for zidKoordinate in listaSvihZidova]
            listax0KoordSvihZ.sort()
            # print(f'soritrane x0 koord {list(listax0KoordSvihZ)}')
            # ako nema niti jednog napravljenog zida, proširi do ruba okvira
            # ili ako su svi napravljeni zidovi lijevo
            sviLijevo = True
            for koord in listax0KoordSvihZ:
                if koord >= x1 and self.smjer == 1:
                    sviLijevo = False
                    # print("ima zid lijevo")
            if (len(listax0KoordSvihZ) == 0 or sviLijevo is True) and self.smjer == 1:
                x1 = x1 + (800 - x1)
                # print(f"ovo se aktiviralo {x1}")

            # prosiri do najblizeg desnog vertikalnog zida
            for koord in listax0KoordSvihZ:
                if koord >= x1 and self.smjer == 1:
                    x1 = x1 + (koord - x1)
                    break
                # if len(listax0KoordSvihZ) == 0 or prosiren==False:
                # x1 = x1 + (800 - x1)
                # print(f"ovo se aktiviralo {x1}")

            self.prikaz.coords(self.__image, x0, y0, x1, y1)

            # print(f"ovo se aktiviralo 2 {x1}")
            if x0 not in listax0KoordSvihZ or x0 == 0:
                # print(f"ovo se aktiviralo 3 {x1}")
                Koordinate.dodajZid(x0, y0, x1, y1, self.smjer)
                # print(Koordinate.zidovi())
                self.dodanUListuZidova = True

        if self.prazanProstorLijevo() is True:
            # proširi lijevo
            # print("prazan prostor levo")
            x0, y0, x1, y1 = self.prikaz.coords(self.__image)
            # ako nema napravljenog zida proširi do lijevog ruba okvira
            listaSvihZidova = Koordinate.zidovi()
            listax1KoordSvihZ = [int(zidKoordinate[2]) for zidKoordinate in listaSvihZidova]
            listax1KoordSvihZ.sort(reverse=True)
            for koord in listax1KoordSvihZ:
                if koord <= x0 and self.smjer == 1:
                    break
            # prosiri do najblizeg lijevog vertikalnog zida
            prosiren = False
            for zid in listaSvihZidova:
                # trazi prvi zid lijevo
                if zid[2] <= x0 and zid[1] <= y0 <= zid[3] and self.smjer == 1:
                    x0 = x0 - (x0 - zid[2])
                    prosiren = True
                    break
            # ako nema zida lijevo, a ima napravljenih ili nema zidova uopce
            if len(listaSvihZidova) == 0 or prosiren is False:
                x0 = x0 + (0 - x0)
            self.prikaz.coords(self.__image, x0, y0, x1, y1)
            if x1 not in listax1KoordSvihZ or x0 == 0:
                Koordinate.dodajZid(x0, y0, x1, y1, self.smjer)
                self.dodanUListuZidova = True

        if self.prazanProstorGore() is True:
            # proširi gore
            x0, y0, x1, y1 = self.prikaz.coords(self.__image)
            listaSvihZidova = Koordinate.zidovi()
            listay1KoordSvihZ = [int(zidKoordinate[3]) for zidKoordinate in listaSvihZidova]
            listay1KoordSvihZ.sort()
            prosiren = False
            for zid in listaSvihZidova:
                # trazi prvi zid gore, ako postoji zid iznad i x koordinate zida su iznad
                if zid[3] <= y0 and zid[0] <= x1 <= zid[2] and self.smjer == -1:
                    y0 = y0 - (y0 - zid[3])
                    prosiren = True
                    break
            # ako nema zida lijevo, a ima napravljenih ili nema zidova uopce
            if len(listaSvihZidova) == 0 or prosiren is False:
                y0 = 0
            self.prikaz.coords(self.__image, x0, y0, x1, y1)
            if y1 not in listay1KoordSvihZ or x0 == 0:
                Koordinate.dodajZid(x0, y0, x1, y1, self.smjer)
                self.dodanUListuZidova = True

        if self.prazanProstorDolje() is True:
            # proširi dolje
            x0, y0, x1, y1 = self.prikaz.coords(self.__image)
            listaSvihZidova = Koordinate.zidovi()
            listay0KoordSvihZ = [int(zidKoordinate[1]) for zidKoordinate in listaSvihZidova]
            listay0KoordSvihZ.sort()
            prosiren = False
            for zid in listaSvihZidova:
                # trazi prvi zid dolje, ako postoji zid ispod i x koordinate zida su ispod
                if zid[1] >= y1 and zid[0] <= x1 <= zid[2] and self.smjer == -1:
                    # print(koord)
                    y1 = y1 + (zid[1] - y1)
                    # print("prosiren je dole do prvog zida")
                    prosiren = True
                    break
            # ako nema zida lijevo, a ima napravljenih ili nema zidova uopce
            if len(listaSvihZidova) == 0 or prosiren is False:
                # print("nema zidova ili nije prosiren")
                y1 = y1 + (600 - y1)
            self.prikaz.coords(self.__image, x0, y0, x1, y1)
            if y0 not in listay0KoordSvihZ or x0 == 0:
                Koordinate.dodajZid(x0, y0, x1, y1, self.smjer)
                self.dodanUListuZidova = True


class Koordinate(object):
    __zidovi = []
    __loptice = []
    __okvir_xPocetak = 0.0
    __okvir_yPocetak = 0.0
    __okvir_xKraj = 800.0
    __okvir_yKraj = 600.0

    @staticmethod
    def dodajZid(xPocetak, yPocetak, xKraj, yKraj, smjer):
        xPocetak = float(xPocetak)
        yPocetak = float(yPocetak)
        xKraj = float(xKraj)
        yKraj = float(yKraj)
        Koordinate.__zidovi.append((xPocetak, yPocetak, xKraj, yKraj, smjer))

    @staticmethod
    def izbrisi_sve_zidove():
        Koordinate.__zidovi.clear()
        Koordinate.dodajZid(-10, -10, -10, -10, -1)

    @staticmethod
    def koordinate_slobodne(koord):
        slobodne = True
        for i in range(len(Koordinate.zidovi())):
            if Koordinate.zidovi()[i][0] < koord[0] < Koordinate.zidovi()[i][2] \
                    and Koordinate.zidovi()[i][1] < koord[1] < Koordinate.zidovi()[i][3]:
                slobodne = False
                break
        return slobodne

    @staticmethod
    def dodajLopticu(x0, y0, x1, y1):
        x0L = float(x0)
        x1L = float(x1)
        y0L = float(y0)
        y1L = float(y1)
        Koordinate.__loptice.append((x0L, y0L, x1L, y1L))

    @staticmethod
    def izbrisi_sve_loptice():
        Koordinate.__loptice.clear()
        Koordinate.dodajLopticu(10, 10, 50, 50)

    @staticmethod
    def updateLoptice(noveKoord):
        Koordinate.__loptice = noveKoord

    @staticmethod
    def okvir_xPocetak():
        return Koordinate.__okvir_xPocetak

    @staticmethod
    def okvir_yKraj():
        return Koordinate.__okvir_yKraj

    @staticmethod
    def okvir_yPocetak():
        return Koordinate.__okvir_yPocetak

    @staticmethod
    def okvir_xKraj():
        return Koordinate.__okvir_xKraj

    @staticmethod
    def zidovi():
        return list(Koordinate.__zidovi)

    @staticmethod
    def loptice():
        return list(Koordinate.__loptice)

    @staticmethod
    def dodajOkvir(xPocetak, yPocetak, xKraj, yKraj):
        xPocetak = float(xPocetak)
        yPocetak = float(yPocetak)
        xKraj = float(xKraj)
        yKraj = float(yKraj)
        Koordinate.__okvir.append((xPocetak, yPocetak, xKraj, yKraj))


class Igrac(object):
    def __init__(self, ime="Player"):
        self.__ime = ime
        self.__brojZivota = 3
        self.__bodovi = 0

    @property
    def ime(self):
        return self.__ime

    @ime.setter
    def ime(self, value):
        self.__ime = value

    @property
    def brojZivota(self):
        return self.__brojZivota

    @brojZivota.setter
    def brojZivota(self, value):
        self.__brojZivota = value

    @property
    def bodovi(self):
        return self.__bodovi

    @bodovi.setter
    def bodovi(self, value):
        self.__bodovi = value
