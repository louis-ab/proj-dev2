from tkinter import *
import random
from PIL import Image, ImageTk
import json

CheminsImages = ['./1.jpeg', './2.jpeg', './3.jpeg', './4.jpeg']


class Colonie:
    def __init__(self, nourriture, reine = -1, listeDesFourmis=[], tailleColonie=0, oeufs=0, larves=0):
        self.nourriture = nourriture
        if reine == -1:
            self.reine = Reine()
        else:
            self.reine = reine
        self.listeDesFourmis = listeDesFourmis
        self.tailleColonie = 0
        self.oeufs = 0
        self.larves = 0
        self.naissances = 0
        self.morts = 0
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
                                         ("attaque de lezard", 100, 150),
                                         ("nourriture bonus", 0, 200),
                                         ("colonie agrandis", 0, 10),
                                         ("attaque fongique", 0, 25)
                                         ]
        self.poidsEvenementsAleatoire = [20, 5, 10, 2, 1, 1, 1, 15, 1, 2]

    def jour(self):
        self.tailleColonie = 0
        self.oeufs = 0
        self.larves = 0
        self.morts = 0
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
                self.morts += 1
                self.listeDesFourmis.pop(self.listeDesFourmis.index(fourm))
        if self.nourriture > 0:
            self.reine.jour(1)
            self.nourriture -= 1
            nouvellesFourmis = self.reine.pond()
            for nouvelleFourmi in nouvellesFourmis:
                self.listeDesFourmis.append(nouvelleFourmi)
            self.naissances = len(nouvellesFourmis)
            self.oeufs += 1
        else:
            self.reine.jour(0)
            self.naissances = 0

        updateNaissanceDeces(self)
        nourritureRapporter()
        evenementsAleatoires()
        if self.reine.stade == 'mort':
            self.reine = Reine()

    def stats(self):
        return (self.reine.stade != 'mort', self.tailleColonie, self.oeufs, self.larves, self.nourriture)


class Fourmi:
    def __init__(self, stade='oeuf', age=-1, ageMax=-1):
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

        if age != -1:
            self.age = age
        if ageMax == -1:
            self.ageMax = random.randint(300, 310)
        else:
            self.ageMax = ageMax

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
    def __init__(self, stade='adulte', age=-1, ageMax=-1):
        super().__init__(stade, age)

        if ageMax == -1:
            self.ageMax = random.randint(600, 610)
        else:
            self.ageMax = ageMax


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

    def passerDeuxJours(self):
        self.minutes += 2880 - self.minutes % 2880
        updateFourmis()
        return self.affichage()

    @property
    def vitesse(self):
        return self.__vitesse

    @vitesse.setter
    def vitesse(self, value):
        self.__vitesse = max(value, 1)

