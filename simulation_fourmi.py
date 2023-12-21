import tkinter
import random
import json
from PIL import Image, ImageTk

CheminsImages = ['./1.jpeg', './2.jpeg', './3.jpeg', './4.jpeg']


class PasNombre(Exception):
    """Le nombre de mort et la fréquence doivent être des NOMBRES"""


class TropGrand(Exception):
    """Le nombree est trop grand"""


class Colonie:
    """Représente une colonie de fourmis, contenant une reine et plusieurs fourmis."""

    def __init__(self, nourriture, reine=None, liste_des_fourmis=None,
                 taille_colonie=0, oeufs=0, larves=0):
        self.nourriture = nourriture
        if reine is None:
            self.reine = Reine()
        else:
            self.reine = reine
        self.liste_des_fourmis = liste_des_fourmis
        self.taille_colonie = 0
        self.oeufs = 0
        self.larves = 0
        self.naissances = 0
        self.morts = 0
        if liste_des_fourmis is not None:
            self.liste_des_fourmis = liste_des_fourmis
            for fourm in liste_des_fourmis:
                if fourm.stade == 'oeuf':
                    self.oeufs += 1
                elif fourm.stade == 'larve':
                    self.larves += 1
                elif fourm.stade == 'adulte':
                    self.taille_colonie += 1
        else:
            self.liste_des_fourmis = []

        for oeuf in range(oeufs - self.oeufs):
            self.liste_des_fourmis.append(Fourmi())
        for larve in range(larves - self.larves):
            self.liste_des_fourmis.append(Fourmi(stade='larve'))
        for adulte in range(taille_colonie - self.taille_colonie):
            self.liste_des_fourmis.append(Fourmi(stade='adulte'))
        self.liste_evenements_aleatoire = [("rienNeSePasse", 0, 0),
                                           ("attaque de fourmis", 0, 3),
                                           ("fourmisPerdu", 1, 4),
                                           ("attaque d'araignée", 10, 25),
                                           ("attaque d'humain", 1, 50),
                                           ("attaque d'oiseau", 50, 100),
                                           ("attaque de lezard", 100, 150),
                                           ("nourriture bonus", 0, 200),
                                           ("colonie agrandis", 0, 10),
                                           ("attaque fongique", 0, 25),
                                           ("climatique", 50, 150)
                                           ]
        self.poids_evenements_aleatoire = [20, 5, 10, 2, 1, 1, 1, 15, 1, 2, 0.5]

    def jour(self):
        """Simule la colonie un jour plus tard."""
        self.taille_colonie = 0
        self.oeufs = 0
        self.larves = 0
        self.morts = 0
        for fourm in self.liste_des_fourmis:
            if fourm.stade in ('larve', 'adulte') and self.nourriture > 0:
                fourm.jour(1)
                self.nourriture -= 1
            else:
                fourm.jour(0)
            if fourm.stade == 'oeuf':
                self.oeufs += 1
            elif fourm.stade == 'larve':
                self.larves += 1
            elif fourm.stade == 'adulte':
                self.taille_colonie += 1
            elif fourm.stade == 'mort':
                self.morts += 1
                self.liste_des_fourmis.pop(self.liste_des_fourmis.index(fourm))
        if self.nourriture > 0:
            self.reine.jour(1)
            self.nourriture -= 1
            nouvelles_fourmis = self.reine.pond()
            for nouvelle_fourmi in nouvelles_fourmis:
                self.liste_des_fourmis.append(nouvelle_fourmi)
            self.naissances = len(nouvelles_fourmis)
            self.oeufs += 1
        else:
            self.reine.jour(0)
            self.naissances = 0

        update_naissance__deces(self)
        nourriture_rapporter()
        evenements_aleatoires()
        if self.reine.stade == 'mort':
            self.reine = Reine()

    def stats(self):
        """Renvoie le nombre de fourmis de chaque type et la nourriture.
        PRE : -
        POST : Renvoie dans un tuple si la reine est vivante, le nombre de fourmi,
               d'œufs et de larves, et la quantité de nourriture de la colonie
        """
        return (self.reine.stade != 'mort', self.taille_colonie,
                self.oeufs, self.larves, self.nourriture)


