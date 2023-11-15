from tkinter import *
from time import sleep
import argparse


class Fourmi:
    def __init__(self,stade='oeuf'):
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
    
    @property
    def stade(self):
        return self.__stade
    
    @stade.setter
    def stade(self,nouvStade):
        liste = ['oeuf','larve','adulte','mort']
        if liste.index(nouvStade) > liste.index(self.__stade):
            self.__stade = nouvStade
        else:
            return 'Impossible de revenir a un stade précédent'
    
    def jour(self):
        global nourriture
        
        if self.stade == 'oeuf':
            self.age += 1
            if self.age == 10:
                self.__stade = 'larve'
            
        elif self.__stade == 'larve':
            self.age += 1
            if nourriture > 0:
                nourriture -= 1
            else:
                self.__stade = 'mort'
            if self.age == 20:
                self.__stade = 'adulte'
            
        elif self.__stade == 'adulte':
            self.age += 1
            if nourriture > 0:
                nourriture -= 1
            else:
                self.__stade = 'mort'
    
    def __str__(self):
        return f'Stade : {self.stade}, age : {self.age}'


class Reine(Fourmi):
    def __init__(self,stade='adulte'):
        super().__init__(stade)
    
    def pond(self):
        return Fourmi('oeuf')


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
    return ('Jour ' + str(day) + ' ' + heure)


def update_temps():
    global m
    m += 1
    jour = temps(m)
    return jour
    


def update_fourmis():
    for fourm in fourmisColonie:
        fourm.jour()
        if fourm.stade == 'mort':
            fourmisColonie.pop(fourmisColonie.index(fourm))
    reineColonie.jour()
    if nourriture > 0:
        nouvelleFourmi = reineColonie.pond()
        fourmisColonie.append(nouvelleFourmi)
    else:
        reineVivante = 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('nourriture', type = int)
    parser.add_argument('vitesse', type = int)
    args = parser.parse_args()
    
    nourriture = args.nourriture
    vitesse = args.vitesse
    m = 0
    reineVivante = 1
    
    reineColonie = Reine()
    fourmisColonie = []
    
    while nourriture > 0:
        nbOeufs = 0
        nbLarves = 0
        nbFourmis = 0
        for fourm in fourmisColonie:
            if fourm.stade == 'oeuf':
                nbOeufs += 1
            elif fourm.stade == 'larve':
                nbLarves += 1
            elif fourm.stade == 'adulte':
                nbFourmis += 1
        sleep(1)
        for minute in range(vitesse):
            tempsAffichage = update_temps()
        print(f"{tempsAffichage} | Reine : {reineVivante} | Œufs : {nbOeufs} | Larves : {nbLarves} | Fourmis : {nbFourmis} | Nourriture : {nourriture}")