class Sauvegarde:
    def __init__(self, path=''):
        if not path.endswith('.json'):
            path = path + '.json'
        self.path = path

    def sauve(self, colonie, temps):

        listeDesFourmis = []
        for fourmi in colonie.listeDesFourmis:
            listeDesFourmis.append({'stade': fourmi.stade, 'age': fourmi.age, 'ageMax': fourmi.ageMax})
        reine = {'stade': colonie.reine.stade, 'age': colonie.reine.age, 'ageMax': colonie.reine.ageMax}

        data = json.dumps({'nourriture': colonie.nourriture,
                           'listeDesFourmis': listeDesFourmis,
                           'reine': reine,
                           'minutes': temps.minutes,
                           'vitesse': temps.vitesse})

        try:
            with open(self.path, 'w') as fichier:
                fichier.write(data)
                sauvegardeTexte.config(bg=vertClair)

        except IOError:
            sauvegardeTexte.config(bg=rouge)

    def charge(self):
        global notreColonie, temps
        try:
            with open(self.path, 'r') as fichier:
                data = json.loads(fichier.read())

                listeDesFourmis = []
                for fourmi in data['listeDesFourmis']:
                    fourmi = Fourmi(stade=fourmi['stade'], age=fourmi['age'], ageMax=fourmi['ageMax'])
                    listeDesFourmis.append(fourmi)
                reine = Reine(stade=data['reine']['stade'], age=data['reine']['age'], ageMax=data['reine']['ageMax'])

                notreColonie = Colonie(nourriture = data['nourriture'],
                                    reine = reine,
                                    listeDesFourmis = listeDesFourmis)

                temps = Temps(minutes=data['minutes'], vitesse=data['vitesse'])
                jourSuivant_bouton.config(command=temps.jourSuivant)

                sauvegardeTexte.config(bg=vertClair)

        except (FileNotFoundError, IOError):
            sauvegardeTexte.config(bg=rouge)

    def sauveInterface(self):
        self.path = sauvegardeTexte.get("1.0", "end-1c")
        if not self.path.endswith('.json'):
            self.path = self.path + '.json'
        self.sauve(notreColonie, temps)

    def chargeInterface(self):
        self.path = sauvegardeTexte.get("1.0", "end-1c")
        if not self.path.endswith('.json'):
            self.path = self.path + '.json'
        self.charge()


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

    if nbFourmis < 30:
        imageEcran.config(image=images[0])
    elif nbFourmis < 100:
        imageEcran.config(image=images[1])
    elif nbFourmis < 400:
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

            if evenementActuel[0] == 'nourriture bonus':
                minNourriture = evenementActuel[1]
                maxNourriture = evenementActuel[2]

                nbrDeNourriture = random.randint(minNourriture, maxNourriture)
                countNourriture = 0
                while countNourriture < nbrDeNourriture:
                    notreColonie.nourriture += 1
                    countNourriture += 1

                if nbrDeNourriture == 1:
                    message = "Les fourmis ont trouvé 1 nourriture dans la nature"
                else:
                    message = "Les fourmis ont trouvé " + str(nbrDeNourriture) + " nourritures dans la nature"

            if evenementActuel[0] == 'colonie agrandis':
                minFourmi = evenementActuel[1]
                maxFourmi = evenementActuel[2]

                nbrDeFourmi = random.randint(minFourmi, maxFourmi)
                countFourmi = 0
                while countFourmi < nbrDeFourmi:
                    notreColonie.tailleColonie += 1
                    countFourmi += 1

                if nbrDeFourmi == 1:
                    message = "Il y a 1 fourmi qui a rejoint votre colonie"
                else:
                    message = "Il y a " + str(nbrDeFourmi) + " fourmis qui ont rejoint votre colonie"


    message = "Les événements : \n" + message
    if notreColonie.nourriture == 0:
        message += "\nIl n'y a plus de nourriture !"
    evenementsDeLaJournee.config(text=message)


def nourritureRapporter():
    if notreColonie.tailleColonie >= 1:
        for fourmi in notreColonie.listeDesFourmis:
            if fourmi.stade == 'adulte':
                notreColonie.nourriture += random.randint(1, 2)

def updateNaissanceDeces(colonie):
    textNul = "Il n'y a eu aucune naissance\n et aucune mort naturelle aujourd'hui"
    nbrMort = colonie.morts
    nbrNaissance = colonie.naissances
    if nbrMort > 0 and nbrNaissance > 0:
        text = f"Il y a eu {nbrNaissance} naissance(s)\n et {nbrMort} morts naturelle(s) aujourd'hui"
    elif nbrNaissance == 0:
        text = f"Il n'y a eu aucune naissance\n et {nbrMort} morts naturelle(s) aujourd'hui"
    elif nbrMort == 0:
        text = f"Il y a eu {nbrNaissance} naissance(s)\n et aucune mort naturelle aujourd'hui"
    else:
        text = textNul
    naissancesMortsDeLaJournee.config(text=text)

def demarre():
    global notreColonie, temps

    nourritureDebut = nourritureTexte.get("1.0", "end-1c")
    fourmiDebut = fourmiTexte.get("1.0", "end-1c")

    nourritureTitre.destroy()
    fourmiTitre.destroy()
    nourritureTexte.destroy()
    fourmiTexte.destroy()
    commence_bouton.destroy()

    notreColonie = Colonie(nourriture=int(nourritureDebut), tailleColonie=int(fourmiDebut))
    updateFourmis()

temps = Temps(0)
sauvegarde = Sauvegarde()

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
oeufsEcran = Label(window, text="Œufs : 0", font="georgia 17 bold", bg=brun)
larvesEcran = Label(window, text="Larves : 0", font="georgia 17 bold", bg=brun)
fourmisEcran = Label(window, text="Fourmis : ?", font="georgia 17 bold", bg=brun)
nourritureEcran = Label(window, text="Nourriture : ?", font="georgia 17 bold", bg=brun)
jourEcran = Label(window, text="Jour 0", font="georgia 17 bold", bg=brunFonce)
heureEcran = Label(window, text='00:00', font="georgia 17 bold", bg=brunFonce)
evenementsDeLaJournee = Label(window, text="Les événements : \n", font="georgia 17 bold", bg=brunFonce)
naissancesMortsDeLaJournee = Label(window, text="Naissances et Morts", font="georgia 17 bold", bg=brunFonce)