class Fourmi:
    """Représente une fourmi. Elle a un stade et un age qui dépend du stade."""

    def __init__(self, stade='oeuf', age=None, age_max=None):
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

        if age is not None:
            self.age = age
        if age_max is None:
            self.age_max = random.randint(300, 310)
        else:
            self.age_max = age_max

    @property
    def stade(self):
        """Le stade de la fourmi."""
        return self.__stade

    @stade.setter
    def stade(self, nouv_stade):
        liste = ['oeuf', 'larve', 'adulte', 'mort']
        if liste.index(nouv_stade) > liste.index(self.__stade):
            self.__stade = nouv_stade
        else:
            print('Impossible de revenir a un stade précédent')

    def jour(self, nourriture):
        """Simule la fourmi pendant un jour.
        PRE : nourriture est 1 ou 0.
        POST : si le stade n'est pas mort, self.age est augmenté de 1
               si la fourmi atteint certains ages elle passe au stade suivant
               si elle ne reçoit pas de nourriture alors qu'elle en a besoin elle meurt
        """

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
            if self.age >= self.age_max:
                self.__stade = 'mort'
            if not nourriture:
                self.__stade = 'mort'

    def __str__(self):
        return f'Stade : {self.stade}, age : {self.age}'


class Reine(Fourmi):
    """Représente une Reine. Elle est une fourmi qui pond des œufs."""

    def __init__(self, stade='adulte', age=None, age_max=None):
        super().__init__(stade, age)

        if age_max is None:
            self.age_max = random.randint(600, 610)
        else:
            self.age_max = age_max

    def pond(self):
        """Pond un/des œuf(s) et les renvoie.
        PRE : -
        POST : Renvoie une liste contenant un nombre aléatoire d'objets Fourmi qui sont des oeufs/
        Louis
        """
        if notre_colonie.taille_colonie < 1000 and notre_colonie.taille_colonie != 0:
            oeuf_min = 10
            oeuf_max = 30
        else:
            oeuf_min = 0
            oeuf_max = 4
        return [Fourmi() for pondu in range(random.randint(oeuf_min, oeuf_max))]


