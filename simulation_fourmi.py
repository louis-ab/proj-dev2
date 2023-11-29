from tkinter import *
import random
from PIL import Image, ImageTk

CheminsImages = ['./1.jpeg', './2.jpeg', './3.jpeg', './4.jpeg']
m = 0


class Colonie:
    def __init__(self, nourriture, vitesseTemps=1000, listeDesFourmis=[], tailleColonie=0, oeufs=0, larves=0):
        self.nourriture = nourriture
        self.vitesseTemps = vitesseTemps
        self.reine = Reine()
        self.listeDesFourmis = listeDesFourmis
        self.tailleColonie = 0
        self.oeufs = 0
        self.larves = 0
        for fourm in listeDesFourmis:
            if fourm.stade == 'oeuf':
                self.oeufs += 1
            elif fourm.stade == 'larve':
                self.larves += 1
            elif fourm.stade == 'adulte':
                self.tailleColonie += 1
        for oeuf in range(oeufs - self.oeufs):
            self.listeDesFourmis.append(Fourmi(stade='oeuf'))
        for larve in range(larves - self.larves):
            self.listeDesFourmis.append(Fourmi(stade='larve'))
        for adulte in range(tailleColonie - self.tailleColonie):
            self.listeDesFourmis.append(Fourmi(stade='adulte'))
        self.listeEvenementsAleatoire = [("rienNeSePasse", 0, 0),
                                         ("attaque de fourmis", 0, 3),
                                         ("fourmisPerdu", 1, 4),
                                         ("attaque d'araignée", 10, 25),
                                         ("attaque d'humain", 1, 50),
                                         ("attaque d'oiseau", 50, 100),
                                         ("attaque de lezard", 100, 150)
                                         ]
        self.poidsEvenementsAleatoire = [20, 5, 10, 2, 1, 1, 1]

    def jour(self):
        self.tailleColonie = 0
        self.oeufs = 0
        self.larves = 0
        for fourm in self.listeDesFourmis:
            if (fourm.stade == 'larve' or fourm.stade == 'adulte') and self.nourriture > 0:
                fourm.jour(1)
                self.nourriture -= 1
            else:
                fourm.jour(0)
            if fourm.stade == 'oeuf':
                self.oeufs += 1
            elif fourm.stade == 'larve':
                self.larves += 1
            elif fourm.stade == 'adulte':
                self.tailleColonie += 1
            elif fourm.stade == 'mort':
                self.listeDesFourmis.pop(self.listeDesFourmis.index(fourm))
        if self.nourriture > 0:
            self.reine.jour(1)
            self.nourriture -= 1
            nouvellesFourmis = self.reine.pond()
            for nouvelleFourmi in nouvellesFourmis:
                self.listeDesFourmis.append(nouvelleFourmi)
            self.oeufs += 1
        else:
            self.reine.jour(0)

        updateNaissanceDeces()
        nourritureRapporter()
        evenementsAleatoires()
        if self.reine.stade == 'mort':
            self.reine = Reine()

    def stats(self):
        return (self.reine.stade != 'mort', self.tailleColonie, self.oeufs, self.larves, self.nourriture)


class Fourmi:
    def __init__(self, stade='oeuf'):
        if stade == 'oeuf':
            self.__stade = 'oeuf'
            self.age = 0
        elif stade == 'larve':
            self.__stade = 'larve'
            self.age = 10
        elif stade == 'adulte':
            self.__stade = 'adulte'
            self.age = 20
        else:
            print("Stade non reconnu, oeuf par défaut")
            self.__stade = 'oeuf'
            self.age = 0
        self.ageMax = random.randint(300, 310)

    @property
    def stade(self):
        return self.__stade

    @stade.setter
    def stade(self, nouvStade):
        liste = ['oeuf', 'larve', 'adulte', 'mort']
        if liste.index(nouvStade) > liste.index(self.__stade):
            self.__stade = nouvStade
        else:
            return 'Impossible de revenir a un stade précédent'

    def jour(self, nourriture):

        if self.stade == 'oeuf':
            self.age += 1
            if self.age == 10:
                self.__stade = 'larve'

        elif self.__stade == 'larve':
            self.age += 1
            if not nourriture:
                self.__stade = 'mort'
            if self.age == 20:
                self.__stade = 'adulte'

        elif self.__stade == 'adulte':
            self.age += 1
            if self.age >= self.ageMax:
                self.__stade = 'mort'
            if not nourriture:
                self.__stade = 'mort'

    def __str__(self):
        return f'Stade : {self.stade}, age : {self.age}'