# les boutons pour le temps
vitesseNormal_bouton = Button(window, text='Vitesse normale', command=vitesseNormal, font="georgia 17 bold")
vitesseAccelere_bouton = Button(window, text='Vitesse accélérée', command=vitesseAccelere, font="georgia 17 bold")
vitesseTresAccelere_bouton = Button(window, text='Vitesse très accélérée', command=vitesseTreAccelere,
                                    font="georgia 17 bold")
jourSuivant_bouton = Button(window, text='Jour suivant', command=temps.jourSuivant, font="georgia 17 bold")
passerDeuxJours_bouton = Button(window, text='Passer 2 jours', command=temps.passerDeuxJours, font="georgia 17 bold")

sauveEcran = Label(window, text="Chemin de sauvegarde :", font="georgia 17 bold", bg=brun)
sauvegardeTexte = Text(window, font="georgia 17 bold", bg=vertClair, width=1, height=1)
sauve_bouton = Button(window, text='Sauvegarder', command=sauvegarde.sauveInterface, font="georgia 17 bold")
charge_bouton = Button(window, text='Charger', command=sauvegarde.chargeInterface, font="georgia 17 bold")

# l'image
imageEcran = Label(window, image=images[0])

for i in range(18):
    window.columnconfigure(i, weight=1)
    window.rowconfigure(i, weight=1)
window.columnconfigure(18, weight=1)
window.rowconfigure(18, weight=20)

jourEcran.grid(column=0, row=0, sticky='nsew', pady=1)
heureEcran.grid(column=0, row=1, sticky='nsew', pady=1)
reineEcran.grid(column=0, row=2, sticky='nsew', pady=1)
oeufsEcran.grid(column=0, row=3, sticky='nsew', pady=1)
larvesEcran.grid(column=0, row=4, sticky='nsew', pady=1)
fourmisEcran.grid(column=0, row=5, sticky='nsew', pady=1)
nourritureEcran.grid(column=0, row=6, sticky='nsew', pady=1)
evenementsDeLaJournee.grid(column=0, row=11, sticky='nsew', pady=1)
naissancesMortsDeLaJournee.grid(column=0, row=12, sticky='nsew', pady=1)

sauveEcran.grid(column=0, row=13, sticky='nsew', pady=1)
sauvegardeTexte.grid(column=0, row=14, sticky='nsew', pady=1)
sauve_bouton.grid(column=0, row=15, sticky='nsew', pady=1)
charge_bouton.grid(column=0, row=16, sticky='nsew', pady=1)
passerDeuxJours_bouton.grid(column=0, row=17, sticky='nsew', pady=1)


# les boutons pour le temps
vitesseNormal_bouton.grid(column=0, row=7, sticky='nsew', pady=1)
vitesseAccelere_bouton.grid(column=0, row=8, sticky='nsew', pady=1)
vitesseTresAccelere_bouton.grid(column=0, row=9, sticky='nsew', pady=1)
jourSuivant_bouton.grid(column=0, row=10, sticky='nsew', pady=1)

# l'image
imageEcran.grid(column=1, row=0, rowspan=100, sticky='nsew', pady=1)

# Écran de démarage
nourritureTitre = Label(window, text="Nourriture :", font="georgia 17 bold", bg=brun)
fourmiTitre = Label(window, text="Fourmis :", font="georgia 17 bold", bg=brun)
nourritureTexte = Text(window, font="georgia 17 bold", bg=vertClair)
fourmiTexte = Text(window, font="georgia 17 bold", bg=vertClair)
commence_bouton = Button(window, text="Démarrer", command=demarre, font="georgia 17 bold")

nourritureTitre.place(x=450, y=150, width=200, height=50)
fourmiTitre.place(x=850, y=150, width=200, height=50)
nourritureTexte.place(x=450, y=200, width=200, height=50)
fourmiTexte.place(x=850, y=200, width=200, height=50)
commence_bouton.place(x=650, y=300, width=200, height=50)

updateTemps()
window.mainloop()