class Temps:
    """Contrôle le temps et sa vitesse"""

    def __init__(self, minutes=0, vitesse=1000):
        self.minutes = minutes
        self.__vitesse = vitesse

    def affichage(self):
        """
        calcule l'heure actuelle et le jour actuel

        PRÉ:-
        POST : retourne une chaîne de caractère avec le numéro du jour et l’heure actuelle
        """
        minute = self.minutes % 60
        if minute < 10:
            minute = '0' + str(minute)

        hour = (self.minutes // 60) % 24
        if hour < 10:
            hour = '0' + str(hour)

        day = self.minutes // 1440

        heure = str(hour) + ':' + str(minute)
        return 'Jour ' + str(day), heure

    def update(self):
        """
        ajoute 1 minute à chaque lancement de la fonction
        PRÉ:-
        POST: self.affiche() affiche l’heure et le temps actue dans l'interface graphique,
              augmente self.minutes de 1,
              updade_fourmis() exécute la simulation, modifie le nombre de fourmis et de nouriture de la colonie
        """
        self.minutes += 1
        if self.minutes % 1440 == 0:
            update_fourmis()
        return self.affichage()

    def jour_suivant(self):
        """
        passe 1 jour dans la simulation
        PRÉ:-
        POST: retourne la fonction affiche() ce qui affiche l'heure et le jour actuel dans l'interface graphique,
              permet d'avancer la fonction d'1 jour,
              updade_fourmis() exécute la simulation, modifie le nombre de fourmis et de nouriture de la colonie
        """
        self.minutes += 1440 - self.minutes % 1440
        update_fourmis()
        return self.affichage()

    def passer_deux_jours(self):
        """
        passe 2 jours dans la simulation
        PRÉ: existance de la self.fonction jour_suivant()
        POST: exécute la fonction jour_suivant() 2 fois, ce qui permet d'avancer la simulation de 2 jours
        """
        self.jour_suivant()
        self.jour_suivant()

    @property
    def vitesse(self):
        return self.__vitesse

    @vitesse.setter
    def vitesse(self, value):
        self.__vitesse = max(value, 1)


class Sauvegarde:
    """Permet de créer et charger des fichiers de sauvegarde."""

    def __init__(self, path=''):
        if not path.endswith('.json'):
            path += '.json'
        self.path = path

    def sauve(self, colonie, temps):
        """
        sauvegarde l'état de la colonie et du temps dans un fichier json
        PRE : -
        POST : l'état est sauvegardé dans un fichier JSON.
        RAISES : IOError si le fichier ne peut pas être ouvert/créé en lecture.
        """

        liste_des_fourmis = []
        for fourmi in colonie.liste_des_fourmis:
            liste_des_fourmis.append({'stade': fourmi.stade, 'age': fourmi.age,
                                      'age_max': fourmi.age_max})
        reine = {'stade': colonie.reine.stade, 'age': colonie.reine.age,
                 'age_max': colonie.reine.age_max}

        data = json.dumps({'nourriture': colonie.nourriture,
                           'liste_des_fourmis': liste_des_fourmis,
                           'reine': reine,
                           'minutes': temps.minutes,
                           'vitesse': temps.vitesse})

        try:
            with open(self.path, 'w', encoding="utf8") as fichier:
                fichier.write(data)
                sauvegarde_texte.config(bg=VERT_CLAIR)

        except IOError:
            sauvegarde_texte.config(bg=ROUGE)

    def charge(self):
        """
        Charge une simulation depuis un fichier de sauvegarde
        PRE : -
        POST : notre_colonie et temps sont la colonie et le temps sauvegardée dans le fichier
        RAISES : - FileNotFoundError si le fichier indiqué par self.path n'existe pas,
                 - IOError si il ne peut pas être lu.
        """
        global notre_colonie, temps
        try:
            with open(self.path, encoding="utf8") as fichier:
                data = json.loads(fichier.read())

                liste_des_fourmis = []
                for fourmi in data['liste_des_fourmis']:
                    fourmi = Fourmi(stade=fourmi['stade'], age=fourmi['age'],
                                    age_max=fourmi['age_max'])
                    liste_des_fourmis.append(fourmi)
                reine = Reine(stade=data['reine']['stade'], age=data['reine']['age'],
                              age_max=data['reine']['age_max'])

                notre_colonie = Colonie(nourriture=data['nourriture'],
                                        reine=reine,
                                        liste_des_fourmis=liste_des_fourmis)

                temps = Temps(minutes=data['minutes'], vitesse=data['vitesse'])
                jour_suivant_bouton.config(command=temps.jour_suivant)

                sauvegarde_texte.config(bg=VERT_CLAIR)

        except (FileNotFoundError, IOError):
            sauvegarde_texte.config(bg=ROUGE)

    def sauve_interface(self):
        """
        sauvegarde l'état de la colonie et du temps dans un fichier json depuis l'interface.
        PRE : -
        POST : l'état est sauvegardé dans un fichier JSON.
        RAISES : IOError si le fichier ne peut pas être ouvert/créé en lecture.
        """
        self.path = sauvegarde_texte.get("1.0", "end-1c")
        if not self.path.endswith('.json'):
            self.path += '.json'
        self.sauve(notre_colonie, temps)

    def charge_interface(self):
        """
        Charge une simulation depuis un fichier de sauvegarde dans l'interface.
        PRE : -
        POST : notre_colonie et temps sont la colonie et le temps sauvegardée dans le fichier
        RAISES : - FileNotFoundError si le fichier indiqué par self.path n'existe pas,
                 - IOError si il ne peut pas être lu.
        """
        self.path = sauvegarde_texte.get("1.0", "end-1c")
        if not self.path.endswith('.json'):
            self.path += '.json'
        self.charge()


def update_temps():
    """met à jour les données de temps

    PRE: le jour et l'heure
    POST: modifie dans l'interface le jour et l'heure
    """
    jour, heure = temps.update()

    heure_ecran.config(text=heure)
    jour_ecran.config(text=jour)
    window.after(temps.vitesse, update_temps)


def update_fourmis():
    """met à jour les stats de la colonie

    PRE: les stats de la colonie et des images
    POST: modifie dans l'interface l'image,
          la reine, le nombre de fourmis,d'oeuf et de larves et la quantité de nourriture
    """
    notre_colonie.jour()
    reine, nb_fourmis, nb_oeufs, nb_larves, nourriture = notre_colonie.stats()

    if reine == 0:
        reine_ecran.config(text="Reine : 0")
    if nourriture == 0:
        nourriture_ecran.config(bg=ROUGE)

    if nb_fourmis < 30:
        image_ecran.config(image=images[0])
    elif nb_fourmis < 100:
        image_ecran.config(image=images[1])
    elif nb_fourmis < 400:
        image_ecran.config(image=images[2])
    else:
        image_ecran.config(image=images[3])

    oeufs_ecran.config(text="Œufs : " + str(nb_oeufs))
    larves_ecran.config(text="Larves : " + str(nb_larves))
    fourmis_ecran.config(text="Fourmis : " + str(nb_fourmis))
    nourriture_ecran.config(text="Nourriture : " + str(nourriture))


def vitesse_normale():
    """vitesse normale de la simulation"""
    temps.vitesse = 1000


def vitesse_accelere():
    """vitesse accélérée de la simulation"""
    temps.vitesse = 100


def vitesse_tres_accelere():
    """vitesse très accélérée de la simulation"""
    temps.vitesse = 10


def evenements_aleatoires():
    """générer un evenement aleatoire

    PRE: une liste des événements possibles
    POST: renvoie une variable qui contient une chaîne de caractère affichant un évènement aléatoire
            qui modifie la taille de la colonie ou la quantité de nourriture chaque jour.
    """
    message = "Rien de particulier ne s'est passé hier"
    if notre_colonie.taille_colonie > 1000:
        evenement_actuel = \
            random.choices(notre_colonie.liste_evenements_aleatoire,
                           weights=notre_colonie.poids_evenements_aleatoire)[0]
        if evenement_actuel[0] == 'nourriture bonus':
            min_nourriture = evenement_actuel[1]
            max_nourriture = evenement_actuel[2]

            nbr_de_nourriture = random.randint(min_nourriture, max_nourriture)
            count_nourriture = 0
            while count_nourriture < nbr_de_nourriture:
                notre_colonie.nourriture += 1
                count_nourriture += 1

            if nbr_de_nourriture == 1:
                message = "Les fourmis ont trouvé 1 nourriture dans la nature"
            else:
                message = "Les fourmis ont trouvé " + str(nbr_de_nourriture) \
                          + " nourriture dans la nature"
        elif evenement_actuel[0] == 'colonie agrandis':
            min_fourmi = evenement_actuel[1]
            max_fourmi = evenement_actuel[2]

            nbr_de_fourmi = random.randint(min_fourmi, max_fourmi)
            count_fourmi = 0
            while count_fourmi < nbr_de_fourmi:
                notre_colonie.taille_colonie += 1
                count_fourmi += 1

            if nbr_de_fourmi == 1:
                message = "Il y a 1 fourmi qui a rejoint votre colonie"
            else:
                message = "Il y a " + str(nbr_de_fourmi) \
                          + " fourmis qui ont rejoint votre colonie"
        elif evenement_actuel[0] == 'rienNeSePasse':
            pass

        else:
            min_morts = evenement_actuel[1]
            max_morts = evenement_actuel[2]

            if max_morts > notre_colonie.taille_colonie:
                max_morts = notre_colonie.taille_colonie
                min_morts = 1

            nbr_de_mort = random.randint(min_morts, max_morts)
            count_morts = 0
            position_fourmis = 0
            while count_morts < nbr_de_mort:
                if notre_colonie.liste_des_fourmis[position_fourmis].stade == 'adulte':
                    notre_colonie.liste_des_fourmis[position_fourmis].stade = 'mort'
                    count_morts += 1
                position_fourmis += 1

            if evenement_actuel[0] == 'fourmisPerdu':
                if nbr_de_mort == 1:
                    message = "1 fourmi s'est perdue dans la nature"
                else:
                    message = str(nbr_de_mort) + " fourmis se sont perdues dans la nature"
            elif evenement_actuel[0] == 'climatique':
                message = str(nbr_de_mort) + " fourmis sont morts de raison climatique"
            elif nbr_de_mort == 0:
                message = "Il y a eu une " + evenement_actuel[0] + " qui n'a pas tuée de fourmi"
            elif nbr_de_mort == 1:
                message = "Il y a eu une " + evenement_actuel[0] + " qui a tuée " \
                          + str(nbr_de_mort) + " de fourmi"
            else:
                message = "Il y a eu une " + evenement_actuel[0] + " qui a tuée " \
                          + str(nbr_de_mort) + " de fourmis"

        message = "Les événements : \n" + message
        if notre_colonie.nourriture == 0:
            message += "\nIl n'y a plus de nourriture !"
        evenements_de_la_journee.config(text=message)


def nourriture_rapporter():
    """augmentation de la nourriture

    PRE: la taille et la quantité de nourriture de la colonie
    POST: modifie la quantité de nourriture chaque jour
    """
    if notre_colonie.taille_colonie >= 1:
        for fourmi in notre_colonie.liste_des_fourmis:
            if fourmi.stade == 'adulte':
                notre_colonie.nourriture += random.randint(1, 2)


def update_naissance__deces(colonie):
    """met à jour le nombre de naissance et de décès

    PRE: des variables qui comptent les morts et les naissances de la colonie
    POST: renvoie une variable contenant une chaîne de caractères
          qui affiche le nombre de naissance et de décès chaque jour.
    """
    text_nul = "Il n'y a eu aucune naissance\n et aucune mort naturelle aujourd'hui"
    nbr_mort = colonie.morts
    nbr_naissance = colonie.naissances
    if nbr_mort > 0 and nbr_naissance > 0:
        text = \
            f"Il y a eu {nbr_naissance} naissance(s)\n et {nbr_mort} morts naturelle(s) aujourd'hui"
    elif nbr_naissance == 0:
        text = f"Il n'y a eu aucune naissance\n et {nbr_mort} morts naturelle(s) aujourd'hui"
    elif nbr_mort == 0:
        text = f"Il y a eu {nbr_naissance} naissance(s)\n et aucune mort naturelle aujourd'hui"
    else:
        text = text_nul
    naissances_morts_de_la_journee.config(text=text)


def demarre():
    """
    création de la colonie
    PRE: nourriture_texte et fourmi_texte contiennent un nombre entier
    POST: création de la colonie avec les paramètres entré par l'utilisateur(nombre de fourmis et quantité de nourriture),
          lancement de la simulation,
          retire dans l'interface graphique les champs pour entrer la nouriture et le nombre de fourmis initials
    RAISE: PasNombre si nourriture_debut et fourmi_debut sont pas des nombres
    """
    global notre_colonie, temps

    nourriture_debut = nourriture_texte.get("1.0", "end-1c")
    fourmi_debut = fourmi_texte.get("1.0", "end-1c")

    try:
        if not (nourriture_debut.isdigit() and fourmi_debut.isdigit()):
            raise PasNombre("La quantité de fourmis et de nourriture doivent être des NOMBRES")

        nourriture_titre.destroy()
        fourmi_titre.destroy()
        nourriture_texte.destroy()
        fourmi_texte.destroy()
        commence_bouton.destroy()

        notre_colonie = Colonie(nourriture=int(nourriture_debut), taille_colonie=int(fourmi_debut))
        update_fourmis()

    except PasNombre as e:
        print(e)


temps = Temps()
sauvegarde = Sauvegarde()

##########################
##########################
# l'interface graphique'
##########################
##########################


# les couleurs de l'appli
JAUNE = "#F0EAD2"
VERT_CLAIR = "#DDE5B6"
VERT = "#ADC178"
BRUN = "#A98467"
BRUN_FONCE = "#6C584C"
ROUGE = "#BB0000"

window = tkinter.Tk()


window.title("La colonie de fourmis")
window.geometry("1600x900")
window.minsize(1600, 900)
window.config(background=JAUNE)

images = []
for i in range(4):
    im = Image.open(CheminsImages[i]).resize((900, 900))
    images.append(ImageTk.PhotoImage(im))

reine_ecran = tkinter.Label(window, text="Reine : 1", font="georgia 17 bold", bg=BRUN)
oeufs_ecran = tkinter.Label(window, text="Œufs : 0", font="georgia 17 bold", bg=BRUN)
larves_ecran = tkinter.Label(window, text="Larves : 0", font="georgia 17 bold", bg=BRUN)
fourmis_ecran = tkinter.Label(window, text="Fourmis : ?", font="georgia 17 bold", bg=BRUN)
nourriture_ecran = tkinter.Label(window, text="Nourriture : ?", font="georgia 17 bold", bg=BRUN)
jour_ecran = tkinter.Label(window, text="Jour 0", font="georgia 17 bold", bg=BRUN_FONCE)
heure_ecran = tkinter.Label(window, text='00:00', font="georgia 17 bold", bg=BRUN_FONCE)
evenements_de_la_journee = tkinter.Label(window, text="Les événements : \n",
                                         font="georgia 17 bold", bg=BRUN_FONCE)
naissances_morts_de_la_journee = tkinter.Label(window, text="Naissances et Morts",
                                               font="georgia 17 bold", bg=BRUN_FONCE)

# les boutons pour le temps
vitesse_normal_bouton = tkinter.Button(window, text='Vitesse normale', command=vitesse_normale,
                                       font="georgia 17 bold")
vitesse_accelere_bouton = tkinter.Button(window, text='Vitesse accélérée', command=vitesse_accelere,
                                         font="georgia 17 bold")
vitesse_tres_accelere_bouton = tkinter.Button(window, text='Vitesse très accélérée',
                                              command=vitesse_tres_accelere, font="georgia 17 bold")
jour_suivant_bouton = tkinter.Button(window, text='Jour suivant', command=temps.jour_suivant,
                                     font="georgia 17 bold")
passer_deux_jours_bouton = tkinter.Button(window, text='Passer 2 jours',
                                          command=temps.passer_deux_jours, font="georgia 17 bold")

sauve_ecran = tkinter.Label(window, text="Chemin de sauvegarde :", font="georgia 17 bold", bg=BRUN)
sauvegarde_texte = tkinter.Text(window, font="georgia 17 bold", bg=VERT_CLAIR, width=1, height=1)
sauve_bouton = tkinter.Button(window, text='Sauvegarder', command=sauvegarde.sauve_interface,
                              font="georgia 17 bold")
charge_bouton = tkinter.Button(window, text='Charger', command=sauvegarde.charge_interface,
                               font="georgia 17 bold")

# l'image
image_ecran = tkinter.Label(window, image=images[0])

for i in range(18):
    window.columnconfigure(i, weight=1)
    window.rowconfigure(i, weight=1)
window.columnconfigure(18, weight=1)
window.rowconfigure(18, weight=20)

jour_ecran.grid(column=0, row=0, sticky='nsew', pady=1)
heure_ecran.grid(column=0, row=1, sticky='nsew', pady=1)
reine_ecran.grid(column=0, row=2, sticky='nsew', pady=1)
oeufs_ecran.grid(column=0, row=3, sticky='nsew', pady=1)
larves_ecran.grid(column=0, row=4, sticky='nsew', pady=1)
fourmis_ecran.grid(column=0, row=5, sticky='nsew', pady=1)
nourriture_ecran.grid(column=0, row=6, sticky='nsew', pady=1)
evenements_de_la_journee.grid(column=0, row=11, sticky='nsew', pady=1)
naissances_morts_de_la_journee.grid(column=0, row=12, sticky='nsew', pady=1)

sauve_ecran.grid(column=0, row=13, sticky='nsew', pady=1)
sauvegarde_texte.grid(column=0, row=14, sticky='nsew', pady=1)
sauve_bouton.grid(column=0, row=15, sticky='nsew', pady=1)
charge_bouton.grid(column=0, row=16, sticky='nsew', pady=1)
passer_deux_jours_bouton.grid(column=0, row=17, sticky='nsew', pady=1)

# les boutons pour le temps
vitesse_normal_bouton.grid(column=0, row=7, sticky='nsew', pady=1)
vitesse_accelere_bouton.grid(column=0, row=8, sticky='nsew', pady=1)
vitesse_tres_accelere_bouton.grid(column=0, row=9, sticky='nsew', pady=1)
jour_suivant_bouton.grid(column=0, row=10, sticky='nsew', pady=1)

# l'image
image_ecran.grid(column=1, row=0, rowspan=100, sticky='nsew', pady=1)

# Écran de démarage
nourriture_titre = tkinter.Label(window, text="Nourriture :", font="georgia 17 bold", bg=BRUN)
fourmi_titre = tkinter.Label(window, text="Fourmis :", font="georgia 17 bold", bg=BRUN)
nourriture_texte = tkinter.Text(window, font="georgia 17 bold", bg=VERT_CLAIR)
fourmi_texte = tkinter.Text(window, font="georgia 17 bold", bg=VERT_CLAIR)
commence_bouton = tkinter.Button(window, text="Démarrer", command=demarre, font="georgia 17 bold")

nourriture_titre.place(x=450, y=150, width=200, height=50)
fourmi_titre.place(x=850, y=150, width=200, height=50)
nourriture_texte.place(x=450, y=200, width=200, height=50)
fourmi_texte.place(x=850, y=200, width=200, height=50)
commence_bouton.place(x=650, y=300, width=200, height=50)


##########################
##########################
# fenêtre ajout d'événements
##########################
##########################

window_evenements = tkinter.Tk()


window_evenements.title("Ajout d'événements aléatoires")
window_evenements.geometry("600x600")
window_evenements.minsize(600, 600)
window_evenements.config(background=JAUNE)

nouvel_evenement = tkinter.Label(window_evenements, text="Nom de l'événement",
                                 font="georgia 17 bold", bg=BRUN)
mort_min_evenement = tkinter.Label(window_evenements, text="Nombre de mort minimum",
                                   font="georgia 17 bold", bg=BRUN)
mort_max_evenement = tkinter.Label(window_evenements, text="Nombre de mort maximum",
                                   font="georgia 17 bold", bg=BRUN)
poid_evenement = tkinter.Label(window_evenements, text="Fréquence d'apparition de l'événement",
                               font="georgia 17 bold", bg=BRUN_FONCE)

evenement_ajoute = tkinter.Label(window_evenements,
                                 text="Votre événement a été ajouté à la simulation!",
                                 font="georgia 17 bold", bg=VERT)
evenement_utilisateur_erreur = tkinter.Label(window_evenements, text="ERREUR",
                                             font="georgia 17 bold", bg=ROUGE)


evenement_utilisateur = tkinter.Entry(window_evenements, bg=VERT_CLAIR)
mort_min_utilisateur = tkinter.Entry(window_evenements, bg=VERT_CLAIR)
mort_max_utilisateur = tkinter.Entry(window_evenements, bg=VERT_CLAIR)
poids_evenement_utilisateur = tkinter.Entry(window_evenements, bg=VERT_CLAIR)

nouvel_evenement.pack()
evenement_utilisateur.pack()

mort_min_evenement.pack()
mort_min_utilisateur.pack()
mort_max_evenement.pack()
mort_max_utilisateur.pack()

poid_evenement.pack()
poids_evenement_utilisateur.pack()

def ajout_evenement():
    """Permet d'ajouter un événement aléatoire."""

    evenement = evenement_utilisateur.get()
    mort_min = mort_min_utilisateur.get()
    mort_max = mort_max_utilisateur.get()
    poids = poids_evenement_utilisateur.get()

    try:
        if not (mort_min.isdigit() and mort_max.isdigit() and poids.isdigit()):
            raise PasNombre("Le nombre de mort et la fréquence doivent être des NOMBRES")
    except PasNombre as e:
        evenement_utilisateur_erreur.config(text=str(e))
        evenement_utilisateur_erreur.pack()
        return
    try:
        mort_min = int(mort_min)
        mort_max = int(mort_max)
        poids = int(poids)
        if mort_min > mort_max:
            raise TropGrand("Le nombre de morts minimum doit être INFÉRIEUR au nombre de morts \
                             maximum")
        notre_colonie.liste_evenements_aleatoire.append((evenement, mort_min, mort_max))
        notre_colonie.poids_evenements_aleatoire.append(poids)
        evenement_ajoute.config(text="Votre événement '" + evenement +
                                "' a été ajouté à la simulation!")
        evenement_ajoute.pack()
    except TropGrand as e:
        evenement_utilisateur_erreur.config(text=str(e))
        evenement_utilisateur_erreur.pack()


bouton_evenement = tkinter.Button(window_evenements, text="Ajouter l'événement à la simulation",
                                  command=ajout_evenement, font="georgia 17 bold")
bouton_evenement.pack()
update_temps()
window_evenements.mainloop()
window.mainloop()