class Reine(Fourmi):
    def __init__(self, stade='adulte'):
        super().__init__(stade)
        self.ageMax = random.randint(600, 610)


    def pond(self):
        if notreColonie.tailleColonie < 1000 and notreColonie.tailleColonie != 0:
            oeufMin = 10
            oeufMax = 30
        else:
            oeufMin = 0
            oeufMax = 4
        return [Fourmi('oeuf') for pondu in range(random.randint(oeufMin, oeufMax))]


class Temps:
    def __init__(self, minutes=0, vitesse=1000):
        self.minutes = minutes
        self.__vitesse = vitesse

    def affichage(self):
        minute = self.minutes % 60
        if minute < 10:
            minute = '0' + str(minute)

        hour = (self.minutes // 60) % 24
        if hour < 10:
            hour = '0' + str(hour)

        day = self.minutes // 1440

        heure = str(hour) + ':' + str(minute)
        return ('Jour ' + str(day), heure)

    def update(self):
        self.minutes += 1
        if self.minutes % 1440 == 0:
            updateFourmis()
        return self.affichage()

    def jourSuivant(self):
        self.minutes += 1440 - self.minutes % 1440
        updateFourmis()
        return self.affichage()

    @property
    def vitesse(self):
        return self.__vitesse

    @vitesse.setter
    def vitesse(self, value):
        self.__vitesse = max(value, 1)


def updateTemps():
    jour, heure = temps.update()

    heureEcran.config(text=heure)
    jourEcran.config(text=jour)
    window.after(temps.vitesse, updateTemps)


def updateFourmis():
    notreColonie.jour()
    reine, nbFourmis, nbOeufs, nbLarves, nourriture = notreColonie.stats()

    if reine == 0:
        reineEcran.config(text="Reine : 0")
    if nourriture == 0:
        nourritureEcran.config(bg=rouge)

    if nbFourmis < 5:
        imageEcran.config(image=images[0])
    elif nbFourmis < 10:
        imageEcran.config(image=images[1])
    elif nbFourmis < 15:
        imageEcran.config(image=images[2])
    else:
        imageEcran.config(image=images[3])

    oeufsEcran.config(text="Œufs : " + str(nbOeufs))
    larvesEcran.config(text="Larves : " + str(nbLarves))
    fourmisEcran.config(text="Fourmis : " + str(nbFourmis))
    nourritureEcran.config(text="Nourriture : " + str(nourriture))


def vitesseNormal():
    temps.vitesse = 1000


def vitesseAccelere():
    temps.vitesse = 100


def vitesseTreAccelere():
    temps.vitesse = 10


def evenementsAleatoires():
    textEvenements = "Rien de particulier ne s'est passé hier"
    message = textEvenements
    if notreColonie.tailleColonie > 1000:
        evenementActuel = \
        random.choices(notreColonie.listeEvenementsAleatoire, weights=notreColonie.poidsEvenementsAleatoire, k=1)[0]
        if evenementActuel[0] != 'rienNeSePasse':
            minMorts = evenementActuel[1]
            maxMorts = evenementActuel[2]

            if maxMorts > notreColonie.tailleColonie:
                maxMorts = notreColonie.tailleColonie
                minMorts = 1

            nbrDeMort = random.randint(minMorts, maxMorts)
            countMorts = 0
            positionFourmis = 0
            while countMorts < nbrDeMort:
                if notreColonie.listeDesFourmis[positionFourmis].stade == 'adulte':
                    notreColonie.listeDesFourmis[positionFourmis].stade = 'mort'
                    countMorts += 1
                positionFourmis += 1

            if evenementActuel[0] == 'fourmisPerdu':
                if nbrDeMort == 1:
                    message = "1 fourmi s'est perdue dans la nature"
                else:
                    message = str(nbrDeMort) + " fourmis se sont perdues dans la nature"
            elif nbrDeMort == 0:
                message = "Il y a eu une " + evenementActuel[0] + " qui n'a pas tuée de fourmi"
            elif nbrDeMort == 1:
                message = "Il y a eu une " + evenementActuel[0] + " qui a tuée " + str(nbrDeMort) + " de fourmi"
            else:
                message = "Il y a eu une " + evenementActuel[0] + " qui a tuée " + str(nbrDeMort) + " de fourmis"


    message = "Les événements : \n" + message
    if notreColonie.nourriture == 0:
        message += "\nIl n'y a plus de nourriture !"
    evenementsDeLaJournee.config(text=message)


def nourritureRapporter():
    if notreColonie.tailleColonie >= 1:
        for fourmi in notreColonie.listeDesFourmis:
            if fourmi.stade == 'adulte':
                notreColonie.nourriture += random.randint(1,2)

def updateNaissanceDeces():
    textNul = "Il y a eu aucune naissance et aucune mort naturel aujourd'hui"
    nbrMort = 0
    nbrNaissance = notreColonie.oeufs
    if Fourmi.stade == 'mort':
        nbrMort += 1
        print(f"Il y a eu {nbrNaissance} naissance et {nbrMort} morts naturel aujourd'hui")
    elif nbrMort == 0:
        print(f"Il y a eu {nbrNaissance} naissance et aucune mort naturel aujourd'hui")
    else:
        print(textNul)

temps = Temps(0)

# création de la fourmilière
notreColonie = Colonie(500)

##########################
##########################
# l'interface graphique'
##########################
##########################


# les couleurs de l'appli
jaune = "#F0EAD2"
vertClair = "#DDE5B6"
vert = "#ADC178"
brun = "#A98467"
brunFonce = "#6C584C"
rouge = "#BB0000"

window = Tk()

window.title("La colonie de fourmis")
window.geometry("1600x900")
window.minsize(1600, 900)
window.config(background=jaune)

images = []
for i in range(4):
    im = Image.open(CheminsImages[i]).resize((900, 900))
    images.append(ImageTk.PhotoImage(im))

reineEcran = Label(window, text="Reine : 1", font="georgia 17 bold", bg=brun)
oeufsEcran = Label(window, text="Œufs : " + str(notreColonie.oeufs), font="georgia 17 bold", bg=brun)
larvesEcran = Label(window, text="Larves : " + str(notreColonie.larves), font="georgia 17 bold", bg=brun)
fourmisEcran = Label(window, text="Fourmis : " + str(notreColonie.tailleColonie), font="georgia 17 bold", bg=brun)
nourritureEcran = Label(window, text="Nourriture : " + str(notreColonie.nourriture), font="georgia 17 bold", bg=brun)
jourEcran = Label(window, text="Jour 0", font="georgia 17 bold", bg=brunFonce)
heureEcran = Label(window, text='00:00', font="georgia 17 bold", bg=brunFonce)
evenementsDeLaJournee = Label(window, text="Les événements : \n", font="georgia 17 bold", bg=brunFonce)

# les boutons pour le temps
vitesseNormal_bouton = Button(window, text='Vitesse normale', command=vitesseNormal, font="georgia 17 bold")
vitesseAccelere_bouton = Button(window, text='Vitesse accélérée', command=vitesseAccelere, font="georgia 17 bold")
vitesseTresAccelere_bouton = Button(window, text='Vitesse très accélérée', command=vitesseTreAccelere,
                                    font="georgia 17 bold")
jourSuivant_bouton = Button(window, text='Jour suivant', command=temps.jourSuivant, font="georgia 17 bold")

# l'image
imageEcran = Label(window, image=images[0])

for i in range(12):
    window.columnconfigure(i, weight=1)
    window.rowconfigure(i, weight=1)
window.columnconfigure(12, weight=1)
window.rowconfigure(12, weight=20)

jourEcran.grid(column=0, row=0, sticky='nsew', pady=1)
heureEcran.grid(column=0, row=1, sticky='nsew', pady=1)
reineEcran.grid(column=0, row=2, sticky='nsew', pady=1)
oeufsEcran.grid(column=0, row=3, sticky='nsew', pady=1)
larvesEcran.grid(column=0, row=4, sticky='nsew', pady=1)
fourmisEcran.grid(column=0, row=5, sticky='nsew', pady=1)
nourritureEcran.grid(column=0, row=6, sticky='nsew', pady=1)
evenementsDeLaJournee.grid(column=0, row=11, sticky='nsew', pady=1)

# les boutons pour le temps
vitesseNormal_bouton.grid(column=0, row=7, sticky='nsew', pady=1)
vitesseAccelere_bouton.grid(column=0, row=8, sticky='nsew', pady=1)
vitesseTresAccelere_bouton.grid(column=0, row=9, sticky='nsew', pady=1)
jourSuivant_bouton.grid(column=0, row=10, sticky='nsew', pady=1)

# l'image
imageEcran.grid(column=1, row=0, rowspan=100, sticky='nsew', pady=1)

window.after(notreColonie.vitesseTemps, updateTemps())
window.mainloop()
