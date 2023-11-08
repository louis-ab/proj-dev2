from tkinter import *

m = 0
nourriture = 500
vitesseActuelle = 1000

class fourmi:
    def __init__(self,stade='oeuf'):
        if stade == 'oeuf':
            self.stade = 'oeuf'
            self.age = 0
        elif stade == 'larve':
            self.stade = 'larve'
            self.age = 10
        elif stade == 'adulte':
            self.stade = 'adulte'
            self.age = 20
        else:
            print("Stade non reconnu, oeuf par défaut")
            self.stade = 'oeuf'
            self.age = 0
    
    def __str__(self):
        return f'Stade : {self.stade}, age : {self.age}'
    
    def jour(self):
        global nourriture
        
        if self.stade == 'oeuf':
            self.age += 1
            if self.age == 10:
                self.stade = 'larve'
            
        elif self.stade == 'larve':
            self.age += 1
            if nourriture > 0:
                nourriture -= 1
            else:
                self.stade = 'mort'
            if self.age == 20:
                self.stade = 'adulte'
            
        elif self.stade == 'adulte':
            self.age += 1
            if nourriture > 0:
                nourriture -= 1
            else:
                self.stade = 'mort'

class reine:
    def __init__(self):
        self.age = 0
        self.stade = 'vivant'
    
    def __str__(self):
        return f'Age : {self.age}'
    
    def jour(self):
        global nourriture
        
        if nourriture > 0:
            nourriture -= 1
            self.age += 1
            return fourmi('oeuf')
        else:
            self.stade = 'mort'

reineColonie = reine()
fourmisColonie = []

def temps(nombreMinutes):
    minute = nombreMinutes % 60
    if minute < 10:
        minute = '0' + str(minute)

    hour = (nombreMinutes // 60) % 24
    if hour < 10:
        hour = '0' + str(hour)
    
    day = nombreMinutes // 1440
    if nombreMinutes % 1440 == 0:
        update_fourmis()


    heure = str(hour)+':'+str(minute)
    return ('Jour ' + str(day),heure)


def update_temps():
    global m
    m += 1
    jour, heure = temps(m)

    heureEcran.config(text=heure)
    jourEcran.config(text=jour)
    window.after(vitesseActuelle, update_temps)


def update_fourmis():
    nbOeufs = 0
    nbLarves = 0
    nbFourmis = 0
    for fourm in fourmisColonie:
        fourm.jour()
        if fourm.stade == 'oeuf':
            nbOeufs += 1
        elif fourm.stade == 'larve':
            nbLarves += 1
        elif fourm.stade == 'adulte':
            nbFourmis += 1
        else:
            fourmisColonie.pop(fourmisColonie.index(fourm))
    if nourriture > 0:
        nouvelleFourmi = reineColonie.jour()
        fourmisColonie.append(nouvelleFourmi)
        nbOeufs += 1
    else:
        reineEcran.config(text="Reine : 0")
        nourritureEcran.config(bg=rouge)

    oeufsEcran.config(text="Œufs : " + str(nbOeufs))
    larvesEcran.config(text="Larves : " + str(nbLarves))
    fourmisEcran.config(text="Fourmis : " + str(nbFourmis))
    nourritureEcran.config(text="Nourriture : " + str(nourriture))


def vitesseNormal():
    global vitesseActuelle
    vitesseActuelle = 1000

def vitesseAccelere():
    global vitesseActuelle
    vitesseActuelle = 100


def jourSuivant():
    global m
    m += 1440 - m%1440
    update_fourmis()



##########################
##########################
#l'interface graphique'
##########################
##########################


#les couleurs de l'appli
jaune = "#F0EAD2"
vertClair = "#DDE5B6"
vert = "#ADC178"
brun = "#A98467"
brunFonce = "#6C584C"
rouge = "#FF0000"

window = Tk()

window.title("La colonie de fourmis")
window.geometry("720x400")
window.minsize(300,200)
window.config(background=jaune)

reineEcran = Label(window, text="Reine : 1", font="georgia 17 bold", bg=brun)
oeufsEcran = Label(window, text="Œufs : 0", font="georgia 17 bold", bg=brun)
larvesEcran = Label(window, text="Larves : 0", font="georgia 17 bold", bg=brun)
fourmisEcran = Label(window, text="Fourmis : 0", font="georgia 17 bold", bg=brun)
nourritureEcran = Label(window, text="Nourriture : " + str(nourriture), font="georgia 17 bold", bg=brun)
jourEcran = Label(window, text="Jour 0", font="georgia 17 bold", bg=brunFonce)
heureEcran = Label(window, text='00:00', font="georgia 17 bold", bg=brunFonce)

#les boutons pour le temps
vitesseNormal_bouton = Button(window, text='Vitesse normale', command=vitesseNormal, font="georgia 17 bold")
vitesseAccelere_bouton = Button(window, text='Vitesse accélérée', command=vitesseAccelere, font="georgia 17 bold")
jourSuivant_bouton = Button(window, text='Jour suivant', command=jourSuivant, font="georgia 17 bold")


for i in range(11):
    window.columnconfigure(i, weight=1)
    window.rowconfigure(i, weight =1)
window.columnconfigure(10, weight=1)
window.rowconfigure(10, weight =20)

jourEcran.grid(column=0, row= 0, sticky='nsew', pady=1)
heureEcran.grid(column=0, row =1, sticky='nsew', pady=1)
reineEcran.grid(column=0, row=2, sticky='nsew', pady=1)
oeufsEcran.grid(column=0, row=3, sticky='nsew', pady=1)
larvesEcran.grid(column=0, row=4, sticky='nsew', pady=1)
fourmisEcran.grid(column=0, row=5, sticky='nsew', pady=1)
nourritureEcran.grid(column=0, row=6, sticky='nsew', pady=1)

#les boutons pour le temps
vitesseNormal_bouton.grid(column=0, row =7, sticky='nsew', pady=1)
vitesseAccelere_bouton.grid(column=0, row =8, sticky='nsew', pady=1)
jourSuivant_bouton.grid(column=0, row =9, sticky='nsew', pady=1)

window.after(vitesseActuelle,update_temps)
window.mainloop()
